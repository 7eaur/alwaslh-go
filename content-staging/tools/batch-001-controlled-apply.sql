\set ON_ERROR_STOP on
\if :{?apply}
\else
\set apply false
\endif

-- BATCH-001-G9-EN-PB3-U1
-- Default mode is transactional verification + ROLLBACK.
-- COMMIT requires an explicit: psql -v apply=true -f content-staging/tools/batch-001-controlled-apply.sql
-- Legacy page UUIDs are provenance keys only. Modern lessons are resolved through the canonical
-- PostgreSQL source identity public.lessons/<legacy page UUID>/image/0 plus immutable SHA-256.
-- RAW extraction paths remain documentary evidence and are never mutated by this executor.

BEGIN;
SET LOCAL lock_timeout = '5s';
SET LOCAL statement_timeout = '60s';
SET LOCAL application_name = 'alwaslh-content-rebuild-batch-001';

DO $$
DECLARE missing text[];
BEGIN
  SELECT array_agg(required_name ORDER BY required_name) INTO missing
  FROM (VALUES
    ('classes'), ('subjects'), ('subject_class_links'), ('curriculum_sections'), ('lessons'),
    ('lesson_assets'), ('media_assets'), ('content_source_assets'), ('question_bank_revisions'),
    ('question_bank_revision_lessons'), ('question_bank_revision_sources')
  ) AS required(required_name)
  WHERE to_regclass('public.' || required_name) IS NULL;
  IF missing IS NOT NULL THEN
    RAISE EXCEPTION 'BATCH-001 schema drift: missing tables %', missing;
  END IF;
END $$;

CREATE TEMP TABLE _batch001_scope AS
SELECT c.id AS class_id, s.id AS subject_id
FROM classes c
JOIN subjects s ON s.slug = 'english'
JOIN subject_class_links scl ON scl.class_id = c.id AND scl.subject_id = s.id
WHERE c.slug = 'grade-9' AND c.status = 'active' AND s.status = 'active' AND scl.status = 'active';

DO $$ DECLARE n int; BEGIN
  SELECT count(*) INTO n FROM _batch001_scope;
  IF n <> 1 THEN RAISE EXCEPTION 'BATCH-001 scope drift: expected 1 active grade-9/english offering, got %', n; END IF;
END $$;

SELECT scl.class_id
FROM subject_class_links scl
JOIN _batch001_scope sc USING (class_id, subject_id)
FOR UPDATE;

CREATE TEMP TABLE _batch001_expected_lessons (
  legacy_page_id uuid PRIMARY KEY,
  legacy_slug text NOT NULL,
  position int NOT NULL,
  book_page int NOT NULL,
  target_slug text NOT NULL,
  target_title text NOT NULL,
  source_path text NOT NULL,
  source_sha256 text NOT NULL
) ON COMMIT DROP;

INSERT INTO _batch001_expected_lessons VALUES
('2d98475c-91bf-4000-bfbc-79f7a6a854f9','legacy-sb-2d53aec17e54f46db304',0,1,'curated-english9-pb3-u1-p001-presents-from-london','Presents from London','public.lessons/2d98475c-91bf-4000-bfbc-79f7a6a854f9/image/0','ae3e89be65d1c9ec5f70e361a5e78ea903d6e305f22d399e2c88bf864f6c3a4f'),
('5e207993-508f-426b-ae71-f00aa4f782df','legacy-sb-908a58f8e7b25f82c787',1,2,'curated-english9-pb3-u1-p002-whats-my-job','What''s my job?','public.lessons/5e207993-508f-426b-ae71-f00aa4f782df/image/0','1df05a27195e28e5543747c1f827a4d32c2bf937476c91ae69b0f4fe8b61b413'),
('dc1d6249-c0cb-4982-9711-092b1dcffee3','legacy-sb-4e1131b5222334610174',2,3,'curated-english9-pb3-u1-p003-the-holidays','The holidays','public.lessons/dc1d6249-c0cb-4982-9711-092b1dcffee3/image/0','78741ebd493e6b7dbbc05115472fec173edbeab9e05079b806a61acd1d7d13ac'),
('f2947d7f-5697-4bdc-b561-ad880a1afdf1','legacy-sb-840f23a0e0a98aaa674e',3,4,'curated-english9-pb3-u1-p004-a-postcard-from-london','A postcard from London','public.lessons/f2947d7f-5697-4bdc-b561-ad880a1afdf1/image/0','86d655468bfbc73248da92e0d16d4b4dcccc0217df241e69bac94f6cee6cf321');

