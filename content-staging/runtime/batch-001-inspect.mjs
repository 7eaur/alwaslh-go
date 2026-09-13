import postgres from "postgres";

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error("DATABASE_URL is required");

const sourcePaths = [
  "تاسع انجليزي/الانجليزي_تاسع/الصور/p001 - Presents from London.jpg",
  "تاسع انجليزي/الانجليزي_تاسع/الصور/p002 - What's my job -.jpg",
  "تاسع انجليزي/الانجليزي_تاسع/الصور/p003 - The holidays.jpg",
  "تاسع انجليزي/الانجليزي_تاسع/الصور/p004 - A postcard from London.jpg",
];

const sql = postgres(databaseUrl, { ssl: "prefer", max: 1 });

try {
  const [scope, admins, sections, lessons, batchAssets, media, entitlements, qbItems, qbRevisions, quizzes] =
    await Promise.all([
      sql`
        select c.id as class_id, c.slug as class_slug, c.status as class_status,
               s.id as subject_id, s.slug as subject_slug, s.status as subject_status,
               scl.position as offering_position, scl.status as offering_status
        from classes c
        join subject_class_links scl on scl.class_id = c.id
        join subjects s on s.id = scl.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
      `,
      sql`
        select id, display_name, status, created_at
        from profiles
        where role = 'admin'
        order by case when status = 'active' then 0 else 1 end, created_at, id
      `,
      sql`
        select cs.id, cs.slug, cs.title, cs.position, cs.status
        from curriculum_sections cs
        join classes c on c.id = cs.class_id
        join subjects s on s.id = cs.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
        order by cs.position, cs.title, cs.id
      `,
      sql`
        select l.id, l.section_id, l.slug, l.title, l.position, l.status,
               l.published_at, l.content_revision
        from lessons l
        join classes c on c.id = l.class_id
        join subjects s on s.id = l.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
        order by l.position, l.title, l.id
      `,
      sql`
        select la.id, la.lesson_id, l.slug as lesson_slug, la.position, la.kind,
               la.publication_status, la.media_asset_id, la.storage_key, la.mime_type,
               la.byte_size::text as byte_size, la.width, la.height,
               la.checksum_sha256, la.source_page_number, la.asset_published_at
        from lesson_assets la
        join lessons l on l.id = la.lesson_id
        join classes c on c.id = l.class_id
        join subjects s on s.id = l.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
          and l.slug like 'curated-english9-pb3-u1-%'
        order by l.position, la.position, la.id
      `,
      sql.unsafe(
        `select csa.id as content_source_asset_id,
                csa.document_id,
                csa.position as content_source_position,
                csa.source_path,
                csa.checksum_sha256 as content_source_checksum,
                csa.byte_size::text as content_source_byte_size,
                ma.id as media_asset_id,
                ma.status as media_status,
                ma.source_position,
                ma.source_filename,
                ma.source_page_number,
                ma.source_checksum_sha256,
                ma.source_byte_size::text as source_byte_size,
                coalesce((
                  select json_agg(json_build_object(
                    'id', mv.id,
                    'kind', mv.kind,
                    'profile_version', mv.profile_version,
                    'storage_key', mv.storage_key,
                    'mime_type', mv.mime_type,
                    'byte_size', mv.byte_size,
                    'width', mv.width,
                    'height', mv.height,
                    'checksum_sha256', mv.checksum_sha256
                  ) order by mv.kind, mv.profile_version)
                  from media_variants mv
                  where mv.media_asset_id = ma.id
                ), '[]'::json) as variants
         from content_source_assets csa
         left join media_assets ma on ma.content_source_asset_id = csa.id
         where csa.source_path = any($1::text[])
         order by csa.position, csa.id`,
        [sourcePaths],
      ),
      sql`
        select e.id, e.profile_id, p.display_name, e.scope, e.class_id,
               e.status, e.starts_at, e.expires_at
        from student_entitlements e
        join profiles p on p.id = e.profile_id
        left join classes c on c.id = e.class_id
        where p.role = 'student'
          and e.status = 'active'
          and e.starts_at <= now()
          and (e.expires_at is null or e.expires_at > now())
          and (e.scope = 'all_content' or (e.scope = 'class' and c.slug = 'grade-9'))
        order by e.created_at, e.id
      `,
      sql`
        select count(*)::int as count
        from question_bank_items i
        join classes c on c.id = i.class_id
        join subjects s on s.id = i.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
      `,
      sql`
        select count(*)::int as count
        from question_bank_revisions r
        join question_bank_items i on i.id = r.item_id
        join classes c on c.id = i.class_id
        join subjects s on s.id = i.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
      `,
      sql`
        select count(*)::int as count
        from quizzes q
        join classes c on c.id = q.class_id
        join subjects s on s.id = q.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
      `,
    ]);

  const report = {
    mode: "read-only",
    batchId: "BATCH-001-G9-EN-PB3-U1",
    scope,
    admins,
    sections,
    lessons,
    batchAssets,
    media,
    entitlements,
    counts: {
      questionBankItems: qbItems[0]?.count ?? 0,
      questionBankRevisions: qbRevisions[0]?.count ?? 0,
      quizzes: quizzes[0]?.count ?? 0,
    },
  };
  console.log(`BATCH001_INSPECT ${JSON.stringify(report)}`);
} finally {
  await sql.end({ timeout: 5 });
}
