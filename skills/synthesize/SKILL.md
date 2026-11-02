---
name: synthesize
description: Run a research synthesis with a short interview first and a check-and-fix loop after. Use when the person says "/synthesize", "synthesize this research", "grill me then synthesize", or hands over interviews, surveys, tickets, notes, whiteboard photos or FigJam boards and wants themes they can defend.
---

# /synthesize

Three stages: **grill → synthesize → verify and loop.** You (the main conversation) run the interview and the loop. The `workshop-synthesizer` agent does the synthesis; the `research-verifier` agent attacks it. Neither agent can talk to the person, which is why the questions live here.

## 1. Look before you ask

Before the first question, take stock of the material without synthesizing it:
- Glob or list the files, count sources by type (interviews, tickets, surveys, photos, boards).
- Skim enough to know what's there: who the participants seem to be, whether attributes (role, plan, tenure) are stated, roughly how long each source is.
- Note anything that will change the synthesis: a source that isn't research (a PRD, a sales deck), unreadable photos, a FigJam link with no FigJam tool available.

Say what you found in two lines, then start the interview.

## 2. Grill

Ask **one question at a time**, using AskUserQuestion where available. Every question carries your **recommended answer**, drawn from what you saw, as the first option. Push back on vague answers: "better onboarding" for whom, measured how?

Ask these, in order, and skip any the person already answered:

1. **The decision.** What will this synthesis help someone decide? (A research question with no decision behind it produces themes nobody uses.)
2. **The question.** What's the research question, in one sentence? If it assumes its answer ("confirm users want X"), rephrase it neutrally and offer that as the recommendation.
3. **The audience.** Who reads the report: the team doing the work, a PM, leadership? This sets how much the opening summary has to carry.
4. **Segments.** Which groups should be compared (admins vs solo users, new vs returning)? Recommend only groups the material actually labels.
5. **Hunches to test.** What do they already believe? List these as hypotheses the synthesis must confirm, contradict or leave open. They are never evidence.
6. **Out of scope.** Anything to exclude: sources, topics, a known issue that's already being fixed.

Stop early when the answers are clear; four good questions beat six tired ones. Then show a **brief of five lines or fewer** and ask the person to confirm or correct it:

```
Decision:   <what this informs>
Question:   <neutral research question>
Audience:   <who reads it>
Segments:   <groups to compare, or "none labelled">
Hypotheses: <H1 …; H2 …>   Exclude: <…>
```

If the person says "just run it", skip the interview, write the brief from what you saw, label it "assumed", and go on.

**Flags.** `/synthesize <sources> --quick` asks only the decision and the question. `--no-grill` asks nothing and writes every assumption into the brief. `--batch` asks all open questions at once instead of one at a time.

## 3. Synthesize

Spawn the `workshop-synthesizer` agent with: the confirmed brief, verbatim; every source path, URL or the pasted material; and the instruction to save the report (folder mode) or return it in full.

## 4. Verify and loop (at most 3 passes)

After each synthesizer pass, run both checks:

**a. The quote script.** For text sources on disk:
```bash
python3 ~/.claude/skills/synthesize/scripts/check_quotes.py <report.md> <source_dir>
```
Every `NOT FOUND` line is a flagged issue.

**b. The verifier.** Spawn a fresh `research-verifier` agent with the report, the brief and the sources. Never pass it the synthesizer's reasoning, only the report. It returns a numbered list of issues, each marked BLOCKING or MINOR, or "No blocking issues."

**Then:**
- No `NOT FOUND` lines and no BLOCKING issues → stop and report.
- Otherwise → send the synthesizer its own report plus the flagged issues only, in a **revision pass**: it fixes exactly those and changes nothing else. Then run both checks again.
- After pass 3, stop regardless. Anything still open goes into the report's "Unresolved after review" section, stated plainly.

Do not loop on MINOR issues alone. Pass them along in the final message.

## 5. Report back

In chat, briefly:
- where the report is saved (or the report itself, inline mode)
- the answer to the research question in two or three sentences, and what each hypothesis came to (supported, contradicted, open)
- passes taken, and what the checks caught along the way ("pass 1 dropped two quotes that weren't verbatim; the verifier downgraded Theme 3 from High to Medium")
- anything still unresolved

Don't paste the full report back when it was saved to a file.
