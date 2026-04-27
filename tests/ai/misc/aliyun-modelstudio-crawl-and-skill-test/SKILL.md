---
name: alicloud-ai-misc-crawl-and-skill-test
description: Minimal validation for crawl-and-skill workflow readiness.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate only the minimal request path for this skill.
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- Target skill: skills/ai/misc/alicloud-ai-misc-crawl-and-skill

## Test Steps (Minimal)

1) Open the target skill SKILL.md and choose one minimal input example.
2) Send one minimal request or run the example script.
3) Record request summary, response summary, and success/failure reason.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/misc/alicloud-ai-misc-crawl-and-skill
- Conclusion: pass / fail
- Notes:
