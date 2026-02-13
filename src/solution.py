## Student Name: Urmay Suthar
## Student ID: 218491555

from typing import List, Dict
from datetime import date

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    WORK_START = 9 * 60   # 09:00
    WORK_END = 17 * 60    # 17:00
    STEP_MINUTES = 15

    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60

    # New requirement: Fridays must not start at or after 15:00
    FRIDAY_CUTOFF = 15 * 60  # 15:00

    if not isinstance(meeting_duration, int) or meeting_duration <= 0:
        return []
    if meeting_duration > (WORK_END - WORK_START):
        return []

    def is_friday(day_str: str) -> bool:
        # Accept ISO date strings like "2026-02-01"
        try:
            return date.fromisoformat(day_str).weekday() == 4  # Mon=0 ... Fri=4
        except Exception:
            pass
        # Accept abbreviations if ever used
        return day_str.strip().lower() in {"fri", "friday"}

    friday_rule = is_friday(day)

    def to_minutes(t: str) -> int:
        hh, mm = t.split(":")
        return int(hh) * 60 + int(mm)

    def to_hhmm(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    # Parse + clamp events into working window
    intervals = []
    for e in events:
        if "start" not in e or "end" not in e:
            continue
        try:
            s = to_minutes(e["start"])
            en = to_minutes(e["end"])
        except Exception:
            continue

        if en <= s:
            continue
        if en <= WORK_START or s >= WORK_END:
            continue

        s = max(s, WORK_START)
        en = min(en, WORK_END)
        if en > s:
            intervals.append((s, en))

    # Sort + merge
    intervals.sort()
    merged = []
    for s, en in intervals:
        if not merged:
            merged.append([s, en])
        else:
            if s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], en)
            else:
                merged.append([s, en])

    def overlaps_with_event(meet_start: int, meet_end: int, ev_start: int, ev_end: int) -> bool:
        # meet_end == ev_start counts as conflict
        # meet_start == ev_end is allowed
        return (meet_start < ev_end) and (meet_end >= ev_start)

    results: List[str] = []
    latest_start = WORK_END - meeting_duration

    t = WORK_START
    rem = t % STEP_MINUTES
    if rem != 0:
        t += (STEP_MINUTES - rem)

    while t <= latest_start:
        # Friday rule: meetings must NOT start at 15:00 or later
        if friday_rule and t >= FRIDAY_CUTOFF:
            break  # times only increase, so we can stop early

        # lunch constraint blocks START times only
        if LUNCH_START <= t < LUNCH_END:
            t += STEP_MINUTES
            continue

        meet_end = t + meeting_duration

        conflict = False
        for ev_s, ev_e in merged:
            if overlaps_with_event(t, meet_end, ev_s, ev_e):
                conflict = True
                break

        if not conflict:
            results.append(to_hhmm(t))

        t += STEP_MINUTES

    return results
