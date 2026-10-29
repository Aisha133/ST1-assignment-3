# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 3, Tuesday 1:30pm Tutorial 
- Members, GitHub usernames and cohorts: Aisha (@Aisha133, UG); Hannah (@Hannah-448, UG); Anastasia (@Ajorja, UG); Benjamin (@Benjamin316-uc, UG)
- Repository URL: https://github.com/Aisha133/ST1-assignment-3
- Starting SHA: 91ed9b208925e097c3dd2877dca6a4aec3963fcb

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02 Find a registered patient by patient ID
- Context: PatientService.find_patient raised NotImplementedError, so staff could not get a registered patient back by their ID. Booking and the Stage 9 menu need this lookup to work.
- Requirement: FR-02 Find a patient by patient ID (AC-02.1, AC-02.2). IDs are trimmed, non-blank and case-sensitive.
- Acceptance criteria: (1) AC-02.1: after registering P1, finding "P1" returns that same stored Patient object. (2) AC-02.2: finding a valid ID that was never registered raises LookupError and the stored patients do not change. (3) A blank, spaces-only or non-string ID raises ValueError. (4) " P1 " finds P1 because IDs are trimmed, but "p1" raises LookupError because IDs are case-sensitive.
- Scope: Only PatientService.find_patient and its tests in tests/test_services.py. No search by name and no changes to the data store or domain classes.
- Definition of Done: All criteria met and each one has a test; all tests pass, including the 8 supplied ones; another member has reviewed the commit; everyone has pulled and the tests pass; this record is updated.
- Owner: Anastasia 
- Actual issue link: https://github.com/Aisha133/ST1-assignment-3/issues/2

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06/FR-07 Cancel a scheduled appointment and keep it in history
- Context: AppointmentService.cancel_appointment raised NotImplementedError. Staff need to cancel bookings without losing the record, and the practitioner's time should become free again.
- Requirement: FR-06 Cancel only a SCHEDULED appointment. FR-07 Keep the same appointment, with CANCELLED status, in the current session's history (AC-05.1, AC-05.2, AC-05.3; BR-06, BR-07).
- Acceptance criteria: (1) AC-05.1: cancelling a SCHEDULED appointment changes it to CANCELLED and returns the same stored object. (2) AC-05.2: after cancelling, find_appointment still returns that object and it is still in the appointment list, with the same patient, practitioner and time. (3) AC-05.3: cancelling it again raises ValueError and it stays CANCELLED. (4) Cancelling a COMPLETED appointment raises ValueError and it stays COMPLETED. (5) An unknown appointment ID raises LookupError and a blank ID raises ValueError, and neither changes any appointment. (6) After cancelling, the practitioner can be booked again at that time and the cancelled record is still kept.
- Scope: Only AppointmentService.cancel_appointment and its tests, reusing find_appointment and Appointment.cancel(). No deleting appointments, no completion feature, no rescheduling, and no changes to Appointment.cancel() or the data store.
- Definition of Done: All criteria met and each one has a test; all tests pass; another member has reviewed the commit; everyone has pulled and the tests pass; this record is updated.
- Owner: Hannah
- Actual issue link: https://github.com/Aisha133/ST1-assignment-3/issues/1

## B Commit quality

