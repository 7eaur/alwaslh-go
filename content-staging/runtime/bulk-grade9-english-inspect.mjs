import { readFile } from 'node:fs/promises';
import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');

const manifestUrl = new URL('../curated/grade-9/english/pupil-book-3/reconstruction-candidates.json', import.meta.url);
const manifest = JSON.parse(await readFile(manifestUrl, 'utf8'));
const pages = manifest.page_candidates ?? [];

function fail(message) {
  throw new Error(`BULK_G9_EN_INSPECT_FAIL: ${message}`);
}
function assert(condition, message) {
  if (!condition) fail(message);
}
function uniq(values) {
  return [...new Set(values)];
}

assert(manifest.counts?.page_candidates === 69, `manifest page_candidates=${manifest.counts?.page_candidates}`);
assert(manifest.counts?.raw_images === 69, `manifest raw_images=${manifest.counts?.raw_images}`);
assert(manifest.counts?.raw_pages === 69, `manifest raw_pages=${manifest.counts?.raw_pages}`);
assert(manifest.counts?.questions === 104, `manifest questions=${manifest.counts?.questions}`);
assert(manifest.counts?.sections === 8, `manifest sections=${manifest.counts?.sections}`);
assert(pages.length === 69, `page array count=${pages.length}`);
assert(uniq(pages.map((p) => p.legacy_page_id)).length === 69, 'duplicate legacy_page_id in manifest');
assert(uniq(pages.map((p) => p.book_page)).length === 69, 'duplicate book_page in manifest');
assert(uniq(pages.map((p) => p.raw_image?.raw_path)).length === 69, 'duplicate raw_path in manifest');

const expected = pages.map((page) => ({
  bookPage: page.book_page,
  sourcePage: page.source_page,
  legacyPageId: page.legacy_page_id,
  candidateId: page.candidate_id,
  title: page.manifest_title ?? page.legacy_title,
  section: page.section,
  questionCount: page.question_count ?? 0,
  path: `public.lessons/${page.legacy_page_id}/image/0`,
  sha256: page.raw_image?.sha256,
  byteSize: page.raw_image?.byte_size,
  rawPath: page.raw_image?.raw_path,
}));
const expectedPaths = expected.map((p) => p.path);
const expectedSections = uniq(expected.map((p) => p.section));

const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });

