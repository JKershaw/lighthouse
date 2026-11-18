# Technical review of focused runner roles

**In short.** A fresh Codex/OpenAI reviewer checked the focused runner and Git claim helper against the existing main branch and the commissioned scope. One instruction ambiguity could have caused an Editor session with no maintenance tasks to skip its daily visit; the author corrected it and this reviewer re-read the correction. No remaining must-fix issue was found in this engineering review.

Reviewed on 18 November 2026 by a separate reviewer agent, against main at `60d4950` and the implementation commits `3fa8915` and `ae54050` (the published equivalents of local commits `2b98467` and `93aa34e`), plus the corrected empty-queue instruction in `schedule/roles.md`. The runtime did not expose exact model identity or usage prices. This is a technical review, not scientific review or independent confirmation of findings.

## Checks and findings

- Read AGENTS.md and the changed runner, role, Horizon and Editor instructions. The four roles select from the existing shared queue, and the all-purpose default remains available. The role filter leaves the global readiness report intact. The daily visit is explicit even when Editor has no ready maintenance row; Watch, Research and Horizon do not dispatch it.
- Read the claim implementation and integration tests. Claims are based on fetched main, require a clean synchronised checkout and are committed in a disposable detached worktree. Only a successful fast-forward push and local sync authorise work. A losing claim cannot leak into a later completion push on the session branch. Existing ownership, stale claims, dependency waits and explicit blocks are not bypassed.
- Ran `python3 -m unittest discover -s schedule -p 'test_*.py'`: 55 tests run, with two existing opt-in tests skipped. The new tests exercise two real Git checkouts competing for a task, completion while another run advances main, stale interrupted claims, role handover, blocked publication and the default contract.
- Ran an additional adversarial check against a local Git remote, simulating a lost acknowledgement after the remote accepted a claim push. The helper failed closed, the session branch stayed clean, and a competing checkout was refused with the authoritative owner's identity. No observation or other scientific task was executed.
- Confirmed that the change does not modify `schedule/model.py`, the research queue, scientific records, study protocols or workflow triggers. Publication still requires the actual cleared version and review notes; a graph state is not a scientific verdict. Completion and stale-claim reconciliation remain explicit retained-evidence decisions rather than new execution infrastructure.

A final read-only pass checked the retained lost-acknowledgement regression and the strengthened completion test, which merges another worker's claim in the same queue as well as its separate file. The reviewer ran the final suite: 56 tests run, two existing skips, no new issue or remaining must-fix finding.

## Limits

This review did not activate or inspect external scheduled triggers, perform a live reader visit or independently run the site/browser verification. Those results belong in the implementation's verification record. Production push permissions, model/browser capability and trigger timing must be checked during the separately approved rollout. The daily visit deliberately has no new lock or queue row, so rollout must retain one Editor slot and avoid overlapping Editor/all-purpose runs. Ambiguous ownership or interrupted work still requires reconciliation; age alone never permits repeating a scientific observation.
