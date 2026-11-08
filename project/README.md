# SmartCare (Group 3, Assignment 3)

Requirements baseline: SmartCare A3 2026 revision 2. Runtime uses only the Python standard library; tests use pytest 8.3.5 (verified on Python 3.14.7).

## Run commands

Run everything from this `project/` directory:

```sh
python main.py                  # short supplied demo
python main.py --interactive    # interactive menu
python -m pytest -q             # full test suite
```

If needed: `python -m pip install -r requirements-dev.txt`.

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
- Synthetic data only.

## Behaviour notes

- IDs are trimmed, must not be blank, and are case-sensitive (`D1` and `d1` are different).
- Store lookups return None when a record is absent; service lookups raise LookupError.
- Invalid values, duplicate IDs, practitioner conflicts and illegal status changes raise ValueError.
- Booking takes a local `datetime` at minute precision; the console accepts exactly `YYYY-MM-DD HH:MM`.
- Lists (including practitioner listings) are new lists holding the actual stored objects.

## Structure

`domain.py` entities and guarded cancellation; `data_store.py` the shared session store; `services.py` registration, lookup, booking, cancellation and practitioner listing; `queries.py` pure selection and sorting (`select_appointments`, `appointment_sort_key`); `console.py` the menu, date parser and appointment formatter; `main.py` chooses demo or menu.