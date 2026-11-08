# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Group 3, Tuesday 1:30pm Tutorial (Aisha @Aisha133, Hannah @Hannah-448, Anastasia @Ajorja, Benjamin @Benjamin316-uc; all UG)
Members and responsibilities:  Aisha: pure query and sort key (#12), tutorial answers (A) and formative answers (G); Hannah: service listing (#13), tutorial answers (A) and formative answers (G); Anastasia: workflow test (#14), console/main/README (#15), demos and Copilot review; Benjamin: created issues #14 and #15, PR review; all: design discussion (B) and integrated check. All commits are made on Anastasia's laptop, each with the turn owner's own --author.
Stage 8 integrated SHA, command, working directory and actual result: Stage 8 code bb8d8257bfe18aac918d721f5c048efe40aa9749 (record 1d4d572b5bd428304e6c4578bad8204ccaffc0e3); python -m pytest -q, project/, 44 passed at 1d4d572.

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Domain | Patient identity is needed to identify patients throughout the session. It is also useful if a patient makes another booking. |
| Appointment history | Domain | Appointment history is stored within the data store for the rest of the session, including cancelled appointments (FR-07). |
| Temporary menu choice | Transient | It is only present when the menu itself is in use. |
| Practitioner specialty | Domain | Required practitioner data (FR-03); it is stored and displayed, but no booking rule uses it. |
| Debug print output | Transient | Is only in use during the debugging process if an issue has presented itself. |
| Appointment status | Domain | Is retained to track the appointment and whether it is still scheduled or has been cancelled. |

What is intentionally lost on exit?  Everything in the SmartCareDataStore (all patients, practitioners and appointments, including cancelled history) and any transient menu input. SmartCare is session-only, so a new launch starts with an empty store.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str]: (date_time, appointment_id) | The appointment_sort_key extracts the values that are used to sort the appointments. | Uses the existing Appointment date_time and appointment_id attributes. |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus or None (default None) | A new list[Appointment] of the selected appointments, sorted by appointment_sort_key | Filters through appointments without changing the original list or objects; no validation, input or output (it trusts its inputs). | Uses existing appointment attributes; None means every status. |
| Service listing | list_practitioner_appointments(practitioner_id: str, status: AppointmentStatus or None) | A new list[Appointment] | Checks the practitioner exists (blank ID ValueError, unknown ID LookupError) and that status is an AppointmentStatus (otherwise ValueError), then calls the query on data_store.list_appointments(). | Uses the existing store lookup and the registered practitioner's ID. |
| Console | (string) user input. | Printed messages (string) | Handles the inputs and outputs and human interaction: parses date/time and status text, calls the services and reports ValueError/LookupError without crashing. | Communicates with the service layer; reuses parse_date_time and format_appointment. |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: 
- Practitioner: Practitioner ID and name identifies the practitioner, while specialty describes the practitioner; it is stored and displayed, but no booking rule uses it.
- Patient: patient ID and name is used to identify the patients.
- Appointment: Appointment ID is used to identify the appointment, the actual participants identifies who has the appointment, and date_time/status identifies when the appointment is and if it is still active.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | The domain logic handles the user interaction. | The console should collect the user's input and call the service; the service calls Appointment.cancel(), which only enforces the rule. |
| Service prints/reads the menu | The service layer handles the user interaction and presentation. | The console should manage the user inputs and the menus. |
| Query sorts its source in place | Query unexpectedly modifies stored data. | The query should release an output that is the sorted result without changing any of the original information. |
| Store prints Appointment saved | Storage layer handles presentation. | The store should just store and return the object, or raise an error; the console decides what message to show. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check:

For `appointments.sort(key=appointment_sort_key)`:
- Sorts the appointments in place.
- Returns None.
- The original list is modified.

For `sorted(appointments, key=appointment_sort_key)`:
- Creates and returns a new sorted list.
- The source list keeps its original order.
- The two different lists have different identities.

Meaningful mutation check: Temporarily change select_appointments to sort the source list in place (`appointments.sort(key=appointment_sort_key)`) instead of returning `sorted(...)`, then rerun the query tests. TEST-S9-04 must fail because the saved copy of the source order no longer matches the list after the call. Undo the change and confirm the tests pass again.

