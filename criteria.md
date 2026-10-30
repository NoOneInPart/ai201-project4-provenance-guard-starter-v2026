# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False Positive Rate on Human Writing

Of 10 distinct samples of verified human writing, at most 1 (<= 10%) is classified with the guess `"ai"`.

**Why this target:**
Falsely accusing a real writer of using AI destroys user trust and inflicts unfair disciplinary or reputational damage. Allowing at most 1 false accusation in 10 ensures the threshold errs on the side of caution, pushing questionable human writing into `"unsure"` or `"human"` rather than an outright `"ai"` verdict.

---

## 2. Score Separation Between Clear Human and Clear AI Text

The mean `combined_score` of 5 clearly-AI text samples is at least 0.40 points higher than the mean `combined_score` of 5 clearly-human text samples (on the 0.0 to 1.0 scale).

**Why this target:**
If the score gap between obvious human writing and obvious AI output is narrower than 0.40, the system's signals lack sufficient discriminative power. Demanding a 0.40 separation requires clear divergence between AI and human distributions, leaving room for an `"unsure"` buffer zone without constant boundary overlap.

---

## 3. Label Reachability and Coverage

Across a test suite of diverse inputs (clear human, borderline, and clear AI), each of the three discrete guesses (`"human"`, `"unsure"`, and `"ai"`) appears at least once in the response.

**Why this target:**
All three labels must be active in production. If `"unsure"` is never triggered, the service has collapsed into an aggressive binary classifier that ignores signal disagreement; if either boundary label is unreachable, the scoring thresholds are miscalibrated.

---

## 4. Graceful Rejection of Malformed Input

100% (4 of 4) of malformed requests (empty text string `""`, missing `"text"` field, `null` text value, and an oversized text payload > 50,000 words) return an HTTP 4xx client error status code rather than causing a 500 server crash or returning a false 200 OK.

**Why this target:**
Uncaught exceptions crash service threads and fail silently without leaving an auditable trace. A robust API must reject invalid payloads at the route perimeter with clean 400-level error messages so callers know what failed.

---

## 5. Appeal Path Integrity and State Transition

100% (5 of 5) of submitted appeals to `POST /appeal` with an existing `content_id` successfully return HTTP 200 and record an `under_review` status entry in `audit.log`.

**Why this target:**
The appeal system is the sole safeguard protecting wrongfully accused writers. If an appeal fails to log or fails to transition the submission's status to `under_review`, the writer is effectively disenfranchised and the automated verdict stands without remedy.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
