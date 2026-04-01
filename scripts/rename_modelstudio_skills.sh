#!/usr/bin/env bash
# Rename aliyun-modelstudio-* skills to aliyun-{model}-{function}
# Creates symlinks at old locations for backward compatibility.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# === Mapping: old_name new_name ===
# Sorted by length descending to avoid partial matches in sed
declare -a MAPPING=(
  # Qwen ASR/TTS (add qwen- prefix)
  "aliyun-modelstudio-asr-realtime|aliyun-qwen-asr-realtime"
  "aliyun-modelstudio-asr|aliyun-qwen-asr"
  "aliyun-modelstudio-tts-voice-clone|aliyun-qwen-tts-voice-clone"
  "aliyun-modelstudio-tts-voice-design|aliyun-qwen-tts-voice-design"
  "aliyun-modelstudio-tts-realtime|aliyun-qwen-tts-realtime"
  "aliyun-modelstudio-tts|aliyun-qwen-tts"
  "aliyun-modelstudio-livetranslate|aliyun-qwen-livetranslate"
  "aliyun-modelstudio-multimodal-embedding|aliyun-qwen-multimodal-embedding"
  "aliyun-modelstudio-text-embedding|aliyun-qwen-text-embedding"
  "aliyun-modelstudio-rerank|aliyun-qwen-rerank"

  # CosyVoice (already has model name)
  "aliyun-modelstudio-cosyvoice-voice-clone-workspace|aliyun-cosyvoice-voice-clone-workspace"
  "aliyun-modelstudio-cosyvoice-voice-clone|aliyun-cosyvoice-voice-clone"
  "aliyun-modelstudio-cosyvoice-voice-design-workspace|aliyun-cosyvoice-voice-design-workspace"
  "aliyun-modelstudio-cosyvoice-voice-design|aliyun-cosyvoice-voice-design"

  # Qwen models (already have qwen- in name, just drop modelstudio)
  "aliyun-modelstudio-qwen-deep-research|aliyun-qwen-deep-research"
  "aliyun-modelstudio-qwen-generation|aliyun-qwen-generation"
  "aliyun-modelstudio-qwen-image-edit|aliyun-qwen-image-edit"
  "aliyun-modelstudio-qwen-image|aliyun-qwen-image"
  "aliyun-modelstudio-qwen-coder|aliyun-qwen-coder"
  "aliyun-modelstudio-qwen-ocr|aliyun-qwen-ocr"
  "aliyun-modelstudio-qwen-omni|aliyun-qwen-omni"
  "aliyun-modelstudio-qwen-vl|aliyun-qwen-vl"
  "aliyun-modelstudio-qvq|aliyun-qvq"

  # Wan video models
  "aliyun-modelstudio-wan-edit|aliyun-wan-edit"
  "aliyun-modelstudio-wan-r2v|aliyun-wan-r2v"
  "aliyun-modelstudio-wan-video|aliyun-wan-video"
  "aliyun-modelstudio-digital-human|aliyun-wan-digital-human"

  # Other specific models
  "aliyun-modelstudio-aishi-generation|aliyun-pixverse-generation"
  "aliyun-modelstudio-animate-anyone|aliyun-animate-anyone"
  "aliyun-modelstudio-emo|aliyun-emo"
  "aliyun-modelstudio-emoji|aliyun-emoji"
  "aliyun-modelstudio-liveportrait|aliyun-liveportrait"
  "aliyun-modelstudio-retalk|aliyun-videoretalk"
  "aliyun-modelstudio-zimage-turbo|aliyun-zimage-turbo"

  # Platform tools (keep modelstudio prefix — not model-specific)
  # aliyun-modelstudio-entry — KEEP
  # aliyun-modelstudio-entry-test — KEEP
  # aliyun-modelstudio-crawl-and-skill — KEEP
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

  # Find the actual directory
  old_dir=$(find skills -maxdepth 5 -type d -name "$old" 2>/dev/null | head -1)

  if [[ -z "$old_dir" ]]; then
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

  mv "$old_dir" "$new_dir"
  ln -s "$new" "$old_dir"
  echo "RENAMED: $old -> $new"
  renamed=$((renamed + 1))
done

echo "Phase 1 done: renamed=$renamed, skipped=$skipped"

# ============================================================
# Phase 2: Update old alicloud->aliyun-modelstudio symlinks
# ============================================================
echo ""
echo "=== Phase 1b: Update old alicloud-* symlinks ==="
# The old alicloud-* symlinks point to aliyun-modelstudio-*, need to update targets
for entry in "${MAPPING[@]}"; do
  old_ms="${entry%%|*}"
  new="${entry##*|}"

  # Find alicloud-* symlinks that point to the old modelstudio name
  find skills -maxdepth 5 -type l 2>/dev/null | while read -r link; do
    target=$(readlink "$link")
    if [[ "$target" == "$old_ms" ]]; then
      rm "$link"
      # Point to new name, also create a symlink from old_ms if it exists
      ln -s "$new" "$link"
      echo "RELINKED: $link -> $new"
    fi
  done
done

# ============================================================
# Phase 3: Update file contents
# ============================================================
echo ""
echo "=== Phase 2: Update file contents ==="

# Sort by old name length descending for sed
sorted_mapping=()
for entry in "${MAPPING[@]}"; do
  sorted_mapping+=("$entry")
done
IFS=$'\n' sorted_mapping=($(for e in "${sorted_mapping[@]}"; do echo "$e"; done | awk -F'|' '{print length($1), $0}' | sort -rn | cut -d' ' -f2-))
unset IFS

sed_script=""
for entry in "${sorted_mapping[@]}"; do
  old="${entry%%|*}"
  new="${entry##*|}"
  sed_script+="s|${old}|${new}|g;"
done

echo "Updating SKILL.md files..."
find skills -name "SKILL.md" -not -type l | while read -r f; do
  sed -i "$sed_script" "$f"
done

echo "Updating Python scripts..."
find skills -name "*.py" -not -type l | while read -r f; do
  sed -i "$sed_script" "$f"
done

echo "Updating reference docs..."
find skills -name "*.md" -not -name "SKILL.md" -not -type l | while read -r f; do
  sed -i "$sed_script" "$f"
done

echo "Updating top-level docs..."
for f in README.md README.zh-CN.md README.zh-TW.md AGENTS.md; do
  [[ -f "$f" ]] && sed -i "$sed_script" "$f"
done

echo "Updating examples..."
find examples -name "*.md" -not -type l 2>/dev/null | while read -r f; do
  sed -i "$sed_script" "$f"
done

echo ""
echo "=== All done ==="
