# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group 3, Tuesday 1:30pm Tutorial
Members and UG/PG cohorts: Aisha (@Aisha133, UG); Hannah (@Hannah-448, UG); Anastasia (@Ajorja, UG); Benjamin (@Benjamin316-uc, UG)
Record owner / contribution links for each member: Record compiled by Anastasia from team notes; each member's contribution and artefacts are listed in section I.

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: 

Appointment disappears after cancellation - symptom This statement is a symptom as it describes what is happening rather than explaining why it has happened.

The data-store removal path is probably being called - Hypothesis This statement is a hypothesis as the sentence is worded as an untested guess

The failing test shows store.find_appointment('A1') returns None - Evidence This statement can be seen as evidence as it presents an issue from a test / the code.

The service layer is badly designed - Opinion This statement is classified as opinion as it is based on judgement rather than any specific evidence or facts.

Traceback points to smartcare/services.py line 42 in the example. The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation - Evidence This statement is Evidence as it shows where the error was raised and a traceback is an observed output.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: 

Debugging record F8-02, cancelled history

Expected behaviour: The cancelled appointment is expected to remain in the store and still be returned by find_appointment as the same object. Attempting to cancel an appointment for a second time raises a ValueError and will change nothing, because only appointments that have been SCHEDULED can be cancelled.

Observed behaviour: After cancelling appointment A1, find_appointment('A1') raises "LookupError: Appointment not found" and attempting to cancel the same appointment a second time raises a LookUpError instead of a ValueError. Cancelling itself works, as the appointment status changes to CANCELLED.

Minimal reproduction: As a minimal reproduction is the smallest possible way to find an error or bug in a code, the best steps to take would be to create a new SmartCareDataStore, register another patient ID (P1) alongside that register another practitioner (D1), book an appointment (A1) at 6/11/26 at 10:30, and then proceed to cancel this appointment. Call find_appointment ('A1') and receive a LookupError and compare that return value with what is returned in list_appointments.

Hypothesis: If the find_appointment code incorrectly stores booking history, then it will fail to locate a booking that still exists within the data store, even if the cancelled appointment has been updated correctly.

evidence: Some evidence to inspect include seeing if A1 is still in list_appointments() after an appointment is cancelled. Another thing to inspect is what does the store find_appointment check before it returns a final statement? Compare it to another element in the code, such as find_patient which should not have a status check, this will allow us to see the different return values.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: 

Test expecting cancelled appointments to be deleted: The test expecting the cancelled appointment to be deleted should be changed, as FR-07 does state that appointment history must be retained, therefore the test should instead check whether or not the appointment stays within the data store after being cancelled. This is a test defect: the test expects invented behaviour, so the test is changed, not the code

Test expecting different practitioners at the same time to conflict: This does not reflect AC-04.2 as that says only the same practitioner at the same exact time conflicts and a different practitioner must be allowed so that test is also a test defect and should expect the booking to be allowed.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:

Hypothetical 70-line AppointmentService method
- Duplicate status strings: Status "Scheduled" and "cancelled" is repeated
- Direct collection manipulation: The service bypasses the SmartCareDataStore which breaks the storage boundary
- Printing: This mixes output with domain rules which makes the method harder to test and reuse
- Validation: Input checks are tangled with booking and conflict logic
- Four nested conditionals: Deep nesting hides which condition leads to which outcome

Small refactoring that preserve required behaviour
- Replace the status strings with the existing AppointmentStatus
- Use guard clauses to flatten the nested conditionals
- Extract validation into a small helper method
- Replace direct collection access with calls to existing store methods such as find_appointment, list_appointments.
- Extract the repeated conflict check into one helper

Classification

| Change | Type | Reason |
|---|---|---|
| rename appt to appointment | Refactoring | Only the name changes not the behaviour |
| extract a repeated conflict helper | Refactoring | The same logic moves into one place with same outcome |
| add rescheduling | Feature | It introduces new behaviour that did not exist before |
| restore retained cancellation lookup | Repair | It fixes behaviour that violates FR-07 |
| replace a magic status string with the existing enum | Refactoring | The value is the same, only its representation changes |

