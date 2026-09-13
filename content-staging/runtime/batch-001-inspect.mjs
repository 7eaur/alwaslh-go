import postgres from "postgres";

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error("DATABASE_URL is required");

const lessonSlugs = [
  "legacy-sb-2d53aec17e54f46db304",
  "legacy-sb-908a58f8e7b25f82c787",
  "legacy-sb-4e1131b5222334610174",
  "legacy-sb-840f23a0e0a98aaa674e",
];

const sql = postgres(databaseUrl, { ssl: "prefer", max: 1 });

try {
  const [scope, admins, sections, lessons, assets, questions, entitlements] = await Promise.all([
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
      from profiles where role = 'admin'
      order by case when status = 'active' then 0 else 1 end, created_at, id
    `,
    sql`
      select cs.id, cs.slug, cs.title, cs.position, cs.status
      from curriculum_sections cs
      join classes c on c.id = cs.class_id
      join subjects s on s.id = cs.subject_id
      where c.slug='grade-9' and s.slug='english'
      order by cs.position, cs.id
    `,
    sql.unsafe(
      `select l.id,l.section_id,l.slug,l.title,l.position,l.status,l.published_at,l.content_revision
       from lessons l where l.slug = any($1::text[]) order by l.position,l.id`, [lessonSlugs]
    ),
    sql.unsafe(
      `select l.id as lesson_id,l.slug as lesson_slug,la.id as lesson_asset_id,la.position as asset_position,
              la.kind,la.publication_status,la.media_asset_id,la.storage_key,la.mime_type,
              la.byte_size::text as lesson_asset_byte_size,la.width,la.height,la.checksum_sha256,
              la.source_page_number,la.source_metadata,la.submitted_for_review_at,la.asset_published_at,
              ma.status as media_status,ma.content_source_asset_id,ma.source_position,ma.source_filename,
              ma.source_page_number as media_source_page_number,ma.source_checksum_sha256,
              ma.source_byte_size::text as media_source_byte_size,csa.source_path,csa.position as csa_position,
              csa.checksum_sha256 as csa_checksum,csa.byte_size::text as csa_byte_size,
              coalesce((select json_agg(json_build_object('id',mv.id,'kind',mv.kind,'profile_version',mv.profile_version,
                'storage_key',mv.storage_key,'mime_type',mv.mime_type,'byte_size',mv.byte_size,'width',mv.width,
                'height',mv.height,'checksum_sha256',mv.checksum_sha256) order by mv.kind,mv.profile_version)
                from media_variants mv where mv.media_asset_id=ma.id),'[]'::json) as variants
       from lessons l
       left join lesson_assets la on la.lesson_id=l.id
       left join media_assets ma on ma.id=la.media_asset_id
       left join content_source_assets csa on csa.id=ma.content_source_asset_id
       where l.slug = any($1::text[])
       order by l.position,la.position,la.id`, [lessonSlugs]
    ),
    sql.unsafe(
      `select l.slug as lesson_slug, qrl.position as lesson_question_position,
              i.id as item_id,i.origin,i.legacy_source_key,
              r.id as revision_id,r.revision_number,r.status,r.type,r.prompt,r.options,
              r.answer_status,r.correct_option_index,r.answer_text,r.explanation,r.source_summary,
              r.submitted_for_review_at,r.published_at,
              coalesce((select json_agg(json_build_object('position',qrs.position,'media_asset_id',qrs.media_asset_id,
                'page_number',qrs.page_number,'input_checksum_sha256',qrs.input_checksum_sha256,
                'content_source_asset_id',qrs.content_source_asset_id,'source_quote',qrs.source_quote,
                'source_path',csa.source_path) order by qrs.position)
                from question_bank_revision_sources qrs
                left join content_source_assets csa on csa.id=qrs.content_source_asset_id
                where qrs.revision_id=r.id),'[]'::json) as sources
       from question_bank_revision_lessons qrl
       join lessons l on l.id=qrl.lesson_id
       join question_bank_revisions r on r.id=qrl.revision_id
       join question_bank_items i on i.id=r.item_id
       where l.slug = any($1::text[])
       order by l.position,qrl.position,r.revision_number`, [lessonSlugs]
    ),
    sql`
      select e.id,e.profile_id,p.display_name,e.scope,e.class_id,e.status,e.starts_at,e.expires_at
      from student_entitlements e
      join profiles p on p.id=e.profile_id
      left join classes c on c.id=e.class_id
      where p.role='student' and e.status='active' and e.starts_at<=now()
        and (e.expires_at is null or e.expires_at>now())
        and (e.scope='all_content' or (e.scope='class' and c.slug='grade-9'))
      order by e.created_at,e.id
    `,
  ]);

  console.log(`BATCH001_INSPECT ${JSON.stringify({mode:'read-only',batchId:'BATCH-001-G9-EN-PB3-U1',scope,admins,sections,lessons,assets,questions,entitlements})}`);
} finally {
  await sql.end({ timeout: 5 });
}
