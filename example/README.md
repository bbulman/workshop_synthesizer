# The example study

A small, made-up onboarding study for a fictional app called Spark: four interviews and three support tickets, in [`notes/`](notes/). It's built to catch the ways a synthesis goes wrong, so you can see whether the agents do their job before you trust them with real research.

## Try it

```bash
cd example
```

Then, in Claude Code:

```
/synthesize notes/
```

When the grill asks for your hunches, offer this one: **"People drop off because onboarding is too long."** The data contradicts it, and a good run says so.

## What's planted

| # | Planted | Where | A good run… |
|---|---|---|---|
| 1 | **A split by segment.** Solo users resent the integrations step; admins chose Spark because of it. | Solo: P01 03:09, P03 01:02, T01. Admins: P02 01:58, P04 01:20 | …shows the split as a segment finding (or theme plus counter-evidence) and fills the segment table. **Fails** if it writes "reactions to the integrations step were mixed." |
| 2 | **A strong shared theme.** Nobody can tell how far through setup they are. | All four participants (P01 04:44, P02 03:36, P03 05:13, P04 08:16) plus T03 | …rates it High, 4 of 4 participants. |
| 3 | **A hypothesis the data contradicts.** "Onboarding is too long." | P03 05:13 "It wasn't long exactly", P04 08:16 "Not the length." | …marks the hypothesis **Contradicted** and points at the progress theme instead. **Fails** if it marks it supported because people mention setup. |
| 4 | **A problem one segment has after setup.** Team staff land on an empty dashboard. | P04 04:04, T02 | …keeps it, at Medium (one interview plus a ticket), labelled as team staff. |
| 5 | **A single-source issue.** Trial-to-paid billing is unclear. | P03 08:50 only | …lists it as an outlier or a Low theme, with a suggested follow-up in Gaps. **Fails** if it's promoted to a finding about "users". |
| 6 | **An admin wish in the middle source.** Admins want control over staff setup. | P02 06:09 and P04 11:44 | …finds both. Missing P02's half is the "lost in the middle" failure the coverage check exists for. |
| 7 | **Quotes that invite paraphrase.** | P01 03:09 "I almost closed the tab", P03 02:24 "I counted, it asked me three times" | …quotes them exactly. "I almost quit" or "it kept asking me" fails the gate. |

## The quote gate on its own

[`bad-report.md`](bad-report.md) is a short report with four quotes: one exact, one paraphrased, one stitched together from two interviews, and one with a word changed. Run the gate on it:

```bash
python3 ../skills/synthesize/scripts/check_quotes.py bad-report.md notes/
```

It should pass the first quote and print `NOT FOUND` for the other three.
