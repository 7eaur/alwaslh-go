import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');

const sourcePages = [
  { bookPage: 5, sourcePage: 9, legacyPageId: '706771c2-2145-4682-9bdd-4e7df5c69bf9', path: 'public.lessons/706771c2-2145-4682-9bdd-4e7df5c69bf9/image/0', sha256: 'fc9e15f23d3f5c9a7928aecc70888e30be2c454ab16883e1a3c82290fd581fdb' },
  { bookPage: 6, sourcePage: 10, legacyPageId: '71ba9a99-e009-401f-b65f-8a956218a633', path: 'public.lessons/71ba9a99-e009-401f-b65f-8a956218a633/image/0', sha256: 'fd99f85698dd4870bf8fccf85aa53f47bf484d19b2052473155540627f6aa420' },
  { bookPage: 7, sourcePage: 11, legacyPageId: '710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b', path: 'public.lessons/710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b/image/0', sha256: '3b7415622af90557ad09585eef776b5ce3fe2c68776a1963b4a2cbf677f5ba61' },
  { bookPage: 8, sourcePage: 12, legacyPageId: '4b6090c2-744e-4fc6-8908-87c211a8713b', path: 'public.lessons/4b6090c2-744e-4fc6-8908-87c211a8713b/image/0', sha256: '3678974564e2a219840da4fc175d62d9811bd80666d01c81d4f9b49f2328e258' },
];

const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });

function assert(condition, message) {
  if (!condition) throw new Error(`IMPORT001_INSPECT_FAIL: ${message}`);
}

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
  assert(scope[0].class_status === 'active' && scope[0].subject_status === 'active' && scope[0].offering_status === 'active', 'scope not active');

  const sections = await sql`
    select id, slug, title, position, status
    from curriculum_sections
    where class_id = ${scope[0].class_id} and subject_id = ${scope[0].subject_id}
    order by position, id
  `;

  const paths = sourcePages.map((page) => page.path);
  const sourceAssets = await sql`
    select id, source_path, position, checksum_sha256, byte_size::text byte_size, is_present
    from content_source_assets
    where source_path in ${sql(paths)}
    order by source_path, id
  `;

  const byPath = new Map();
  for (const asset of sourceAssets) {
    if (!byPath.has(asset.source_path)) byPath.set(asset.source_path, []);
    byPath.get(asset.source_path).push(asset);
  }

  for (const page of sourcePages) {
    const matches = byPath.get(page.path) ?? [];
    assert(matches.length === 1, `source identity ${page.legacyPageId} count=${matches.length}`);
    assert(matches[0].checksum_sha256 === page.sha256, `source checksum drift ${page.legacyPageId}`);
    assert(matches[0].is_present === true, `source absent ${page.legacyPageId}`);
  }

  const sourceAssetIds = sourceAssets.map((row) => row.id);
  const chains = sourceAssetIds.length === 0 ? [] : await sql`
    select csa.id source_asset_id, csa.source_path, csa.checksum_sha256,
           ma.id media_asset_id, ma.status media_status, ma.source_position, ma.source_filename,
           la.id lesson_asset_id, la.lesson_id, la.position lesson_asset_position,
           la.kind lesson_asset_kind, la.publication_status, la.asset_published_at,
           l.id lesson_id, l.slug lesson_slug, l.title lesson_title, l.position lesson_position,
           l.status lesson_status, l.published_at lesson_published_at, l.section_id,
           cs.slug section_slug, cs.title section_title, cs.position section_position,
           coalesce((select json_agg(json_build_object(
             'id', mv.id,
             'kind', mv.kind,
             'profile_version', mv.profile_version,
             'storage_key', mv.storage_key,
             'mime_type', mv.mime_type,
             'byte_size', mv.byte_size,
             'width', mv.width,
             'height', mv.height,
             'checksum_sha256', mv.checksum_sha256
           ) order by mv.kind, mv.profile_version, mv.id)
           from media_variants mv where mv.media_asset_id = ma.id), '[]'::json) variants
    from content_source_assets csa
    left join media_assets ma on ma.content_source_asset_id = csa.id
    left join lesson_assets la on la.media_asset_id = ma.id
    left join lessons l on l.id = la.lesson_id
    left join curriculum_sections cs on cs.id = l.section_id
    where csa.id in ${sql(sourceAssetIds)}
    order by csa.source_path, ma.id, la.id, l.id
  `;

  const targetSlug = 'curated-english9-pb3-u2-describing-people-and-animals';
  const targetSlugRows = await sql`
    select id, slug, title, position, status, published_at, section_id
    from lessons
    where class_id = ${scope[0].class_id}
      and subject_id = ${scope[0].subject_id}
      and slug = ${targetSlug}
  `;

  const candidateLegacyLessons = await sql`
    select distinct l.id, l.slug, l.title, l.position, l.status, l.published_at, l.section_id
    from lessons l
    join lesson_assets la on la.lesson_id = l.id
    join media_assets ma on ma.id = la.media_asset_id
    where l.class_id = ${scope[0].class_id}
      and l.subject_id = ${scope[0].subject_id}
      and ma.content_source_asset_id in ${sql(sourceAssetIds)}
    order by l.position, l.id
  `;

  const publication = sourceAssetIds.length === 0 ? { lessons: 0, lessonAssets: 0 } : (await sql`
    select
      count(distinct l.id) filter (where l.published_at is not null)::int lessons,
      count(distinct la.id) filter (where la.publication_status <> 'draft' or la.asset_published_at is not null)::int lesson_assets
    from media_assets ma
    join lesson_assets la on la.media_asset_id = ma.id
    join lessons l on l.id = la.lesson_id
    where ma.content_source_asset_id in ${sql(sourceAssetIds)}
  `)[0];

  console.log('IMPORT001_INSPECT_PASS', JSON.stringify({
    mode: 'read-only',
    task: 'IMPORT-001',
    intendedLesson: {
      title: 'Describing people and animals',
      slug: targetSlug,
      pages: sourcePages.map(({ bookPage, sourcePage, legacyPageId, path, sha256 }) => ({ bookPage, sourcePage, legacyPageId, path, sha256 })),
    },
    scope,
    sections,
    sourceAssets,
    chains,
    targetSlugRows,
    candidateLegacyLessons,
    publication,
  }));
} catch (error) {
  console.error(error?.stack || error);
  await sql.end({ timeout: 1 });
  process.exit(1);
}

await sql.end({ timeout: 1 });
