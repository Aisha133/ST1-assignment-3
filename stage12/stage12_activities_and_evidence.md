# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 3, Tuesday 1:30pm Tutorial
Members and UG/PG applicability: Aisha (@Aisha133), Hannah (@Hannah-448), Anastasia (@AJorja), Benjamin (@Benjamin316-uc); all UG. Common scope only; Stages 10–11 are not applicable and their templates are retained unchanged.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare v1.0 (UG common scope); SmartCare A3 2026 revision 2 (FR-01–FR-09, QRY-01–04, FP-01–03, UI-01/02; FR-10 retired).
Common starting SHA / branch / applicable members: ea0f2fe1dcb05e5121b4b95475043ef7e5b7542e on main (Stage 9 record; code at 6f4df006ff4c7bf86f58567b33d9deb32c1f6d12, merge of PR #16); all four members.
PG starting SHA / branch / applicable members or not applicable: Not applicable (all-UG group).
Working-state review and approved integration: On 09/11/2026, from the repository root: `git status --short`, `git diff` and `git diff --cached` printed nothing; `git rev-parse HEAD` gave ea0f2fe…; branches main, debug/stage08 and feature/stage9-queries (both merged and kept). No unreviewed local work. The only Stage 12 changes are the reviewed release corrections in issue #17 / PR #18.
Protected common candidate and PG differences: The Stage 9 common checkpoint 6f4df00 stays recoverable in history. The release candidate is 82c9ad67ab5a99e8147353e281953368ede10f31, the merge of PR #18; no PG differences.
Feature freeze / owner / verifier: Feature freeze from the start of Stage 12 (09/11/2026): no new features, only behaviour-preserving quality fixes and README/evidence. Owner: Anastasia (release integration). Verifiers: Aisha (PR #18 review) and Benjamin (fresh-copy run).


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: Release with conditions (all four members agreed). Passing tests only check the code: they do not show that someone else can set it up from the README, that the dependency is safe, or that users know the limitation. Before sign-off the README setup must be completed and checked by another person, the dependency's source and licence reviewed, and the limitation documented, then rechecked. Our own release followed this: all 57 tests passed, but Aisha's review found the README had no venv commands and Ben's fresh copy hit the PowerShell block, so we fixed and rechecked before signing off. Plain "Release" was rejected because passing tests are not enough.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | TEST-S9-09 (cancelled A1 listed by default as the same object, excluded by SCHEDULED, still findable); TEST-S9-10; REG-F8-02; release UI-01 run | tests/test_workflows.py, tests/test_regressions.py; stage12/evidence/release_ui01_output.txt (run on 82c9ad6) | Benjamin (PR #16); Aisha (PR #18) | Yes: tests assert identity and status, not just "no error" | None |
| Architecture responsibilities are appropriate | Code inspection (E); README Structure; TEST-S9-12 mutation (console catching only ValueError) | project/smartcare/*.py; project/README.md at 82c9ad6 | Aisha (PR #18) | Yes for this scope: inspection plus tests; responsibility is a design claim, not something a test fully proves | None |
| Rescheduling is safe — PG only | Not applicable (all-UG group) | — | — | — | — |
| AI use is responsible — common recheck / PG assurance | Copilot decisions recorded in Stage 6–9 records; stage09/evidence/copilot_review.md; Stage 12 E recheck | stage09 record E; stage12 record E | Whole group (E recheck) | Partly: Copilot evidence is complete for Stage 9; earlier stages record decisions| Disclosed in README and here (E) |
| System is maintainable | README structure/commands; 57 named, requirement-linked tests; focused modules; Stage 12 quality fixes | project/README.md; project/tests; PR #18 | Aisha (PR #18) | Yes for course scope | Technical debt listed in G |
| FR-01–03 register/find and validation | Stage 6/7 service and domain tests (duplicates, blank IDs, unknown lookups) | tests/test_services.py, tests/test_domain.py | Stage 6–7 commit-page reviews (see those records) | Yes | None |
| FR-04–05 booking/conflict rules | Stage 6/7 booking tests; REG-F8-01; TEST-S9-10; release UI-01 conflict step | tests/test_services.py, tests/test_regressions.py, tests/test_workflows.py | Benjamin (PR #11, #16) | Yes | None |
| FR-06–08 cancellation/history/find | Stage 6/7 cancel tests; REG-F8-02; TEST-S9-09/10; UI-02 repeated cancel | as above | Benjamin (PR #11, #16) | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | TEST-S9-01..09 with four mutation checks | tests/test_queries.py, tests/test_workflows.py; stage09 record C | Benjamin (PR #16) | Yes | None |
| UI full console sequence and error recovery | TEST-S9-11/12/13; release UI-01 and UI-02 runs | stage12/evidence/ (run on 82c9ad6) | Aisha (PR #18) | Yes | None |
| Session-only scope / FR-10 retired | README Scope and limitations; UI-01 exit message; no storage code | project/README.md | Aisha (PR #18) | Yes: deliberate scope limit | None |
| PG RES and assurance integration | Not applicable (all-UG group) | — | — | — | — |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Windows, Python 3.14.7, pytest 8.3.5 (.venv) | project/: `python -m pip install -r requirements-dev.txt`; `python main.py`; `python -m pytest -q` | ea0f2fe (starting state) | 57 passed; demo printed "A1: P1 with DR1, 2026-10-01 09:00, scheduled" | This record, A |
| Complete PG if applicable | Not applicable | — | — | — | — |
| Affected focused checks after correction | Windows, Python 3.14.7, pytest 8.3.5 | project/: `python -m pytest -q tests/test_regressions.py` | 11099fa | 2 passed (REG-F8-02 covers find_appointment) | commit 11099fa |
| Full integrated recheck | Windows, Python 3.14.7, pytest 8.3.5 | project/: `python -m pytest -q` on main after merging PR #18 | 82c9ad67ab5a99e8147353e281953368ede10f31 | 57 passed | https://github.com/Aisha133/ST1-assignment-3/pull/18 |
Prior assertions preserved / reviewed test diff: No test file changed in Stage 12 (PR #18 changes only data_store.py, services.py and the READMEs). All 57 earlier assertions are preserved.
Remaining failure / limitation: None.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | — | A clinic front desk needs to book patients with practitioners without double-booking, and keep cancelled history. Stakeholders: reception staff, practitioners, patients and the clinic manager. | Stated in project/README.md (Purpose) and here; demo owner Anastasia | project/README.md |
| Register and find Patient and two Practitioners | P1 Alex Example; D1 Taylor Example (General practice); D2 Jordan Example (Cardiology) | FR-01–03 | All registered and found with names and IDs | release_ui01_output.txt |
| Valid booking | A1, P1, D1, 2026-10-01 09:00 | FR-04 | "Appointment booked successfully.", status Scheduled | release_ui01_output.txt |
| Same practitioner exact-time conflict rejected | A-CONFLICT, P1, D1, same time | FR-05 | "Error: Practitioner already has a SCHEDULED appointment at this time"; the next D1 list still shows only A1 (no partial appointment) | release_ui01_output.txt |
| Different practitioner same time allowed | A2, P1, D2, same time | FR-05 | Booked, Scheduled | release_ui01_output.txt |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1; find A1 | FR-06–08 | "Appointment cancelled successfully."; A1 found with status Cancelled (same object in TEST-S9-09) | release_ui01_output.txt; TEST-S9-09 |
| Invalid/repeated cancellation rejected | Cancel A1 again; find UNKNOWN | FR-06, FR-08 | "Error: Only SCHEDULED appointments may be cancelled"; "Error: Appointment not found" | release_ui02_output.txt |
| Default all-status listing | List D1, blank filter | FR-09, QRY-02 | Cancelled A1 still listed (1 found) | release_ui01_output.txt |
| Explicit filtering / empty vs unknown / deterministic order | Filter scheduled; list unknown D9 (test); A3 in the freed slot, then list | QRY-02–04 | "No appointments found." for Scheduled; unknown practitioner is LookupError (TEST-S9-08); final list 1. A1, 2. A3 (time then ID); equal-time ties also in TEST-S9-04 | release_ui01_output.txt; TEST-S9-04/08 |
| Invalid date/status/menu/lookup recovery and continued operation | 99; P9; blank ID; "not a date"; 2026-02-30; "pending" | UI-02 | Each reported; P1 found afterwards; menu kept running | release_ui02_output.txt |
| Session-only limitation and normal exit | 0 | Session-only scope | "Goodbye. Session data discarded."; a new launch starts empty (no restart storage) | release_ui01_output.txt |
| One meaningful requirement-linked pytest test explained | `python -m pytest -q tests/test_workflows.py -k history` | FR-07 / QRY-04 | TEST-S9-09 passes; explained: asserts the cancelled A1 is the same object, excluded by SCHEDULED and still findable; it does not prove behaviour for other inputs or across sessions | tests/test_workflows.py (TEST-S9-09); explanation recorded here by Anastasia |
| Architecture and one actual AI decision / known limitation | README Structure; Stage 9 Copilot review | E/N | Copilot's identity suggestion Rejected (copy mutation 5 failed), status-parsing Modified into TEST-S9-13; limitation: no feature to mark COMPLETED, and session-only data | stage09 record E |
| PG reschedule identity/participants/time and no-op | Not applicable | — | — | — |
| PG conflict/invalid status/failure non-mutation | Not applicable | — | — | — |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable | — | — | — |
Stable demo owner / fresh process / command: Anastasia. Fresh process each run, from project/: `Get-Content ..\stage12\evidence\release_ui01_input.txt | python main.py --interactive | Out-File -Encoding utf8 ..\stage12\evidence\release_ui01_output.txt` (and the same for ui02). No live AI or internet needed. The inputs are the Stage 9 UI-01 (published reference run) and UI-02 inputs, rerun on the release candidate.
PG demonstrations through service/tests or not applicable: Not applicable (all-UG group).


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | domain.py, data_store.py, services.py, queries.py, console.py | No finding: entities validate their own fields; Appointment guards cancel; the store only adds/finds/lists; services coordinate and use the shared store; queries are pure with explicit inputs; only console.py reads input or prints (grep: `print(`/`input(` appear only in console.py) | No change |
| PascalCase and snake_case naming | all modules | No finding: classes PascalCase (SmartCareDataStore, AppointmentService), functions/variables snake_case | No change |
| Useful type hints and meaningful docstrings | data_store.py; services.py | Finding: `find_appointment` and `has_practitioner_conflict` had lost their docstrings during Stage 8; `find_patient`/`find_practitioner` docstrings began with leftover "Stage 6" labels | Restored/tidied in 11099fa; 57 passed |
| Four-space indentation and imports/layout | all modules | Finding: `has_practitioner_conflict`'s condition layout and double quotes in `find_appointment` did not match the rest of the file; data_store.py and services.py had no final newline | Restored in 11099fa; final newlines added in 9133b2e, which accidentally re-added the two "Stage 6" docstring labels, re-fixed in 2ee6271; 57 passed |
| Focused methods / duplication / dead or commented code | data_store.py `find_appointment` | Finding: the Stage 8 leftover loop repeated the blank-ID check by hand (duplicating `required_text`) and scanned every appointment instead of a dictionary lookup. A stray `# this is for test` comment in queries.py was removed in Stage 9 (581e065) | Restored to the dictionary lookup with `required_text` (11099fa); behaviour identical (same message, None for unknown, same object); REG-F8-02 2 passed, full 57 passed |
| Globals / leakage / unnecessary inheritance or frameworks | all modules | No finding: only module constants (LINE, MENU) in console.py; no inheritance or frameworks | No change |
| No SQLite/persistence/repository ABCs/speculative features | all modules | No finding | No change |
| Synthetic data / secrets / dependencies / provenance | tests, evidence files, requirements-dev.txt, `git ls-files` | No finding: only synthetic names/IDs (Alex/Taylor/Jordan/Morgan Example); no credentials; .gitignore excludes .venv, caches and .idea; the only dependency is pytest==8.3.5 from PyPI (MIT licence), pulling in colorama, iniconfig, packaging and pluggy as its own dependencies; the Stage 8 utility was never committed | No change |
| Significant common Copilot contributions and human verification | Stage 6–9 records (Copilot sections); stage09/evidence/copilot_review.md | Every recorded Copilot output had a human Accept/Modify/Reject decision checked against code/tests; Copilot never approved a PR | No change |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | — | Not applicable (all-UG group) | — |

| AI claim                                                                                    | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---------------------------------------------------------------------------------------------|---|---|---|---|
| Copilot (Stage 9): no Critical/Important defects in the query, service listing and console  | QRY-01–04, UI-01/02; queries.py, services.py, console.py | Our own run (56 passed) and four mutations that each failed the expected tests; Copilot said it did not run the suite | Accept as consistent, not as proof | No change |
| Copilot (Stage 9): identity is checked for only one result element                          | FP-02; test_queries.py | Appointment has no `__eq__`; a mutation returning copies failed 5 of 6 query tests | Reject: already covered | No change |
| Copilot (Stage 9): console status parsing is not tested for spaces/case/cancelled/completed | UI-02, QRY-02; console.py parse_status | Checked the menu tests' inputs; confirmed the gap | Modify: one direct unit test instead of extra menu runs | TEST-S9-13 (c06c739); a mutation fails only that test; 57 passed |
| Copilot (drafting help, Stages 6–12): code, test and record drafts                          | all | Every draft was run, tested and reviewed by another member before merging; results recorded from our own runs only | Accept only after human verification | Disclosed in README and records |
Access route or approved equivalent / limitations: GitHub Copilot Chat on github.com (the Copilot button next to the repository search bar), model set to Auto with the balanced setting; Stage 9 used the PR #16 context. Chat only; no agent mode was used.
Available AI evidence and missing evidence honestly disclosed: Copilot prompts and responses are recorded in the Stage 6–9 records (Stage 9 verbatim in stage09/evidence/copilot_review.md).


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | project/README.md (Purpose, Included in this release) | Benjamin | Present; read from the fresh copy |
| Out-of-scope capabilities and known limitations | project/README.md (Scope and limitations) | Benjamin | Present |
| Confirmed teaching Python version and dependency installation | project/README.md (Environment) | Benjamin | Worked as written on Python 3.11.4: venv created; PowerShell blocked the activate script and the README's Set-ExecutionPolicy note fixed it; pip installed pytest 8.3.5 |
| Working directory / demo / interactive / test commands | project/README.md (Environment, Run commands); root README | Benjamin | All three commands worked from project/ (demo line, menu then 0 exit, 57 passed) |
| Repository structure and architecture responsibilities | project/README.md (Structure); root README (Application and evidence) | Benjamin | Present |
| Responsible AI summary / synthetic-data rule | project/README.md (Responsible AI use, Synthetic data rule) | Benjamin | Present |
| Release label/version and SHA links | project/README.md (Release line); root README Group index | Benjamin | Release line present; root index shows the Stage 9 state until the final evidence commit (by design, see K) |
Root README index and project/README verified: Benjamin, 09/11/2026 about 15:15
Fresh clone or extracted ZIP / candidate identity: `git clone https://github.com/Aisha133/ST1-assignment-3.git` into a new folder; `git rev-parse HEAD` = 82c9ad67ab5a99e8147353e281953368ede10f31 (the release SHA)
Verifier and clean environment / actual version: Benjamin, Windows, his own laptop, a new folder on the Desktop and a new virtual environment; Python 3.11.4; Git 2.55.0
Setup/run/test commands and observed results: From the repository root: `python -m venv .venv`; `.venv\Scripts\Activate.ps1` (blocked, "running scripts is disabled"); `Set-ExecutionPolicy -Scope Process Bypass` as the README says, then activate worked; `cd project`; `python -m pip install -r requirements-dev.txt` installed pytest 8.3.5 with colorama, iniconfig, packaging and pluggy; `python main.py` printed "A1: P1 with DR1, 2026-10-01 09:00, scheduled" and the session note; `python main.py --interactive` showed the menu and 0 gave "Goodbye. Session data discarded."; `python -m pytest -q` gave 57 passed. Transcript: stage12/evidence/fresh_copy_benjamin.txt
Missing local file or setup gap / remedy and recheck: No missing files. The execution-policy block happened exactly as the README warns, and its note fixed it, which confirms the review fix in 0c4d5c0. One harmless slip: Benjamin first typed the README's path as a command (PowerShell error, no effect) before opening it in an editor. Benjamin reported the README itself was clear; the only confusing step was "go somewhere new" in our own instruction message (choosing a folder to clone into), which is not part of the README. The README starts from an existing copy and does not show how to get one (see debt in G).


## G Known limitations debt and release notes

Delivered features: Patient and practitioner registration and lookup with validation; appointment booking with the exact-time practitioner conflict rule; cancellation that keeps history; appointment lookup; a practitioner's appointments listed by status, ordered by date/time then ID; an interactive menu that recovers from invalid input; 57 automated tests.
Important fixes: Stage 8 F8-01 (practitioner conflict check compared the wrong way, ba53bbc) and F8-02 (cancelled appointments hidden from lookup, 817c99f), each with a regression test. Stage 12: behaviour-preserving clean-up of the data-store lookup left from Stage 8 (11099fa).
Architecture/quality improvements: One shared session store with services; a pure, explicit-input query and named sort key (Stage 9); console catching only ValueError/LookupError so real bugs are not hidden; docstrings and layout restored in Stage 12.
Known limitations: Session-only data; no feature to mark an appointment COMPLETED; exact-time conflict rule only (no durations, patient conflicts or past-date rule); console-only interface.
AI-assisted development note: GitHub Copilot reviewed work in Stages 6–9 and every suggestion was checked and decided by the group; helped draft code, tests and record wording. All results come from the group's own runs, and every code change had another member's review.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Console tests check output text with `in`, so wording changes break them | Low: rewording a message needs a test update | Low | Assert on stored state alongside key messages | Yes: the messages are part of the UI contract for this release |
| run_menu is one long if/elif function | Medium: harder to extend with new options | Low | Split each option into a small helper function | Yes: readable at the current size, fully tested |
| No COMPLETED transition | Medium: COMPLETED appears only in tests | Low | Add a domain method and service if required | Yes: not required by revision 2 |
| Timezone-naive local times | Low for one clinic | Low | Define a timezone policy before multi-site use | Yes: declared scope |
| README does not show how to get a copy (`git clone`) or where to put it | Low: a new user without Git experience may hesitate, as in the fresh-copy check | Low | Add a short "Get the code" step to the README | Yes: the repository URL is in the root README and the run steps work once cloned (F) |
Session-only synthetic data and minute-precision local time: Declared in README Scope and limitations: records exist only while the program runs; times are local, naive and minute-precision.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: Out of scope (README): no logins or roles, no patient portal, no SMS/email, no billing/insurance, no clinical decision support.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Single user, single process; no timezone policy; no logging/monitoring; no formal usability or accessibility evaluation.
Difference between accepted scope limit and unresolved required behaviour: All of the above are deliberate scope limits from revision 2 or the course's release framing. No current requirement is unmet (H); none of them hides a failing requirement.
PG assurance residual risks / owner / status or not applicable: Not applicable (all-UG group).


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Maintainable code (E): find_appointment | Inspecting data_store.py on ea0f2fe: hand-written blank check and full scan, no docstring (Stage 8 leftover) | Low; quality only, behaviour correct | Anastasia; restore the starter's lookup | 11099fa (data_store.py now matches the supplied starter) | REG-F8-02 2 passed; full 57 passed | None |
| Maintainable code (E): docstrings | has_practitioner_conflict missing its docstring; "Stage 6" labels in services.py | Low | Anastasia; restore/tidy | 11099fa | Full 57 passed | None |
| README reproducibility/content (F) | Root index still showed Stage 8 (44 passed); project README lacked release label, install steps, out-of-scope, AI-use summary and synthetic-data rule | Medium: Stage 12 README requirement unmet | Anastasia; update both READMEs (staff text untouched) | 5928dc8 | Fresh-clone check (F) | Index updated to Stage 12 in the final evidence commit |
| README reproducibility (F), raised in review | Aisha's PR #18 review: README said "create and activate a virtual environment" with no commands, so a fresh-copy verifier could get stuck | Medium: blocks reproducing from the README alone | Anastasia; add venv commands for Windows and macOS plus the PowerShell execution-policy note | 0c4d5c0 | Re-approved by Aisha; fresh-copy check (F) | None |
| Accurate AI-use summary (E), raised in review | Aisha's PR #18 review: the README described Copilot only as a reviewer, omitting its Stage 8 debugging-hypothesis use | Low: incomplete disclosure | Anastasia; add the Stage 8 use | 0c4d5c0 | Re-approved by Aisha | None |
| Process slip during correction | 9133b2e (final newlines) accidentally re-added the two "Stage 6" docstring labels; found by checking the pushed diff | Low; docstring text only | Anastasia; re-apply | 2ee6271 | 57 passed; diff shows only the two lines | None |
Justified no-change conclusion if no defect found: No functional defect was found: the starting full suite passed (57), the release demonstrations matched the requirements, and the quality findings above were all behaviour-preserving.
Release blockers still open / status: None after PR #18 was reviewed, re-approved and merged and the fresh-copy check passed (F).


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Issue #17 https://github.com/Aisha133/ST1-assignment-3/issues/17; PR #18 https://github.com/Aisha133/ST1-assignment-3/pull/18 (release/stage12 → main), reviewed at 2ee6271 and re-reviewed at 0c4d5c0.
Independent reviewer / feedback / response: Aisha. Requested changes (https://github.com/Aisha133/ST1-assignment-3/pull/18#pullrequestreview-5820055778): add the virtual-environment commands, and mention Copilot's Stage 8 hypothesis use. Both fixed in 0c4d5c0 with replies on each comment; approved (https://github.com/Aisha133/ST1-assignment-3/pull/18#pullrequestreview-5820136683).
Integration commit / full recheck: Merge commit 82c9ad67ab5a99e8147353e281953368ede10f31; `python -m pytest -q` in project/ on main: 57 passed; release demos rerun on it (stage12/evidence/).
Tracked and untracked file inspection / cleanliness: `git ls-files` lists only .gitignore, the two READMEs, project/ source and tests, requirements-dev.txt, the stage records, and stage09/stage12 evidence files. `git status --short` is clean.
Secrets/staff material/caches/tool-metadata exclusion check: No credentials, real records, staff solutions, private QA, .venv, __pycache__, .pytest_cache, .idea or Stage 8 utility/backups are tracked (.gitignore covers them).
Candidate recovery plan / known-good SHA: The release SHA 82c9ad67ab5a99e8147353e281953368ede10f31 and the Stage 9 checkpoint 6f4df00 stay in main's history; `git switch --detach <sha>` (or `git archive`) recovers either. Branches feature/stage9-queries and release/stage12 are kept. No history rewriting.
Named substantive contributions: Aisha: Stage 9 query and tests, tutorial/formative answers. Hannah: Stage 9 service listing and tests, tutorial/formative answers. Anastasia: integration, workflow and console tests, console menu, demos, Copilot reviews, Stage 12 corrections and record. Benjamin: PR reviews in Stages 8–9, issue creation. Stage 12: Aisha (PR #18 review), Benjamin (fresh-copy check), Hannah (retrospective draft), Anastasia (code review, corrections, release integration and record). Earlier stages are in the Stage 6–8 records and the contribution log.


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: READY WITH DOCUMENTED LIMITATIONS
Approver / date / rationale and evidence: Aisha, Hannah, Benjamin and Anastasia (each agreed in the group chat), 09/11/2026. Evidence: 57 requirement-linked tests passed on the release SHA 82c9ad6 on Anastasia's laptop (Python 3.14.7) and on Benjamin's fresh clone (Python 3.11.4); the release demonstrations match FR-01–FR-09 and UI-01/02 (D); every change was reviewed (PR #18 by Aisha, with requested changes fixed and re-approved); no open defects (H). Documented limitations are listed in project/README.md and G, so READY FOR COURSE RELEASE would overstate it.
What risks remain / conditions / owners: The accepted limitations in G (session-only data, no COMPLETED feature, exact-time conflict rule only, no timezone policy) and the low-priority debt items. No conditions outstanding. Owner for any later correction: Anastasia, through the published assessment process.
Can the team explain the system: Yes: each member wrote their own contribution lines (N) and will explain the common project in the individual Cadmus oral (due 13/11/2026).
Can a change be recovered: Yes: see I (known-good SHAs and kept branches).
Common decision / PG decision where different: Common only.


## K Final tested release SHA

Exact common tested SHA: 82c9ad67ab5a99e8147353e281953368ede10f31 (merge of PR #18)
Exact PG tested SHA or not applicable: Not applicable
Final submitted SHA / repository URL: The evidence-only commits after 82c9ad6 on main: "Complete Stage 12 release record" (aea6167) and "Add contribution log", which is tagged v1.0; its full SHA is listed on the v1.0 GitHub Release page (https://github.com/Aisha133/ST1-assignment-3/releases/tag/v1.0) and by `git rev-parse v1.0`. A commit cannot contain its own SHA, so it is identified by tag and title here. Repository: https://github.com/Aisha133/ST1-assignment-3
Evidence-only later commit and difference explanation: These 2 commits add only this record, the contribution log, stage12/evidence/ (release demo inputs/outputs and the fresh-copy transcript) and the root README group index; no code or test changes after 82c9ad6, so the tested code and the submitted code are identical.
Executable changes after testing and re-verification: None.
Source ZIP name / SHA correspondence / extracted comparison: SmartCare-release.zip, made with `git archive --format=zip --output=../SmartCare-release.zip <v1.0 SHA>` and attached to the v1.0 GitHub Release (Canvas accepts a URL only). Before the final commit, a dry-run ZIP of the tested code 82c9ad6 was extracted into a separate folder: on 09/11/2026 (about 18:27) the extracted root held .gitignore, README.md, project/ and the stage06–stage12 folders (stage10_pg/stage11_pg templates unchanged); a search for .git, .venv, __pycache__, .pytest_cache and .idea folders found none; `python -m pytest -q` in the extracted project/ gave 57 passed. The final ZIP check (structure and pytest in the extracted copy) is recorded in the v1.0 Release notes.


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [x] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository URL accessible to marker and exact candidate SHA identified.
- [x] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [x] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: Canvas "Assignment 3 Overview", submitting a website URL (the repository); the source ZIP is attached to the GitHub Release v1.0 because Canvas takes a URL only
Deadline/timezone: 9 November 2026, 23:59 (Canberra, AEDT)
Repository access arrangement: Public repository https://github.com/Aisha133/ST1-assignment-3
Mixed-candidate upload arrangement: Not applicable (all-UG group)
Oral/video recording/accessibility arrangements: Individual oral assessment recorded in Cadmus, due 13 November 2026
Remaining administration or release dependency: Group reflection and individual confidential peer forms are submitted separately as directed on Canvas; nothing else blocks this release


## M Formative questions

1. What is a release candidate? A version of the software that has passed through all tests, and is complete in regards to all features being implemented. This version of the software is potentially ready to be released to the public / or given to stakeholders. It is identified by an exact commit SHA and may still have documented limitations.

2. What is feature freeze and why is it used? A feature freeze is the point in development when no more features will be added to the software. It is used as halting new code makes the existing features and code easier to test without the source code consistently changing, alongside this, it helps reduce bugs before a possible release.

3. What is regression testing in a release context? In the context of release, it is performing the regression tests right before the software is to be launched, its purpose is to ensure that the code does not have any major issues or bugs in it before the software is given to the public. It means re-running the whole accumulated test suite on the exact release candidate, so any fixes made during release haven't broken behaviour that already worked.

4. What is a known limitation? It is something that has already been documented and or logged as weakness within the software previously. It is disclosed and accepted for this release, such as SmartCare's session-only data, rather than a hidden defect.

5. What is technical debt? It is when an engineer fixes a code through a fast or temporary solution instead of the right way, indicating that the issue will come back up again in the future.

6. What are release notes? Are documents that are published alongside any maintenance or updates, informing the public what has changed, why it has been changed and how the issue has been fixed.

7. What is software maintenance? Software maintenance is regularly updating and modifying a software after it has been released to ensure that it is kept up to date and that there are no issues present in the code.

8. What is the purpose of the individual demonstration/viva? To verify academic integrity and to make sure that a student understands their own work, and to ensure that the work is theirs.

9. What should the final responsible-AI check establish before release? It should establish that the code is completed, safe and also accurate before it can be released to the public. It should also be confirmed that the ai-generated content was reviewed by a human to reduce any potential risks.

10. What is the main course conclusion about AI and the role of the software engineer? The courses main conclusion about AI is that AI is a tool that can help engineers with their work and also support them, it however does not replace the human capability of judgement, analysing evidence, identifying problems and also testing the AI itself to ensure it aligns correctly with the code and also what the stakeholder wanted.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: The 57 requirement-linked tests passing on the exact release SHA 82c9ad6, on Anastasia's laptop and on Benjamin's fresh clone, backed by the break-it-on-purpose (mutation) checks that showed the tests catch the key failures: the conflict rule, retained history, the registered ID and console recovery (stage09 record C; this record C and F).
Weakest area: The console tests check printed messages rather than stored state, and run_menu is one long function (both recorded as debt in G).
How AI use changed from Stage 1 to Stage 12 (drafted by Hannah, agreed by the group): We don't currently have our stage 1 work, so we start from the shared work in Stage 6. In Stage 6 and 7 we used Copilot as a reviewer, but we wrote our own review notes and test ideas first and rejected or modified several Copilot findings. In Stage 8 we wrote both hypotheses before asking Copilot, then checked each of its causes against evidence. In Stage 9 we tested its suggestions, rejecting one and making the other a smaller test. We moved from using AI to produce drafts to checking AI output against our own work and the tests.
Start doing — engineering and AI use: Engineering: Use a branch and PR for every change from the first stage, and run the tests and read the diff before every commit. AI use: Give Copilot the full context (related files, requirements and test results), not just the diff, since in Stage 6 its wrong Critical claims came from only seeing the diff.
Stop doing — engineering and AI use: Engineering: Stop planning too many tests (Stage 7) and stop making small commits without checking them, since one accidentally undid an earlier change. AI use: Stop treating a confident AI answer as a finding until it is checked: Copilot's "Critical" ratings in Stage 6 and the non-existent method in Stage 8 were stated confidently but were wrong.
Continue doing — engineering and AI use: Engineering: Continue writing regression tests before fixing faults, running "break it on purpose" checks, and having another member review each PR. AI use: Continue writing our own hypothesis then asking Copilot, then comparing and checking its suggestions, as we did when we rejected one and narrowed the other in Stage 9.
What worked / caused rework / future delivery improvement: What worked: What worked well was human-first reviews, regression tests before fixes, mutation checks, and peer review that found real problems. The Stage 9 review caught that the README didn't record the actual test result, and the PR #18 review caught the missing venv commands and the incomplete AI-use summary. What caused rework: Records with wrong or missing details, too many Stage 7 tests planned, and the Stage 12 commit that undid an earlier change. Copilots incorrect critical findings also cost time to disprove, though we still checked them. Future delivery: Use a completion checklist for each record, run the suite and read the diff before every commit and also use branches and PRs from the start. Share more complete context with AI tools, and keep a running AI log as we go. Being able to commit from each member's computer would help show contributions a lot easier. (Retrospective drafted by Hannah and agreed by all four members.)
One paragraph — If AI can write code why do we still need software engineers: AI is able to produce code quickly, however it can't take responsibility for whether that code is correct. In our project Copilot made wrong "Critical" claims, named a method that doesn't exist and hadn't run tests and couldn't approve a PR, so every output needed human checking. Engineers set the requirements, write the tests, form hypotheses, check evidence and are accountable for what gets used. AI can speed write code but judging and verifying the code remains a software engineering task.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | A clinic front desk books patients with practitioners without double-booking and keeps cancelled history; stakeholders are reception staff, practitioners, patients and the clinic manager (README Purpose). |
| Two requirements and acceptance criteria | FR-05: the same practitioner cannot have two SCHEDULED appointments at the exact same time, but a different practitioner can (TEST-S9-10, REG-F8-01). FR-07: a cancelled appointment stays findable and listed (TEST-S9-09, REG-F8-02). |
| Domain model and architecture | Patient, Practitioner, Appointment (with AppointmentStatus); one SmartCareDataStore per session; services coordinate; pure query; console for I/O (README Structure). |
| Design trade-off | Session-only in-memory store: simple and easy to test, but data is lost on exit (FR-10 retired). Also a plain if/elif menu: easy to read, longer to extend. |
| Meaningful test and its limits / 100 percent coverage | TEST-S9-09 proves the cancelled A1 is the same object, excluded by SCHEDULED and still findable. It does not prove other inputs or other sessions. 100% coverage would only show every line ran, not that the assertions check the right behaviour. |
| Diagnosed defect and verification | F8-02: find_appointment skipped cancelled appointments (`status.value != "cancelled"`); found by a failing regression test and evidence run; fixed in 817c99f; REG-F8-02 passes. |
| Shared store and session-state/query responsibilities | One store shared by all services keeps every operation in the same session; the query receives the list explicitly, so it stays pure and testable. |
| What would break if session-state lookup/query responsibilities changed? | A new store per menu option would lose bookings between options; a query reading a global store or sorting in place would change stored order and make results depend on hidden state (the in-place-sort mutation failed 4 query tests). |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancelling only depends on the appointment's own status, so Appointment.cancel() guards it. A conflict needs all stored appointments, so the service checks the shared store before adding. |
| FR-07 retained history test | TEST-S9-09 (tests/test_workflows.py) and REG-F8-02 (tests/test_regressions.py). |
| Actual AI change rejected/modified or honestly accepted with verification | Stage 9 Copilot: identity suggestion Rejected (copy mutation 5 failed); status-parsing suggestion Modified into TEST-S9-13 (c06c739). |
| Unresolved limitation / future production work | Session-only data and no COMPLETED feature; real deployment would need storage, logins/roles, privacy and security review, a timezone policy and accessibility testing. |
| Personal implementation contribution | **Aisha:** Me and Hannah answered the tutorial and formative questions for sections 8, 9 and 12. I built find_practitioner (Stage 6), I conducted the tests TEST-S7-04 to 06 for appointment status and cancelling (Stage 7); the pure query select_appointments and its sort key with TEST-S9-01 to 06, including the break-it-on-purpose check (Stage 9). **Hannah:** I built cancel_appointment with Anastasia (Stage 6); TEST-S7-07 to 09 for registration and duplicates (Stage 7); the service listing list_practitioner_appointments with TEST-S9-07 to 09 and its break-it check (Stage 9); tutorial and formative answers with Aisha (Stages 8, 9 and 12). **Benjamin:** I built TEST-S7-10 to 12 for the practitioner conflict rule. I created issue #9 in Stage 8 and #14 and #15 in Stage 9. **Anastasia:** find_patient and the service tests (Stage 6); TEST-S7-01 to 03 and the regression runs (Stage 7); the regression tests, both fault fixes and the refactor (Stage 8); the workflow test, console menu, demos and Copilot review (Stage 9); the release code review and fixes, and the integration (Stage 12). |
| Personal test/review/design/integration contribution | **Aisha:** I reviewed #4 (Stage 7); wrote the first F8-01/F8-02 hypotheses and also created issue #8 (Stage 8); reviewed the release PR #18 and caught the missing venv commands and also the incomplete AI summary (Stage 12). **Hannah:** I created issues #1 (Stage 6) and #10 (Stage 8); reviewed #5 (Stage 7); drafted the Stage 12 retrospective and the AI paragraph. **Benjamin:** I also reviewed and tested Copilot findings/reports and comparisons in their respective stages. I reviewed PR #11 and #16, where I found a missing verification result in the README. Finally, I did the fresh-copy check for Stage 12 on my laptop. **Anastasia:** Reviewed #7 (Stage 7) and committed everyone's turns on my laptop. |
| PG agentic change and rescheduling verification | Not applicable (all-UG group) |
| PG responsible-AI risk/remediation or supported no finding | Not applicable (all-UG group) |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.
Separate reflection / peer / common team viva evidence links and routing: Group reflection and peer forms are submitted separately through Canvas, and the individual oral through Cadmus, none of them is stored in Git.
No further coding stage. Later corrections use the published assessment process.