## Student Name: Urmay Suthar
## Student ID: 218491555

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from src.solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

"""TODO: Add at least 5 additional test cases to test your implementation."""

# --- TODO: Add at least 5 additional test cases to test your implementation. ---

def test_meeting_must_end_by_1700():
    """
    Constraint:
    A meeting cannot be suggested if it would end after 17:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "16:00" in slots      # 16:00–17:00 is allowed
    assert "16:15" not in slots  # 16:15–17:15 would end after 17:00


def test_back_to_back_after_event_is_allowed():
    """
    Functional requirement:
    Starting exactly when an event ends should be allowed.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:00" in slots      # 11:00–11:30 starts exactly at event end


def test_meeting_ending_at_event_start_is_not_allowed():
    """
    Constraint (based on public tests behavior):
    If a meeting would end exactly when an event starts, it should NOT be suggested.
    """
    events = [{"start": "09:30", "end": "10:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots  # 09:00–09:30 ends exactly at 09:30 (event start)
    assert "10:00" in slots      # 10:00–10:30 starts exactly at event end


def test_overlapping_events_are_merged_and_block_time():
    """
    Constraint:
    Overlapping events should behave like one continuous block.
    """
    events = [
        {"start": "10:00", "end": "11:30"},
        {"start": "11:00", "end": "12:00"},  # overlaps with the first
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "11:15" not in slots
    assert "12:00" not in slots  # lunch start is blocked anyway
    assert "13:00" in slots      # after lunch should be available


def test_event_partially_overlaps_working_hours_blocks_inside_portion():
    """
    Constraint:
    An event that partially overlaps working hours should still block the overlapping portion.
    """
    events = [{"start": "08:30", "end": "09:30"}]  # overlaps work start (09:00–09:30)
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots  # 09:00–09:30 overlaps the event portion inside work hours
    assert "09:30" in slots      # starts when the event ends


def test_invalid_meeting_duration_returns_empty():
    """
    Constraint:
    Non-positive meeting durations should return no slots.
    """
    events = [{"start": "10:00", "end": "11:00"}]

    assert suggest_slots(events, meeting_duration=0, day="2026-02-01") == []
    assert suggest_slots(events, meeting_duration=-15, day="2026-02-01") == []