Behaviour that must stay unchanged
- The same exceptions are raised: ValueError for invalid values, duplicate appointment IDs and practitioner conflicts, and LookupError for absent patients, practitioners or appointments.
- Only the same practitioner at exactly the same time with a SCHEDULED appointment counts as a conflict (FR-05, AC-04.1, AC-04.2).
- A rejected booking stores nothing
- A cancelled appointment stays stored and listed with status CANCELLED
- A second cancel is rejected with ValueError and changes nothing
- All existing tests still pass

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: 

Failure used: tests/test_services.py::test_same_practitioner_same_time_is_rejected
Exception/assertion: Failed:Did not raise <class 'ValueError'>
Expected vs observed: A ValueError was expected on the second booking of D1 at 09:00. However the booking was accepted silently.
Test line: tests\test_services.py: line 386
Call path: The test calls AppointmentService.book_appointment, which calls data_store.has_practitioner_conflict. That returns False, so no error is raised and the appointment is stored.
Requirement: FR-05 / AC-04.1

Ranked causes

| Rank | Cause | Evidence | Distinguish from the others |
|---|---|---|---|
| 1 | The comparison in has_practitioner_conflict is inverted (!= instead of ==) | It explains both symptoms: same practitioner is allowed, different practitioner is rejected | Call has_practitioner_conflict(D1) and (D2) directly after booking D1. The results come out flipped. |
| 2 | book_appointment passes the wrong practitioner ID | It is poor as a wrong ID would not flip both results consistently | The traceback shows it passes practitioner.practitioner_id of the booking being made, so print the argument received |
| 3 | The stored appointment holds an unexpected practitioner | Poor | Print a1.practitioner.practitioner_id. It showed D1 and test_registration_and_booking still passes |

Why a traceback alone doesn't establish the cause: A traceback shows where a failure was detected, not where the fault originated. Here the failure was a missing exception inside the test, with no frame pointing at has_practitioner_conflict. In F8-02 the LookupError was raised in services.py but the real cause was in data_store.py.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason:

Changing code straight after seeing an error replaces diagnosis with guessing. A failure shows that something is wrong but not what may have caused the issue or where the problem is. The cause is still unknown, therefore, indicating that the fix may hide the symptom and fixing one test won't explain the problem. It is important to investigate all probable causes, as the test may be the defect, meaning it destroys the evidence and nothing is learned. Further emphasising that it is important to investigate the issue before implementing any changes.

Classification responses (1–5, each with reason):

Appointment disappears after cancellation - symptom It describes what is seen, not why

The data-store removal path is probably being called - hypothesis. Having probably in the sentence marks an untested guess

Failing test shows store.find_appointment('A1') returns - None evidence. It is an observed, repeatable fact.

The service layer is badly designed - opinion. This cannot be tested, and the service correctly raises LookupError when the store returns None.

Traceback points to services.py line 42 - evidence. It shows where the error was raised, not where the fault is.

Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect:

Expected: A cancelled appointment stays stored and find_appointment('A1') returns it; and a second cancel raises ValueError (FR-07 / AC-05.2, FR-08 / AC-05.3).

Observed: find_appointment('A1') raises LookupError after cancelling; and a second cancel raises LookupError instead of ValueError.

Reproduction (steps to reproduce):

1. Fresh store; register patient P1 and practitioner D1.
2. Book A1: P1 with D1 at 2026-10-01 09:00.
3. Cancel appointment A1.
4. Call find_appointment('A1'), observe the LookupError instead of the cancelled appointment.
5. Try and cancel appointment A1 for a second time, observe the lookup error instead of the expected error.

Hypothesis: If the find_appointment code incorrectly stores booking history, then it will fail to locate a booking that still exists within the data store, even if the cancelled appointment has been updated correctly.

Evidence to inspect: If A1 is still in list_appointments(), and what the store's find_appointment checks compared with find_patient.

Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks:

Assertion: Failed: Did not raise <class 'ValueError'> Expected/observed: ValueError expected on the second D1 booking at 09:00 the booking was accepted Test line: tests\test_services.py: line 386 Call path: test → book_appointment → has_practitioner_conflict, which returns False. Requirement: FR-05 / AC - 04.1 Ranked causes and checks:

