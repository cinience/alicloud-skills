# install-serverless-devs-and-docker

Source:
- https://help.aliyun.com/zh/functioncompute/fc/developer-reference/install-serverless-devs-and-docker

## Key steps (FC 3.0 + Serverless Devs)

- Install Node.js (14+) and npm.
- Install Serverless Devs via npm and verify with `s -v`.
- Configure credentials with `s config add` (select Alibaba Cloud provider and enter AccountID/AK/SK, set alias).
- Initialize a Python starter project: `s init start-fc3-python` and `cd` into the directory.
- Deploy with `s deploy`, invoke with `s invoke -e "test"`, remove with `s remove`.

## Files created by init

- `s.yaml`
- `code/`
- `readme.md`