| Original example | Strong or Weak | Reason                                                                                                                                                                              |
|---|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changes | Weak          | It does not say what changed or why, so a reviewer has to open the code to find out. It could also cover lots of unrelated edits.                                                   |
| final version | Weak          | It describes a moment in time, not a change. "Final" is rerely true and gives no behaviour or requirement to check against.                                                         |
| Add patient search by ID | Strong        | It starts with a verb and names one specific behaviour that links to FR-02, so the reviewer knows what to look for in the diff. Adding the issue number would make it even bettter. |
| fix stuff | Weak          | "Fix" without saying what was broken can't be checked. Nobody can link it to a test, issue or requirement.                                                                          |
| Prevent cancellation of completed appointments | Strong        | It names an exact rule (FR-06 / BR-06) and the state it applies to, so it is clear what test should prove it works.                                                                 |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: Only the cancellation part matches the issue (FR-06/FR-07). Renaming patient fields and restructuring other code are separate changes with no requirement behind them. Mixing them in makes the PR harder to review and hides the cancellation code among unrelated edits.
- Responsibility and architecture concerns: Renaming Patient fields changes something the data store, services, console and tests all rely on, so it could break other people's work. Adding a dependency breaks the "standard library only" setup that every member and the markers use. Restructuring could also move rules away from where they belong, such as moving the status check out Appointment.cancel()
- Testing and review concerns: Passing tests only prove what the tests check. They don't show the renames or restructure were wanted, or that the new dependency installs on everyone's machine. A big mixed diff is easy to skim, so a real bug in the cancellation could be missed, and if something breaks later it is hard to tell which change caused it.
- Changes to remove or separate, with reasons: Keep only the cancellation method and its tests. Remove the field renames, or give them their own issue if they are really needed. Do any restructuring later as a separate, reviewed refactor. Drop the new dependency unless an issue justifies it and the team and tutor agree.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: Which requirement and acceptance criteria were checked; which tests were run, by whom, on which commit and with what result; whether the changed lines were actually read; whether the error cases (unknown ID, blank ID, cancelling twice, cancelling COMPLETED) are tested; whether anything is left unchanged after an error; and whether anything unrelated changed.
- Follow-up review question 1: Which acceptance criterion does each changed line meet, and is any criterion not covered by code or a test?
- Follow-up review question 2: Which test proves the method returns the stored appointment and not a copy, and would that test fail if a new object were returned?
- Follow-up review question 3: Which tests check that cancelling twice, or cancelling a COMPLETED appointment, raises ValueError and leaves the status unchanged?
- Follow-up review question 4: What command was run, in which folder, on which commit, and what was the exact pass count? Did you see it run, or are you assuming?
- Follow-up review question 5: Does the change keep the cancelled appointment in the store (FR-07), and which assertion checks it can still be found and listed afterwards?
- Additional questions if useful: Were any files other than services.py and tests/test_services.py changed? Is the "only SCHEDULED" rule left in Appointment.cancel() rather than copied into the service?

## E Team workflow agreement

