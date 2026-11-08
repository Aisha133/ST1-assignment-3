"""Stage 9 tests for the pure query helpers in smartcare/queries.py.

These build Appointment objects directly (no store or services), because
the query only works on the list it is given. Only made-up data is used.
"""

from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments


NINE = datetime(2026, 10, 1, 9, 0)
TEN = datetime(2026, 10, 1, 10, 0)


def make_appointments():
    """Return an unsorted list with two practitioners and every status.

    D1 has A3 (09:00, CANCELLED), A2 (09:00, COMPLETED) and A1 (10:00,
    SCHEDULED); D2 has A4 (09:00, SCHEDULED). A2 and A3 share 09:00, which
    is allowed because neither is SCHEDULED, so the ID tie-break is tested.
    """
    patient = Patient('P1', 'Alex Example')
    d1 = Practitioner('D1', 'Taylor Example', 'General practice')
    d2 = Practitioner('D2', 'Morgan Example', 'General practice')
    a1 = Appointment('A1', patient, d1, TEN)
    a2 = Appointment('A2', patient, d1, NINE, status=AppointmentStatus.COMPLETED)
    a3 = Appointment('A3', patient, d1, NINE)
    a3.cancel()
    a4 = Appointment('A4', patient, d2, NINE)
    return [a1, a3, a4, a2], a1, a2, a3, a4


def snapshot(appointments):
    """Record each appointment's fields so we can check nothing changed."""
    return [
        (a.appointment_id, a.practitioner.practitioner_id, a.date_time, a.status)
        for a in appointments
    ]


def test_sort_key_is_date_time_then_id():
    """TEST-S9-01 / FP-03: the named key returns (date_time, appointment_id)
    and does not change the appointment.
    """
    appointments, a1, _, _, _ = make_appointments()

    assert appointment_sort_key(a1) == (TEN, 'A1')
    assert a1.status is AppointmentStatus.SCHEDULED


def test_only_the_requested_practitioner_is_selected():
    """TEST-S9-02 / QRY-01: D1's appointments only; D2's A4 is the control."""
    appointments, a1, a2, a3, a4 = make_appointments()

    result = select_appointments(appointments, 'D1')

    assert a4 not in result
    assert select_appointments(appointments, 'D2') == [a4]


def test_default_is_all_statuses_and_each_status_filters():
    """TEST-S9-03 / QRY-02: no status means every status (history kept);
    each enum status gives only that status; no match gives [].
    """
    appointments, a1, a2, a3, a4 = make_appointments()

    assert select_appointments(appointments, 'D1') == [a2, a3, a1]
    assert select_appointments(
        appointments, 'D1', AppointmentStatus.SCHEDULED
    ) == [a1]
    assert select_appointments(
        appointments, 'D1', AppointmentStatus.CANCELLED
    ) == [a3]
    assert select_appointments(
        appointments, 'D1', AppointmentStatus.COMPLETED
    ) == [a2]
    assert select_appointments(
        appointments, 'D2', AppointmentStatus.CANCELLED
    ) == []


def test_sorted_by_time_then_id_without_changing_the_source():
    """TEST-S9-04 / QRY-03, FP-03: 09:00 before 10:00; equal 09:00 times
    ordered by ID (A2 before A3); source order and fields unchanged.
    """
    appointments, a1, a2, a3, a4 = make_appointments()
    order_before = list(appointments)
    fields_before = snapshot(appointments)

    result = select_appointments(appointments, 'D1')

    assert result == [a2, a3, a1]
    assert result == sorted(result, key=appointment_sort_key)
    assert appointments == order_before
    assert snapshot(appointments) == fields_before


def test_repeated_calls_give_the_same_result():
    """TEST-S9-05 / FP-01: unchanged inputs give the same answer every time
    and the source is still unchanged after both calls.
    """
    appointments, a1, a2, a3, a4 = make_appointments()
    order_before = list(appointments)

    first = select_appointments(appointments, 'D1')
    second = select_appointments(appointments, 'D1')

    assert first == second == [a2, a3, a1]
    assert appointments == order_before


def test_always_returns_a_new_list():
    """TEST-S9-06 / FP-02: a distinct list for empty, already-sorted and
    unsorted input; the same Appointment objects are reused, unchanged.
    """
    appointments, a1, a2, a3, a4 = make_appointments()
    empty = []
    already_sorted = [a2, a3, a1]

    empty_result = select_appointments(empty, 'D1')
    sorted_result = select_appointments(already_sorted, 'D1')
    unsorted_result = select_appointments(appointments, 'D1')

    assert empty_result == [] and empty_result is not empty
    assert sorted_result == already_sorted
    assert sorted_result is not already_sorted
    assert unsorted_result is not appointments
    assert unsorted_result[0] is a2
    assert a2.status is AppointmentStatus.COMPLETED