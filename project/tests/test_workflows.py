"""Stage 9 tests for service listing, a full workflow and the console menu.

Every test builds a fresh store and services, so tests do not affect each
other. Only made-up data is used.
"""

from datetime import datetime

import pytest

from smartcare.console import run_menu
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


NINE = datetime(2026, 10, 1, 9, 0)


def make_services():
    """Fresh store with P1, D1 and D2 registered; returns all the services."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General practice')
    practitioners.register_practitioner('D2', 'Morgan Example', 'General practice')
    return data_store, patients, practitioners, appointments


# ---- Service listing, QRY-04 (TEST-S9-07 to TEST-S9-09)


def test_known_practitioner_with_no_matches_gives_an_empty_list():
    """TEST-S9-07 / QRY-04: a known practitioner with no appointments, or no
    appointments of the requested status, gives [] and no error.
    """
    data_store, _, _, appointments = make_services()
    appointments.book_appointment('A1', 'P1', 'D1', NINE)

    assert appointments.list_practitioner_appointments('D2') == []
    assert appointments.list_practitioner_appointments(
        'D1', AppointmentStatus.CANCELLED
    ) == []


def test_unknown_blank_and_invalid_status_are_errors_not_empty():
    """TEST-S9-08 / QRY-04: unknown ID is LookupError; blank ID is
    ValueError; a text status such as 'scheduled' is ValueError (not
    "no matches"). Stored appointments are unchanged after each.
    """
    data_store, _, _, appointments = make_services()
    booked = appointments.book_appointment('A1', 'P1', 'D1', NINE)

    with pytest.raises(LookupError):
        appointments.list_practitioner_appointments('D9')
    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments('   ')
    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments('D1', 'scheduled')

    assert data_store.list_appointments() == [booked]


def test_listing_keeps_history_and_uses_the_registered_id():
    """TEST-S9-09 / QRY-04, FR-07: omitted status includes the cancelled
    appointment (same object); SCHEDULED-only leaves it out without removing
    it; ' D1 ' with spaces still finds D1's appointments.
    """
    data_store, _, _, appointments = make_services()
    a1 = appointments.book_appointment('A1', 'P1', 'D1', NINE)
    appointments.cancel_appointment('A1')

    all_statuses = appointments.list_practitioner_appointments(' D1 ')

    assert all_statuses == [a1] and all_statuses[0] is a1
    assert appointments.list_practitioner_appointments(
        'D1', AppointmentStatus.SCHEDULED
    ) == []
    assert appointments.find_appointment('A1') is a1
    assert data_store.list_appointments() == [a1]

# ---- Integrated workflow (TEST-S9-10)


def test_full_booking_workflow_through_the_services():
    """TEST-S9-10 / UI-01 sequence via services: conflict rejected with no
    change, other practitioner allowed, cancel keeps history, filter works,
    freed slot can be rebooked, and a failed booking does not use its ID.
    """
    data_store, patients, _, appointments = make_services()
    a1 = appointments.book_appointment('A1', 'P1', 'D1', NINE)

    with pytest.raises(ValueError):
        appointments.book_appointment('A9', 'P1', 'D1', NINE)
    assert data_store.list_appointments() == [a1]
    with pytest.raises(LookupError):
        appointments.book_appointment('A9', 'P9', 'D1', NINE)
    assert data_store.list_appointments() == [a1]

    a2 = appointments.book_appointment('A2', 'P1', 'D2', NINE)
    appointments.cancel_appointment('A1')
    assert appointments.find_appointment('A1').status is AppointmentStatus.CANCELLED
    assert appointments.list_practitioner_appointments('D1') == [a1]

    a3 = appointments.book_appointment('A3', 'P1', 'D1', NINE)
    assert appointments.list_practitioner_appointments('D1') == [a1, a3]
    assert appointments.list_practitioner_appointments(
        'D1', AppointmentStatus.SCHEDULED
    ) == [a3]
    a9 = appointments.book_appointment('A9', 'P1', 'D1', datetime(2026, 10, 1, 11, 0))
    assert data_store.list_appointments() == [a1, a2, a3, a9]