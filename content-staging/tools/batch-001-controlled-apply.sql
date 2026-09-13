\set ON_ERROR_STOP on
\if :{?apply}
\else
\set apply false
\endif

-- BATCH-001-G9-EN-PB3-U1
-- Default mode is a live transactional verification that always ROLLBACKs.
-- Explicit apply requires: psql -v apply=true -f content-staging/tools/batch-001-controlled-apply.sql
-- This script intentionally does NOT publish lessons, lesson assets, or question revisions.

BEGIN;
SET LOCAL lock_timeout = '5s';
SET LOCAL statement_timeout = '60s';
SET LOCAL application_name = 'alwaslh-content-rebuild-batch-001';

-- Fail closed if the modern schema is not the expected contract.
DO $$
DECLARE
  missing text[];
BEGIN
  SELECT array_agg(required_name ORDER BY required_name)
  INTO missing
  FROM (VALUES
    ('classes'), ('subjects'), ('subject_class_links'), ('curriculum_sections'),
    ('lessons'), ('lesson_assets'), ('media_assets'), ('content_source_assets'),
    ('question_bank_items'), ('question_bank_revisions'),
    ('question_bank_revision_lessons'), ('question_bank_revision_sources')
  ) AS required(required_name)
  WHERE to_regclass('public.' || required_name) IS NULL;

  IF missing IS NOT NULL THEN
    RAISE EXCEPTION 'BATCH-001 schema drift: missing tables %', missing;
  END IF;
END $$;

CREATE TEMP TABLE _batch001_scope (
  class_id uuid NOT NULL,
  subject_id uuid NOT NULL,
  PRIMARY KEY (class_id, subject_id)
) ON COMMIT DROP;

INSERT INTO _batch001_scope (class_id, subject_id)
SELECT c.id, s.id
FROM classes c
JOIN subjects s ON s.slug = 'english'
JOIN subject_class_links scl ON scl.class_id = c.id AND scl.subject_id = s.id
WHERE c.slug = 'grade-9'
  AND c.status = 'active'
  AND s.status = 'active'
  AND scl.status = 'active';

DO $$
DECLARE n integer;
BEGIN
  SELECT count(*) INTO n FROM _batch001_scope;
  IF n <> 1 THEN
    RAISE EXCEPTION 'BATCH-001 scope drift: expected exactly 1 active grade-9/english offering, got %', n;
  END IF;
END $$;

-- Lock the offering so the scope cannot change under this transaction.
SELECT scl.class_id
FROM subject_class_links scl
JOIN _batch001_scope sc USING (class_id, subject_id)
FOR UPDATE;

CREATE TEMP TABLE _batch001_lessons (
  lesson_id uuid PRIMARY KEY,
  position integer NOT NULL,
  book_page integer NOT NULL,
  target_slug text NOT NULL,
  target_title text NOT NULL,
  source_path text NOT NULL,
  source_sha256 text NOT NULL
) ON COMMIT DROP;

INSERT INTO _batch001_lessons VALUES
('2d98475c-91bf-4000-bfbc-79f7a6a854f9', 0, 1, 'curated-english9-pb3-u1-p001-presents-from-london', 'Presents from London', 'تاسع انجليزي/الانجليزي_تاسع/الصور/p001 - Presents from London.jpg', 'ae3e89be65d1c9ec5f70e361a5e78ea903d6e305f22d399e2c88bf864f6c3a4f'),
('5e207993-508f-426b-ae71-f00aa4f782df', 1, 2, 'curated-english9-pb3-u1-p002-whats-my-job', 'What''s my job?', 'تاسع انجليزي/الانجليزي_تاسع/الصور/p002 - What''s my job -.jpg', '1df05a27195e28e5543747c1f827a4d32c2bf937476c91ae69b0f4fe8b61b413'),
('dc1d6249-c0cb-4982-9711-092b1dcffee3', 2, 3, 'curated-english9-pb3-u1-p003-the-holidays', 'The holidays', 'تاسع انجليزي/الانجليزي_تاسع/الصور/p003 - The holidays.jpg', '78741ebd493e6b7dbbc05115472fec173edbeab9e05079b806a61acd1d7d13ac'),
('f2947d7f-5697-4bdc-b561-ad880a1afdf1', 3, 4, 'curated-english9-pb3-u1-p004-a-postcard-from-london', 'A postcard from London', 'تاسع انجليزي/الانجليزي_تاسع/الصور/p004 - A postcard from London.jpg', '86d655468bfbc73248da92e0d16d4b4dcccc0217df241e69bac94f6cee6cf321');

