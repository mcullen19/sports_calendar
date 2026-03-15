# Task 05: GitHub Actions Workflow

## Description

Create workflow to run aggregation on schedule and publish to GitHub Pages.

## Acceptance Criteria

- [x] Triggers: `schedule` (cron `0 */6 * * *`) + `workflow_dispatch`
- [x] Config built from CALENDAR_CONFIG (full YAML) or TEAMSNAP/SPORTSYOU/BLAST_ICAL_URL secrets
- [x] Steps: checkout → setup Python v6 → create config → install deps → run script → copy to output/ → peaceiris/actions-gh-pages
- [x] `permissions: contents: write` for gh-pages deploy; `gh-pages` branch created on first run
- [x] README: first-time setup order (secrets → run workflow → enable Pages), add/remove feeds
