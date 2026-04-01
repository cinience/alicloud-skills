# Multi-Cloud Docs/API Benchmark Rubric

## Providers

- Alibaba Cloud
- AWS
- Azure
- GCP
- Tencent Cloud
- Volcano Engine
- Huawei Cloud

## Dimensions (100 points)

- Discoverability (15): official docs/API pages easy to find
- Information Architecture (20): overview, quick start, developer reference coverage
- API Clarity (20): request/response/examples/error guidance
- Operational Guidance (15): troubleshooting, FAQ, best practices
- Freshness Signals (10): release notes/changelog/update signals
- Consistency (20): naming, structure, and navigation consistency

Scoring weights are configurable in `references/scoring.json`.

## Priority Tags

- P0: blocks integration or causes high failure risk
- P1: significantly reduces developer efficiency
- P2: quality and consistency optimization

## Source Confidence Levels

- L0: user-pinned authoritative links (highest confidence)
- L1: machine-readable official metadata/repository
- L2: official-domain search discovery
- L3: discovery insufficient or empty
