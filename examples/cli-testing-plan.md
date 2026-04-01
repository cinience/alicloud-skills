# Alibaba Cloud Skills CLI 完整测试方案

更新时间：2026-02-28

## 1. 目标与范围

本方案用于系统验证当前仓库 CLI（`apps/cmd/alicloud-skills`）的可用性、稳定性和关键能力链路。

覆盖范围：
- 构建与单元测试
- CLI 参数和帮助语义
- 一次性执行模式（`-e`）
- 技能加载与运行路径
- 非实时语音闭环（TTS → ASR）交叉验证

不在本方案范围：
- 前端应用（`apps/web`）UI 自动化测试
- 云资源高风险写操作（创建/删除生产资源）

## 2. 前置条件

1. Go 环境可用（与 `apps/go.mod` 兼容）。
2. 已配置 `DASHSCOPE_API_KEY`（环境变量或 `~/.alibabacloud/credentials`）。
3. 网络可访问 DashScope 接口。
4. 在仓库根目录执行所有命令。

建议：
- 使用临时二进制路径，避免污染：`/tmp/alicloud-skills-cli`。

## 2.1 一键执行脚本（推荐）

仓库内提供自动化脚本：

```bash
scripts/run_cli_test_plan.sh --help
```

常用方式：

```bash
# 跑核心回归（L0/L1/L2/L3）
scripts/run_cli_test_plan.sh

# 跑完整回归（含 L4）
scripts/run_cli_test_plan.sh --with-l4

# 本地无语音凭证时跳过 L3
scripts/run_cli_test_plan.sh --skip-l3
```

输出目录默认：`output/cli-test/YYYYMMDD-HHMMSS/`，自动生成 `summary.md` 与各项日志。

## 2.2 CLI 内置瀑布流（LLM + Tool）

当需要直接观察单次请求内部的 LLM/tool 交互时，可在 CLI 增加 `--waterfall`：

```bash
/tmp/alicloud-skills-cli -e "ping" --waterfall --timeout-ms 120000
```

输出将包含：
- 每个步骤类型（`llm` / `tool`）
- 每步耗时（毫秒）
- 每轮 LLM token（`input/output/total`）
- 每步大概内容摘要（截断显示）

## 3. 测试分层

### L0：静态与构建层

目标：确认代码可编译、核心包测试通过。

```bash
go -C apps test ./cmd/alicloud-skills/...
go -C apps test ./internal/agent/...
go -C apps build -o /tmp/alicloud-skills-cli ./cmd/alicloud-skills
```

通过标准：
- 全部命令 exit code = 0
- 无编译错误

### L1：CLI 语义层

目标：确认帮助语义清晰、不会误入交互。

```bash
/tmp/alicloud-skills-cli --help
/tmp/alicloud-skills-cli help
/tmp/alicloud-skills-cli run --help
/tmp/alicloud-skills-cli api --help
```

通过标准：
- `run --help` 输出 `run [prompt...]` 与非交互执行说明（不进入 REPL）
- `api --help` 明确提示“当前无独立 api 子命令，使用 `-e`”
- `help` 输出根用法及快捷帮助

### L2：执行链路层

目标：确认 CLI 可发起一次真实请求并正常退出。

```bash
/tmp/alicloud-skills-cli -e "ping" --timeout-ms 120000
```

通过标准：
- exit code = 0
- 输出含语义正确回复（如 Pong/可用响应）

### L3：技能能力层（重点）

目标：验证非实时 TTS 与非实时 ASR 的闭环一致性。

#### Case A：中文闭环

```bash
/tmp/alicloud-skills-cli -e "Use aliyun-qwen-tts to synthesize the exact text '欢迎使用阿里云。' with non-realtime mode, then use aliyun-qwen-asr with non-realtime mode to transcribe that generated audio, and finally return: input_text, asr_text, normalized_equal (true/false), plus the audio URL." --timeout-ms 180000
```

#### Case B：英文闭环

```bash
/tmp/alicloud-skills-cli -e "Use aliyun-qwen-tts to synthesize the exact text 'Welcome to Alibaba Cloud.' with non-realtime mode, then use aliyun-qwen-asr with non-realtime mode to transcribe that generated audio, and finally return: input_text, asr_text, normalized_equal (true/false), plus the audio URL." --timeout-ms 180000
```

通过标准：
- 两个 case 的 `normalized_equal` 均为 `true`
- 均返回有效 `audio_url`
- ASR 状态为成功（或等价成功语义）

### L4：典型场景与鲁棒性层

目标：覆盖高频业务请求、边界输入、超时与稳定性。

#### A. 典型业务 Case

1) 技能列表可见性（发现链路）

```bash
printf '/skills\n/quit\n' | /tmp/alicloud-skills-cli
```

通过标准：
- 输出中包含 `aliyun-qwen-tts`、`aliyun-qwen-asr`

2) 文生图最小可用链路

```bash
/tmp/alicloud-skills-cli -e "Use aliyun-qwen-image to generate a 512*512 minimalist icon about cloud and return output image url only." --timeout-ms 180000
```

