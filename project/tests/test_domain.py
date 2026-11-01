"""Stage 7 tests for the domain classes: Patient, Practitioner, Appointment.

These test each class on its own, without the services or data store.
They add evidence the supplied test_starter.py checks do not give:
trimming, whitespace-only fields, invalid appointment inputs, the starting
status and the cancel guard. Only made-up data is used.
"""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


BOOKING_TIME = datetime(2026, 10, 1, 9, 0)


def make_appointment():
    """Make a patient, a practitioner and a new appointment between them."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General practice')
    appointment = Appointment('A1', patient, practitioner, BOOKING_TIME)
    return patient, practitioner, appointment


# ---- Valid and invalid construction (TEST-S7-01 to TEST-S7-03)


def test_valid_patient_and_practitioner_keep_trimmed_fields():
    """TEST-S7-01 / FR-01, FR-03 (domain part only) and the ID rules: valid
    values are kept, with spaces around them removed.
    """
    patient = Patient('  P1 ', ' Alex Example ')
    practitioner = Practitioner(' D1 ', 'Taylor Example', 'General practice')

    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General practice'


def test_blank_patient_id_and_required_fields_are_rejected():
    """TEST-S7-02 / ID rules and FR-01, FR-03 required fields: a blank
    patient ID (reference test intention), a spaces-only name and a
    spaces-only specialty are each rejected with ValueError.
    """
    with pytest.raises(ValueError):
        Patient('   ', 'Alex Example')
    with pytest.raises(ValueError):
        Patient('P1', '   ')
    with pytest.raises(ValueError):
        Practitioner('D1', 'Taylor Example', '   ')


def test_invalid_appointment_inputs_are_rejected():
    """TEST-S7-03 / BR-04, BR-08 and the date/time rules: a patient ID
    string instead of a Patient, a time with seconds, or a status given as
    text are each rejected with ValueError.
    """
    patient, practitioner, _ = make_appointment()

    with pytest.raises(ValueError):
        Appointment('A1', 'P1', practitioner, BOOKING_TIME)
    with pytest.raises(ValueError):
        Appointment(
            'A1', patient, practitioner, datetime(2026, 10, 1, 9, 0, 30)
        )
    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, BOOKING_TIME, status='scheduled')