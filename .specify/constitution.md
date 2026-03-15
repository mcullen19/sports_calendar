# Project Constitution

## Core Principles

This project consolidates family sports calendars (hockey, lacrosse) from multiple sources into a single iCal feed for display on Skylight.

## Technical Standards

- **Language**: Python
- **Output**: Valid RFC 5545 iCal (`.ics`) format
- **Hosting**: GitHub Actions for scheduling; GitHub Pages for serving the feed
- **No cloud server**: Zero-cost, serverless approach
- **Config-driven**: `ical_sources` (url + optional label) in config.yaml or CALENDAR_CONFIG secret

## Development Approach

- Specifications define the *what* and *why* before implementation
- Use existing libraries (e.g., `icalendar`, `requests`) where appropriate
- Prefer simple, maintainable code over clever solutions
- Assume sources may change; design for easy addition/removal of calendar feeds
- Per-source labels so events identify kid/team when consolidated
