# Stage 7 Testing and Verification Record

Group/tutorial: Group 3, Tuesday 1:30pm Tutorial  Members/cohorts: Aisha (@Aisha133, UG); Hannah (@Hannah-448, UG); Anastasia (@Ajorja, UG); Benjamin (@Benjamin316-uc, UG)
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register P1 "Alex Example" with a new ID; it is stored and find_patient("P1") returns it. | Register P1 again (or " P1 ") with another name; ValueError is raised. | The stored patient `is` the original object and its name is unchanged after the rejected duplicate. |
| FR-05 Prevent practitioner conflict | Book D1 at 09:00, then book D2 at 09:00 for the same patient; both are stored. | Book D1 at 09:00, then book D1 at 09:00 again with a new ID; ValueError is raised. | After the rejection the appointment list is still just the first booking and it is still SCHEDULED. |
| FR-06 Cancel appointment | Cancel a SCHEDULED appointment; it returns the same object, now CANCELLED. | Cancel the same appointment again, or cancel a COMPLETED one; ValueError is raised. | `status is AppointmentStatus.CANCELLED` (or stays COMPLETED) and the returned object `is` the booked one. |
| FR-07 Retain cancelled history | After cancelling A1, find_appointment("A1") still returns it and it is still in list_appointments(). | Cancel an unknown ID A9; LookupError is raised and nothing is removed or changed. | find_appointment("A1") `is` the original object and list_appointments() still contains it with the same patient, practitioner and time. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: It is always true, so it passes even if the code is completely broken. It proves nothing about any behaviour.

`assert appointment is not None`
Judgement: Weak/unclear  Why: It only shows something came back. It does not check it is the right appointment, the right status, or that it is the stored object, so a wrong or new object would still pass.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: It checks the exact required status after cancelling (FR-06). Limit: on its own it does not prove the same object was kept in the store (FR-07); `is` would be slightly stricter than `==` for an enum.

