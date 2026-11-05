# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A piece of text submitted to Provenance Guard passes through a seven-step pipeline:

1. **Ingestion & Validation (`app.py::submit`):** The service receives a `POST` request with JSON containing `text` and `creator_id`. It validates that the payload is well-formed, non-empty, and within the 50,000-word limit, rejecting malformed requests with clean 400-level error codes.
2. **Provenance Assignment (`app.py::submit`):** The service generates an immutable, unique identifier (`content_id` via UUID4). This links the submission to its author and serves as the tracking handle for auditing and future appeals.
3. **Semantic Perplexity Signal (`detector.py::model_signal`):** The text is passed to a local causal language model (GPT-2). The model computes token perplexity to measure how statistically predictable the phrasing is, mapping the result to a normalized 0.0–1.0 score (`model_score`, where higher means more AI-like).
4. **Structural Stylometry Signal (`stylometry.py::style_signal`):** The text is analyzed mechanically without semantic comprehension. It measures sentence length variation (burstiness / coefficient of variation), vocabulary diversity (type-token ratio), and expressive punctuation density, combining them into a normalized 0.0–1.0 score (`style_score`, where higher means more AI-like).
5. **Signal Combination (`scoring.py::combine_signals`):** The combining rule applies a 60/40 weighted blend to merge `model_score` and `style_score` into a single composite `combined_score` (0.0 to 1.0).
6. **Label Classification & Confidence (`scoring.py::score_to_label`):** The composite score is compared against calibrated thresholds (`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.70`) to produce a categorical `guess` (`human`, `unsure`, or `ai`), a confidence percentage, and a respectful reader-facing explanation (`label`).
7. **Audit Logging & Response Dispatch (`audit.py::log_decision` & `app.py`):** The complete decision (timestamp, UUID, author, all three scores, and status `"decided"`) is appended as an immutable JSON line to `logs/audit.jsonl`, and the full JSON payload is returned to the client.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Token perplexity against a local causal language model (GPT-2), quantifying how statistically predictable each subsequent token is in context.

**Why that might differ between human and AI writing:**
Large language models generate text by repeatedly sampling statistically probable next tokens, producing remarkably smooth, expected transition sequences with low perplexity. Human writers wander—introducing abrupt tonal shifts, regional slang, uncommon metaphors, and creative vocabulary that repeatedly surprise the language model.

**What it can't see:**
It cannot distinguish **authorship** from **linguistic simplicity**. Authors writing in plain, direct English—such as non-native (ESL) speakers using safe, familiar vocabulary, younger students, or authors writing technical/encyclopedic documentation—produce highly predictable text that scores with high AI likelihood. Conversely, AI text specifically prompted to use archaic, baroque 19th-century prose spikes in perplexity and fools this detector into reporting "human."

### Signal two — the style signal

**What it measures:**
The physical, surface geometry of the text: sentence length variation (coefficient of variation: $\sigma / \mu$), vocabulary diversity (type-token ratio), and expressive punctuation density (commas, semicolons, dashes, colons, exclamations).

**Why that might differ between human and AI writing:**
AI-generated text naturally clusters around uniform, medium-length sentences (~14–18 words each) that march in rhythmic step with safe vocabulary repetition. Human writing is naturally bursty and irregular—frequently pairing a short three-word punchy sentence with a sprawling, forty-word clause loaded with expressive punctuation.

**What it can't see:**
It cannot comprehend meaning or context. Because it evaluates purely typographical geometry, trivial surface edits easily manipulate it: inserting intentional typos (which artificially inflates vocabulary variety), breaking long sentences with random punctuation, or injecting arbitrary dashes fools the stylometry engine into reporting high human burstiness on entirely synthetic text.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted linear combination of the model perplexity signal and the structural style signal. When the two signals disagree, the combined score lands toward the center ("unsure"). We weight the model signal slightly higher because GPT-2 measures token probability distributions across whole contexts, whereas surface stylometry heuristics can be disproportionately swayed by short texts or punctuation quirks.

**The numbers:**
- `WEIGHT_MODEL_SIGNAL = 0.6`
- `WEIGHT_STYLE_SIGNAL = 0.4`

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

