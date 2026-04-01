#!/usr/bin/env bash
# Rename all skills from alicloud-* to aliyun-{product}-{function}
# Creates symlinks at old locations for backward compatibility.
# Idempotent: skips already-renamed directories.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# === Mapping: old_name new_name ===
declare -a MAPPING=(
  # Model Studio (百炼)
  "alicloud-ai-audio-asr|aliyun-modelstudio-asr"
  "alicloud-ai-audio-asr-realtime|aliyun-modelstudio-asr-realtime"
  "alicloud-ai-audio-cosyvoice-voice-clone|aliyun-modelstudio-cosyvoice-voice-clone"
  "alicloud-ai-audio-cosyvoice-voice-design|aliyun-modelstudio-cosyvoice-voice-design"
  "alicloud-ai-audio-livetranslate|aliyun-modelstudio-livetranslate"
  "alicloud-ai-audio-tts|aliyun-modelstudio-tts"
  "alicloud-ai-audio-tts-realtime|aliyun-modelstudio-tts-realtime"
  "alicloud-ai-audio-tts-voice-clone|aliyun-modelstudio-tts-voice-clone"
  "alicloud-ai-audio-tts-voice-design|aliyun-modelstudio-tts-voice-design"
  "alicloud-ai-code-qwen-coder|aliyun-modelstudio-qwen-coder"
  "alicloud-ai-entry-modelstudio|aliyun-modelstudio-entry"
  "alicloud-ai-entry-modelstudio-test|aliyun-modelstudio-entry-test"
  "alicloud-ai-image-qwen-image|aliyun-modelstudio-qwen-image"
  "alicloud-ai-image-qwen-image-edit|aliyun-modelstudio-qwen-image-edit"
  "alicloud-ai-image-zimage-turbo|aliyun-modelstudio-zimage-turbo"
  "alicloud-ai-misc-crawl-and-skill|aliyun-modelstudio-crawl-and-skill"
  "alicloud-ai-multimodal-qvq|aliyun-modelstudio-qvq"
  "alicloud-ai-multimodal-qwen-ocr|aliyun-modelstudio-qwen-ocr"
  "alicloud-ai-multimodal-qwen-omni|aliyun-modelstudio-qwen-omni"
  "alicloud-ai-multimodal-qwen-vl|aliyun-modelstudio-qwen-vl"
  "alicloud-ai-research-qwen-deep-research|aliyun-modelstudio-qwen-deep-research"
  "alicloud-ai-search-multimodal-embedding|aliyun-modelstudio-multimodal-embedding"
  "alicloud-ai-search-rerank|aliyun-modelstudio-rerank"
  "alicloud-ai-search-text-embedding|aliyun-modelstudio-text-embedding"
  "alicloud-ai-text-qwen-generation|aliyun-modelstudio-qwen-generation"
  "alicloud-ai-video-aishi-generation|aliyun-modelstudio-aishi-generation"
  "alicloud-ai-video-animate-anyone|aliyun-modelstudio-animate-anyone"
  "alicloud-ai-video-digital-human|aliyun-modelstudio-digital-human"
  "alicloud-ai-video-emo|aliyun-modelstudio-emo"
  "alicloud-ai-video-emoji|aliyun-modelstudio-emoji"
  "alicloud-ai-video-liveportrait|aliyun-modelstudio-liveportrait"
  "alicloud-ai-video-retalk|aliyun-modelstudio-retalk"
  "alicloud-ai-video-wan-edit|aliyun-modelstudio-wan-edit"
  "alicloud-ai-video-wan-r2v|aliyun-modelstudio-wan-r2v"
  "alicloud-ai-video-wan-video|aliyun-modelstudio-wan-video"

  # Workspace dirs (data only)
  "alicloud-ai-audio-cosyvoice-voice-clone-workspace|aliyun-modelstudio-cosyvoice-voice-clone-workspace"
  "alicloud-ai-audio-cosyvoice-voice-design-workspace|aliyun-modelstudio-cosyvoice-voice-design-workspace"

  # Independent AI Products
  "alicloud-ai-chatbot|aliyun-chatbot-manage"
  "alicloud-ai-cloud-call-center|aliyun-ccc-manage"
  "alicloud-ai-contactcenter-ai|aliyun-ccai-manage"
  "alicloud-ai-content-aicontent|aliyun-aicontent-generate"
  "alicloud-ai-content-aimiaobi|aliyun-aimiaobi-generate"
  "alicloud-ai-pai-aiworkspace|aliyun-pai-workspace"
  "alicloud-ai-recommend-airec|aliyun-airec-manage"
  "alicloud-ai-search-dashvector|aliyun-dashvector-search"
  "alicloud-ai-search-milvus|aliyun-milvus-search"
  "alicloud-ai-search-opensearch|aliyun-opensearch-search"
  "alicloud-ai-text-document-mind|aliyun-docmind-extract"
  "alicloud-ai-translation-anytrans|aliyun-anytrans-translate"

  # Compute
  "alicloud-compute-ecs|aliyun-ecs-manage"
  "alicloud-compute-fc-agentrun|aliyun-fc-agentrun"
  "alicloud-compute-fc-serverless-devs|aliyun-fc-serverless-devs"
  "alicloud-compute-swas-open|aliyun-swas-manage"

  # Database
  "alicloud-database-analyticdb-mysql|aliyun-adb-mysql"
  "alicloud-database-rds-supabase|aliyun-rds-supabase"

  # Data
  "alicloud-data-analytics-dataanalysisgbi|aliyun-gbi-analytics"
  "alicloud-data-lake-dlf|aliyun-dlf-manage"
  "alicloud-data-lake-dlf-next|aliyun-dlf-manage-next"

  # Media
  "alicloud-media-ice|aliyun-ice-manage"
  "alicloud-media-live|aliyun-live-manage"
  "alicloud-media-mps|aliyun-mps-manage"
  "alicloud-media-video-translation|aliyun-mps-video-translation"
  "alicloud-media-vod|aliyun-vod-manage"

  # Network
  "alicloud-network-alb|aliyun-alb-manage"
  "alicloud-network-cdn|aliyun-cdn-manage"
  "alicloud-network-dns-cli|aliyun-dns-cli"
  "alicloud-network-esa|aliyun-esa-manage"

  # Observability
  "alicloud-observability-openclaw-sls-integration|aliyun-sls-openclaw-integration"
  "alicloud-observability-pts|aliyun-pts-manage"
  "alicloud-observability-sls-log-query|aliyun-sls-log-query"

  # Backup
  "alicloud-backup-bdrc|aliyun-bdrc-backup"
  "alicloud-backup-hbr|aliyun-hbr-backup"

  # Security
  "alicloud-security-center-sas|aliyun-sas-manage"
  "alicloud-security-cloudfw|aliyun-cloudfw-manage"
  "alicloud-security-content-moderation-green|aliyun-green-moderation"
  "alicloud-security-id-verification-cloudauth|aliyun-cloudauth-verify"
  "alicloud-security-kms|aliyun-kms-manage"

  # Storage
  "alicloud-storage-oss-ossutil|aliyun-oss-ossutil"

  # Platform
  "alicloud-platform-aliyun-cli|aliyun-cli-manage"
  "alicloud-platform-devops|aliyun-devops-manage"
  "alicloud-platform-docs-api-review|aliyun-platform-docs-review"
  "alicloud-platform-multicloud-docs-api-benchmark|aliyun-platform-docs-benchmark"
  "alicloud-platform-openapi-product-api-discovery|aliyun-openapi-discovery"
  "alicloud-platform-openclaw-setup|aliyun-openclaw-setup"

  # Other
  "alicloud-skill-creator|aliyun-skill-creator"
  "alicloud-solution-content-article-illustrator|aliyun-solution-article-illustrator"
)