Score-example prediction and explanation of passing the named key: The key=appointment_sort_key block tells Python which function must be used in order to decide the order of the appointments. Python will then use the values returned by that function to compare the different orders and sort the appointments as they should be.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: 

Cancellation vs deletion: Cancellation keeps the appointment in the store and only changes its status to CANCELLED, so it stays findable and listed. Deletion removes the record entirely, which would destroy history and is not allowed.

Checks:
- Same-session lookup: After booking and cancelling A1, data_store.find_appointment('A1') and appointment_service.find_appointment('A1') must both return the same Appointment object with status CANCELLED. The F8-02 repair restored this by removing the `status.value != "cancelled"` condition.
- All-status listing: list_appointments() after cancelling must still contain the cancelled appointment.
- SCHEDULED-only exclusion: select_appointments with status=AppointmentStatus.SCHEDULED must exclude the cancelled appointment, returning [], without removing it from the store. This will prove the exclusion is a filter on the result, not a deletion.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: 
- The query stays pure: it takes the list, practitioner ID and status as arguments, uses loops and the named key, and returns sorted(...) of a new list; it never sorts or changes its argument, reads input, prints or touches the store.
- Validation lives in the service, not the query: the service checks the practitioner through data_store.find_practitioner (ValueError blank, LookupError unknown) and that status is an AppointmentStatus or None, then passes the registered practitioner's ID so " D1 " still matches.
- Text-to-enum conversion happens only in the console (blank = all; scheduled/cancelled/completed; anything else ValueError).
- One store and one set of services for the whole menu session; the console catches only ValueError and LookupError, prints them and continues, so expected errors never crash or partly change records.
- Equal-time tie-break test uses CANCELLED/COMPLETED appointments sharing 09:00 so no SCHEDULED conflict rule is broken.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | D1 and D2 appointments | select_appointments (query) | Only D1's; D2's A4 excluded | TEST-S9-02 |
| QRY-02 | D1 with SCHEDULED, CANCELLED, COMPLETED | select_appointments with None / each enum | None = all three; each enum only its own; no match [] | TEST-S9-03 |
| QRY-03 | unsorted, two at 09:00 (A2, A3) and one at 10:00 | select_appointments + appointment_sort_key | [A2, A3, A1]; source order and fields unchanged | TEST-S9-04 |
| FP-01 | same inputs twice | select_appointments | identical results; source unchanged; code has no globals/I/O | TEST-S9-05; code inspection |
| FP-02 | empty, already-sorted, unsorted lists | select_appointments | always a distinct new list; same unchanged objects | TEST-S9-06 |
| FP-03 | one appointment | appointment_sort_key | (date_time, appointment_id); sorting uses it | TEST-S9-01, S9-04 |
| QRY-04 known/empty | D2 with no appointments; D1 with no CANCELLED | list_practitioner_appointments (service) | [] with no error | TEST-S9-07 |
| QRY-04 unknown/invalid | 'D9'; '   '; status 'scheduled' (text) | list_practitioner_appointments | LookupError; ValueError; ValueError; store unchanged | TEST-S9-08 |
| QRY-04 omitted status, FR-07 | A1 booked then cancelled; ' D1 ' | list_practitioner_appointments | [A1] (same object) with all statuses; [] for SCHEDULED; still findable | TEST-S9-09 |
| FR-01–FR-08 integrated | P1, D1, D2 | services workflow | conflict rejected with no change; unknown participant rejected; D2 allowed; cancel keeps history; filter; freed slot rebooked; failed booking does not reserve its ID | TEST-S9-10 |
| UI-01 | menu inputs in stage09/evidence/ui01_input.txt | run_menu (console) | each step succeeds or is rejected as specified; exit discards data | TEST-S9-11; ui01 output |
| UI-02 | menu inputs in stage09/evidence/ui02_input.txt | run_menu (console) | each bad input reported; records unchanged; next action succeeds | TEST-S9-12; ui02 output |


Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection:
Empty means a known practitioner simply has no matching appointments, so the result is [] with no error. Unknown means a valid ID that is not registered (LookupError). Invalid means the input itself is wrong: a blank ID or a status that is not an AppointmentStatus (ValueError), which must not be mistaken for "no matches". The console converts status text to the enum; direct service callers must pass the enum or None. Results contain the actual stored Appointment objects (checked with `is`), not copies. Errors are raised by the domain/store/services and reported by the console; tests check the stored lists are unchanged after every rejection.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| TEST-S9-01 / FP-03 | queries.py `appointment_sort_key`; tests/test_queries.py `test_sort_key_is_date_time_then_id` | Key returns `(date_time, appointment_id)`; the appointment is unchanged | Passed | 581e065 |
| TEST-S9-02 / QRY-01 | queries.py `select_appointments`; `test_only_the_requested_practitioner_is_selected` | Practitioner isolation: D2's A4 is not in D1's result; D2 gives `[A4]` | Passed | 581e065 |
| TEST-S9-03 / QRY-02 | `select_appointments`; `test_default_is_all_statuses_and_each_status_filters` | Default None gives all three D1 statuses; each enum gives only its own; no match gives `[]` | Passed | 581e065 |
| TEST-S9-04 / QRY-03, FP-03 | `select_appointments`; `test_sorted_by_time_then_id_without_changing_the_source` | Source `[A1, A3, A4, A2]` gives `[A2, A3, A1]`: 09:00 before 10:00 and equal-time ID tie-break (A2 before A3); the named key is reused to check order; source order and fields unchanged | Passed. Mutation (sort the source in place, return it): 4 failed, 2 passed (S9-03..06); restored, 50 passed | 581e065 |
| TEST-S9-05 / FP-01 | `select_appointments`; `test_repeated_calls_give_the_same_result` | Two calls with the same input give the same list; source unchanged after both | Passed | 581e065 |
| TEST-S9-06 / FP-02 | `select_appointments`; `test_always_returns_a_new_list` | Empty, already-sorted and unsorted inputs each give a distinct new list holding the same unchanged objects | Passed | 581e065 |
| TEST-S9-07 / QRY-04 | services.py `AppointmentService.list_practitioner_appointments`; tests/test_workflows.py `test_known_practitioner_with_no_matches_gives_an_empty_list` | Known-empty: D2 with no appointments and D1 with no CANCELLED both give `[]`, no error | Passed | 79ed388 |
| TEST-S9-08 / QRY-04 | `list_practitioner_appointments`; `test_unknown_blank_and_invalid_status_are_errors_not_empty` | Unknown `'D9'` is LookupError; blank `'   '` is ValueError; text status `'scheduled'` is ValueError; stored list still `[A1]` | Passed | 79ed388 |
| TEST-S9-09 / QRY-04, FR-07 | `list_practitioner_appointments`; `test_listing_keeps_history_and_uses_the_registered_id` | Retained history: cancelled A1 is listed by default as the same object (`is`), excluded by SCHEDULED, still findable; `' D1 '` uses the registered ID | Passed. Mutation (pass the raw ID): 1 failed, 2 passed (S9-09); restored, 53 passed | 79ed388 |
| TEST-S9-10 / FR-01–FR-08 | services workflow; `test_full_booking_workflow_through_the_services` | Conflict and unknown patient rejected with the list unchanged; D2 allowed at the same time; cancel keeps A1; filter; freed slot rebooked as A3; failed booking did not reserve A9 | Passed. Mutation (conflict check ignores status): 2 failed, 52 passed (S6-16 and S9-10); restored, 54 passed | baa7910 |
| TEST-S9-11 / UI-01 | console.py `run_menu`; `test_console_ui01_main_workflow` | The real menu runs the published reference sequence; key messages, final order A1 then A3, "2 appointments found." and normal exit | Passed | ae59ddb |
| TEST-S9-12 / UI-02 | `run_menu`; `test_console_ui02_recovers_from_bad_input` | Every bad input is reported and the menu continues; P1 is found afterwards | Passed. Mutation (catch only ValueError): 1 failed, 5 passed (uncaught LookupError on 'P9'); restored, 56 passed | ae59ddb |
| TEST-S9-13 / UI-02, QRY-02 | console.py `parse_status`; `test_parse_status_accepts_every_status_and_blank` | Blank and spaces give None; `' Scheduled '`, `'CANCELLED'`, `'completed'` give their enums; `'pending'` is ValueError (added after Copilot review) | Passed. Mutation (no strip/lower): 1 failed, 56 passed (S9-13 only); restored, 57 passed | c06c739 |

