#!/usr/bin/env python3
import json
from pathlib import Path

MASTER = Path("content-staging/manifests/MASTER_CONTENT_MANIFEST.json")
LOG = Path("content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md")

master = json.loads(MASTER.read_text(encoding="utf-8"))
processed_exam = []
for source in master.get("sources", []):
    status = str(source.get("review_status") or "")
    exam = source.get("exam_reconstruction")
    if status.startswith("processed_") and isinstance(exam, dict):
        processed_exam.append((source["id"], int(exam.get("correction_sheet_candidates") or 0)))
assert len(processed_exam) == 9, processed_exam
correction_total = sum(value for _, value in processed_exam)
assert correction_total == 140, processed_exam
master["reconstruction_progress"]["correction_sheet_candidates"] = correction_total
MASTER.write_text(json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

text = LOG.read_text(encoding="utf-8")
marker = "## 10. ACTIVE CHECKPOINT"
rule = "---\n\n### Shared handoff rule"
a = text.index(marker)
b = text.index(rule, a)
active = """## 10. ACTIVE CHECKPOINT

- state: `READY`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `d28c2943c8ff20ec42f3091e3c693eba373da35d`
- last completed source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- current source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- current source baseline from live manifest: `61 images/pages; 138 legacy questions; no listed duplicate-page/missing-image/malformed-image anomalies; technical verification NOT VERIFIED`
- current operation: `read History manifest/pages -> technically verify all 61 source images -> prove exact source identity before using any master reference -> reconstruct Book/Unit/Lesson/page boundaries from History evidence only -> isolate review/non-lesson material -> map the 138 legacy questions only where structurally evidenced -> assert global 25,755 invariant -> checkpoint`
- next source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- blockers: `none for the current source; source 1794eea5-4772-4c94-bd2b-b08e5815e733 (Grade 9 English book) remains review_needed in corpus master but is explicitly skipped because closed Grade 9 English work must not be rerun without fresh drift evidence; reconcile that closed source from existing verified evidence at a dedicated non-rerun reconciliation gate.`
- owner decision required now: `no`

"""
text = text[:a] + active + text[b:]
run = """

## RUN 2026-09-14T12:14:00+03:00 — Worker B

- state: COMPLETE
- start HEAD: `d9564231905245126316125e55ae46b5604549a1`
- end HEAD before handoff-log commit: `d28c2943c8ff20ec42f3091e3c693eba373da35d`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- completed in this run:
  - verified Worker A's English 1446 handoff against live HEAD and canonical reconstruction evidence;
  - technically verified all 42 English 1447 source images with existence/readability/byte-size/SHA-256/MIME = 42/42 and no within-source SHA duplicates;
  - preserved source numbering anomalies exactly: missing numeric labels 12, 26, 37 and duplicate numeric labels 18, 27, 29;
  - generated and visually reviewed complete contact sheets for all 42 source records;
  - resolved 13 complete Individual Exam Models / 39 finalized pages from source-record identity + visual evidence, without inheriting 1446 boundaries;
  - isolated 3 page records as review_required rather than fabricating model 13 or silently repairing metadata;
  - structurally mapped all 234/234 legacy questions to finalized models; semantic correctness remains NOT VERIFIED;
  - finalized reconstruction and canonical manifests/status documents;
  - reconciled the global correction-candidate aggregate from the nine processed exam source records only: 140 total; no source evidence changed.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/da6fc228-1ada-4627-8306-80d9d3401490.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/da6fc228-1ada-4627-8306-80d9d3401490-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/da6fc228-1ada-4627-8306-80d9d3401490.json`;
  - discovery run `34826039800`: success after validation-only schema correction from initial run `34825927300`;
  - source-order evidence run `34826307823`: success; artifact `10340652157`; SHA-256 `358985b359cc04f8ae14693ddbd0a880b33d132c13a8a26f0eb249139fbe72cd`;
  - finalization run `34826701560`: success with `ENGLISH_1447_FINALIZATION_VERIFY_PASS`;
  - final artifact `10340672655`; SHA-256 `e709c14fb086289ece84a44f0e4cab495b18b08f9d0d413f6838c26631321a95`.
- ambiguity/review_required:
  - source record 29 (stored page 29): distinct unmatched paper-2 record; `review_required`;
  - source records 38..39: model-13 paper 2 + correction, but paper 1 is `NOT VERIFIED`; both `review_required`; numeric page 37 was not fabricated;
  - source record 27 metadata says model-13 paper 1 but visual evidence is a correction/result sheet in completed model 9; RAW metadata remains unchanged;
  - standalone official Answer Keys: 0 / NOT VERIFIED.
- invariant result: PASS (`2,236 + 967 + 351 + 22,201 = 25,755`)
- Sources processed: 12/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 140
- Source images technical: 950/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,201
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- current source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- exact next operation: `Do not rerun closed Grade 9 English source 1794eea5-4772-4c94-bd2b-b08e5815e733 absent fresh drift evidence. Start History from its own 61-image/138-question manifest: technical verification -> exact identity -> visual/structural reconstruction -> question mapping -> invariant -> checkpoint.`
- next source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- blockers: `none for History; Grade 9 English corpus-master review_needed state is a deferred non-rerun reconciliation item, not permission to rerun its closed work.`
- handoff note: `Worker A must re-fetch live HEAD and this baton. English 1447 is closed. Proceed with History while preserving the no-rerun rule for Grade 9 English.`
"""
if "## RUN 2026-09-14T12:14:00+03:00 — Worker B" not in text:
    text = text.rstrip() + run + "\n"
LOG.write_text(text, encoding="utf-8")
print(json.dumps({"processed_exam_groups": len(processed_exam), "correction_candidates": correction_total, "next_source": "0a76f44b-0a4f-4e36-9ea9-badecf78bf23"}, ensure_ascii=False))