`assert len(results) > 0`
Judgement: Weak/unclear  Why: It only shows the list is not empty. It would pass with the wrong appointments, duplicates or the wrong order, so it does not prove which items are correct.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: It checks the store returns the exact same object, which proves retained history and identity (FR-07 / AC-05.2). Limit: it does not check the status, so pair it with a status assertion.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 
- Blank identifiers: patient ID "" or "   " or None at registration or lookup gives ValueError (ID rules: IDs are trimmed and non-blank); " P1 " is treated as "P1", so registering it after P1 is a duplicate (ValueError) and looking it up finds P1. "p1" is a different ID (case-sensitive), so lookup gives LookupError.
- Whitespace-only names: Patient("P1", "   ") or a practitioner specialty "   " gives ValueError and nothing is stored (FR-01/FR-03 required name and specialty).
- Same-time practitioner bookings: D1 at 09:00 twice gives ValueError and only the first is stored (AC-04.1); D2 at 09:00 is allowed (AC-04.2); D1 at 09:01 is allowed because the rule is exact time only, with no duration rule.
- Cancelled appointments: a CANCELLED appointment no longer blocks D1 at 09:00, so a new booking there is allowed, and the cancelled one is still findable and listed (BR-05, FR-07).
- Invalid status transitions: cancelling a CANCELLED or COMPLETED appointment gives ValueError and the status does not change (FR-06, BR-06); a status given as the text "scheduled" instead of the enum gives ValueError (BR-08).

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Only asserts the object is not None | Rewrite: assert the returned appointment `is` the stored one and has the expected status, so a wrong or new object fails. |
| 2 | Only asserts the object is not None | Rewrite: assert the exact field values (patient, practitioner, time) and check the store contains it, so the actual requirement is checked. |
| 3 | Asserts True, so it can never fail | Rewrite: assert a specific outcome linked to a criterion, e.g. after a rejected duplicate the original is still stored and unchanged. |
| 4 | Assumes SMS notifications exist, which is an invented requirement (not in revision 2) | Reject; replace with a test of a real requirement, e.g. cancelling keeps the appointment retrievable (AC-05.2). |
| 5 | Also assumes SMS notifications, an invented requirement that would need mocking a service that does not exist | Reject; replace with a real criterion, e.g. same practitioner and same time is rejected while another practitioner is allowed (AC-04.1/04.2). |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
Coverage only shows which lines ran during the tests, not whether the tests checked the right result. A test can run every line and then only `assert True` or "is not None", so it passes even when the behaviour is wrong. Coverage also can't show missing requirements (a rule nobody wrote code for), wrong expectations, or untested edge cases where the code runs but the inputs were never unusual.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status                                                         | Supplied or student-authored |
|---|---|---|---|---|---|----------------------------------------------------------------------------------|---|
| FR-01 | AC-01.1 | TEST-S7-07 | Service | test_services.py::test_register_patient_stores_the_patient | Valid patient with new ID is stored and findable (complete service evidence) | Planned, not yet run                                                             | Student |
| FR-01 | AC-01.2 | (supplied) | Service | test_starter.py::test_duplicate_patient_preserves_original | Duplicate "P1" rejected, original kept | Passed at 3c109e0 (30 passed)                                                    | Supplied |
| FR-01, FR-03 | AC-01.2 boundary; BR-02 "practitioner IDs unique" | TEST-S7-08 | Service | test_services.py::test_duplicate_ids_with_spaces_do_not_overwrite | " P1 " and " D1 " rejected after trimming; originals kept unchanged | Planned, not yet run                                                             | Student |
| FR-01, FR-03 | ID contract: "IDs are trimmed, non-blank" | TEST-S7-01 | Domain (partial evidence) | test_domain.py::test_valid_patient_and_practitioner_keep_trimmed_fields | Trimmed IDs stored; names and specialty kept | Planned, not yet run                                                             | Student |
| FR-01, FR-03 | ID contract (blank ID); "required name" / "required specialty" | TEST-S7-02 | Domain (partial evidence) | test_domain.py::test_blank_patient_id_and_required_fields_are_rejected | Blank patient ID (reference intention), spaces-only name and specialty each ValueError | Planned, not yet run                                                             | Student |
| FR-02 | AC-02.1, AC-02.2 | TEST-S6-01 to S6-05 | Service | test_services.py (Stage 6 patient lookup tests) | Known ID same object; unknown LookupError; blank ValueError; trimmed; case-sensitive | Passed at 3c109e0 (30 passed)                                                    | Student (Stage 6) |
| FR-03 (supporting lookup) | "known ID returns stored practitioner" | TEST-S6-06 to S6-09 | Service | test_services.py (Stage 6 practitioner tests) | Lookup contract | Passed at 3c109e0 (30 passed)                                                    | Student (Stage 6) |
| FR-04, FR-08 | AC-03.1, AC-06.1 | (supplied) | Service | test_starter.py::test_registration_and_booking | Stored SCHEDULED appointment linked to the registered objects (is); find_appointment returns the same object; list is exactly [appointment] | Passed at 3c109e0 (30 passed)                                                    | Supplied (already complete, so not duplicated) |
| FR-04 | AC-03.2 | TEST-S7-09 | Service | test_services.py::test_booking_unknown_patient_or_practitioner_stores_nothing | Unknown patient and unknown practitioner each LookupError; nothing stored | Planned, not yet run                                                             | Student |
| FR-04 | BR-04 "real Patient object"; BR-08; date/time contract | TEST-S7-03 | Domain | test_domain.py::test_invalid_appointment_inputs_are_rejected | String patient, time with seconds and text status each ValueError | Planned, not yet run                                                             | Student |
| FR-05 | AC-04.1 | TEST-S7-10 | Service | test_services.py::test_same_practitioner_same_time_is_rejected | ValueError; only the first booking stored, still SCHEDULED | Planned, not yet run                                                             | Student |
| FR-05 | AC-04.2; boundary "exactly the same datetime" | TEST-S7-11 | Service | test_services.py::test_other_practitioner_or_other_minute_is_allowed | D2 at the same time and D1 one minute later both stored | Planned, not yet run                                                             | Student |
| FR-06 | AC-05.1 | TEST-S7-05; TEST-S6-10 | Domain; Service | test_domain.py::test_cancel_changes_status; test_services.py::test_cancel_changes_status_to_cancelled | SCHEDULED becomes CANCELLED | s6 test passed at 3c109e0, s7 Planned, not yet run                               | Student |
| FR-06 | AC-05.3 | TEST-S7-06; TEST-S6-12 (strengthened) | Domain; Service | test_domain.py::test_repeated_cancellation_is_rejected; test_services.py::test_cancelling_twice_is_rejected | Second cancel ValueError, stays CANCELLED, still the same stored object | s6 test passed at 3c109e0, s7 test and strengthened s6 test Planned, not yet run | Student |
| FR-06 | BR-06 "only SCHEDULED" | TEST-S6-13 (strengthened) | Service | test_services.py::test_completed_appointment_cannot_be_cancelled | COMPLETED cannot be cancelled; both appointments still stored | Original passed at 3c109e0 (30 passed); strengthened version planned | Student (Stage 6) |
| FR-07 | AC-05.2 | TEST-S6-11, S6-16 | Service | test_services.py::test_cancelled_appointment_is_kept_in_history, test_cancelled_slot_can_be_booked_again | Cancelled appointment still found and listed; slot freed | Passed at 3c109e0 (30 passed)                                                    | Student (Stage 6) |
| BR-08 | "statuses are SCHEDULED, CANCELLED, COMPLETED" | TEST-S7-04 | Domain | test_domain.py::test_new_appointment_starts_scheduled | Starts SCHEDULED with the exact objects and time | Planned, not yet run                                                             | Student |
| BR-03 | "appointment IDs unique" | TEST-S7-12 | Service | test_services.py::test_duplicate_appointment_id_with_spaces_is_rejected | " A1 " duplicate rejected; original kept | Planned, not yet run                                                             | Student |
| NFR-01 | "invalid operations preserve state" | TEST-S6-03b (strengthened) | Service | test_services.py::test_find_patient_spaces_only_id_raises_value_error | Store unchanged after rejected lookup | Planned, not yet run                                                             | Student |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-S7-08 | FR-01, FR-03 | AC-01.2; BR-02 | Boundary | Register " P1 " after P1 and " D1 " after D1 | ValueError each; both originals still stored, unchanged | Supplied tests only use exactly "P1" and "D1" |
| TEST-S7-09 | FR-04 | AC-03.2 | Negative | Book with unknown patient P9, then unknown practitioner D9 | LookupError each time; nothing stored | Supplied test only tries an unknown patient; this adds the practitioner side |
| TEST-S7-10 | FR-05 | AC-04.1 | Negative | Book D1 at 09:00 twice | ValueError; list is only the first; first still SCHEDULED | Supplied test checks the error only; this checks state after rejection |
| TEST-S7-11 | FR-05 | AC-04.2; "exact datetime" | Positive / Boundary | Book D2 at the same time, then D1 at 09:01 | Both stored | Same patient twice shows no invented patient-conflict rule; 09:01 shows no invented duration rule |
| TEST-S7-12 | FR-05 / BR-03 | "appointment IDs unique" | Boundary | Book " A1 " when A1 exists | ValueError; original time kept | Supplied test only uses exactly "A1" |
| TEST-S7-03 | FR-04 | BR-04, BR-08, date/time contract | Negative | Create Appointment with "P1" text, 09:00:30, status "scheduled" | ValueError each | Supplied tests never try invalid appointment inputs |
| TEST-S7-02 | FR-01 | ID contract | Negative | Patient("   ", name), then spaces-only name and specialty | ValueError each | Reference intention: blank patient ID rejected; supplied only uses "" for specialty |
| TEST-S7-04 | FR-04 / BR-08 | Initial status | Positive | Create an Appointment | SCHEDULED with the exact objects and time | Reference intention: new appointment starts SCHEDULED |
| TEST-S7-05 | FR-06 | AC-05.1 | Positive | Cancel a new appointment at domain level | CANCELLED | Reference intention: cancellation changes status |
| TEST-S7-06 | FR-06 | AC-05.3 | Negative | Cancel twice at domain level | ValueError; stays CANCELLED | Reference intention: repeated cancellation rejected |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
Verification asks "are we building the product right?", i.e. does the code meet the stated requirements and acceptance criteria.

