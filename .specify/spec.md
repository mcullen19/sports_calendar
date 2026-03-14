# Specification: Family Sports Calendar Aggregator

## Overview

Build an application that aggregates sports game and event schedules from multiple team/league apps into a single iCal feed. The feed is consumed by a Skylight family calendar so all events appear in one place.

## Problem Statement

Kids play ice hockey and lacrosse. Each team uses a different app for schedules:
- **Hockey**: TeamSnap, sportsYou, Gamesheets (league-managed)
- **Lacrosse**: Blast

Checking each app separately is time-consuming and error-prone. A single consolidated view is needed.

## Requirements

### Functional

1. **Ingest multiple calendar sources**
   - iCal subscription URLs from TeamSnap, sportsYou, and Blast
   - Schedule data from Gamesheets API (hockey league source of truth)

2. **Merge and deduplicate events**
   - Combine all events into one calendar
   - Deduplicate when the same game appears in multiple sources (e.g., Gamesheets + TeamSnap)
   - Prefer canonical source (Gamesheets for league games) when duplicates exist

3. **Output a single iCal feed**
   - Valid RFC 5545 format
   - Usable by Skylight's "Subscribe to calendar" feature
   - Human-readable event titles (e.g., "Kid 1 – Hockey vs Eagles" or "Kid 2 – Lacrosse practice")

4. **Run on a schedule**
   - Refresh the aggregated feed periodically (e.g., every 6 hours)
   - No manual trigger required for normal operation

5. **Publish the feed**
   - Stable public URL (e.g., `https://<user>.github.io/sports-calendar/feed.ics`)
   - Skylight subscribes to this URL once; updates propagate automatically

### Non-Functional

- **No always-on server**: Use GitHub Actions + GitHub Pages
- **No paid services**: Free tier only
- **Configurable**: Add/remove sources or change credentials without modifying code
- **Privacy**: No storage of personal data beyond what is in the source calendars

## User Journey

1. User configures iCal URLs and Gamesheets API credentials (via repo secrets or config)
2. GitHub Action runs on schedule, fetches all sources, merges, deduplicates, outputs `feed.ics`
3. Action publishes `feed.ics` to GitHub Pages
4. User adds the feed URL to Skylight as a subscribed calendar
5. Skylight displays the consolidated schedule; updates appear when the action next runs

## Success Criteria

- One URL to subscribe to in Skylight
- All hockey and lacrosse events visible in a single calendar view
- Duplicates eliminated or minimized
- Feed updates automatically without user intervention