Full suite on integrated main 6f4df00: `python -m pytest -q` from project/ gave 57 passed (44 earlier and 13 Stage 9).

Purity explanation from code inspection, including absence of hidden state and I/O: `select_appointments` uses only its three arguments. It reads no global or module variable, does not touch the data store, and has no `input()`/`print()`. It appends matches to a local `selected` list and returns `sorted(selected, key=appointment_sort_key)`, so the caller's list is never reordered and no Appointment attribute is assigned. `appointment_sort_key` only reads two attributes and returns a tuple. The same inputs therefore always give the same output with no side effects (TEST-S9-04/05/06 and the in-place-sort mutation).

What the tests do and do not establish: They establish the query and service contracts, retained cancelled history, unchanged stored lists after each rejection, and that the real `run_menu` handles the UI-01 and UI-02 sequences. Each key rule is backed by a mutation that made a named test fail. They do not establish behaviour beyond the inputs used. Console tests replace `input()` with a fake, and the demonstrations use piped input rather than live typing. Nothing is tested across sessions because there is no persistence. COMPLETED appointments exist only when created directly in tests, since no feature completes an appointment. Performance with large lists is not tested.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | stage09/evidence/ui01_input.txt, run from project/ with `Get-Content ..\stage09\evidence\ui01_input.txt \| python main.py --interactive` (mirrors the published Final Console Demonstration run) | Register/find P1, D1, D2; book A1; reject A-CONFLICT; book A2 with D2; list D1; cancel A1; find A1 as Cancelled; list all; SCHEDULED-only empty; book A3 in the freed slot; list A1 and A3; unknown choice; exit | As expected. Conflict reported as "Error: Practitioner already has a SCHEDULED appointment at this time" and D1 still listed only A1. After cancelling, A1 was found as Cancelled and still listed (1 found). Scheduled filter: "No appointments found." A3 booked at the same time. Final list "1. A1 (Cancelled), 2. A3 (Scheduled), 2 appointments found." 99 gave "Unknown choice. Choose a number from 0 to 8."; exit gave "Goodbye. Session data discarded." | stage09/evidence/ui01_output.txt (b6a0292); TEST-S9-11 |
| UI-02 invalid-input recovery | stage09/evidence/ui02_input.txt, same command | Each bad input reported, records unchanged, next action succeeds | As expected: 9 errors plus 1 unknown choice. Unknown choice 99; unknown P9; blank ID; duplicate P1 (first P1 kept); unknown patient in a booking; "not a date"; impossible 2026-02-30; unknown appointment; repeated cancel of A1 ("Only SCHEDULED appointments may be cancelled", A1 stays Cancelled); status "pending". A1 booked successfully after three rejected attempts with the same ID (so they did not reserve it), and "Patient found. P1: Alex Example" afterwards; normal exit | stage09/evidence/ui02_output.txt (b6a0292); TEST-S9-12, TEST-S9-13 |
| Automated service workflow | tests/test_workflows.py TEST-S9-10, fresh store with P1, D1, D2 | FR-01–FR-08 integrated through the services | Passed. `data_store.list_appointments()` checked as `[A1]` after each rejected booking and as `[A1, A2, A3, A9]` at the end | baa7910 |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Record A and B committed in a067a67 (08/11/2026, about 13:19), before the Copilot request (08/11/2026, about 17:05; the response was saved by 17:07).
Actual prompt/context supplied: The Stage 9 handout section 8 prompt, plus the current contracts and test and mutation evidence, sent to GitHub Copilot Chat (github.com) with PR #16 as context. Recorded verbatim in stage09/evidence/copilot_review.md (c09ad32).
Actual response: stage09/evidence/copilot_review.md (c09ad32). It found no Critical or Important findings and gave two Optional test suggestions. Copilot stated that it did not run the suite.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| No Critical/Important defects; query pure, canonical ID used, console catches only ValueError/LookupError | queries.py, services.py, console.py; TEST-S9-01..12 | (overall) | Accept as consistent with our own evidence, but not treated as proof: Copilot did not run anything | No change | Our own run: 56 passed at b6a0292, plus four mutations that each failed the expected tests |
| Identity checked for only one result element (`unsorted_result[0] is a2`) | test_queries.py; domain.py Appointment has no `__eq__` | Optional | Reject. Partly incorrect: without `__eq__`, `result == [a2, a3, a1]` in S9-03/04/05 already compares every element by identity, so extra checks would be redundant | No change | Temporarily made the query return copies: 5 failed, 1 passed in test_queries.py; restored |
| Console status parsing not tested for spaces/case or cancelled/completed | console.py `parse_status`; menu tests only typed `''`, `'scheduled'`, `'pending'` | Optional | Modify. Correct gap, but a small direct unit test is clearer than the suggested extra full menu runs | Added TEST-S9-13 (c06c739) | 57 passed; removing `.strip().lower()` failed only S9-13 (1 failed, 56 passed); restored, 57 passed |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: Domain invariants stay in domain.py: only a SCHEDULED appointment can be cancelled, and cancelling changes status without deleting. The shared SmartCareDataStore only stores, finds and lists records and returns None when absent. The services coordinate: they validate IDs and the status type, turn None into LookupError, apply the conflict rule, and pass the registered ID to the query. The pure query only filters and sorts the list it is given. The console handles all input/output: it converts text to dates and enums, calls services, prints results and reports ValueError/LookupError. No layer prints from inside the domain/store/service, and the query never reads input or the store.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? Where each responsibility lives across one shared session. The menu must create one store and one set of services for the whole run, or a booking made at option 5 would not exist at option 8. Validation sits in the service, not the pure query, so the query can trust its inputs and stay pure. Text-to-enum conversion happens only at the console boundary. The service must pass the registered practitioner ID rather than the raw input (TEST-S9-09 failed when this was broken).
2. Which Copilot suggestion did you reject as over-engineering, and why? Copilot made no large redesign suggestion. The suggestion we rejected was adding identity checks for every result element: our existing equality checks already compare identity (the copy mutation failed 5 of 6 query tests), so it added code without new protection. We also scaled down its second suggestion from extra full menu runs to one direct `parse_status` test (Modify).
3. How did you prove cancelled appointments remain retrievable and listable in the same session? TEST-S9-09 cancels A1 and then checks that the default listing returns the same object, SCHEDULED-only excludes it, `find_appointment('A1')` still returns it and the store still lists it. TEST-S9-10 and the UI-01 output show A1 found as Cancelled and listed beside the new A3 in the freed slot. The Stage 8 F8-02 regression test still passes.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? It only uses the arguments it is given, it has no input(), print() or store access, and it builds a separate list and returns sorted(...), so the caller's list and the Appointment objects are not changed. The same inputs always give the same result. Sorting the source list in place with appointments.sort(...) would break purity, because the caller's list is changed (our mutation check made TEST-S9-03 to S9-06 fail). Printing, reading input or changing an appointment's status inside the query would also break it.
2. Which explicit inputs are needed, and why avoid a global store? It needs the list of appointments, the practitioner ID and the optional status (None means all). Passing them in makes the function easy to test with small made-up lists and means it can't depend on hidden data. A global store would make results depend on whatever happened earlier, so the same call could give different answers and tests could affect each other.
3. How can a new list reuse Appointment objects safely? The new list holds references to the same stored Appointment objects, not copies, so a listed appointment is the real record (checked with "is" in TEST-S9-09). This is safe because the query only reads the objects and never changes them, and any change such as cancelling still has to go through the service and Appointment.cancel().
4. Why use a named key, and what breaks equal-time ties? appointment_sort_key gives one clear definition of the order, (date_time, appointment_id), that can be reused and tested on its own (TEST-S9-01). The appointment ID breaks ties, so two appointments at 09:00 are ordered A2 then A3 every time (TEST-S9-04), instead of depending on the order they were stored in.
5. How do default and explicit status filters differ? The default, status=None, returns every status, so cancelled history is still listed. An explicit AppointmentStatus such as SCHEDULED returns only appointments with that status, so a cancelled appointment is left out of the result but is not removed from the store (TEST-S9-03, S9-09).
6. How do empty, unknown practitioner and invalid filter cases differ? Empty means the practitioner is registered but has no matching appointments, so the result is [] with no error (TEST-S9-07). Unknown means the ID is not registered, so a LookupError is raised. Invalid means the input itself is wrong: a blank ID or a status that is not an AppointmentStatus raises ValueError (TEST-S9-08). Keeping them separate means a typo is never mistaken for "no appointments".
7. Which console errors recover, and how is unchanged state checked? The console catches ValueError and LookupError: unknown or blank IDs, duplicates, unknown participants, bad or impossible dates, conflicts, repeated cancellation and invalid status. It prints the error and shows the menu again (ui02_output.txt, TEST-S9-12); other errors are not caught, so real bugs are not hidden. Unchanged state is checked by comparing the stored list after each rejection (TEST-S9-08, S9-10) and by doing a successful action afterwards, such as booking A1 after three failed attempts with that ID and finding P1 at the end.
8. What is data integrity for registered participants, conflicts and history? Data integrity means the stored data always follows the rules.
   - Registered participants: An appointment can only be booked for a patient and practitioner that are registered. Otherwise book_appointment raises LookupError.
   - Conflicts: The same practitioner cannot have two SCHEDULED appointments at the exact same time. A different practitioner at that time is allowed.
   - History: Cancelled appointments stay in the store and can still be found and listed.
   - A rejected action changes nothing: after a conflict or unknown patient, the stored list is unchanged (TEST-S9-10).