2. What question does validation answer?
Validation asks "are we building the right product?", i.e. do the requirements actually meet what the clinic and its users need.

3. What is a unit test?
A small automated test that checks one piece of behaviour of one unit (e.g. one class or method) on its own, such as Appointment.cancel() rejecting a second cancel.

4. What is a pytest fixture?
A reusable piece of setup that pytest gives to a test (marked with @pytest.fixture), such as a fresh data store. We used plain helper functions instead, which do the same job for us.

5. What is parametrisation in pytest?
Running the same test function several times with different inputs using @pytest.mark.parametrize, e.g. "", "   " and None as bad IDs. We did not use it, where several inputs break the same rule we check each with its own pytest.raises inside one test, which is easier for us to read.

6. What is regression testing?
Rerunning all the existing tests after any change to check that nothing that used to work has broken. We keep every test from earlier stages for this.

7. What does code coverage tell us, and what does it not prove?
Coverage shows which lines of code ran during the tests. It does not prove the tests checked the right results, that all requirements are tested, or that edge cases are covered.

8. What makes an assertion weak?
An assertion is weak when it would still pass if the behaviour were wrong, e.g. assert True, "is not None", or len(x) > 0, or when it checks something unrelated to the requirement.

9. What is the appropriate role of GitHub Copilot as a test assistant?
To suggest candidate test ideas after we have planned our own. Every candidate must be checked against the requirement and could be weak or invent requirements, so we Accept, Modify or Reject it with a reason and only trust a test after running it ourselves.

10. What is the Stage 7 engineering rule?
Every test must trace to a requirement or contract, assert the required observable behaviour (identity, value, state or exact error), set up its own fresh data, and be run and reported honestly, keeping all earlier tests as a regression suite.

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