-- Lock and validate the four pre-existing lesson identities. No replacement insert is allowed.
SELECT l.id
FROM lessons l
JOIN _batch001_lessons e ON e.lesson_id = l.id
JOIN _batch001_scope sc ON sc.class_id = l.class_id AND sc.subject_id = l.subject_id
FOR UPDATE;

DO $$
DECLARE n integer;
BEGIN
  SELECT count(*) INTO n
  FROM lessons l
  JOIN _batch001_lessons e ON e.lesson_id = l.id
  JOIN _batch001_scope sc ON sc.class_id = l.class_id AND sc.subject_id = l.subject_id
  WHERE l.status = 'active' AND l.published_at IS NULL;
  IF n <> 4 THEN
    RAISE EXCEPTION 'BATCH-001 lesson drift: expected 4 exact active unpublished lessons, got %', n;
  END IF;

  SELECT count(*) INTO n
  FROM lessons l
  JOIN _batch001_scope sc ON sc.class_id = l.class_id AND sc.subject_id = l.subject_id
  JOIN _batch001_lessons e ON e.target_slug = l.slug
  WHERE l.id <> e.lesson_id;
  IF n <> 0 THEN
    RAISE EXCEPTION 'BATCH-001 slug collision: % target slugs belong to different lesson identities', n;
  END IF;
END $$;

-- Provenance gate: every lesson must resolve to exactly one draft lesson asset -> ready media -> exact immutable source asset.
DO $$
DECLARE n integer;
BEGIN
  SELECT count(*) INTO n
  FROM _batch001_lessons e
  JOIN lesson_assets la ON la.lesson_id = e.lesson_id
  JOIN media_assets ma ON ma.id = la.media_asset_id
  JOIN content_source_assets csa ON csa.id = ma.content_source_asset_id
  WHERE la.publication_status = 'draft'
    AND la.asset_published_at IS NULL
    AND ma.status = 'ready'
    AND csa.is_present = true
    AND csa.source_path = e.source_path
    AND csa.checksum_sha256 = e.source_sha256
    AND ma.source_checksum_sha256 = e.source_sha256;
  IF n <> 4 THEN
    RAISE EXCEPTION 'BATCH-001 provenance drift: expected 4 exact draft/ready/source chains, got %', n;
  END IF;

  SELECT count(*) INTO n
  FROM _batch001_lessons e
  WHERE 1 <> (
    SELECT count(*)
    FROM lesson_assets la
    JOIN media_assets ma ON ma.id = la.media_asset_id
    JOIN content_source_assets csa ON csa.id = ma.content_source_asset_id
    WHERE la.lesson_id = e.lesson_id
      AND la.publication_status = 'draft'
      AND la.asset_published_at IS NULL
      AND ma.status = 'ready'
      AND csa.is_present = true
      AND csa.source_path = e.source_path
      AND csa.checksum_sha256 = e.source_sha256
      AND ma.source_checksum_sha256 = e.source_sha256
  );
  IF n <> 0 THEN
    RAISE EXCEPTION 'BATCH-001 provenance ambiguity: % lessons do not have exactly one exact source chain', n;
  END IF;
END $$;

-- The validated pre-state requires the curated section to be absent. Existing section means count drift / possible prior apply.
DO $$
DECLARE n integer;
BEGIN
  SELECT count(*) INTO n
  FROM curriculum_sections cs
  JOIN _batch001_scope sc ON sc.class_id = cs.class_id AND sc.subject_id = cs.subject_id
  WHERE cs.slug = 'curated-english9-pb3-unit-1-revision';
  IF n <> 0 THEN
    RAISE EXCEPTION 'BATCH-001 section drift: expected 0 target sections before apply, got %', n;
  END IF;
