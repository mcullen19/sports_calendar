# Task 02: Fetch iCal Feeds

## Description

Implement fetching of iCal content from configurable URLs.

## Acceptance Criteria

- [x] Load config from config.yaml (PyYAML)
- [x] `fetch_labeled_icals(sources)` accepts list of `{url, label}`; returns `[(content, label), ...]`
- [x] HTTP GET each URL with timeout (30s) and error handling
- [x] Skip sources that fail; log warnings
