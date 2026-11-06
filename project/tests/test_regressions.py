"""Stage 8 regression tests for the two prepared defects.

Each test reproduces one defect with small synthetic data and stays in the
suite after the repair, so the defect cannot come back unnoticed.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


BOOKING_TIME = datetime(2026, 10, 1, 9, 0)


def make_booking_setup():
    """Fresh store with patients P1, P2 and practitioners D1, D2 registered."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PatientService(data_store).register_patient('P2', 'Sam Example')
    PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General practice'
    )
    PractitionerService(data_store).register_practitioner(
        'D2', 'Morgan Example', 'General practice'
    )
    return data_store, AppointmentService(data_store)


def test_f8_01_conflict_checks_the_same_practitioner():
    """REG-F8-01 / FR-05, AC-04.1, AC-04.2: a second SCHEDULED booking for
    the SAME practitioner at the same time is rejected and nothing changes;
    a DIFFERENT practitioner at that time is allowed.
    """
    data_store, appointment_service = make_booking_setup()
    first = appointment_service.book_appointment('A1', 'P1', 'D1', BOOKING_TIME)

    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P2', 'D1', BOOKING_TIME)
    assert data_store.list_appointments() == [first]

    other = appointment_service.book_appointment('A3', 'P2', 'D2', BOOKING_TIME)
    assert data_store.list_appointments() == [first, other]


def test_f8_02_cancelled_appointment_can_still_be_found():
    """REG-F8-02 / FR-07, AC-05.2, FR-08, AC-05.3: after cancelling, the
    store and the service both return the same appointment, it is still
    listed, and a second cancel is rejected with ValueError without change.
    """
    data_store, appointment_service = make_booking_setup()
    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', BOOKING_TIME
    )
    appointment_service.cancel_appointment('A1')

    assert data_store.find_appointment('A1') is appointment
    assert appointment_service.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert appointment.status is AppointmentStatus.CANCELLED