END $$;

CREATE TEMP TABLE _batch001_questions (
  lesson_id uuid NOT NULL,
  source_index integer NOT NULL,
  current_prompt text NOT NULL,
  decision text NOT NULL CHECK (decision IN ('approved','corrected')),
  target_type question_bank_question_type NOT NULL,
  target_prompt text NOT NULL,
  target_options jsonb,
  target_correct_option_index integer,
  PRIMARY KEY (lesson_id, source_index)
) ON COMMIT DROP;

INSERT INTO _batch001_questions VALUES
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',0,'How old is Saleh?','approved','multiple_choice','How old is Saleh?',NULL,NULL),
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',1,'Saleh is seventeen years old.','approved','true_false','Saleh is seventeen years old.',NULL,NULL),
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',2,'What does Mr Al Sabri want to buy for Saleh?','corrected','multiple_choice','What does Mr Al Sabri suggest Taha buy for Saleh?','["a pair of shorts","a school uniform","a bicycle","a camera"]'::jsonb,0),
('2d98475c-91bf-4000-bfbc-79f7a6a854f9',3,'What does Saleh like?','approved','multiple_choice','What does Saleh like?',NULL,NULL),
('5e207993-508f-426b-ae71-f00aa4f782df',0,'Taha works in a clinic.','corrected','true_false','The dentist works in a clinic.',NULL,NULL),
('5e207993-508f-426b-ae71-f00aa4f782df',1,'What is Taha''s job?','corrected','multiple_choice','What is the job of the person who takes care of people''s teeth?','["a dentist","a teacher","a doctor","a police officer"]'::jsonb,0),
('5e207993-508f-426b-ae71-f00aa4f782df',2,'What time does the office worker start work?','approved','multiple_choice','What time does the office worker start work?',NULL,NULL),
('5e207993-508f-426b-ae71-f00aa4f782df',3,'Where does the doctor work?','corrected','multiple_choice','Where does the dentist work?','["in a clinic","in an office","in a hospital","in a school"]'::jsonb,0),
('dc1d6249-c0cb-4982-9711-092b1dcffee3',0,'The family went to London for the holidays.','corrected','true_false','One speaker went to a village by the sea in the holidays.',NULL,NULL),
('dc1d6249-c0cb-4982-9711-092b1dcffee3',1,'What did Amna do every day?','corrected','multiple_choice','What did the first speaker do every day?','["went swimming and fishing","stayed at home","went shopping","worked on a farm"]'::jsonb,0),
('dc1d6249-c0cb-4982-9711-092b1dcffee3',2,'Where did Mr Al Sabri and his family go on holiday?','corrected','multiple_choice','Where did the first speaker go in the holidays?','["a village by the sea","London","Paris","Sana''a"]'::jsonb,0),
('f2947d7f-5697-4bdc-b561-ad880a1afdf1',0,'Amna wrote a postcard to Mariam.','approved','true_false','Amna wrote a postcard to Mariam.',NULL,NULL),
('f2947d7f-5697-4bdc-b561-ad880a1afdf1',1,'What did Amna write to Mariam?','approved','multiple_choice','What did Amna write to Mariam?',NULL,NULL);

-- Resolve questions by existing lesson linkage + exact current prompt; ambiguity or previously changed content is a hard stop.
CREATE TEMP TABLE _batch001_question_resolution ON COMMIT DROP AS
SELECT e.lesson_id, e.source_index, e.decision, e.target_type, e.target_prompt,
       e.target_options, e.target_correct_option_index, r.id AS revision_id
FROM _batch001_questions e
JOIN question_bank_revision_lessons rl ON rl.lesson_id = e.lesson_id
JOIN question_bank_revisions r ON r.id = rl.revision_id
WHERE r.prompt = e.current_prompt
  AND r.status = 'draft'
  AND r.published_at IS NULL;

