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
| | | | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