- **Input:** `"The quick brown fox jumps over the lazy dog"`
- **Model signal (`detector.py`):** `0.0697` (confidently human — the distinct pangram is surprising to GPT-2).
- **Style signal (`stylometry.py`):** `0.7000` (confidently AI — because it is a single isolated sentence with zero expressive punctuation, sentence length spread is 0.0 and punctuation density is 0.0, which maxes out the AI-penalty components despite a high type-token ratio).
- **What the rule does with it:** The rule computes $0.6 \times 0.0697 + 0.4 \times 0.7000 = 0.3218$. Because the model signal carries 60% weight, it pulls the combined score down away from the high style score, landing it safely in the human/low-borderline zone ($0.3218 < 0.35$) and preventing a false AI accusation.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text. |
| unsure | 0.35 – 0.70 | We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either. |
| high-confidence AI | 0.70 – 1.00 | We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->
I worded the "unsure" label to place the burden of uncertainty squarely on the tool rather than the author. Using neutral phrasing like "we cannot reliably tell" and stating that patterns "could come from either" explicitly acknowledges the inherent limitations of statistical detection. This prevents casting suspicion or making false accusations against innocent human writers who simply write cleanly, concisely, or with conventional technical vocabulary.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "It is important to remember that education plays a vital role in personal development. In addition, schools provide students with the necessary tools to succeed in the future. Furthermore, teachers help students build critical thinking skills and foster a love for learning. Moreover, education enables individuals to explore new opportunities and achieve their personal goals. Therefore, investing in quality education is essential for the progress of modern society.", "creator_id": "ai_test"}'
```

```json
{
  "combined_score": 0.7816,
  "confidence": 0.7816,
  "content_id": "728968f5-12f3-4b07-814c-5defc3b06801",
  "guess": "ai",
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "model_score": 0.876,
  "style_score": 0.6401
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "728968f5-12f3-4b07-814c-5defc3b06801", "reasoning": "I wrote this paragraph for an education essay rubric following strict structural guidelines. Please have a human reviewer inspect it."}'
```

```json
{
  "content_id": "728968f5-12f3-4b07-814c-5defc3b06801",
  "message": "Your appeal has been received. Your submission status is now under review.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.6644,
      "content_id": "822c1ad6-02b0-4568-b117-9c51852bb23b",
      "creator_id": "wiki_test",
      "guess": "unsure",
      "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
      "model_score": 0.7289,
      "status": "decided",
      "style_score": 0.5677,
      "timestamp": "2026-10-31T23:32:25+00:00"
    },
    {
      "combined_score": 0.7816,
      "content_id": "728968f5-12f3-4b07-814c-5defc3b06801",
      "creator_id": "ai_test",
      "guess": "ai",
      "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
      "model_score": 0.876,
      "status": "decided",
      "style_score": 0.6401,
      "timestamp": "2026-10-31T23:32:35+00:00"
    },
    {
      "content_id": "728968f5-12f3-4b07-814c-5defc3b06801",
      "creator_id": "ai_test",
      "event": "appeal",
      "reasoning": "I wrote this paragraph for an education essay rubric following strict structural guidelines. Please have a human reviewer inspect it.",
      "status": "under_review",
      "timestamp": "2026-10-31T23:35:10+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Assistance formulating the acceptance criteria in `criteria.md` in a way that would be concrete and measurable.
- *What came back:* Specific mathematical definitions and statistical targets for false positives, separation spread, and malformed input handling.
- *What I changed:* Tweaked the target numbers (such as setting the required score spread to 0.40) and rewrote the wording to make each criterion less intensely technical and more plainly observable.

**Moment 2**

- *What I asked for:* Generating candidate text samples to test the AI detection boundary.
- *What came back:* Standard corporate/academic boilerplate about education with uniform sentence pacing and textbook transition phrases.
- *What I changed:* Kept the base text as the pure AI test case, and then manually created the "lightly edited AI" test sample by tweaking sentences.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
10 per minute provides generous headroom for an authentic writer who is iteratively revising drafts (rarely submitting more than 2–3 times per minute), but it immediately chokes automated scripts attempting high-speed threshold mapping or brute-force evasion attacks. 200 per day provides comfortable headroom for heavy legitimate drafting or full-day classroom use, while capping long-running scrapers from probing the model all day.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->
The limiter keys primarily on `creator_id`, falling back to the caller's remote IP address (`get_remote_address()`) if `creator_id` is empty or missing. Keying on `creator_id` ensures that multiple legitimate users sharing an IP address (such as students in a university computer lab, dorm, or household) do not inadvertently exhaust each other's quota, while the IP fallback prevents anonymous spammers or malformed requests from bypassing limits.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 200
  [ 9/15] 200
  [10/15] 200
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
============================================================

5 of 15 were rate limited. Paste the run above into your README
under **Rate Limiting**, and check GET /log recorded the rejections.

Wrote results\flood_2026-11-04_1614.md
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