DO $$
DECLARE n integer;
BEGIN
  SELECT count(*) INTO n FROM _batch001_question_resolution;
  IF n <> 13 THEN
    RAISE EXCEPTION 'BATCH-001 question identity drift: expected 13 exact draft prompt/lesson matches, got %', n;
  END IF;

  SELECT count(*) INTO n
  FROM _batch001_questions e
  WHERE 1 <> (
    SELECT count(*) FROM _batch001_question_resolution r
    WHERE r.lesson_id = e.lesson_id AND r.source_index = e.source_index
  );
  IF n <> 0 THEN
    RAISE EXCEPTION 'BATCH-001 question ambiguity: % reviewed locators do not resolve exactly once', n;
  END IF;

  SELECT count(*) INTO n
  FROM question_bank_revisions r
  JOIN question_bank_revision_lessons rl ON rl.revision_id = r.id
  JOIN _batch001_lessons l ON l.lesson_id = rl.lesson_id
  WHERE r.status = 'draft' AND r.published_at IS NULL;
  IF n <> 13 THEN
    RAISE EXCEPTION 'BATCH-001 question set drift: expected exactly 13 draft revisions linked to the four lessons, got %', n;
  END IF;

  SELECT count(*) INTO n
  FROM _batch001_question_resolution qr
  JOIN question_bank_revision_sources rs ON rs.revision_id = qr.revision_id
  JOIN _batch001_lessons l ON l.lesson_id = qr.lesson_id
  WHERE rs.page_number = l.book_page
    AND rs.input_checksum_sha256 = l.source_sha256;
  IF n <> 13 THEN
    RAISE EXCEPTION 'BATCH-001 question provenance drift: expected 13 source links matching page/checksum, got %', n;
  END IF;

  SELECT count(*) INTO n FROM _batch001_question_resolution WHERE decision = 'corrected';
  IF n <> 7 THEN
    RAISE EXCEPTION 'BATCH-001 correction count drift: expected 7, got %', n;
  END IF;
END $$;

-- Lock all 13 revisions after resolution and before mutation.
SELECT r.id
FROM question_bank_revisions r
JOIN _batch001_question_resolution qr ON qr.revision_id = r.id
FOR UPDATE;

-- Snapshot the reversible business fields inside this transaction. In default mode they are restored by ROLLBACK.
CREATE TEMP TABLE _batch001_lesson_before ON COMMIT DROP AS
SELECT l.id, l.section_id, l.slug, l.title, l.position, l.published_at
FROM lessons l JOIN _batch001_lessons e ON e.lesson_id = l.id;

CREATE TEMP TABLE _batch001_question_before ON COMMIT DROP AS
SELECT r.id, r.type, r.prompt, r.options, r.correct_option_index, r.answer_text,
       r.answer_status, r.explanation, r.method, r.status, r.published_at
FROM question_bank_revisions r
JOIN _batch001_question_resolution qr ON qr.revision_id = r.id
WHERE qr.decision = 'corrected';

CREATE TEMP TABLE _batch001_mutation_counts(kind text PRIMARY KEY, affected integer NOT NULL) ON COMMIT DROP;

WITH sc AS (SELECT class_id, subject_id FROM _batch001_scope), ins AS (
  INSERT INTO curriculum_sections (class_id, subject_id, slug, title, position, status)
  SELECT class_id, subject_id, 'curated-english9-pb3-unit-1-revision', 'Unit 1 - Revision', 1, 'active'
  FROM sc
  RETURNING id
)
INSERT INTO _batch001_mutation_counts
SELECT 'section_insert', count(*) FROM ins;

WITH section AS (
  SELECT cs.id
  FROM curriculum_sections cs
  JOIN _batch001_scope sc ON sc.class_id = cs.class_id AND sc.subject_id = cs.subject_id
  WHERE cs.slug = 'curated-english9-pb3-unit-1-revision'
), upd AS (
  UPDATE lessons l
  SET section_id = section.id,
      slug = e.target_slug,
      title = e.target_title,
      position = e.position
  FROM _batch001_lessons e, section
  WHERE l.id = e.lesson_id
  RETURNING l.id
)
INSERT INTO _batch001_mutation_counts
SELECT 'lesson_update', count(*) FROM upd;