| Practice | Team agreement                                                                                                                                                                                                                                                                                                                                                    |
|---|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Branch naming | No feature branches: on our tutor's advice we work directly on main. Everyone uses Anastasia's PC, one person at a time, and each commit records who made it with git commit --author. We always pull and run the full test suite before changing anything.                                                                                                       |
| Commit message convention | Start with a verb and name the behaviour or test that changed, plus the issue number, e.g. "Add patient lookup by ID (refs #2)". No vague messages like "update" or "changes".                                                                                                                                                                                    |
| PR size | There are no PRs in our workflow, so each commit covers one issue: one behaviour plus its tests, small enough to review in one go.                                                                                                                                                                                                                                |
| Another-member review requirement | A member who did not write the code reviews every code commit on GitHub (the commit page and comments), runs the full test suite, and writes their own notes before using Copilot. For Stage 6, Benjamin reviewed all three code commits (Anastasia's, Aisha's and Hannah's), so no one reviewed their own work. We may rotate the reviewer role in later stages. |
| Merge rule | 	Every commit must pass the full test suite before it is pushed. To save time, the three code commits were made first and then each one was reviewed separately against its own issue using its own diff. Any requested changes are made in a follow-up commit and rechecked by the reviewer. After the reviews, everyone pulls and runs the tests.                |
| Significant Copilot disclosure rule | Any significant AI use (GitHub Copilot) is recorded in section H: the prompt, a summary of the output, what we checked, Accept/Modify/Reject and the result. Synthetic data only.                                                                                                                                                                                 |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link                                                  | Requirement                | Owner     | Acceptance criteria or precise link                                                                      | Status                              |
|-------------------------------------------------------------|----------------------------|-----------|----------------------------------------------------------------------------------------------------------|-------------------------------------|
| [#2](https://github.com/Aisha133/ST1-assignment-3/issues/2) | FR-02 patient lookup       | Anastasia | 	AC-02.1, AC-02.2, plus blank/trimmed/case-sensitive ID rules (see section A)                            | Closed: done in c1475fa, reviewed by Benjamin |
| [#3](https://github.com/Aisha133/ST1-assignment-3/issues/3) | FR-03 supporting practitioner lookup | Aisha     | Kown ID returns stored practitioner, unknown ID LookupError, blank/non-string ValueError, trimmed, case sensitive. | Closed: done in 4240d68, reviwed by Benjamin |
| [#1](https://github.com/Aisha133/ST1-assignment-3/issues/1) | FR-06/FR-07 cancellation with retained history                           | Hannah    |  AC-05.1, AC-05.2, AC-05.3, plus COMPLETED, unknown and blank ID cases (see section A)                                                                                                        | Closed: done in 9accf8a, reviewed by Benjamin                                    |


## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.


Change 1: Patient lookup (#2)
- PR link and title: No PR (main-only workflow, tutor-approved). Commit "Add patient lookup by ID (refs #2)": https://github.com/Aisha133/ST1-assignment-3/commit/c1475fa
- Linked issue and requirement: #2, FR-02 Find a registered patient by patient ID
- Feature branch: None (main-only workflow; see section E)
- Changed behaviour: PatientService.find_patient now returns the stored Patient, raises LookupError for a valid unknown ID, and uses the data store's existing validation for blank or invalid IDs (ValueError). Added tests/test_services.py with two setup helpers and 7 FR-02 tests.
- Meaningful commits: https://github.com/Aisha133/ST1-assignment-3/commit/c1475fa (author: Anastasia)
- Test command, directory and observed result: python -m pytest, in project/, 15 passed (8 supplied + 7 new)
- Another-member reviewer: Benjamin
- Human observations recorded before Copilot: Benjamin's review notes for #2: human notes finished 3:20, Copilot output and decisions recorded by 3:40, approval comment 3:47
- Requirement, responsibilities, test assertions and unrelated-scope checks: Every acceptance criterion in #2 is covered by code and a test. The method returns the stored object and uses the right error each time (ValueError comes from the store's required_text; LookupError when the store returns None). The tests use is and check the store is unchanged after LookupError. Only find_patient and the new test file changed.
- Key feedback: Cosmetic only: the docstring says "Stage 6 return the stored patient..." instead of "Return...", and the test file had no newline at the end. Not blocking.
- Author response/change and verification: The missing newline was fixed by the next commit (4240d68). The "Stage 6" docstring wording was noted as non-blocking and left unchanged (cosmetic; see M).
- Reviewer recheck and approval: Approved with no required changes: https://github.com/Aisha133/ST1-assignment-3/commit/c1475fafd9aebfa2e4be7bc1861c6550e33d41a9#commitcomment-207167184
- Merge outcome and SHA: Pushed directly to main as c1475fa (main-only workflow)
- Significant Copilot assistance: Copilot review comparison by Benjamin (section H).
- Linked issue closure: Closed #2 with a comment naming c1475fa
- Each member updated main: All members pulled and tested
- Integrated verification after merge: python -m pytest, in project/, 15 passed at c1475fa

Change 2: Practitioner lookup (#3)
- PR link and title: No PR (main-only workflow, tutor-approved). Commit "Add practitioner lookup by ID (refs #3)": https://github.com/Aisha133/ST1-assignment-3/commit/4240d68
- Linked issue and requirement: #3, FR-03 supporting practitioner lookup
- Feature branch: None (main-only workflow; see section E)
- Changed behaviour: PractitionerService.find_practitioner now returns the stored Practitioner, raises LookupError for a valid unknown ID, and uses the data store's validation for blank or invalid IDs. Added 6 FR-03 lookup tests to tests/test_services.py.
- Meaningful commits: https://github.com/Aisha133/ST1-assignment-3/commit/4240d68 (author: Aisha)
- Test command, directory and observed result: python -m pytest, in project/, 21 passed
- Another-member reviewer: Benjamin
- Human observations recorded before Copilot: Benjamin's review notes for #3: human notes finished 4:00, Copilot output and decisions recorded by 4:20, approval comment 4:25
- Requirement, responsibilities, test assertions and unrelated-scope checks: Every criterion in #3 is covered. It uses the same pattern as find_patient and the supplied find_appointment, returns the stored object (tests use is and check the specialty), and uses the right errors. Only find_practitioner and the end of the test file changed.
- Key feedback: Cosmetic only: the docstring still starts "Stage 6 Return..."; only one blank line before the "# ---- FR-03" section comment. The missing newline from #2 is now fixed. Not blocking.
- Author response/change and verification: No changes requested. The cosmetic points (docstring wording, single blank line) were noted as non-blocking and left unchanged (see M).
- Reviewer recheck and approval: Approved with no required changes (cosmetic points noted): https://github.com/Aisha133/ST1-assignment-3/commit/4240d68cdb15d88b02f833321005dc7ecf3af8d3#commitcomment-207170233
- Merge outcome and SHA: Pushed directly to main as 4240d68
- Significant Copilot assistance: Copilot review comparison by Benjamin (section H).
- Linked issue closure: Closed #3 with a comment naming 4240d68
- Each member updated main: All members pulled and tested
- Integrated verification after merge: python -m pytest, in project/, 21 passed at 4240d68

Change 3: Appointment cancellation (#1)
- PR link and title: No PR (main-only workflow, tutor-approved). Commit "Add appointment cancellation that retains history (refs #1)": https://github.com/Aisha133/ST1-assignment-3/commit/9accf8a
- Linked issue and requirement: #1, FR-06/FR-07 Cancel a scheduled appointment and keep it in history
- Feature branch: None (main-only workflow; see section E)
- Changed behaviour: AppointmentService.cancel_appointment now finds the appointment with find_appointment (so blank IDs give ValueError and unknown IDs give LookupError), calls the appointment's own cancel() method so the "only SCHEDULED" rule stays in the Appointment class, and returns the same object. Nothing is deleted, so the cancelled appointment stays in the session's history. Added 9 FR-06/FR-07 tests, including retained history, cancelling twice, cancelling COMPLETED, bad IDs and rebooking the freed slot.
- Meaningful commits: https://github.com/Aisha133/ST1-assignment-3/commit/9accf8a (author: Hannah)
- Test command, directory and observed result: python -m pytest, in project/, 30 passed (8 supplied + 22 in tests/test_services.py)
- Another-member reviewer: Benjamin
- Human observations recorded before Copilot: Benjamin's review notes for #1: human notes finished 4:40, Copilot output and decisions recorded by 4:55, approval comment 5:50
- Requirement, responsibilities, test assertions and unrelated-scope checks: Every criterion in #1 is covered by a test. The service reuses find_appointment and Appointment.cancel() instead of checking or setting the status itself, and deletes nothing. The tests check object identity, status, the list and the details, and check the status is unchanged after every rejection. Only cancel_appointment and the end of the test file changed.
- Key feedback: Minor: the COMPLETED test doesn't check the list afterwards (the status check covers it), and there is one blank line before the section comment. Not blocking. The "Stage 6" docstring wording Benjamin raised in the #2 and #3 reviews was done properly in this commit.
- Author response/change and verification: No changes requested. Minor test points (explicit same-object check after a failed second cancel; list check in the COMPLETED test) carried into the Stage 7 tests.
- Reviewer recheck and approval: Approved with no required changes: https://github.com/Aisha133/ST1-assignment-3/commit/9accf8aceff0f0e39e5a0c64cec598c3672db082#commitcomment-207177605
- Merge outcome and SHA: Pushed directly to main as 9accf8a
- Significant Copilot assistance: Copilot review comparison by Benjamin (section H).
- Linked issue closure: Closed #1 with a comment naming 9accf8a
- Each member updated main: All members pulled and tested
- Integrated verification after merge: python -m pytest, in project/, 30 passed at 9accf8a

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Benjamin, Copilot review comparison for each Stage 6 code commit (c1475fa #2, 4240d68 #3, 9accf8a #1), done after writing his own human review notes each time
- Prompt/purpose and relevant issue/diff: Stage 6 Part H review prompt, given each issue's acceptance criteria and that commit's diff (for #1, also the FR-06/FR-07 retained-history line)
- Summary of output: In all three reviews Copilot rated "missing validation in the service" as Critical (blank/non-string IDs, trimming, case). For #1 it also asked us to confirm cancel() controls the status change and that a cancelled booking frees the slot, suggested a status guard in cancel_appointment, and suggested an explicit same-object check after a failed second cancel. Smaller points: the #2 test-file docstring described tests not yet added; check the store is unchanged after invalid input; no unrelated changes. In #3 it wrongly said the NotImplementedError stub was "left behind". Each time it said it could not confirm the tests ran.
- Human check against actual code, requirements and tests: data_store.py find methods call required_text (domain.py), which raises ValueError and strips spaces, and look up by exact (case-sensitive) key. Appointment.cancel() raises ValueError unless SCHEDULED; the unknown-ID LookupError comes from find_appointment. has_practitioner_conflict only counts SCHEDULED appointments. The #3 diff shows the stub removed. The Stage 6 handout says to use the store's validation and the domain transition. Benjamin ran the suite each time: 15, 21 and 30 passed.
- Decision — Accept / Modify / Reject: Reject: the Critical "missing validation" findings (all three), the service status guard, the #3 "stub left behind" claim. Accept: cancelled slot is free (verified, no change), #2 docstring note (no change needed; matched after #1), no unrelated changes. Modify: store-unchanged check and explicit same-object check, both moved into the Stage 7 tests.
- Reason: The rejected findings were disproved by the actual code and passing tests; Copilot only saw the diff, not data_store.py or domain.py, and a service status guard would duplicate the domain rule. The accepted points matched our own checks. The modified points were good ideas but not needed for these commits, so they became Stage 7 test assertions.
- Verification/evidence: python -m pytest in project/: 15 passed at c1475fa, 21 at 4240d68, 30 at 9accf8a. Approval comments: https://github.com/Aisha133/ST1-assignment-3/commit/c1475fafd9aebfa2e4be7bc1861c6550e33d41a9#commitcomment-207167184 ; https://github.com/Aisha133/ST1-assignment-3/commit/4240d68cdb15d88b02f833321005dc7ecf3af8d3#commitcomment-207170233 ; https://github.com/Aisha133/ST1-assignment-3/commit/9accf8aceff0f0e39e5a0c64cec598c3672db082#commitcomment-207177605

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: Benjamin matched every acceptance criterion to code and a test, ran the suite each time, and noted cosmetic points (the "Stage 6" docstring wording, a missing final newline in #2, single blank lines) and that the #1 COMPLETED test doesn't check the list.
- Copilot noticed: Missing service validation (rated Critical), the #2 test-file docstring being ahead of the tests, and an explicit same-object check after a failed second cancel.
- Overlap: Both saw each change was narrow and limited to its issue, and (for #1) that rebooking depends on the conflict check.
- What did the human reviewer notice that Copilot did not: The cosmetic points and the COMPLETED list check, and he actually ran the tests.
- What did Copilot identify that the human reviewer initially missed: The #2 docstring mismatch and the explicit same-object check (moved into Stage 7).
- Unsupported or incorrect Copilot suggestion: The Critical "missing validation" claims (the store already validates), the #3 "stub left behind" claim, and the #1 service status guard (it would duplicate the domain rule).
- Human judgement accepted, modified or rejected, and why: Decided on evidence from data_store.py, domain.py, the handout and test runs, not on Copilot's confidence (details in H).
- Which evidence justified merge approval: Every criterion matched to a passing test, Benjamin's own runs (15, 21, 30 passed) and diffs limited to each issue.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Anastasia
- Implementation: Implemented PatientService.find_patient: https://github.com/Aisha133/ST1-assignment-3/commit/c1475fa
- Testing: Created tests/test_services.py with setup helpers and 7 FR-02 tests; 15 passed. Assisted Aisha and Hannah with their sections. 
- Review: assisted with all reviews.
- Issue refinement: Created issue #2 (FR-02) with acceptance criteria, scope and Definition of Done
- Design and responsibility discussion: Created and proposed the design and helped delegate responsibilities
- Debugging or integration: Ran tests after each change/commit
- Documentation or team support: Created all documentation, updated the log, ensured reviews were recorded, created notes for code and assisted the team.

- Member: Aisha
- Implementation: Implemented PractitionerService.find_practitioner: https://github.com/Aisha133/ST1-assignment-3/commit/4240d68
- Testing: Added 6 FR-03 lookup tests; 21 passed
- Review: not applicable 
- Issue refinement: Created issue #3
- Design and responsibility discussion: Not applicable 
- Debugging or integration: Set up the shared repo; pushed the group index and record header (34e35bb); took part in the integrated checks on the shared PC
- Documentation or team support: Not applicable

- Member: Hannah
- Implementation: Implemented AppointmentService.cancel_appointment: https://github.com/Aisha133/ST1-assignment-3/commit/9accf8a
- Testing: Added 9 FR-06/FR-07 cancellation tests (status, retained history, cancelling twice, COMPLETED, bad IDs, rebooking); 30 passed 
- Review: not applicable
- Issue refinement: Created issue #1
- Design and responsibility discussion: Not applicable 
- Debugging or integration: Took part in the integrated checks
- Documentation or team support: Not applicable 

- Member: Benjamin
- Implementation: not applicable
- Testing: Pulled and ran the tests on own device
- Review: Reviewed all three code commits, each against its own issue, writing human notes before using Copilot. c1475fa (#2): rejected the Critical "missing validation" claim using data_store.py; approved (https://github.com/Aisha133/ST1-assignment-3/commit/c1475fafd9aebfa2e4be7bc1861c6550e33d41a9#commitcomment-207167184). 4240d68 (#3): caught Copilot's false "stub left behind" claim and rejected its Critical findings with evidence; approved (https://github.com/Aisha133/ST1-assignment-3/commit/4240d68cdb15d88b02f833321005dc7ecf3af8d3#commitcomment-207170233). 9accf8a (#1): full Copilot comparison; rejected the Critical finding and the duplicate status-guard suggestion with evidence from domain.py; verified the rebooking behaviour in has_practitioner_conflict; approved (https://github.com/Aisha133/ST1-assignment-3/commit/9accf8aceff0f0e39e5a0c64cec598c3672db082#commitcomment-207177605)
- Issue refinement: Closed issues #1, #2 and #3 with comments naming each commit
- Design and responsibility discussion: Not applicable
- Debugging or integration: Took part in the integration checks
- Documentation or team support: helped draft / reworded sections



## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

Commit count only shows how often someone saved, not what the work achieved. Someone could split a small change into lots of tiny commits, while someone else makes one well-tested commit or does a review that catches a problem before it causes trouble. A lot of important work leaves few commits at all, like reviewing, writing issues and acceptance criteria, checking Copilot's claims and helping teammates. In our group, the reviews for #2 and #3 produced no code commits, but they checked every acceptance criterion and showed with evidence that Copilot's "Critical" findings were wrong. Because we all use one shared PC, commit counts say even less about who did what, which is why we record the author on every commit and keep a contribution log.

## L Stage 6 formative questions

1. What is version control?

A system that records every change to a project as a history of saved snapshots (commits), with who made each change, when and why. It lets a team work on the same code, see exactly what changed, and go back to an earlier version if something breaks.

2. Why is a feature branch useful?

It keeps one piece of unfinished or unreviewed work separate from main, so it can't break the working version everyone shares. It can be reviewed on its own and merged only when it's approved. (Our group works on main with the tutor's approval. We get a similar effect by having one person change the code at a time and running all the tests before every push.)

3. What makes a commit a good engineering commit?

It is one focused change (for example one behaviour plus its tests), it leaves the project working with all tests passing, it has no unrelated edits or secrets, and its message says what changed so a reviewer can check it against a requirement.

4. What is a pull request?

A request to merge a branch into main. It shows the diff, links to the issue, says what tests were run and what AI help was used, and is where another team member reviews, comments and approves before the change is added.

5. What is the purpose of code review?

To have someone else check that a change meets its requirement and acceptance criteria, handles errors correctly, has meaningful tests, keeps code in the right place and doesn't include unrelated changes. It catches problems before they spread and helps everyone understand the code.

6. What does a Git diff show?

Exactly which lines were added, removed or changed between two versions, file by file. Removed lines start with "-" and added lines start with "+". It lets the reviewer focus on what actually changed instead of rereading whole files.

7. What is a Definition of Done?

A checklist the team agrees on for when work is really finished, not just written: the acceptance criteria are met, meaningful tests pass, another member has reviewed it and any feedback is fixed, everyone has the latest version and the tests pass there, and the records are updated.

8. What is the appropriate role of GitHub Copilot in pull-request review?

A second opinion, used after the human reviewer has written their own notes. It can summarise a change and suggest risks or questions, but every claim has to be checked against the real code, the requirements and an actual test run. It can't approve a change or replace the human reviewer, and saying "tests pass" doesn't mean it ran them. In our reviews it raised "Critical" problems that turned out to be wrong once we checked the data store.

9. Why should individual contribution not be judged only by commit count?

Commits vary hugely in size and value, and a lot of important work produces few or no commits, such as reviews, testing, writing issues, checking AI output and helping others. Counting commits rewards splitting work up artificially and ignores quality. On a shared PC it is even less reliable, so contributions should be judged from the actual work and its evidence.

10. What is the Stage 6 engineering rule?

Every change follows one traceable, reviewed path: requirement → focused issue → small change with meaningful tests → run the full test suite → another member reviews the actual diff (human first, then Copilot) → respond to feedback and retest → integrate → everyone updates and checks, with honest evidence recorded at each step.

## M Completion and handover

- Starting SHA: 91ed9b208925e097c3dd2877dca6a4aec3963fcb
- Final Stage 6 code SHA: 9accf8aceff0f0e39e5a0c64cec598c3672db082
- Test command: python -m pytest
- Working directory: project
- Observed result: 30 passed (8 supplied)
- PR and another-member reviewer: No PRs (main-only, tutor-approved). All three code commits reviewed by Benjamin: c1475fa (#2), 4240d68 (#3), 9accf8a (#1)
- Unresolved issue or none: No functional issues. Cosmetic, non-blocking: "Stage 6" wording left in the find_patient and find_practitioner docstrings, and one blank line (instead of two) before some test section comments. Suggested extra test assertions (store unchanged after invalid input; explicit same-object check after a failed second cancel; list check in the COMPLETED test) carried to Stage 7.
- Stage 7 handover status: Ready for tutor checkpoint
- Final submitted SHA if later than tested SHA: The commit "Complete Stage 6 evidence record" that adds this file. It is evidence-only: it changes only README.md and this record, with no code or test changes after the tested SHA above. A commit cannot contain its own SHA, so its SHA is recorded in the Stage 7 record as the Stage 7 starting point.

- [x] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [x] At least two focused issues link requirements and acceptance criteria.
- [x] Feature work reviewed by another member using the actual diff.
- [x] Human-first review and required Copilot comparison recorded.
- [x] Feedback resolved and approval recorded before merge.
- [x] Everyone pulled main and integrated checks passed.
- [x] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [x] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