1. Inverted comparison (!= instead of ==) in has_practitioner_conflict. Check: call it directly with 'D1' and 'D2'
2. Book_appointment passes the wrong ID. Check: print the argument received
3. The stored appointment holds the wrong practitioner. Check: print a1.practitioner.practitioner_id

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: b05cc735f8d5758046f0da8633caed7a5b05f86b (Stage 7 record committed as 11805ad5b9dd58470660b12c7f4ee0a4c95f274e); SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: python -m pytest, project/, 42 passed on main at 11805ad (Python 3.14.7, pytest 8.3.5); git status clean before preparation.
- Clean preparation SHA if a record-only commit followed Stage 7: 645a14eddf71c7f7710a1fd7bbc9924c088191d7 ("update .gitignore", on debug/stage08 after 11805ad). This was the clean baseline the tool recorded.
- Branch and preparer / how teammates obtained this branch: debug/stage08, prepared by Anastasia on her laptop in the 03/11 tutorial with the tutor's guidance; pushed with git push -u origin debug/stage08. The group works on one laptop; a member on another device would use git fetch origin and git switch --track origin/debug/stage08 (the utility was not applied again).
- Downloaded tool version, source SHA256 and --check outcome: prepare_debugging.py tool_version 1.1; baseline_sha256 986c5445532ffd1d85e88639b6b6f34b84e15b2bbfc1882511a96938c3b641f6; --check: "preflight PASS ... CHECK ONLY: project unchanged; both proposed fault signatures verified in a temporary copy".
- --apply and --verify output summaries / artefact references: --apply: "PREPARED: F8-01 practitioner conflict; F8-02 retained-history lookup; Verified expected failures: test_f8_01_conflict; test_f8_02_history (2 failed)"; fault_sha256 1e804f451b1a9de42c67a38be9a9696029946ec6eb2319d37171fe5ba7a117f0; status "prepared". --verify: "VERIFIED: exactly 2 expected failures; both approved symptom signatures present". Full output saved in team log notes.
- Bounded diff inspected and recovery location (not committed): git show --stat 8bfaa8d: only project/smartcare/data_store.py (the two store methods) and .gitignore changed. Recovery backup in project/.stage8_faults/ (ignored by .gitignore, not committed). git ls-files confirmed the tool script is not tracked.
- Prepared faulty-state commit SHA: 8bfaa8d5d13976e37f3950ccb4d10215f71d5765 ("Prepare debug/stage08"), pushed to debug/stage08, not merged into main.
- Preparation or recovery issues and resolution, if any: none; --restore not needed. The tool was run from the repository root; .gitignore was updated (645a14e) so the tool and its backups stay out of Git.
- Initial prepared full-suite command / result / key failures: python -m pytest -q in project/: 5 failed, 37 passed. F8-01: test_same_practitioner_same_time_is_rejected (DID NOT RAISE ValueError), test_other_practitioner_or_other_minute_is_allowed (ValueError: Practitioner already has a SCHEDULED appointment at this time), test_starter.py::test_conflict_rule_and_different_practitioner (DID NOT RAISE). F8-02: test_cancelled_appointment_is_kept_in_history and test_cancelling_twice_is_rejected (LookupError: Appointment not found).

## C. F8-01 diagnosis and repair