WITH upd AS (
  UPDATE question_bank_revisions r
  SET type = qr.target_type,
      prompt = qr.target_prompt,
      options = CASE WHEN qr.target_options IS NULL THEN r.options ELSE qr.target_options END,
      correct_option_index = CASE WHEN qr.target_options IS NULL THEN r.correct_option_index ELSE qr.target_correct_option_index END,
      answer_text = CASE
        WHEN qr.target_options IS NULL THEN r.answer_text
        ELSE qr.target_options ->> qr.target_correct_option_index
      END
  FROM _batch001_question_resolution qr
  WHERE r.id = qr.revision_id
    AND qr.decision = 'corrected'
  RETURNING r.id
)
INSERT INTO _batch001_mutation_counts
SELECT 'question_update', count(*) FROM upd;

DO $$
DECLARE
  sections integer;
  lesson_updates integer;
  question_updates integer;
  n integer;
BEGIN
  SELECT affected INTO sections FROM _batch001_mutation_counts WHERE kind = 'section_insert';
  SELECT affected INTO lesson_updates FROM _batch001_mutation_counts WHERE kind = 'lesson_update';
  SELECT affected INTO question_updates FROM _batch001_mutation_counts WHERE kind = 'question_update';

  IF sections <> 1 OR lesson_updates <> 4 OR question_updates <> 7 THEN
    RAISE EXCEPTION 'BATCH-001 mutation count mismatch: section %, lessons %, questions % (expected 1/4/7)', sections, lesson_updates, question_updates;
  END IF;

  SELECT count(*) INTO n
  FROM lessons l
  JOIN _batch001_lessons e ON e.lesson_id = l.id
  JOIN curriculum_sections cs ON cs.id = l.section_id
  WHERE l.slug = e.target_slug
    AND l.title = e.target_title
    AND l.position = e.position
    AND l.published_at IS NULL
    AND cs.slug = 'curated-english9-pb3-unit-1-revision';
  IF n <> 4 THEN
    RAISE EXCEPTION 'BATCH-001 post-check failed: expected 4 curated unpublished lessons, got %', n;
  END IF;

  SELECT count(*) INTO n
  FROM question_bank_revisions r
  JOIN _batch001_question_resolution qr ON qr.revision_id = r.id
  WHERE qr.decision = 'corrected'
    AND r.prompt = qr.target_prompt
    AND r.type = qr.target_type
    AND r.status = 'draft'
    AND r.published_at IS NULL
    AND (qr.target_options IS NULL OR (
      r.options = qr.target_options
      AND r.correct_option_index = qr.target_correct_option_index
      AND r.answer_text = qr.target_options ->> qr.target_correct_option_index
    ));
  IF n <> 7 THEN
    RAISE EXCEPTION 'BATCH-001 post-check failed: expected 7 corrected draft revisions, got %', n;
  END IF;

  SELECT count(*) INTO n
  FROM lesson_assets la
  JOIN _batch001_lessons e ON e.lesson_id = la.lesson_id
  WHERE la.publication_status <> 'draft' OR la.asset_published_at IS NOT NULL;
  IF n <> 0 THEN
    RAISE EXCEPTION 'BATCH-001 publication invariant failed: lesson assets changed publication state';
  END IF;
END $$;

-- Audit accounting for this controlled content migration:
-- * curriculum_events: schema does not require an event; no actor is required by table, but none is fabricated here.
-- * question_bank_events: actor_profile_id is NOT NULL. This transaction does not fabricate an actor and does not
--   change lifecycle status, so it appends 0 question_bank_events. Review/publish events remain application-owned.
-- Therefore expected direct business-row mutations are exactly 12 and expected audit/event rows are 0 for this gate.

SELECT kind, affected FROM _batch001_mutation_counts ORDER BY kind;
SELECT 'BATCH-001 controlled transaction validated; publication remained closed' AS result;

\if :apply
COMMIT;
\echo 'BATCH-001 APPLY COMMITTED: 1 section + 4 lesson updates + 7 draft question corrections.'
\else
ROLLBACK;
\echo 'BATCH-001 DRY-RUN PASSED AND ROLLED BACK. Re-run with -v apply=true only after this gate is recorded.'
\endif
