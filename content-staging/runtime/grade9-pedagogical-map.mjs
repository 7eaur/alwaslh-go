import { readFile } from 'node:fs/promises';
import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');

const manifest = JSON.parse(await readFile(new URL('../curated/grade-9/english/pupil-book-3/reconstruction-candidates.json', import.meta.url), 'utf8'));
const pages = manifest.page_candidates ?? [];
if (pages.length !== 69) throw new Error(`G9_PED_MAP_FAIL: expected 69 pages, got ${pages.length}`);

const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });

try {
  const scope = await sql`
    select c.id class_id, s.id subject_id
      from classes c
      join subject_class_links scl on scl.class_id = c.id
      join subjects s on s.id = scl.subject_id
     where c.slug = 'grade-9' and s.slug = 'english'
       and c.status = 'active' and s.status = 'active' and scl.status = 'active'
  `;
  if (scope.length !== 1) throw new Error(`G9_PED_MAP_FAIL: scope count=${scope.length}`);

  const expected = pages.map((p) => ({
    bookPage: p.book_page,
    sourcePage: p.source_page,
    legacyPageId: p.legacy_page_id,
    title: p.manifest_title ?? p.legacy_title,
    section: p.section,
    questionCount: p.question_count ?? 0,
    path: `public.lessons/${p.legacy_page_id}/image/0`,
  }));

  const paths = expected.map((p) => p.path);
  const rows = await sql`
    select csa.source_path,
           csa.id source_asset_id,
           ma.id media_asset_id,
           la.id lesson_asset_id,
           la.position asset_position,
           la.publication_status,
           l.id lesson_id,
           l.slug lesson_slug,
           l.title lesson_title,
           l.position lesson_position,
           l.content_revision,
           l.published_at lesson_published_at,
           cs.id section_id,
           cs.title section_title,
           cs.position section_position,
           count(distinct qrs.revision_id)::int source_question_revisions,
           count(distinct qrl.revision_id)::int linked_question_revisions
      from content_source_assets csa
      join media_assets ma on ma.content_source_asset_id = csa.id
      join lesson_assets la on la.media_asset_id = ma.id
      join lessons l on l.id = la.lesson_id
      left join curriculum_sections cs on cs.id = l.section_id
      left join question_bank_revision_sources qrs on qrs.content_source_asset_id = csa.id
      left join question_bank_revision_lessons qrl on qrl.revision_id = qrs.revision_id and qrl.lesson_id = l.id
     where csa.source_path in ${sql(paths)}
       and l.class_id = ${scope[0].class_id}
       and l.subject_id = ${scope[0].subject_id}
     group by csa.source_path, csa.id, ma.id, la.id, la.position, la.publication_status,
              l.id, l.slug, l.title, l.position, l.content_revision, l.published_at,
              cs.id, cs.title, cs.position
  `;

  if (rows.length !== 69) throw new Error(`G9_PED_MAP_FAIL: mapped rows=${rows.length}`);
  const byPath = new Map(rows.map((r) => [r.source_path, r]));

  const mappedPages = expected.map((p) => {
    const row = byPath.get(p.path);
    if (!row) throw new Error(`G9_PED_MAP_FAIL: missing ${p.path}`);
    if (row.section_title !== p.section) throw new Error(`G9_PED_MAP_FAIL: section mismatch page=${p.bookPage} db=${row.section_title} manifest=${p.section}`);
    return { ...p, ...row };
  });

  const lessons = [];
  const byLesson = new Map();
  for (const page of mappedPages) {
    const current = byLesson.get(page.lesson_id) ?? {
      lessonId: page.lesson_id,
      slug: page.lesson_slug,
      title: page.lesson_title,
      section: page.section_title,
      lessonPosition: page.lesson_position,
      published: page.lesson_published_at !== null,
      pages: [],
      sourceQuestionRevisions: 0,
      linkedQuestionRevisions: 0,
    };
    current.pages.push({
      bookPage: page.bookPage,
      sourcePage: page.sourcePage,
      sourceTitle: page.title,
      assetPosition: page.asset_position,
      sourceQuestionRevisions: page.source_question_revisions,
      linkedQuestionRevisions: page.linked_question_revisions,
    });
    current.sourceQuestionRevisions += page.source_question_revisions;
    current.linkedQuestionRevisions += page.linked_question_revisions;
    byLesson.set(page.lesson_id, current);
  }
  for (const lesson of byLesson.values()) {
    lesson.pages.sort((a, b) => a.bookPage - b.bookPage);
    lessons.push(lesson);
  }
  lessons.sort((a, b) => a.pages[0].bookPage - b.pages[0].bookPage);

  const result = {
    task: 'GRADE9-PEDAGOGICAL-MAP',
    mode: 'read-only',
    counts: {
      pages: mappedPages.length,
      lessons: lessons.length,
      sections: new Set(mappedPages.map((p) => p.section_title)).size,
      sourceQuestionRevisions: mappedPages.reduce((n, p) => n + p.source_question_revisions, 0),
      linkedQuestionRevisions: mappedPages.reduce((n, p) => n + p.linked_question_revisions, 0),
      publishedLessons: lessons.filter((l) => l.published).length,
    },
    lessons,
  };

  console.log('G9_PEDAGOGICAL_MAP_PASS', JSON.stringify(result));
} catch (error) {
  console.error(error?.stack || error);
  await sql.end({ timeout: 1 });
  process.exit(1);
}

await sql.end({ timeout: 1 });
