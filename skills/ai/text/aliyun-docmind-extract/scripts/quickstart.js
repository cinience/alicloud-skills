const Client = require('@alicloud/docmind-api20220711');
const Credential = require('@alicloud/credentials');

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const fileUrl = process.env.DOCMIND_FILE_URL;
const fileName = process.env.DOCMIND_FILE_NAME || 'example.pdf';
const regionId = process.env.ALICLOUD_REGION_ID || 'cn-hangzhou';
const pollIntervalMs = Number(process.env.DOCMIND_POLL_INTERVAL_MS || 10000);
const maxPolls = Number(process.env.DOCMIND_MAX_POLLS || 120);

if (!fileUrl) {
  console.error('Missing env var: DOCMIND_FILE_URL');
  process.exit(1);
}

(async () => {
  const cred = new Credential.default();
  const client = new Client.default({
    endpoint: 'docmind-api.cn-hangzhou.aliyuncs.com',
    accessKeyId: cred.credential.accessKeyId,
    accessKeySecret: cred.credential.accessKeySecret,
    type: 'access_key',
    regionId,
  });

  const submitReq = new Client.SubmitDocStructureJobRequest();
  submitReq.fileUrl = fileUrl;
  submitReq.fileName = fileName;

  const submitResp = await client.submitDocStructureJob(submitReq);
  const jobId = submitResp.body.data.id;
  console.log('jobId:', jobId);

  const resultReq = new Client.GetDocStructureResultRequest();
  resultReq.id = jobId;

  let polls = 0;
  for (;;) {
    const result = await client.getDocStructureResult(resultReq);
    if (result.body.completed) {
      console.log(result.body.status, result.body.data || result.body.message);
      break;
    }
    polls += 1;
    if (polls >= maxPolls) {
      console.error('Polling timed out.');
      process.exit(1);
    }
    await sleep(pollIntervalMs);
  }
})();