通过标准：
- 返回可访问图片 URL（或明确成功结构中的图片字段）

3) 向量检索最小问答链路（如账号具备权限）

```bash
/tmp/alicloud-skills-cli -e "Use aliyun-dashvector-search to create a small test collection, insert two short docs, and run a topk=2 query. Return only concise result JSON." --timeout-ms 180000
```

通过标准：
- 能给出检索结果或清晰的权限/环境缺失错误（不可出现参数幻觉）

#### B. 异常与边界 Case

4) 非法模型名应可诊断

```bash
/tmp/alicloud-skills-cli -e "Use aliyun-qwen-asr with model 'qwen3-asr-flash-xxx' to transcribe https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3 and show raw error." --timeout-ms 120000
```

通过标准：
- 返回明确错误信息（模型不存在/参数非法），不应返回伪成功

5) 缺少鉴权时的失败语义

```bash
env -u DASHSCOPE_API_KEY /tmp/alicloud-skills-cli -e "ping" --timeout-ms 120000
```

通过标准：
- 失败信息可定位到认证配置（而不是无意义 panic）

6) 超时控制有效性

```bash
/tmp/alicloud-skills-cli -e "Use aliyun-wan-video to generate a video and wait for final url." --timeout-ms 1000
```

通过标准：
- 在超时预算内结束并返回 timeout 语义（而不是无限阻塞）

#### C. 稳定性 Case

7) 同一请求重复执行的一致性（3 次）

```bash
for i in 1 2 3; do
  /tmp/alicloud-skills-cli -e "Use aliyun-qwen-tts to synthesize 'Welcome to Alibaba Cloud.' and return only audio url." --timeout-ms 180000
done
```

通过标准：
- 3 次都成功返回
- 响应结构稳定（字段形态一致）

8) 单次进程会话切换（REPL 命令）

```bash
printf '/model\n/new\n/session\n/quit\n' | /tmp/alicloud-skills-cli
```

通过标准：
- `/new` 后 session 变化
- `/model` 与 `/session` 输出语义正确

## 4. 验收判定

发布前建议采用如下门禁：

- 必须通过：L0 + L1 + L2
- 语音相关改动必须通过：L3
- CLI 主流程改动建议通过：L4 中 B6（超时）+ C8（会话命令）
- 任意层失败：禁止发布，先修复再重测

## 5. 输出与留证规范

所有测试输出与证据写入：
- `output/cli-test/YYYYMMDD/`

建议文件：
- `build-and-unit.log`
- `help-semantics.log`
- `oneshot-ping.log`
- `tts-asr-zh.log`
- `tts-asr-en.log`
- `l4-business.log`
- `l4-negative.log`
- `l4-stability.log`
- `summary.md`

`summary.md` 模板：

```md
# CLI 测试汇总

- 日期：YYYY-MM-DD
- 分支：<branch>
- 提交：<commit>

| 层级 | 用例 | 结果 | 备注 |
| --- | --- | --- | --- |
| L0 | 构建+单测 | pass/fail | ... |
| L1 | help 语义 | pass/fail | ... |
| L2 | -e ping | pass/fail | ... |
| L3 | TTS→ASR 中文 | pass/fail | ... |
| L3 | TTS→ASR 英文 | pass/fail | ... |
| L4A | 典型业务 case | pass/fail | ... |
| L4B | 异常/边界 case | pass/fail | ... |
| L4C | 稳定性 case | pass/fail | ... |
```

## 6. 常见失败与排查

1. `init failed` / 鉴权错误
- 检查 `DASHSCOPE_API_KEY`
- 检查 `~/.alibabacloud/credentials` 的 profile

2. ASR/TTS 404 或参数错误
- 核对模型名与接口协议是否匹配：
  - TTS（非实时）：`qwen3-tts-flash`
  - ASR（同步）：`qwen3-asr-flash` / `qwen-audio-asr`
  - ASR（长音频异步）：`qwen3-asr-flash-filetrans`

3. `run --help` 进入 REPL
- 确认为 Cobra 子命令帮助输出，且不会进入 REPL
- 重新 `go build` 后再测

4. 技能重复加载 warning 过多
- 当前为环境中多技能目录并存导致，不影响主流程正确性
- 可通过显式 `-skills-dir` 收敛来源

## 7. 回归策略

建议触发条件：
- 每次合并到 `main`
- 变更 `apps/cmd/alicloud-skills/**` 或 `apps/internal/agent/**`
- 变更 `skills/ai/audio/**`（尤其 ASR/TTS）

最小回归集：
- L0 全量
- L1 全量
- L2 1 条
- L3 中文 + 英文各 1 条
- L4B 至少 1 条（推荐 B6 超时）

## 8. 当前基线（已验证）

基于 2026-02-28 的本地执行结果：
- L0：通过
- L1：通过（`run/api/help` 语义已清晰）
- L2：通过
- L3：通过（中文/英文 `normalized_equal = true`）
