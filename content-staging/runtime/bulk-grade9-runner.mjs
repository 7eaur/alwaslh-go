import { mkdir, writeFile } from 'node:fs/promises';

const mode = process.argv[2] ?? 'inspect';
const scripts = {
  inspect: './bulk-grade9-english-inspect.mjs',
  gate: './bulk-grade9-english-transaction-gate.mjs',
  apply: './bulk-grade9-english-apply.mjs',
  verify: './bulk-grade9-english-verify.mjs',
};

if (!scripts[mode]) {
  throw new Error(`BULK_G9_EN_RUNNER_FAIL: unsupported mode=${mode}`);
}

const manifestRef = process.env.BULK_G9_EN_MANIFEST_REF ?? 'a2e1f9b23aebc28ed0b750688a0fe525bae68bcd';
const manifestUrl = `https://raw.githubusercontent.com/7eaur/alwaslh-go/${manifestRef}/content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`;
const response = await fetch(manifestUrl, { signal: AbortSignal.timeout(20_000) });
if (!response.ok) {
  throw new Error(`BULK_G9_EN_RUNNER_FAIL: manifest fetch status=${response.status}`);
}
const text = await response.text();
const manifest = JSON.parse(text);
if (manifest?.counts?.page_candidates !== 69 || manifest?.counts?.raw_pages !== 69 || manifest?.counts?.raw_images !== 69 || manifest?.counts?.questions !== 104 || manifest?.counts?.sections !== 8) {
  throw new Error(`BULK_G9_EN_RUNNER_FAIL: pinned manifest invariant drift ${JSON.stringify(manifest?.counts ?? null)}`);
}

const targetDir = '/curated/grade-9/english/pupil-book-3';
await mkdir(targetDir, { recursive: true });
await writeFile(`${targetDir}/reconstruction-candidates.json`, text, { encoding: 'utf8', flag: 'w' });
console.log('BULK_G9_EN_RUNNER_MANIFEST_READY', JSON.stringify({ mode, manifestRef, pages: 69, questions: 104, sections: 8 }));

await import(scripts[mode]);
