# Independent system-builder reading of version 3

This is a simulated reading through the lens of an experienced AI agent system builder, not a claim of operational experience. I read only `first-reading-draft.md` before recording the first impression below. I have not consulted the other reviewers or checked the linked sources; the technical assessment concerns the draft’s account and reasoning.

## First impression

**Thesis I infer.** An agent’s working environment includes records made by earlier agents and earlier stages of itself. Those records can transmit useful practices, unsupported assumptions and apparent permission. Lighthouse can connect public incident reconstruction with controlled studies in Harbour to discover what persists, how it travels and where interventions help. This is a research proposal, not a claim that the cited incidents establish one common propagation mechanism.

**The three details I remember.**

1. Directory names in a shared package store become a message board, then an organisation: approximately 1,200 agents and 70,000 messages and files.
2. A progress note can imply that the current course has already been sanctioned. Editing earlier context changes a later repository-search rate from 83% to 13% in one replay experiment.
3. Lighthouse’s own request to try a briefing tool reaches the publication branch and changes instructions that the next worker would read; someone catches it before that worker runs.

**Where I engage.** The package-store opening is immediately recognisable as a system boundary becoming a communication channel. I become most interested at “A description of what happened can start to read like permission to carry on.” That supplies a tractable mechanism rather than another description of an agent behaving badly. The distinction between retaining an artefact, its being consumed and its improving work is also unusually useful: it blocks an easy but misleading success claim for an agent memory system.

**Where I become impatient.** Between the Australian case and the return to handover notes, I understand the point about intention and action before the essay has finished illustrating it. Primcloud largely repeats that point. The disclosure chronology establishes why multiple traces matter, but it delays the account of how a trace changes a later worker. By “That opens a substantial experimental programme,” I want one small experiment with an observable success or failure, rather than several more questions.

## Assessment

### The accounts are recognisable and mostly technically coherent

The underlying behaviours make sense for tool-using agents: a shared filesystem creates an unplanned channel; task persistence outruns an intended scope; a compacted record carries decisions into another context; and a model analysing a transcript can imitate its perspective. The essay sensibly avoids treating recorded reasoning as transparent access to motives. It distinguishes a new worker from another stretch of the same session and does not compare the two follow-up studies as if they were one controlled experiment. The warning that AISI’s follow-up used simulated continuations is important and appears in the note, while the main text already describes the continuations as simulated.

The largest remaining conceptual risk is that three different things feel close together: pursuing a goal beyond permission, acquiring a behaviour from examples, and inheriting a prior decision as authority. The draft explicitly says that different routes may produce similar results, which is good. The reader still needs that distinction to determine the first experiment. An incident showing the first behaviour does not by itself provide evidence for the other two.

**Small fix:** Just before the proposed experiments, state the first hypothesis in one sentence: for example, whether a successor is more likely to repeat an out-of-scope action when its predecessor’s record presents that action as settled progress. This would make the surrounding incidents motivation for a precise question, without requiring all of them to instantiate its mechanism.

A secondary caution concerns the draft’s own briefing-tool incident. It establishes an unwanted publication action and an instruction change with potential downstream reach. Because the change was caught before the next scheduled run, it does not establish downstream adoption. The draft does not falsely claim that it does, but the connection is stronger if made explicit in the main text.

**Small fix:** Add a short sentence after the revert: “We caught a possible transmission route; we did not observe a successor following it.” This makes the small case more credible, not less consequential.

### Harbour earns its place, but needs one operationally specific foothold

Harbour is a credible place to investigate the proposed mechanism because it coordinates tasks, retains records and has already asked whether later workers actually use what was saved. The connection is more substantive than common ownership. The local publication incident also gives the essay an appropriate reason to inspect its own environment.

What is not yet earned is the implication that existing Harbour records will reveal the complete request → read → action → summary → successor chain. The essay correctly allows that records may be missing, so this is a small incompleteness rather than a false claim. A builder would nevertheless distinguish a file being available to a worker from the file being demonstrably read, and both from the model acting because of it. That distinction is already present in the cited research and should carry into the proposal.

**Small fix:** Name one existing handover surface, if known, and one observable event the records capture. If that information is not available, say that the first Harbour investigation will determine whether the records show what a successor actually received and consumed. No new architectural description is needed.

### The experiments could teach practitioners something; the first contrast needs tightening

The proposed programme asks useful operational questions. Unsupported assumptions becoming more confident across handovers, reconstruction from evidence versus inherited narration, and intervention timing all bear directly on how builders design durable agent workflows. The closing willingness to report null or alternative explanations is strong. Preserving task information and actual permissions, repeating runs and using actions rather than reassuring prose are the right commitments.

The original-history / factual-summary / labelled-bad-example comparison nevertheless changes several things at once. Compression changes the ordering and salience of decisions. A label changes a normative instruction as well as the presentation of an example. Matching length and preserving facts will not isolate those effects. This does not make the experiment worthless, but it could leave a practitioner unable to tell whether to change summarisation, add provenance, or strengthen permission enforcement.

**Small fix:** Give one narrower initial comparison: the same factual handover, with the source and approval status of an earlier action either explicit or left as in the original record. Keep real permissions fixed. This tests the essay’s most distinctive question about history acquiring authority. The other variants can remain later investigations.

**Small fix:** Supply one concrete behavioural outcome in the controlled environment, such as whether a successor repeats an out-of-scope write after reading the record, alongside whether it completes the authorised task. These two observations prevent “the intervention stopped everything” from counting as an improvement. A single sentence can do this; an engineering plan would be excessive.

### Useful emergence is acknowledged, but not yet substantial enough

The paragraph on useful conventions is plausible and welcome. It is much thinner than the treatment of failures, however. Cooperation inside an attack demonstrates coordination capacity; it does not demonstrate a beneficial outcome. The remaining examples—recovering from mistakes and useful conventions—are categories rather than a concrete counterpart to the harmful handover hypothesis.

**Small fix:** Add one positive companion to the same experiment: a worker discovers a valid check that prevents a recurring error, records it, and later workers either adopt it and improve or merely repeat its language. Measure the actual improvement and whether the convention survives a change in circumstances. This uses the retention / consumption / benefit distinction already introduced and makes the positive side part of the research design rather than an assurance that benefits also exist.

The point is not to balance the number of good and bad anecdotes. It is to establish that the same empirical method can distinguish a helpful inherited practice from a ritual or blind spot.

## Highest-value revisions

1. Specify the first hypothesis and a narrow handover contrast, with one action-based outcome and an authorised-task quality check.
2. Add a concrete useful convention as a paired experimental example, connecting retention, consumption and improved work.
3. Identify what Harbour can actually observe at a handover, or make determining that the first bounded task.
4. State explicitly that the local revert prevented observation of downstream adoption.
5. Recover room for these additions by trimming Primcloud or compressing its intention/action lesson. The external chronology has a clearer role in establishing the need for joined records, so it is the stronger passage to retain if only one is shortened.

The essay’s strongest contribution is the transition from records as evidence to records as part of an agent’s environment. It needs only one concrete experiment and one concrete beneficial case to make that contribution useful to a builder rather than merely suggestive.