try {
  const scope = await sql`
    select c.id class_id, c.slug class_slug, c.status class_status,
           s.id subject_id, s.slug subject_slug, s.status subject_status,
           scl.status offering_status
      from classes c
      join subject_class_links scl on scl.class_id = c.id
      join subjects s on s.id = scl.subject_id
     where c.slug = 'grade-9' and s.slug = 'english'
  `;
  assert(scope.length === 1, `grade-9/english scope count=${scope.length}`);
  assert(scope[0].class_status === 'active' && scope[0].subject_status === 'active' && scope[0].offering_status === 'active', 'grade-9/english scope is not fully active');

  const sourceAssets = await sql`
    select id, source_path, position, checksum_sha256, byte_size::text byte_size, is_present
      from content_source_assets
     where source_path in ${sql(expectedPaths)}
     order by source_path, id
  `;

  const sourceByPath = new Map();
  for (const row of sourceAssets) {
    const list = sourceByPath.get(row.source_path) ?? [];
    list.push(row);
    sourceByPath.set(row.source_path, list);
  }

  const sourceAnomalies = [];
  for (const page of expected) {
    const matches = sourceByPath.get(page.path) ?? [];
    if (matches.length !== 1) {
      sourceAnomalies.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'source_identity_count', actual: matches.length });
      continue;
    }
    const row = matches[0];
    if (row.checksum_sha256 !== page.sha256) sourceAnomalies.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'source_checksum_drift', expected: page.sha256, actual: row.checksum_sha256 });
    if (row.is_present !== true) sourceAnomalies.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'source_not_present' });
  }

  const sourceAssetIds = sourceAssets.map((row) => row.id);
  const chains = sourceAssetIds.length === 0 ? [] : await sql`
    select csa.id source_asset_id, csa.source_path,
           count(distinct ma.id)::int media_count,
           count(distinct la.id)::int lesson_asset_count,
           count(distinct la.lesson_id)::int lesson_count,
           count(distinct ma.id) filter (where ma.status = 'ready')::int ready_media_count,
           count(distinct la.id) filter (where la.publication_status <> 'draft' or la.asset_published_at is not null)::int non_draft_asset_count,
           count(distinct l.id) filter (where l.published_at is not null)::int published_lesson_count,
           coalesce(array_agg(distinct l.id) filter (where l.id is not null), '{}') lesson_ids,
           coalesce(array_agg(distinct l.slug) filter (where l.slug is not null), '{}') lesson_slugs
      from content_source_assets csa
      left join media_assets ma on ma.content_source_asset_id = csa.id
      left join lesson_assets la on la.media_asset_id = ma.id
      left join lessons l on l.id = la.lesson_id
     where csa.id in ${sql(sourceAssetIds)}
     group by csa.id, csa.source_path
     order by csa.source_path
  `;
  const chainByPath = new Map(chains.map((row) => [row.source_path, row]));

  const chainSummary = {
    exactSourceIdentities: sourceAssets.length,
    pagesWithMedia: expected.filter((p) => (chainByPath.get(p.path)?.media_count ?? 0) > 0).length,
    pagesWithExactlyOneMedia: expected.filter((p) => (chainByPath.get(p.path)?.media_count ?? 0) === 1).length,
    pagesWithLessonAsset: expected.filter((p) => (chainByPath.get(p.path)?.lesson_asset_count ?? 0) > 0).length,
    pagesWithExactlyOneLessonAsset: expected.filter((p) => (chainByPath.get(p.path)?.lesson_asset_count ?? 0) === 1).length,
    pagesWithReadyMedia: expected.filter((p) => (chainByPath.get(p.path)?.ready_media_count ?? 0) > 0).length,
    pagesWithPublishedLesson: expected.filter((p) => (chainByPath.get(p.path)?.published_lesson_count ?? 0) > 0).length,
    pagesWithNonDraftAsset: expected.filter((p) => (chainByPath.get(p.path)?.non_draft_asset_count ?? 0) > 0).length,
  };

  const chainAnomalies = expected.flatMap((page) => {
    const row = chainByPath.get(page.path);
    if (!row) return [{ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'missing_chain' }];
    const items = [];
    if (row.media_count !== 1) items.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'media_count', actual: row.media_count });
    if (row.lesson_asset_count !== 1) items.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'lesson_asset_count', actual: row.lesson_asset_count });
    if (row.ready_media_count !== 1) items.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'ready_media_count', actual: row.ready_media_count });
    if (row.published_lesson_count !== 0) items.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'published_lesson_count', actual: row.published_lesson_count });
    if (row.non_draft_asset_count !== 0) items.push({ bookPage: page.bookPage, legacyPageId: page.legacyPageId, kind: 'non_draft_asset_count', actual: row.non_draft_asset_count });
    return items;
  });

  const sections = await sql`
    select id, slug, title, position, status
      from curriculum_sections
     where class_id = ${scope[0].class_id} and subject_id = ${scope[0].subject_id}
     order by position, id
  `;

  const legacySlugs = expected.map((p) => `legacy-sb-${p.candidateId.replace(/^page-candidate-/, '')}`);
  const legacyLessons = await sql`
    select id, slug, title, position, status, published_at, section_id, content_revision
      from lessons
     where class_id = ${scope[0].class_id}
       and subject_id = ${scope[0].subject_id}
       and slug in ${sql(legacySlugs)}
     order by position, id
  `;
  const curatedLessons = await sql`
    select id, slug, title, position, status, published_at, section_id, content_revision
      from lessons
     where class_id = ${scope[0].class_id}
       and subject_id = ${scope[0].subject_id}
       and slug like 'curated-english9-pb3-%'
     order by position, id
  `;

  const questionSummary = sourceAssetIds.length === 0 ? { revisions: 0, sourceRows: 0, publishedRevisions: 0 } : (await sql`
    select count(distinct qrs.revision_id)::int revisions,
           count(*)::int source_rows,
           count(distinct qbr.id) filter (where qbr.published_at is not null)::int published_revisions
      from question_bank_revision_sources qrs
      join question_bank_revisions qbr on qbr.id = qrs.revision_id
     where qrs.content_source_asset_id in ${sql(sourceAssetIds)}
  `)[0];

  const questionLinks = sourceAssetIds.length === 0 ? { revisions: 0, links: 0, lessons: 0 } : (await sql`
    select count(distinct qrl.revision_id)::int revisions,
           count(*)::int links,
           count(distinct qrl.lesson_id)::int lessons
      from question_bank_revision_lessons qrl
      join question_bank_revision_sources qrs on qrs.revision_id = qrl.revision_id
     where qrs.content_source_asset_id in ${sql(sourceAssetIds)}
  `)[0];

  const result = {
    mode: 'read-only',
    task: 'BULK-GRADE9-ENGLISH-IMPORT',
    manifest: {
      pages: pages.length,
      rawPages: manifest.counts.raw_pages,
      rawImages: manifest.counts.raw_images,
      questions: manifest.counts.questions,
      sections: manifest.counts.sections,
      sourceManifestOnlyPages: manifest.counts.source_manifest_only_pages,
      expectedSections,
    },
    scope: scope[0],
    database: {
      sections: sections.length,
      sectionRows: sections,
      legacyLessons: legacyLessons.length,
      curatedLessons: curatedLessons.length,
      chainSummary,
      questionSummary,
      questionLinks,
    },
    anomalies: {
      source: sourceAnomalies,
      chain: chainAnomalies,
    },
    safeForBulkDryRun: sourceAnomalies.length === 0 && chainAnomalies.every((a) => !['missing_chain', 'media_count', 'ready_media_count', 'published_lesson_count', 'non_draft_asset_count'].includes(a.kind)),
  };

  console.log('BULK_G9_EN_INSPECT_PASS', JSON.stringify(result));
} catch (error) {
  console.error(error?.stack || error);
  await sql.end({ timeout: 1 });
  process.exit(1);
}

await sql.end({ timeout: 1 });