CREATE TEMP TABLE _batch001_lessons ON COMMIT DROP AS
SELECT e.*, l.id AS lesson_id, la.id AS lesson_asset_id, ma.id AS media_asset_id, csa.id AS source_asset_id
FROM _batch001_expected_lessons e
JOIN content_source_assets csa
  ON csa.is_present = true AND csa.source_path = e.source_path AND csa.checksum_sha256 = e.source_sha256
JOIN media_assets ma
  ON ma.content_source_asset_id = csa.id AND ma.status = 'ready' AND ma.source_checksum_sha256 = e.source_sha256
JOIN lesson_assets la
  ON la.media_asset_id = ma.id AND la.publication_status = 'draft' AND la.asset_published_at IS NULL
JOIN lessons l ON l.id = la.lesson_id AND l.slug = e.legacy_slug
JOIN _batch001_scope sc ON sc.class_id = l.class_id AND sc.subject_id = l.subject_id
WHERE l.status = 'active' AND l.published_at IS NULL;

DO $$ DECLARE n int; BEGIN
  SELECT count(*) INTO n FROM _batch001_lessons;
  IF n <> 4 THEN RAISE EXCEPTION 'BATCH-001 provenance lesson resolution drift: expected 4 rows, got %', n; END IF;
  SELECT count(DISTINCT legacy_page_id) INTO n FROM _batch001_lessons;
  IF n <> 4 THEN RAISE EXCEPTION 'BATCH-001 provenance ambiguity: expected 4 source identities, got %', n; END IF;
  SELECT count(DISTINCT lesson_id) INTO n FROM _batch001_lessons;
  IF n <> 4 THEN RAISE EXCEPTION 'BATCH-001 provenance ambiguity: expected 4 unique modern lessons, got %', n; END IF;
END $$;

SELECT l.id FROM lessons l JOIN _batch001_lessons e ON e.lesson_id = l.id FOR UPDATE;

DO $$ DECLARE n int; BEGIN
  SELECT count(*) INTO n
  FROM lessons l JOIN _batch001_scope sc ON sc.class_id=l.class_id AND sc.subject_id=l.subject_id
  JOIN _batch001_lessons e ON e.target_slug=l.slug
  WHERE l.id <> e.lesson_id;
  IF n <> 0 THEN RAISE EXCEPTION 'BATCH-001 target slug collision count %', n; END IF;

  SELECT count(*) INTO n
  FROM curriculum_sections cs JOIN _batch001_scope sc USING (class_id, subject_id)
  WHERE cs.slug='curated-english9-pb3-unit-1-revision';
  IF n <> 0 THEN RAISE EXCEPTION 'BATCH-001 section pre-state drift: expected 0, got %', n; END IF;
END $$;

CREATE TEMP TABLE _batch001_questions (
  legacy_page_id uuid NOT NULL,
  source_index int NOT NULL,
  current_prompt text NOT NULL,
  decision text NOT NULL CHECK (decision IN ('approved','corrected')),
  target_type question_bank_question_type NOT NULL,
  target_prompt text NOT NULL,
  target_options jsonb,
  target_correct_option_index int,
  PRIMARY KEY (legacy_page_id, source_index)
) ON COMMIT DROP;

