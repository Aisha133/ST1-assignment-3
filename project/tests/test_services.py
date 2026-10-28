"""Stage 6 tests for the service classes.

Tests for patient lookup (FR-02), practitioner lookup (FR-03 supporting)
and appointment cancellation (FR-06 and FR-07).

Every test makes its own new data store so the tests do not affect each
other. Only made-up data is used.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


# The date and time used for bookings in these tests.
BOOKING_TIME = datetime(2026, 10, 1, 9, 0)


def make_services():
    """Make an empty data store and the three services that share it."""
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)
    return data_store, patient_service, practitioner_service, appointment_service


def book_one_appointment():
    """Register patient P1 and practitioner D1, then book appointment A1.

    Returns the store, the appointment service and the booked appointment
    so cancellation tests can start from a SCHEDULED appointment.
    """
    data_store, patient_service, practitioner_service, appointment_service = (
        make_services()
    )
    patient_service.register_patient('P1', 'Alex Example')
    practitioner_service.register_practitioner(
        'D1', 'Taylor Example', 'General practice'
    )
    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', BOOKING_TIME
    )
    return data_store, appointment_service, appointment

# ---- FR-02 patient lookup (issue #2)


def test_find_patient_returns_the_stored_patient():
    """TEST-S6-01 / AC-02.1: a registered ID gives back that same patient."""
    # Arrange
    data_store, patient_service, _, _ = make_services()
    patient = patient_service.register_patient('P1', 'Alex Example')

    # Act
    found = patient_service.find_patient('P1')

    # Assert: the same object, not just one with the same name
    assert found is patient
    assert found.name == 'Alex Example'


def test_find_patient_unknown_id_raises_lookup_error():
    """TEST-S6-02 / AC-02.2: an ID that was never registered is not found."""
    data_store, patient_service, _, _ = make_services()
    patient = patient_service.register_patient('P1', 'Alex Example')

    with pytest.raises(LookupError):
        patient_service.find_patient('P2')

    # Nothing in the store should have changed
    assert data_store.list_patients() == [patient]


def test_find_patient_empty_id_raises_value_error():
    """TEST-S6-03a / ID rules: an empty ID is invalid input, not 'not found'."""
    _, patient_service, _, _ = make_services()
    patient_service.register_patient('P1', 'Alex Example')

    with pytest.raises(ValueError):
        patient_service.find_patient('')


def test_find_patient_spaces_only_id_raises_value_error():
    """TEST-S6-03b / ID rules: an ID that is only spaces is invalid."""
    _, patient_service, _, _ = make_services()
    patient_service.register_patient('P1', 'Alex Example')

    with pytest.raises(ValueError):
        patient_service.find_patient('   ')


def test_find_patient_non_text_id_raises_value_error():
    """TEST-S6-03c / ID rules: an ID that is not a string is invalid."""
    _, patient_service, _, _ = make_services()

    with pytest.raises(ValueError):
        patient_service.find_patient(None)


def test_find_patient_ignores_spaces_around_the_id():
    """TEST-S6-04 / ID rules: IDs are trimmed, so ' P1 ' finds P1."""
    _, patient_service, _, _ = make_services()
    patient = patient_service.register_patient('P1', 'Alex Example')

    assert patient_service.find_patient('  P1  ') is patient


def test_find_patient_is_case_sensitive():
    """TEST-S6-05 / ID rules: 'p1' is a different ID from 'P1'."""
    _, patient_service, _, _ = make_services()
    patient_service.register_patient('P1', 'Alex Example')

    with pytest.raises(LookupError):
        patient_service.find_patient('p1')

# ---- FR-03 supporting practitioner lookup (issue #3)


def test_find_practitioner_returns_the_stored_practitioner():
    """TEST-S6-06 / FR-03: a registered ID gives back that same practitioner."""
    _, _, practitioner_service, _ = make_services()
    practitioner = practitioner_service.register_practitioner(
        'D1', 'Taylor Example', 'General practice'
    )

    found = practitioner_service.find_practitioner('D1')

    assert found is practitioner
    assert found.specialty == 'General practice'


def test_find_practitioner_unknown_id_raises_lookup_error():
    """TEST-S6-07 / FR-03: an unregistered ID is not found, store unchanged."""
    data_store, _, practitioner_service, _ = make_services()
    practitioner = practitioner_service.register_practitioner(
        'D1', 'Taylor Example', 'General practice'
    )

    with pytest.raises(LookupError):
        practitioner_service.find_practitioner('D2')

    assert data_store.list_practitioners() == [practitioner]


def test_find_practitioner_empty_id_raises_value_error():
    """TEST-S6-08a / ID rules: an empty ID is invalid input."""
    _, _, practitioner_service, _ = make_services()

    with pytest.raises(ValueError):
        practitioner_service.find_practitioner('')


def test_find_practitioner_spaces_only_id_raises_value_error():
    """TEST-S6-08b / ID rules: an ID that is only spaces is invalid."""
    _, _, practitioner_service, _ = make_services()

    with pytest.raises(ValueError):
        practitioner_service.find_practitioner('   ')


def test_find_practitioner_non_text_id_raises_value_error():
    """TEST-S6-08c / ID rules: an ID that is not a string is invalid."""
    _, _, practitioner_service, _ = make_services()

    with pytest.raises(ValueError):
        practitioner_service.find_practitioner(None)


def test_find_practitioner_trims_and_is_case_sensitive():
    """TEST-S6-09 / ID rules: ' D1 ' finds D1, but 'd1' does not."""
    _, _, practitioner_service, _ = make_services()
    practitioner = practitioner_service.register_practitioner(
        'D1', 'Taylor Example', 'General practice'
    )

    assert practitioner_service.find_practitioner(' D1 ') is practitioner
    with pytest.raises(LookupError):
        practitioner_service.find_practitioner('d1')

# ---- FR-06 / FR-07 cancellation and history (issue #1)


def test_cancel_changes_status_to_cancelled():
    """TEST-S6-10 / AC-05.1: cancelling gives back the same appointment,
    now CANCELLED.
    """
    # Arrange
    _, appointment_service, appointment = book_one_appointment()

    # Act
    cancelled = appointment_service.cancel_appointment('A1')

    # Assert
    assert cancelled is appointment
    assert cancelled.status is AppointmentStatus.CANCELLED


def test_cancelled_appointment_is_kept_in_history():
    """TEST-S6-11 / AC-05.2: after cancelling, the appointment can still be
    found and listed, and its details have not changed.
    """
    data_store, appointment_service, appointment = book_one_appointment()

    appointment_service.cancel_appointment('A1')

    assert appointment_service.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]
    assert appointment.patient.patient_id == 'P1'
    assert appointment.practitioner.practitioner_id == 'D1'
    assert appointment.date_time == BOOKING_TIME


def test_cancelling_twice_is_rejected():
    """TEST-S6-12 / AC-05.3: a second cancel raises ValueError and the
    appointment stays CANCELLED.
    """
    data_store, appointment_service, appointment = book_one_appointment()
    appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]


def test_completed_appointment_cannot_be_cancelled():
    """TEST-S6-13 / FR-06: only SCHEDULED can be cancelled. There is no
    completion feature, so the COMPLETED appointment is made directly (BR-08).
    """
    data_store, appointment_service, first = book_one_appointment()
    completed = Appointment(
        'A2',
        first.patient,
        first.practitioner,
        datetime(2026, 10, 1, 10, 0),
        status=AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A2')

    assert completed.status is AppointmentStatus.COMPLETED


def test_cancel_unknown_appointment_raises_lookup_error():
    """TEST-S6-14: cancelling an ID that does not exist is LookupError and
    the real appointment is untouched.
    """
    data_store, appointment_service, appointment = book_one_appointment()

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A9')

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [appointment]


def test_cancel_empty_id_raises_value_error():
    """TEST-S6-15a / ID rules: an empty ID is invalid and changes nothing."""
    _, appointment_service, appointment = book_one_appointment()

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('')

    assert appointment.status is AppointmentStatus.SCHEDULED


def test_cancel_spaces_only_id_raises_value_error():
    """TEST-S6-15b / ID rules: an ID of only spaces is invalid."""
    _, appointment_service, appointment = book_one_appointment()

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('   ')

    assert appointment.status is AppointmentStatus.SCHEDULED


def test_cancel_non_text_id_raises_value_error():
    """TEST-S6-15c / ID rules: an ID that is not a string is invalid."""
    _, appointment_service, appointment = book_one_appointment()

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment(None)

    assert appointment.status is AppointmentStatus.SCHEDULED


def test_cancelled_slot_can_be_booked_again():
    """TEST-S6-16 / FR-05 with FR-06: a cancelled appointment no longer
    blocks the practitioner's time, and the old record is still kept.
    """
    data_store, appointment_service, old_appointment = book_one_appointment()
    appointment_service.cancel_appointment('A1')

    new_appointment = appointment_service.book_appointment(
        'A2', 'P1', 'D1', BOOKING_TIME
    )

    assert new_appointment.status is AppointmentStatus.SCHEDULED
    assert old_appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [old_appointment, new_appointment]
