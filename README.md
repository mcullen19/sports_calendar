# Family Sports Calendar

Aggregates sports game and event schedules from TeamSnap, sportsYou, Blast, and Gamesheets into a single iCal feed for Skylight (or any iCal-capable calendar).

## Setup

1. **Create virtual environment** (if not already done):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure sources**:
   ```bash
   cp config.example.yaml config.yaml
   # Edit config.yaml with your iCal URLs
   ```

   Each source needs a `url` and optional `label`. Labels are prefixed to event titles (e.g. "Kid 1 - Hockey: Game vs Eagles").

   Get iCal URLs from:
   - **TeamSnap**: Schedule → Sync Calendar / Export → Subscribe
   - **sportsYou**: Calendar → Export / Subscribe
   - **Blast**: Calendar settings → iCal export

## Run locally

```bash
python -m src.main
```

Output: `feed.ics` in the project root.

## GitHub Actions + Pages

1. **Enable GitHub Pages**: Repo → Settings → Pages → Source: Deploy from branch → Branch: `gh-pages` → Save.

2. **Add repository secrets** (Settings → Secrets and variables → Actions):

   **Option A** (recommended): Add `CALENDAR_CONFIG` with your full config YAML (the contents of your `config.yaml`). This supports labels and any number of sources.

   **Option B**: Add individual URL secrets for a simple setup (no labels):
   - `TEAMSNAP_ICAL_URL`
   - `SPORTSYOU_ICAL_URL`
   - `BLAST_ICAL_URL`

3. **Subscribe in Skylight**: Add this URL as a calendar subscription:
   ```
   https://<your-username>.github.io/sports-calendar/feed.ics
   ```

   The workflow runs every 6 hours; you can also trigger it manually (Actions → Build Calendar Feed → Run workflow).