Symptom / observed behaviour: booking practitioner D1 twice at 09:00 is accepted (DID NOT RAISE ValueError), but booking a different practitioner D2 at 09:00 is rejected with "ValueError: Practitioner already has a SCHEDULED appointment at this time".
Expected behaviour and requirement: the same practitioner at exactly the same time must be rejected with ValueError and nothing stored; a different practitioner at that time is allowed (FR-05 / AC-04.1, AC-04.2).
Minimal synthetic reproduction steps: fresh SmartCareDataStore; register patients P1, P2 and practitioners D1, D2; book A1 (P1, D1, 2026-10-01 09:00); book A2 (P2, D1, same time): accepted, should be rejected; book A3 (P2, D2, same time): should be allowed.
Meaningful failing test path/name and exact relevant failure: tests/test_regressions.py::test_f8_01_conflict_checks_the_same_practitioner: "Failed: DID NOT RAISE <class 'ValueError'>" at line 45 (commit b7f15f1). Also detected by the three existing tests listed in B.
Human hypothesis and intended checks: see E, F8-01.
Supported root cause and inspected code/runtime evidence: in has_practitioner_conflict the practitioner condition was appointment.practitioner.practitioner_id != practitioner_id, so it reported a conflict only for OTHER practitioners. This explains both flipped results. The booking call path passes the booked practitioner's ID (services.py), and an evidence run showed the stored appointment holds D1, so the inputs are correct and the comparison is the cause.
Smallest justified fix / diff / why other behaviour is preserved: changed != to == on that one line (git diff: one line). The time and status parts of the condition and the call path are unchanged, so cancelled bookings still free the slot and a different minute is still allowed.
Repair SHA / focused verification result: ba53bbc ("Fix F8-01 ... (refs #8)"): REG-F8-01 1 passed; full suite 3 failed (F8-02 only), 41 passed.

## D. F8-02 diagnosis and repair

Symptom / observed behaviour: after cancelling A1, find_appointment('A1') raises "LookupError: Appointment not found", and a second cancel raises LookupError instead of ValueError. Cancelling itself works (status becomes CANCELLED).
Expected behaviour and requirement: a cancelled appointment stays in the store and is still returned by find_appointment as the same object; a second cancel raises ValueError and changes nothing (FR-07 / AC-05.2, FR-08, AC-05.3).
Minimal synthetic reproduction steps: fresh SmartCareDataStore; register P1 and D1; book A1 at 2026-10-01 09:00; cancel A1; call data_store.find_appointment('A1') and appointment_service.find_appointment('A1'); compare with list_appointments().
Meaningful failing test path/name and exact relevant failure: tests/test_regressions.py::test_f8_02_cancelled_appointment_can_still_be_found: "AssertionError: assert None is <smartcare.domain.Appointment object ...>" from data_store.find_appointment('A1') at line 64 (commit b7f15f1). Also detected by the two existing tests listed in B.
Human hypothesis and intended checks: see E, F8-02.
Supported root cause and inspected code/runtime evidence: the store's find_appointment loop only returned an appointment if appointment.status.value != "cancelled", so any CANCELLED appointment was skipped. Evidence run (from project/): "stored practitioner: D1; still listed: True; status: AppointmentStatus.CANCELLED; store lookup: None": the record is retained but the lookup filters it out. The service then turns None into LookupError, and cancel_appointment's lookup fails before Appointment.cancel() can raise ValueError.
Smallest justified fix / diff / why other behaviour is preserved: removed only the cancelled-status condition, so the loop returns the appointment whose ID matches (git diff: two lines removed, one added). Blank/invalid IDs still raise ValueError, an unknown ID still returns None (service LookupError), and the same stored object is returned. The second-cancel ValueError returns because Appointment.cancel() now runs.
Repair SHA / focused verification result: 817c99f ("Fix F8-02 ... (refs #9)"): tests/test_regressions.py 2 passed; full suite 44 passed.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: If the system is incorrectly checking practitioner availability, then it will allow the same practitioner for a second booking when it should be rejected, and reject a different practitioner when it should be allowed. Because both results are flipped, the check is probably matching the wrong practitioners.
Evidence intended to inspect / competing explanation / discriminating check: inspect the practitioner comparison in has_practitioner_conflict against the FR-05 wording ("same practitioner") and check the time and status parts are unchanged; competing explanations were that the wrong ID is passed in or the stored appointment holds the wrong practitioner; discriminating check: the flipped pattern only fits an inverted comparison. Proposed fix noted at the time: appointment.practitioner.practitioner_id == practitioner_id.
Member and saved sequence/time or commit showing this preceded consultation: first hypothesis by Aisha (04/11); completed in the handout template by Benjamin and Anastasia at 5:33 pm on 04/11, before Copilot was used on 05/11 (team log).