INSERT INTO _batch001_questions VALUES
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',0,'How old is Saleh?','approved','multiple_choice','How old is Saleh?',NULL,NULL),
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',1,'Saleh is seventeen years old.','approved','true_false','Saleh is seventeen years old.',NULL,NULL),
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',2,'What does Mr Al Sabri want to buy for Saleh?','corrected','multiple_choice','What does Mr Al Sabri suggest Taha buy for Saleh?','["a pair of shorts","a school uniform","a bicycle","a camera"]',0),
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',3,'What does Saleh like?','approved','multiple_choice','What does Saleh like?',NULL,NULL),
('5e207993-508f-426b-ae71-f00aa4f782df',0,'Taha works in a clinic.','corrected','true_false','The dentist works in a clinic.',NULL,NULL),
('5e207993-508f-426b-ae71-f00aa4f782df',1,'What is Taha''s job?','corrected','multiple_choice','What is the job of the person who takes care of people''s teeth?','["a dentist","a teacher","a doctor","a police officer"]',0),
('5e207993-508f-426b-ae71-f00aa4f782df',2,'What time does the office worker start work?','approved','multiple_choice','What time does the office worker start work?',NULL,NULL),
('5e207993-508f-426b-ae71-f00aa4f782df',3,'Where does the doctor work?','corrected','multiple_choice','Where does the dentist work?','["in a clinic","in an office","in a hospital","in a school"]',0),
('dc1d6249-c0cb-4982-9711-092b1dcffee3',0,'The family went to London for the holidays.','corrected','true_false','One speaker went to a village by the sea in the holidays.',NULL,NULL),
('dc1d6249-c0cb-4982-9711-092b1dcffee3',1,'What did Amna do every day?','corrected','multiple_choice','What did the first speaker do every day?','["went swimming and fishing","stayed at home","went shopping","worked on a farm"]',0),
('dc1d6249-c0cb-4982-9711-092b1dcffee3',2,'Where did Mr Al Sabri and his family go on holiday?','corrected','multiple_choice','Where did the first speaker go in the holidays?','["a village by the sea","London","Paris","Sana''a"]',0),
('f2947d7f-5697-4bdc-b561-ad880a1afdf1',0,'Amna wrote a postcard to Mariam.','approved','true_false','Amna wrote a postcard to Mariam.',NULL,NULL),
('f2947d7f-5697-4bdc-b561-ad880a1afdf1',1,'What did Amna write to Mariam?','approved','multiple_choice','What did Amna write to Mariam?',NULL,NULL);

CREATE TEMP TABLE _batch001_question_resolution ON COMMIT DROP AS
SELECT q.*, l.lesson_id, l.book_page, l.source_sha256, l.source_asset_id, r.id AS revision_id
FROM _batch001_questions q
JOIN _batch001_lessons l USING (legacy_page_id)
JOIN question_bank_revision_lessons rl ON rl.lesson_id = l.lesson_id
JOIN question_bank_revisions r ON r.id = rl.revision_id
WHERE r.prompt=q.current_prompt AND r.status='draft' AND r.published_at IS NULL;

DO $$ DECLARE n int; BEGIN
  SELECT count(*) INTO n FROM _batch001_question_resolution;
  IF n <> 13 THEN RAISE EXCEPTION 'BATCH-001 question identity drift: expected 13, got %', n; END IF;
  SELECT count(DISTINCT revision_id) INTO n FROM _batch001_question_resolution;
  IF n <> 13 THEN RAISE EXCEPTION 'BATCH-001 question identity ambiguity: expected 13 unique revisions, got %', n; END IF;
  SELECT count(*) INTO n FROM _batch001_question_resolution WHERE decision='corrected';
  IF n <> 7 THEN RAISE EXCEPTION 'BATCH-001 correction count drift: expected 7, got %', n; END IF;
  SELECT count(*) INTO n
  FROM question_bank_revisions r JOIN question_bank_revision_lessons rl ON rl.revision_id=r.id
  WHERE rl.lesson_id IN (SELECT lesson_id FROM _batch001_lessons) AND r.status='draft' AND r.published_at IS NULL;
  IF n <> 13 THEN RAISE EXCEPTION 'BATCH-001 linked draft revision set drift: expected 13, got %', n; END IF;
  SELECT count(*) INTO n
  FROM _batch001_question_resolution q
  WHERE 1 <> (SELECT count(*) FROM question_bank_revision_sources rs
              WHERE rs.revision_id=q.revision_id AND rs.page_number=q.book_page
                AND rs.input_checksum_sha256=q.source_sha256
                AND rs.content_source_asset_id=q.source_asset_id);
  IF n <> 0 THEN RAISE EXCEPTION 'BATCH-001 question provenance ambiguity/missing count %', n; END IF;
END $$;

