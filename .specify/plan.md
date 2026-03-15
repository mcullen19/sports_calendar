# Technical Plan: Family Sports Calendar Aggregator

## Architecture

```
[TeamSnap iCal] ─┐
[sportsYou iCal] ─┼──> [Python Script] ──> feed.ics ──> [GitHub Pages]
[Blast iCal]    ─┤         │
[Gamesheets API]─┘         └── runs via GitHub Actions (scheduled)
```

## Tech Stack

- **Python 3.11+**
- **Libraries**: `icalendar`, `requests`, `PyYAML`
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages (static file serving)

## Implementation Approach

### 1. Config

- `config.example.yaml` template; user copies to `config.yaml` (gitignored)
- `ical_sources`: list of `{url, label}` objects; label is optional, prefixed to event titles
- GitHub Secrets: `CALENDAR_CONFIG` (full YAML, recommended) or `TEAMSNAP_ICAL_URL`, `SPORTSYOU_ICAL_URL`, `BLAST_ICAL_URL`
- Gamesheets section stubbed in config; not yet implemented

### 2. Fetch Module

- Fetch iCal content from each configured URL via HTTP GET
- Fetch Gamesheets schedule data via their API (structure TBD from their docs)
- Handle timeouts and HTTP errors gracefully; log and continue with other sources

### 3. Parse & Merge

- Parse each iCal feed with `icalendar`
- Convert Gamesheets API response to `icalendar` events
- Merge all events into one `Calendar` object
- Normalize event properties (title format, timezone handling)

### 4. Deduplication

- Key: hash of `DTSTART` + `SUMMARY` (event_key)
- First occurrence wins; identical events from multiple sources are dropped
- Labels applied after dedup so same event from different sources is merged before labeling

### 5. Output

- Serialize merged calendar to `feed.ics`
- Validate output is well-formed RFC 5545

### 6. GitHub Actions Workflow

- Trigger: `schedule` (cron `0 */6 * * *`) + `workflow_dispatch` (manual)
- Config built from secrets in "Create config" step; written to config.yaml before script runs
- Steps: checkout → setup Python → create config → install deps → run script → copy feed.ics to output/ → peaceiris/actions-gh-pages to gh-pages
- `permissions: contents: write` required for Pages deploy

### 7. GitHub Pages

- Publish from `gh-pages` branch or `docs/` folder
- Ensure `feed.ics` is served with `Content-Type: text/calendar`
- Resulting URL: `https://<username>.github.io/sports-calendar/feed.ics`

## File Layout (as implemented)

```
sports_calendar/
├── .gitignore           # config.yaml, feed.ics, .venv, etc.
├── .specify/
│   ├── constitution.md
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── .github/workflows/
│   └── build-feed.yml
├── config.example.yaml
├── requirements.txt     # icalendar, requests, PyYAML
├── README.md
└── src/
    ├── __init__.py
    ├── main.py          # Load config, orchestrate fetch → merge → write feed.ics
    ├── fetch.py         # fetch_ical, fetch_labeled_icals (Gamesheets stubbed)
    └── merge.py         # parse_ical, merge_icals, event_key dedup, label prefix
```

## Risks & Mitigations

- **Gamesheets API structure unknown**: Stub with placeholder; implement when docs/credentials available
- **iCal URLs may require auth**: Some team apps use time-limited or tokenized URLs; document how to refresh
- **Skylight refresh rate**: May cache feed; 6-hour schedule is a reasonable default