### F8-02 human entry
Likely cause and why plausible: If the find_appointment code incorrectly stores booking history, then it will fail to locate a booking that still exists within the data store, even if the cancelled appointment has been updated correctly. So the record is probably not lost; the lookup is not finding it.
Evidence intended to inspect / competing explanation / discriminating check: check A1 is still in list_appointments() after cancelling, and what the store's find_appointment checks before returning, compared with find_patient (which has no status check); competing explanation: the record was removed or replaced on cancel; discriminating check: list_appointments() still containing the same A1 object rules that out. Proposed fix noted at the time: delete the condition "and appointment.status.value != 'cancelled'".
Member and saved sequence/time or commit showing this preceded consultation: first hypothesis by Aisha (04/11); completed in the handout template by Benjamin and Anastasia at 6:07 pm on 04/11, before Copilot was used on 05/11 (team log)

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: handout diagnostic prompt with the F8-01 observed/expected behaviour, reproduction, failing tests, hypothesis and has_practitioner_conflict code, plus the rank-three-causes task and no-rewrite/no-invented-requirements constraints; sent in its own chat by Anastasia and Benjamin on 05/11.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Ranked suggestion: the practitioner comparison is inverted (!= instead of ==). Evidence check: compare the condition with FR-05 and the flipped results. Observed evidence: the condition reads practitioner_id != practitioner_id; both flipped results match. Correct. Accept: matches our hypothesis and was confirmed by the fix (REG-F8-01 fail to pass).
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Ranked suggestion: the booking service passes the wrong practitioner ID. Evidence check: the booking call path. Observed evidence: book_appointment passes practitioner.practitioner_id of the booking being made (services.py, also visible in the traceback). Wrong. Reject.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Ranked suggestion: the stored appointment holds an unexpected practitioner. Evidence check: inspect the stored A1. Observed evidence: evidence run printed "stored practitioner: D1"; test_registration_and_booking (identity checks) still passes. Wrong. Reject.
Final human conclusion and comparison with initial hypothesis: the root cause is the inverted practitioner comparison, the same as our initial hypothesis. Copilot's top suggestion agreed; the evidence ruled out its other two.

### F8-02 Copilot review
Actual prompt / output reference and member: handout diagnostic prompt with the F8-02 details and both find_appointment methods (store and service), in a separate chat by Anastasia and Benjamin on 05/11.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Ranked suggestion: find_appointment deliberately skips cancelled appointments. Evidence check: status after cancelling, list_appointments() and the store lookup. Observed evidence: "still listed: True; status: CANCELLED; store lookup: None". Correct. Accept: matches our hypothesis and was confirmed by the fix.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Ranked suggestion: the second-cancel path looks up the appointment before checking its status. Evidence check: the cancel call path. Observed evidence: cancel_appointment does call find_appointment first, which is why the second cancel gave LookupError; but that order is the intended Stage 6 design, and Appointment.cancel() raises ValueError once the lookup works. Copilot also named a non-existent AppointmentService.cancel (it is cancel_appointment). Partly correct. Modify: kept as the explanation of the second symptom, a consequence of cause 1, not a separate defect; the order was not changed.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Ranked suggestion: the record was removed, replaced or its ID changed during cancellation. Evidence check: the backing collection and object identity. Observed evidence: A1 still listed as the same object; test_cancel_changes_status_to_cancelled ("cancelled is appointment") passes. Wrong. Reject.
Final human conclusion and comparison with initial hypothesis: the root cause is the cancelled-status filter in the store's find_appointment; the record was never lost. This matches our initial hypothesis that the lookup, not the record, was the problem (Aisha's first wording said "stores", but the evidence showed storing was correct). The second-cancel symptom was a knock-on effect.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | b7f15f1 (tests added on prepared state) | python -m pytest tests/test_regressions.py, project/ | REG-F8-01 failed: DID NOT RAISE ValueError (line 45); full suite 7 failed, 37 passed |
| F8-01 after repair | ba53bbc | python -m pytest tests/test_regressions.py::test_f8_01_conflict_checks_the_same_practitioner, project/ | 1 passed; full suite 3 failed (F8-02 only), 41 passed |
| F8-02 before repair | b7f15f1 and ba53bbc | python -m pytest tests/test_regressions.py, project/ | REG-F8-02 failed: assert None is <Appointment> from data_store.find_appointment('A1') (line 64) |
| F8-02 after repair | 817c99f | python -m pytest tests/test_regressions.py, project/ | 2 passed |
| Full suite after both repairs, before refactor | 817c99f | python -m pytest -q, project/ | 44 passed |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: REG-F8-01 books the same practitioner twice with two different patients, so it can only fail on the practitioner rule; it uses pytest.raises(ValueError), then checks the list is still only the first booking (a rejected booking stores nothing), then that a different practitioner at that time is stored (AC-04.2). The inverted comparison failed the first check. REG-F8-02 checks the store lookup ("is" the same object, not None) separately from the service lookup (no LookupError), that the appointment is still listed, and that a second cancel still raises ValueError with status CANCELLED. The cancelled filter failed the store check. All 42 earlier tests are retained, so every previous behaviour is rechecked on each run.
Unrelated failures investigated / resolution: all 5 prepared failures and both new regression tests traced to F8-01 or F8-02, and all passed after the two repairs.

