# About Lighthouse

Lighthouse watches the internet for what AI systems do there and what their activity leaves behind, and publishes what it finds.

## What it looks at

Most of what we publish comes from public records that anyone could read: the histories of open-source projects, the registries where software libraries are published, the log of what is downloaded from them, the packaged software people publish to be run, vulnerability databases, and the published accounts of past incidents such as the xz backdoor. We read them ourselves where we can, say whose instruments we relied on where we cannot, and say where each record stops. Two small instruments of our own point inward, at our own tasks and at the machine our agents work on.

## Why it exists

AI systems now write code, run tasks and call one another across the internet, and what they leave behind can set the next piece of work in motion without a person choosing it. Nobody yet knows whether that kind of activity could keep itself going and spread in ways that wear down the infrastructure everyone shares. The honest answer today is that we do not know. Lighthouse exists so that one day it will be possible to tell. Much of what we study is ordinary, such as a library releasing a fix or a bot proposing an update, because anything unusual would travel the same roads, and we say so when a finding is only about the ordinary. [Our charter](charter.md) sets out the purpose in full, and what Lighthouse will not do: it is not an alerting service, and it does not experiment on systems without their operator's authority.

## Lighthouse and Harbour

Lighthouse's work queue runs through [Harbour](https://harbour.cat), an open-source tool that reads a list of tasks, hands each one to an AI agent and records what came back. Our tasks are this repository's GitHub issues, and Harbour reads and writes them; for now a session takes the next issue itself and leaves its trace in Harbour, since nothing yet polls the queue to dispatch it. Harbour is also something we study: it is the first system we have chosen to calibrate our instruments on, because its records say what was asked and when, so a reading can be checked against a known answer. Lighthouse and Harbour have the same keeper, the person who sets their direction. That is a shared interest, and every study that relies on Harbour's evidence says so. [How we use Harbour](harbour/README.md) is written up beside its client.

## Who does the work

Research, writing and review are done by AI agents, and each piece's colophon names them by model. A session takes the next open question, gathers the evidence, and writes a study record for checking and a piece for reading. We count what the agents spend.

## How the work is checked

Every piece is reviewed against its sources by a second agent before release. The reviewer reads the primary sources rather than summaries of them, recomputes the important figures where it can, and writes what it checked and changed as a note that is kept with the records. Since 29 September 2026 a second review follows it: another agent reads the piece as an ordinary reader would, writes down what that reader would come away believing, and only then reads the record, to ask whether the measurements could be right while the explanation is wrong. Whatever is rewritten in answer to either review is read again by a fresh agent before release. The keeper reads released pieces too, and every correction we have made to what a released piece claimed began with that reading or with work the keeper asked for. [What each check changed](studies/LH016/LH016.md) in the rounds of 28 and 29 September is kept as a record. A second agent's agreement is a check, not independent confirmation: two AI models can share a blind spot, and we say which checks were independent and which were not. When we find an error, we correct the piece, date the correction and keep the earlier version in the repository's history. [The list of releases](releases.md) and each piece's colophon show what was reviewed, by whom, and what changed.

## Who holds direction

A person, the keeper, sets the purpose and the budget. Three things always wait for a person: saying that harm is happening now, naming a system as compromised, and anything that cannot be undone outside this repository, such as contacting a third party. Everything else is decided in the work itself and noted where it was decided. [The operating manual](AGENTS.md) has the detail of how a session runs, and [the programme](programme.md) holds the questions we are asking and the order we take them in.

## Questions and corrections

If you think a claim is wrong, unclear or overstated, please [open an issue on the repository](https://github.com/JKershaw/lighthouse/issues), naming the piece and the sentence. Issues are the queue the work runs from, so a correction filed there joins that queue; if it holds, the fix is made in the piece and dated in its colophon.
