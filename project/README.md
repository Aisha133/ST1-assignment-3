# SmartCare (Group 3, Assignment 3)

Requirements baseline: SmartCare A3 2026 revision 2. Runtime uses only the Python standard library; tests use pytest 8.3.5 (verified on Python 3.14.7).

Release: **SmartCare v1.0**, UG common scope. The exact release SHA is recorded in `stage12/stage12_activities_and_evidence.md` (section K).

## Purpose

SmartCare is a small console application for a clinic's front desk. It registers patients and practitioners, books appointments without double-booking a practitioner, cancels appointments while keeping their history, and lists a practitioner's appointments by status and time. It is a teaching release built over Stages 6–9 and released in Stage 12. It is not production healthcare software.

## Included in this release

- FR-01–FR-09: register/find patients and practitioners; book with validation and the practitioner conflict rule; cancel and keep history; find appointments; list a practitioner's appointments.
- QRY-01–04 and FP-01–03: a pure, explicit-input query (`select_appointments`) with a named sort key (`appointment_sort_key`).
- UI-01/UI-02: an interactive menu that reports invalid input and keeps running.
- Not included: FR-10 restart persistence (retired), and PG-only rescheduling/assurance (Stages 10–11; this is an all-UG group).

## Environment

The course's verified baseline is Python 3.13 with pytest 8.3.5. This release was verified on Python 3.14.7 with pytest 8.3.5. The application uses only the standard library; pytest is the only development dependency (pinned in `requirements-dev.txt`).

From the repository root, create and activate a virtual environment, then:

```sh
cd project
python -m pip install -r requirements-dev.txt
```

## Run commands

Run everything from this `project/` directory:

```sh
python main.py                  # short supplied demo
python main.py --interactive    # interactive menu
python -m pytest -q             # full test suite
```

## Verification

Last verified on 08/11/2026 (Windows, Python 3.14.7, pytest 8.3.5), from this `project/` directory: `python -m pytest -q` gave 57 passed (Stage 6–8 tests plus TEST-S9-01..13). Console demonstration inputs and outputs for UI-01 and UI-02 are in `stage09/evidence/`.

## Interactive menu

| Option | Action | Input |
|---|---|---|
| 1 / 2 | Register patient / find patient | patient ID, name / patient ID |
| 3 / 4 | Register practitioner / find practitioner | practitioner ID, name, specialty / practitioner ID |
| 5 | Book appointment | appointment ID, patient ID, practitioner ID, date/time `YYYY-MM-DD HH:MM` |
| 6 / 7 | Cancel appointment / find appointment | appointment ID |
| 8 | List a practitioner's appointments | practitioner ID; status blank for all, or `scheduled` / `cancelled` / `completed` |
| 0 | Exit | session data is discarded |

Invalid input (unknown or blank IDs, duplicates, unknown participants, malformed or impossible dates, conflicts, repeated cancellation, invalid status, unknown option) is reported as an error and the menu continues without changing stored records.

## Scope and limitations

- Data exists only for the current session and is lost on exit; a new run starts empty. Restart persistence (FR-10) is retired, so there is no file or database storage.
- Cancelling keeps the appointment (status CANCELLED) so it can still be found and listed; nothing is deleted.
- Conflict rule: only the same practitioner at exactly the same date/time with a SCHEDULED appointment conflicts. There are no duration, patient-conflict or past-date rules.
- There is no feature to mark an appointment COMPLETED; that status is only created directly in tests.
- Synthetic data only. Times are local, naive and minute-precision, with no timezone policy.
- Out of scope: authentication/roles, patient portal, SMS/email notifications, billing/insurance, clinical decision support, multi-user concurrency or scale, operations/monitoring, and formal usability/accessibility evaluation. Passing tests do not imply production, clinical or security certification.

## Behaviour notes

- IDs are trimmed, must not be blank, and are case-sensitive (`D1` and `d1` are different).
- Store lookups return None when a record is absent; service lookups raise LookupError.
- Invalid values, duplicate IDs, practitioner conflicts and illegal status changes raise ValueError.
- Booking takes a local `datetime` at minute precision; the console accepts exactly `YYYY-MM-DD HH:MM`.
- Lists (including practitioner listings) are new lists holding the actual stored objects.

## Responsible AI use

GitHub Copilot was used as a reviewer in Stages 6–9; each suggestion was checked against code, requirements and tests and recorded as Accept/Modify/Reject in the stage records (for example, `stage09/evidence/copilot_review.md` and record E). It helped to draft areas as well as to record certain pieces of information. All code was run and tested by the group with a running log of work.

## Synthetic data rule

Use made-up names and IDs only (for example P1 Alex Example, D1 Taylor Example). Never enter real patient information.

## Structure

- `smartcare/domain.py`: Patient, Practitioner, Appointment and AppointmentStatus; entities validate their own fields, and Appointment guards cancellation.
- `smartcare/data_store.py`: SmartCareDataStore, the one shared in-memory store for the current session (add/find/list).
- `smartcare/services.py`: PatientService, PractitionerService and AppointmentService coordinate use cases, including the practitioner conflict check against the shared store and practitioner listing.
- `smartcare/queries.py`: pure functions `select_appointments` and `appointment_sort_key`, with explicit inputs and no state.
- `smartcare/console.py`: the interactive menu, date/status parsing and output; the only place that reads input or prints.
- `main.py`: runs the short demo, or the menu with `--interactive`.
- `tests/`: pytest tests for the domain, services, Stage 8 regressions, queries, workflows and console.