## H. Refactoring decision and before/after verification

Smell and exact location: magic status string: has_practitioner_conflict in project/smartcare/data_store.py compared appointment.status.value == "scheduled" (plain text), while the rest of the code uses the AppointmentStatus enum.
Small proposed structural change / why justified: replace it with appointment.status is AppointmentStatus.SCHEDULED. If the enum's text ever changed, the string comparison would silently stop finding conflicts; using the enum keeps one source of truth. Planned by Anastasia on 06/11, before editing (team log; issue #10 created by Hannah).
External behaviour to preserve / relevant tests: same practitioner at the same time still conflicts (ValueError, nothing stored); a CANCELLED booking still frees the slot; another practitioner or another minute is still allowed; return values, exceptions and stored records unchanged. Tests: test_same_practitioner_same_time_is_rejected, test_other_practitioner_or_other_minute_is_allowed, test_cancelled_slot_can_be_booked_again, test_f8_01_conflict_checks_the_same_practitioner, plus the full suite.
Before result: see G, full passing suite (44 passed at 817c99f).
Actual change / diff / separate refactor SHA: 9bdead1 ("Refactor: use AppointmentStatus enum instead of magic string in conflict check (refs #10)"): one line changed.
Focused and full after-refactor commands / working directory / results / evidence: python -m pytest with the four focused tests above, project/: 4 passed; python -m pytest -q, project/: 44 passed.
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: accepted: the same 44 tests pass before and after, including the conflict and cancelled-slot tests, so the change improved readability and consistency without changing behaviour.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: #8 F8-01 (created by Aisha), #9 F8-02 (created by Benjamin), #10 refactor (created by Hannah); repairs and refactor implemented by Anastasia.
Branch / prepared, repair and refactor checkpoints: debug/stage08: prepared 8bfaa8d (B); failing tests b7f15f1 (G); F8-01 repair ba53bbc (C); F8-02 repair 817c99f (D); refactor 9bdead1 (H).
PR link and another member's reviewer identity: https://github.com/Aisha133/ST1-assignment-3/pull/11, reviewed by Benjamin (@Benjamin316-uc).
Key human feedback, difference from Copilot findings and response/outcome: Benjamin's review: "Reviewed both repairs against FR-05/AC-04.1-04.2 and FR-07/AC-05.2/FR-08: each is minimal and fixes the root cause. Regression tests failed before repair for the intended reasons and pass after. The refactor replaces a magic string with the existing enum without changing behaviour. My run: 44 passed. Approved." Unlike Copilot, the human review checked the actual diff and ran the suite itself; no changes requested, approved as submitted.
Actual review approval / merge evidence: https://github.com/Aisha133/ST1-assignment-3/pull/11#pullrequestreview-5809414317; merged by Anastasia as merge commit bb8d825 ("Merge pull request #11 from Aisha133/debug/stage08", merge commit, branch kept); issues #8–#10 closed by the merge.
Integrated code SHA and team pull/retest command / working directory / result: bb8d8257bfe18aac918d721f5c048efe40aa9749; git switch main, git pull, then python -m pytest -q in project/: 44 passed (team present on the shared laptop).
Evidence-only later SHA / explanation if different: the later commit "Complete Stage 8 evidence record" adds only this record and the README; there are no code or test changes after bb8d825.
Each member's substantive contribution and artefact:
- Anastasia: ran the preparation with the tutor (645a14e, 8bfaa8d); co-wrote the defect reports and hypotheses; ran the evidence check; wrote the regression tests (b7f15f1), both repairs (ba53bbc, 817c99f) and the refactor (9bdead1); opened and merged PR #11; compiled this record.
- Aisha: wrote the first hypotheses for both defects; created issue #8; wrote the tutorial answers (A) and formative answers (K) with Hannah.
- Hannah: created issue #10 (refactor scope); tutorial answers (A) and formative answers (K) with Aisha.
- Benjamin: co-wrote the defect reports and hypotheses (5:33, 6:07 pm); ran copilot prompts with Anastasia; created issue #9; reviewed and approved PR #11.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? F8-02 cause 2: that the second cancel failed because the service looks the appointment up before checking its status. It sounded like a second, separate bug, but the evidence showed it was only a knock-on effect of the cancelled filter (cause 1): once the lookup worked, Appointment.cancel() raised ValueError as designed, with no change to the order. Copilot also named a method that does not exist (AppointmentService.cancel).
2. What evidence changed your group's view? Running the evidence check: A1 was still in list_appointments() with status CANCELLED while data_store.find_appointment('A1') returned None. That showed the record was never lost and the lookup was filtering it out, so Aisha's first wording ("incorrectly stores booking history") was refined to a lookup problem. Reading the booking call path similarly ruled out the "wrong ID passed in" explanation for F8-01.
3. How did regression tests protect the refactoring? We refactored only once all 44 tests passed, then ran the same tests after the change and got the same 44 passed, including the conflict tests, the cancelled-slot test and REG-F8-01. If replacing the "scheduled" string with the enum had changed the conflict rule, those tests would have failed straight away.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: When a code appears an engineer should assess the severity of what has happened, understand the issue and try to reproduce it, find what in the code has triggered the issue, and then proceed to write a regression test. If the code being formulated is for a business, it would be best to inform stakeholders of any issues that have arisen.

