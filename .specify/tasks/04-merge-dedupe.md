# Task 04: Merge and Deduplicate

## Description

Parse all iCal feeds, merge events, deduplicate, output single calendar.

## Acceptance Criteria

- [ ] Parse each iCal string with icalendar library
- [ ] Combine all VEVENT components into one Calendar
- [ ] Deduplicate by DTSTART + similar SUMMARY
- [ ] Write merged calendar to `feed.ics` in RFC 5545 format