# ============================================================
# Phase 1: Rename directories and create symlinks
# ============================================================
echo "=== Phase 1: Rename directories + create symlinks ==="
renamed=0
skipped=0

for entry in "${MAPPING[@]}"; do
  old="${entry%%|*}"
  new="${entry##*|}"

  # Find the actual directory (skip if already a symlink = already renamed)
  old_dir=$(find skills -maxdepth 5 -type d -name "$old" 2>/dev/null | head -1)

  if [[ -z "$old_dir" ]]; then
    # Check if it's already a symlink (previously renamed)
    old_link=$(find skills -maxdepth 5 -type l -name "$old" 2>/dev/null | head -1)
    if [[ -n "$old_link" ]]; then
      skipped=$((skipped + 1))
      continue
    fi
    echo "WARN: directory not found for $old"
    continue
  fi

  parent_dir=$(dirname "$old_dir")
  new_dir="$parent_dir/$new"

  if [[ -d "$new_dir" ]]; then
    echo "SKIP: $new_dir already exists"
    skipped=$((skipped + 1))
    continue
  fi

  # Rename
  mv "$old_dir" "$new_dir"
  # Create symlink for backward compatibility (relative)
  ln -s "$new" "$old_dir"
  echo "RENAMED: $old_dir -> $new_dir (symlink created)"
  renamed=$((renamed + 1))
done

echo "Phase 1 done: renamed=$renamed, skipped=$skipped"

# ============================================================
# Phase 2: Update file contents (SKILL.md, *.py, *.md)
# ============================================================
echo ""
echo "=== Phase 2: Update file contents ==="

# Build sed expression from mapping — process longer names first to avoid partial matches
# Sort by old name length descending
sorted_mapping=()
for entry in "${MAPPING[@]}"; do
  sorted_mapping+=("$entry")
done
IFS=$'\n' sorted_mapping=($(for e in "${sorted_mapping[@]}"; do echo "$e"; done | awk -F'|' '{print length($1), $0}' | sort -rn | cut -d' ' -f2-))
unset IFS

# Build a single sed script
sed_script=""
for entry in "${sorted_mapping[@]}"; do
  old="${entry%%|*}"
  new="${entry##*|}"
  sed_script+="s|${old}|${new}|g;"
done

# Apply to all SKILL.md files (follow symlinks to reach actual files)
echo "Updating SKILL.md files..."
find skills -name "SKILL.md" -not -type l | while read -r f; do
  sed -i "$sed_script" "$f"
done

# Apply to all Python scripts
echo "Updating Python scripts..."
find skills -name "*.py" -not -type l | while read -r f; do
  sed -i "$sed_script" "$f"
done

# Apply to all reference .md files inside skills/
echo "Updating reference docs..."
find skills -name "*.md" -not -name "SKILL.md" -not -type l | while read -r f; do
  sed -i "$sed_script" "$f"
done

# Apply to top-level READMEs
echo "Updating top-level READMEs..."
for f in README.md README.zh-CN.md README.zh-TW.md; do
  [[ -f "$f" ]] && sed -i "$sed_script" "$f"
done

# Apply to examples/
echo "Updating examples..."
find examples -name "*.md" -not -type l 2>/dev/null | while read -r f; do
  sed -i "$sed_script" "$f"
done

# Apply to AGENTS.md if it exists
[[ -f AGENTS.md ]] && sed -i "$sed_script" AGENTS.md

echo ""
echo "=== All done ==="
echo "Run verification:"
echo "  find skills -type l | wc -l                              # should be ~85"
echo "  find skills -name SKILL.md -exec grep -l 'name: alicloud-' {} \;  # should be empty"
echo "  grep -r 'alicloud-' README.md examples/ | wc -l         # should be 0"