2. Where should expected behaviour come from during debugging?

Response: Areas of the source code that define how the system should work.

3. What is a debugging hypothesis?

Response: A debugging hypothesis is a testable explanation on how current code produces an observed bug and or defect inside the code.

4. What is a regression test and why is it retained?

Response: A regression test is the process of re-running all functional and non-functional tests on the code, to then ensure that any possible fixes or changes in the code do not break any existing functionality.

5. What is meant by root cause?

Response: A root cause is typically the underlying issue of a problem.

6. What is refactoring?

Response: Refactoring is the process of improving internal structure of the source code without changing any functionality.

7. What is a swallowed exception?

Response: Is when a try/except block catches an error and does nothing with it (e.g. except: pass)the failure is therefore hidden, and the program is able to carry on as if nothing went wrong.

8. What is a code smell?

Response: A sign inside a source code that typically points to an underlying or deeper issue.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: It should be treated through testing, hypothesis and also review of the code.

10. What is the Stage 8 engineering rule?

Response: The stage 8 rule is to diagnose before you fix. This rule entails for the programmer to reproduce the failure, record/create a human hypothesis before making one with copilot, confirm the cause of evidence, make the smallest repair that restores the requirement, keep a regression test, refactor only while all tests path, and have another member review it to ensure that it is up to standard.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: the commit "Complete Stage 8 evidence record" (record and README only, no code or test changes after bb8d825). A commit cannot contain its own SHA, so it is recorded as the Stage 9 starting commit.
Unresolved issues or incomplete checks / owner / next action: none for the Stage 8 requirements. Noted for later (not changed, to keep this stage to one refactor): the prepared methods find_appointment and has_practitioner_conflict lost their docstrings, and find_appointment repeats its own blank-ID check instead of using required_text like the other find methods. Possible candidates for a later tidy-up through review.
Handover note: main at bb8d825 has both defects repaired, 2 retained regression tests and one refactor; python -m pytest in project/ gives 44 passed. Stage 9 starts from this commit after the record is committed. The Stage 8 tool and its backups are not in the repository.
