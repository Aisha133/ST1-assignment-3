GitHub Copilot Chat (github.com, PR #16 context), 08/11/2026 5:10. Prompt: Stage 9 handout section 8 plus contracts and test evidence. Response pasted verbatim below.

Act as a query and console integration reviewer for SmartCare.

   Review the supplied code and tests for:
   1. explicit inputs, purity and source non-mutation;
   2. domain, service, data-store and console responsibilities;
   3. validation and recovery without partial state changes;
   4. correct object identity, enum filtering and ordering;
   5. retained history and integrity risks;
   6. missing query, workflow and console tests.

   Do not redesign the domain or add storage/frameworks.
   Do not invent fields or requirements or delete cancelled history.
   Separate observed evidence from optional improvements.
   Rank findings as Critical, Important or Optional.
   For each finding, identify the code/test evidence to check.

   Current contracts: select_appointments(appointments, practitioner_id, status=None) returns a new list for that practitioner, None = all statuses, ordered by appointment_sort_key = (date_time, appointment_id), with no mutation or I/O. list_practitioner_appointments raises ValueError for a blank ID, LookupError for an unknown ID, ValueError for a non-AppointmentStatus status, and returns [] for a known practitioner with no matches. The console converts status text to the enum (blank = all), keeps one store per session, and reports ValueError/LookupError and continues. Session-only data; cancelling keeps history.

   Test evidence: python -m pytest -q from project/ gives 56 passed. Mutation checks: in-place sort fails TEST-S9-03..06; passing the raw ID fails TEST-S9-09; a conflict check that ignores status fails TEST-S9-10; catching only ValueError fails TEST-S9-12.

   Review pull request https://github.com/Aisha133/ST1-assignment-3/pull/16 (branch feature/stage9-queries), focusing on project/smartcare/queries.py, services.py (list_practitioner_appointments), console.py (run_menu) and project/tests/test_queries.py, test_workflows.py.


Gathered additional information and 1 other tool call

Using results of get file and 4 other tool calls

Results of /repos/Aisha133/ST1-assignment-3/pulls/16/files and 2 other tool calls

View file project/smartcare/data_store.py
Assessment: No Critical or Important findings. The implementation matches the stated contracts on the reviewed paths, and the reported 56 passing tests and mutation checks support that assessment. I did not independently run the suite.

Observed evidence
Query purity and ordering: select_appointments builds a separate selection and returns it sorted by the named (date_time, appointment_id) key. Status comparison uses enum identity, and the function performs no I/O or store access.
Service boundary and validation: list_practitioner_appointments resolves the practitioner through the store, rejects unknown practitioners and non-enum statuses, and passes the registered practitioner’s canonical ID to the query. The store lookup also rejects blank IDs.
Console responsibilities and recovery: parse_status and run_menu handle text-to-enum conversion; run_menu keeps one store and service set for the session, delegates operations, and catches ValueError/LookupError to continue.
State and history: The listing path filters results without modifying stored appointments. The tests check canceled appointments remain findable and included by default, while scheduled-only listing excludes them: test_workflows.py. The integrated workflow also checks rejected bookings leave the appointment list unchanged and that cancellation allows rebooking the slot: test_workflows.py.
Test coverage: Query tests cover practitioner and status filtering, time/ID ordering, source-list and object-field non-mutation, and distinct result lists: test_queries.py. Service and console tests cover empty, unknown, blank, invalid-status, history, workflow, and recovery cases. The supplied mutation results target the key risks in sorting, canonical IDs, conflict status, and console exception handling.
Optional coverage improvements
These are test-strengthening suggestions, not observed implementation defects.

Optional — identity coverage: test_always_returns_a_new_list checks identity for one returned appointment, but not every result element. Consider asserting each selected result is the corresponding original Appointment object, so the query’s object-identity contract is fully pinned.
Optional — console status parsing coverage: The menu tests exercise blank, lowercase scheduled, and invalid status text, but not whitespace/case normalization or the cancelled and completed choices. Consider adding inputs for those cases at test_workflows.py.
Merge-readiness: Low risk on the requested scope; no blocking code findings. The reported mutation checks are useful evidence that the regression tests detect the identified failure modes.