SELECT r.id FROM question_bank_revisions r JOIN _batch001_question_resolution q ON q.revision_id=r.id FOR UPDATE;

CREATE TEMP TABLE _batch001_mutation_counts(kind text PRIMARY KEY, affected int NOT NULL) ON COMMIT DROP;

WITH ins AS (
  INSERT INTO curriculum_sections(class_id,subject_id,slug,title,position,status)
  SELECT class_id,subject_id,'curated-english9-pb3-unit-1-revision','Unit 1 - Revision',1,'active' FROM _batch001_scope
  RETURNING id
)
INSERT INTO _batch001_mutation_counts SELECT 'section_insert',count(*) FROM ins;

WITH section AS (
  SELECT cs.id FROM curriculum_sections cs JOIN _batch001_scope sc USING(class_id,subject_id)
  WHERE cs.slug='curated-english9-pb3-unit-1-revision'
), upd AS (
  UPDATE lessons l SET section_id=section.id, slug=e.target_slug, title=e.target_title, position=e.position
  FROM _batch001_lessons e, section WHERE l.id=e.lesson_id RETURNING l.id
)
INSERT INTO _batch001_mutation_counts SELECT 'lesson_update',count(*) FROM upd;

WITH upd AS (
  UPDATE question_bank_revisions r
  SET type=q.target_type,
      prompt=q.target_prompt,
      options=COALESCE(q.target_options,r.options),
      correct_option_index=CASE WHEN q.target_options IS NULL THEN r.correct_option_index ELSE q.target_correct_option_index END,
      answer_text=CASE WHEN q.target_options IS NULL THEN r.answer_text ELSE q.target_options ->> q.target_correct_option_index END
  FROM _batch001_question_resolution q
  WHERE r.id=q.revision_id AND q.decision='corrected'
  RETURNING r.id
)
INSERT INTO _batch001_mutation_counts SELECT 'question_update',count(*) FROM upd;

DO $$ DECLARE s int; l int; q int; n int; BEGIN
  SELECT affected INTO s FROM _batch001_mutation_counts WHERE kind='section_insert';
  SELECT affected INTO l FROM _batch001_mutation_counts WHERE kind='lesson_update';
  SELECT affected INTO q FROM _batch001_mutation_counts WHERE kind='question_update';
  IF s<>1 OR l<>4 OR q<>7 THEN RAISE EXCEPTION 'BATCH-001 mutation counts %,%,% expected 1,4,7',s,l,q; END IF;

  SELECT count(*) INTO n
  FROM lessons x JOIN _batch001_lessons e ON e.lesson_id=x.id
  JOIN curriculum_sections cs ON cs.id=x.section_id
  WHERE x.slug=e.target_slug AND x.title=e.target_title AND x.position=e.position
    AND x.published_at IS NULL AND cs.slug='curated-english9-pb3-unit-1-revision';
  IF n<>4 THEN RAISE EXCEPTION 'BATCH-001 post lesson validation expected 4 got %',n; END IF;

  SELECT count(*) INTO n
  FROM question_bank_revisions r JOIN _batch001_question_resolution e ON e.revision_id=r.id
  WHERE e.decision='corrected' AND r.prompt=e.target_prompt AND r.type=e.target_type
    AND r.status='draft' AND r.published_at IS NULL
    AND (e.target_options IS NULL OR (r.options=e.target_options AND r.correct_option_index=e.target_correct_option_index AND r.answer_text=e.target_options->>e.target_correct_option_index));
  IF n<>7 THEN RAISE EXCEPTION 'BATCH-001 post question validation expected 7 got %',n; END IF;
END $$;

-- Audit accounting: 0 required event rows for this migration transaction. No lifecycle actor is fabricated.
SELECT kind,affected FROM _batch001_mutation_counts ORDER BY kind;
SELECT legacy_page_id,lesson_id,target_slug FROM _batch001_lessons ORDER BY position;

\if :apply
COMMIT;
\echo 'BATCH-001 APPLY COMMITTED: provenance-resolved 1 section + 4 lessons + 7 draft question corrections.'
\else
ROLLBACK;
\echo 'BATCH-001 DRY-RUN PASSED AND ROLLED BACK.'
\endif