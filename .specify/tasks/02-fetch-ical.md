# Task 02: Fetch iCal Feeds

## Description

Implement fetching of iCal content from configurable URLs.

## Acceptance Criteria

- [ ] Load config (YAML or env vars) with iCal URLs
- [ ] HTTP GET each URL with timeout and error handling
- [ ] Return raw iCal content (string/bytes) per source
- [ ] Skip sources that fail; log errors
