# Task 04: Merge and Deduplicate

## Description

Parse all iCal feeds, merge events, deduplicate, prefix labels, output single calendar.

## Acceptance Criteria

- [x] Parse each iCal string with icalendar; extract VEVENTs
- [x] Deduplicate by event_key (hash of DTSTART + SUMMARY); first occurrence wins
- [x] Prefix event SUMMARY with label when present (`_prefix_summary`)
- [x] Write merged calendar to `feed.ics` in RFC 5545 format