9. What is Copilot's review role, and who verifies findings? Copilot only suggests possible causes and issues and the team verifies each finding against evidence before accepting, modifying or rejecting it. Copilot cannot approve the PR; that was Benjamin's human review. In our review we rejected one Copilot suggestion and modified the other after testing them.
10. How do pure functions and OOP responsibilities work together? Classes own state and rules. The store holds records, services enforce rules, domain objects guard their own behaviour. While pure functions do stateless filtering and sorting on data the service passes in and return a new result without changing anything. The console only collects input and prints results; it calls services and never decides the rules itself.

## H. Review, completion and common handover

Issues and bounded branches: Issues #12 (query, Aisha), #13 (service listing, Hannah), #14 (workflow test, Anastasia) and #15 (console/README/demos, Anastasia), all closed by PR #16. Branch feature/stage9-queries, kept after merge.
PR/diff and another-member human reviewer: https://github.com/Aisha133/ST1-assignment-3/pull/16. Reviewer Benjamin (@Benjamin316-uc): reviewed at c06c739 and requested the README verification result (https://github.com/Aisha133/ST1-assignment-3/pull/16#pullrequestreview-5816921128); re-reviewed and approved at 0de9339: https://github.com/Aisha133/ST1-assignment-3/pull/16#pullrequestreview-5816959762
Review responses and Copilot comparison: Reply to Benjamin's README comment linking the fix 0de9339 (resolved). Copilot comparison comment: https://github.com/Aisha133/ST1-assignment-3/pull/16#issuecomment-6718457885. Copilot response: stage09/evidence/copilot_review.md.
Integrated common Stage 9 SHA: 6f4df006ff4c7bf86f58567b33d9deb32c1f6d12 (merge of PR #16 into main)
Full regression command, working directory, actual count/result and evidence: `python -m pytest -q` from project/ on main at 6f4df00: 57 passed (08/11/2026, Windows, Python 3.14.7, pytest 8.3.5)
README run instructions and scope/limitations: project/README.md (Run commands, Verification, Interactive menu, Scope and limitations, Behaviour notes)
Unresolved issues and support/action: No failing tests or open defects. Known limitations are documented in the README: session-only data, and no feature to mark an appointment COMPLETED. Minor tidy-up: the docstrings for `find_appointment` and `has_practitioner_conflict` in data_store.py were lost during Stage 8 and are not yet restored (no behaviour impact).
UG common candidate / PG future branch plan: All-UG group. 6f4df00 on main is the protected common candidate for Stage 12. No PG Stage 10/11 work.

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated.
- [x] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [x] Human design, Copilot critique, review and integration recorded honestly.
- [x] Reflections and ten formative responses completed.
- [x] README updated; earlier code/tests/records preserved.
- [x] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
