#!/usr/bin/env bash
# Batch publish skills to ClawHub with rate-limit awareness
# Max 5 new skills per hour — waits 62 minutes between batches
set -euo pipefail

LOG="/home/vipas/workspace/saker-ai/alicloud-skills/scripts/publish.log"
BATCH_SIZE=5
WAIT_SECONDS=3720  # 62 minutes
S="/home/vipas/workspace/saker-ai/alicloud-skills/skills"

# Absolute paths for all 75 remaining skills
DIRS=(
  "$S/ai/audio/aliyun-qwen-tts-voice-clone"
  "$S/ai/audio/aliyun-qwen-tts-voice-design"
  "$S/ai/code/aliyun-qwen-coder"
  "$S/ai/content/aliyun-aicontent-generate"
  "$S/ai/content/aliyun-aimiaobi-generate"
  "$S/ai/entry/aliyun-modelstudio-entry"
  "$S/ai/entry/aliyun-modelstudio-entry-test"
  "$S/ai/image/aliyun-qwen-image"
  "$S/ai/image/aliyun-qwen-image-edit"
  "$S/ai/image/aliyun-zimage-turbo"
  "$S/ai/misc/aliyun-modelstudio-crawl-and-skill"
  "$S/ai/multimodal/aliyun-qvq"
  "$S/ai/multimodal/aliyun-qwen-ocr"
  "$S/ai/multimodal/aliyun-qwen-omni"
  "$S/ai/multimodal/aliyun-qwen-vl"
  "$S/ai/platform/aliyun-pai-workspace"
  "$S/ai/recommendation/aliyun-airec-manage"
  "$S/ai/research/aliyun-qwen-deep-research"
  "$S/ai/search/aliyun-dashvector-search"
  "$S/ai/search/aliyun-milvus-search"
  "$S/ai/search/aliyun-opensearch-search"
  "$S/ai/search/aliyun-qwen-multimodal-embedding"
  "$S/ai/search/aliyun-qwen-rerank"
  "$S/ai/search/aliyun-qwen-text-embedding"
  "$S/ai/service/aliyun-ccai-manage"
  "$S/ai/service/aliyun-ccc-manage"
  "$S/ai/service/aliyun-chatbot-manage"
  "$S/ai/text/aliyun-docmind-extract"
  "$S/ai/text/aliyun-qwen-generation"
  "$S/ai/translation/aliyun-anytrans-translate"
  "$S/ai/video/aliyun-animate-anyone"
  "$S/ai/video/aliyun-emoji"
  "$S/ai/video/aliyun-emo"
  "$S/ai/video/aliyun-liveportrait"
  "$S/ai/video/aliyun-pixverse-generation"
  "$S/ai/video/aliyun-videoretalk"
  "$S/ai/video/aliyun-wan-digital-human"
  "$S/ai/video/aliyun-wan-edit"
  "$S/ai/video/aliyun-wan-r2v"
  "$S/ai/video/aliyun-wan-video"
  "$S/backup/aliyun-bdrc-backup"
  "$S/backup/aliyun-hbr-backup"
  "$S/compute/fc/aliyun-fc-agentrun"
  "$S/compute/fc/aliyun-fc-serverless-devs"
  "$S/compute/swas/aliyun-swas-manage"
  "$S/data-analytics/aliyun-gbi-analytics"
  "$S/database/analyticdb/aliyun-adb-mysql"
  "$S/database/rds/aliyun-rds-supabase"
  "$S/data-lake/aliyun-dlf-manage"
  "$S/data-lake/aliyun-dlf-manage-next"
  "$S/media/ice/aliyun-ice-manage"
  "$S/media/live/aliyun-live-manage"
  "$S/media/mps/aliyun-mps-manage"
  "$S/media/video/aliyun-mps-video-translation"
  "$S/media/vod/aliyun-vod-manage"
  "$S/network/cdn/aliyun-cdn-manage"
  "$S/network/dns/aliyun-dns-cli"
  "$S/network/esa/aliyun-esa-manage"
  "$S/network/slb/aliyun-alb-manage"
  "$S/observability/pts/aliyun-pts-manage"
  "$S/observability/sls/aliyun-sls-log-query"
  "$S/observability/sls/aliyun-sls-openclaw-integration"
  "$S/platform/cli/aliyun-cli-manage"
  "$S/platform/devops/aliyun-devops-manage"
  "$S/platform/docs/aliyun-platform-docs-benchmark"
  "$S/platform/docs/aliyun-platform-docs-review"
  "$S/platform/openapi/aliyun-openapi-discovery"
  "$S/platform/openclaw/aliyun-openclaw-setup"
  "$S/platform/skills/aliyun-skill-creator"
  "$S/security/content/aliyun-green-moderation"
  "$S/security/firewall/aliyun-cloudfw-manage"
  "$S/security/host/aliyun-sas-manage"
  "$S/security/identity/aliyun-cloudauth-verify"
  "$S/security/key-management/aliyun-kms-manage"
  "$S/solutions/aliyun-solution-article-illustrator"
  "$S/storage/oss/aliyun-oss-ossutil"
)

echo "$(date): Starting batch publish of ${#DIRS[@]} skills" | tee "$LOG"

batch=0
count=0
ok=0
fail=0
for dir in "${DIRS[@]}"; do
  skill=$(basename "$dir")

  if (( count > 0 && count % BATCH_SIZE == 0 )); then
    batch=$((batch + 1))
    echo "$(date): Batch $batch done (ok=$ok fail=$fail). Waiting ${WAIT_SECONDS}s (~62min)..." | tee -a "$LOG"
    sleep "$WAIT_SECONDS"
  fi

  if [[ ! -d "$dir" ]]; then
    echo "$(date): SKIP $skill — dir not found: $dir" | tee -a "$LOG"
    continue
  fi

  echo "$(date): Publishing $skill..." | tee -a "$LOG"
  retries=0
  while true; do
    output=$(clawhub publish "$dir" --version 1.0.0 2>&1) && {
      echo "$output" >> "$LOG"
      echo "$(date): OK: $skill" | tee -a "$LOG"
      ok=$((ok + 1))
      break
    }
    echo "$output" >> "$LOG"
    if echo "$output" | grep -q "Rate limit"; then
      retries=$((retries + 1))
      if (( retries > 3 )); then
        echo "$(date): GIVE UP: $skill after $retries rate-limit retries" | tee -a "$LOG"
        fail=$((fail + 1))
        break
      fi
      echo "$(date): Rate limited on $skill, waiting 62min (retry $retries/3)..." | tee -a "$LOG"
      sleep 3720
    else
      echo "$(date): FAIL: $skill (non-rate-limit error)" | tee -a "$LOG"
      fail=$((fail + 1))
      break
    fi
  done

  count=$((count + 1))
done

echo "$(date): All done! total=$count ok=$ok fail=$fail batches=$((batch + 1))" | tee -a "$LOG"
