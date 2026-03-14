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
- **Libraries**: `icalendar`, `requests`
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages (static file serving)

## Implementation Approach

### 1. Config

- `config.yaml` or `.env.example` for source URLs (user fills in secrets)
- GitHub Secrets for: `TEAMSNAP_ICAL_URL`, `SPORTSYOU_ICAL_URL`, `BLAST_ICAL_URL`, `GAMESHEETS_API_KEY` (or similar)
- Config should allow optional sources (if one isn't configured, skip it)

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

- Compare events by: `DTSTART` + similar `SUMMARY` (or location)
- When duplicates found: prefer Gamesheets for hockey league games; otherwise keep first encountered
- Threshold for "similar" (e.g., Levenshtein or substring match) to avoid false merges

### 5. Output

- Serialize merged calendar to `feed.ics`
- Validate output is well-formed RFC 5545

### 6. GitHub Actions Workflow

- Trigger: `schedule` (cron, e.g. `0 */6 * * *` for every 6 hours) + `workflow_dispatch` (manual)
- Steps: checkout → setup Python → install deps → run script → commit/push `feed.ics` to `gh-pages` (or `output/` deployed via Pages)

### 7. GitHub Pages

- Publish from `gh-pages` branch or `docs/` folder
- Ensure `feed.ics` is served with `Content-Type: text/calendar`
- Resulting URL: `https://<username>.github.io/sports-calendar/feed.ics`

## File Layout

```
sports_calendar/
├── .specify/
│   ├── constitution.md
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── src/
│   ├── fetch.py      # Fetch iCal URLs and Gamesheets API
│   ├── merge.py      # Parse, merge, deduplicate
│   └── main.py       # Orchestrate and write feed.ics
├── config.example.yaml
├── requirements.txt
├── .github/
│   └── workflows/
│       └── build-feed.yml
└── README.md
```

## Risks & Mitigations

- **Gamesheets API structure unknown**: Stub with placeholder; implement when docs/credentials available
- **iCal URLs may require auth**: Some team apps use time-limited or tokenized URLs; document how to refresh
- **Skylight refresh rate**: May cache feed; 6-hour schedule is a reasonable default
