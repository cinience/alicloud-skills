---
name: alicloud-ai-text-document-mind
description: Use Document Mind (DocMind) via Node.js SDK to submit document parsing jobs and poll results. Designed for Claude Code/Codex document understanding workflows.
---

Category: provider

# Document Mind (DocMind) — Node.js SDK

Use DocMind to extract document structure, text, and layout with async jobs.

## Prerequisites

- Install SDKs:
  - `npm install @alicloud/docmind-api20220711 @alicloud/tea-util @alicloud/credentials`
- Provide credentials via standard Alibaba Cloud env vars:
  - `ALICLOUD_ACCESS_KEY_ID`
  - `ALICLOUD_ACCESS_KEY_SECRET`
  - `ALICLOUD_REGION_ID` (optional default; if unset, choose the most reasonable region for the task or ask the user)

## Quickstart (submit + poll)

```js
const Client = require('@alicloud/docmind-api20220711');
const Credential = require('@alicloud/credentials');
const Util = require('@alicloud/tea-util');

const cred = new Credential.default();
const regionId = process.env.ALICLOUD_REGION_ID || 'cn-hangzhou'; // Example default; choose/ask if unset.
const client = new Client.default({
  endpoint: `docmind-api.${regionId}.aliyuncs.com`,
  accessKeyId: cred.credential.accessKeyId,
  accessKeySecret: cred.credential.accessKeySecret,
  type: 'access_key',
  regionId,
});

async function submitByUrl(fileUrl, fileName) {
  const req = new Client.SubmitDocStructureJobRequest();
  req.fileUrl = fileUrl;
  req.fileName = fileName;
  const resp = await client.submitDocStructureJob(req);
  return resp.body.data.id;
}

async function pollResult(jobId) {
  const req = new Client.GetDocStructureResultRequest();
  req.id = jobId;
  const resp = await client.getDocStructureResult(req);
  return resp.body;
}

(async () => {
  const jobId = await submitByUrl('https://example.com/example.pdf', 'example.pdf');
  console.log('jobId:', jobId);

  // Poll every 10s until completed.
  for (;;) {
    const result = await pollResult(jobId);
    if (result.completed) {
      console.log(result.status, result.data || result.message);
      break;
    }
    await new Promise((r) => setTimeout(r, 10000));
  }
})();
```

## Script quickstart

```bash
DOCMIND_FILE_URL="https://example.com/example.pdf" \\
node skills/ai/text/alicloud-ai-text-document-mind/scripts/quickstart.js
```

Environment variables:

- `DOCMIND_FILE_URL`
- `DOCMIND_FILE_NAME` (optional)
- `DOCMIND_POLL_INTERVAL_MS` (optional, default 10000)
- `DOCMIND_MAX_POLLS` (optional, default 120)

## Local file upload

```js
const fs = require('fs');
const advanceReq = new Client.SubmitDocStructureJobAdvanceRequest();
advanceReq.fileUrlObject = fs.createReadStream('./example.pdf');
advanceReq.fileName = 'example.pdf';
const runtime = new Util.RuntimeOptions({});
const resp = await client.submitDocStructureJobAdvance(advanceReq, runtime);
```

## Notes for Claude Code/Codex

- DocMind is async: submit a job, then poll until `completed=true`.
- Poll every ~10s; max processing window is 120 minutes.
- Keep files publicly accessible when using URL submission.

## Error handling

- `UrlNotLegal`: URL not publicly accessible or malformed.
- `DocProcessing`: job still running; keep polling.
- `Fail`: check `message` and error code for root cause.

## References

- DocMind Node.js SDK: `@alicloud/docmind-api20220711`

- Source list: `references/sources.md`
