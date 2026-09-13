import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });

const pages = [
  [5,'706771c2-2145-4682-9bdd-4e7df5c69bf9'],
  [6,'71ba9a99-e009-401f-b65f-8a956218a633'],
  [7,'710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b'],
  [8,'4b6090c2-744e-4fc6-8908-87c211a8713b'],
  [9,'b2449f0f-71f1-4e36-a739-cf64340f9c90'],
  [10,'75616176-b12d-47bb-bb6e-34cc3f902901'],
];

try {
  const out = [];
  for (const [bookPage, legacyPageId] of pages) {
    const path = `public.lessons/${legacyPageId}/image/0`;
    const source = await sql`select id from content_source_assets where source_path=${path} and is_present=true`;
    if (source.length !== 1) throw new Error(`source count drift page ${bookPage}: ${source.length}`);
    const rows = await sql`
      select qbr.id, qbr.type::text type, qbr.prompt, qbr.options, qbr.correct_option_index,
             qbr.answer_text, qbr.status::text status, qbr.published_at,
             coalesce(array_agg(qrl.lesson_id order by qrl.lesson_id) filter (where qrl.lesson_id is not null), '{}') lesson_ids
      from question_bank_revision_sources qrs
      join question_bank_revisions qbr on qbr.id=qrs.revision_id
      left join question_bank_revision_lessons qrl on qrl.revision_id=qbr.id
      where qrs.content_source_asset_id=${source[0].id}
      group by qbr.id
      order by qbr.id
    `;
    out.push({ bookPage, legacyPageId, count: rows.length, rows });
  }
  console.log('G9_U2_QUESTION_INSPECT_PASS', JSON.stringify({total:out.reduce((n,p)=>n+p.count,0), pages:out}));
} catch (error) {
  console.error('G9_U2_QUESTION_INSPECT_FAIL', error?.stack || error);
  await sql.end({timeout:1});
  process.exit(1);
}
await sql.end({timeout:1});
