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

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2bb56c79-b76c-48c5-befb-132bea857962` | unsure | 0.500 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `f640514c-7251-4c2d-aeb7-0dd2bdf853a3` | unsure | 0.500 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `98b61cde-57ec-40b0-980f-7150efa81d1a` | unsure | 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `838e965a-9987-40c6-a1fb-026f445a0027` | unsure | 0.500 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `5502dbab-8fd8-4300-a53f-9549d5d42d43` | human | 0.769 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2a990a00-c1e8-45f6-b9c3-97498cbfcd8d` | unsure | 0.500 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `d3be11f0-fc01-4a3e-bcd5-54cce4bb31fc` | unsure | 0.500 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `bec2fd28-546f-4a56-8b70-a60d5ccb6b08` | unsure | 0.500 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `5759f0e0-8eb5-4708-ab3d-70eecf99e675` | unsure | 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `95da49ed-a2b5-40d6-9a70-705dc51b2fdf` | ai | 0.890 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `218338de-0234-4587-bd85-f1e7f1a3fc5d` | unsure | 0.500 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `999d7828-a04e-497a-a9a1-1241d6193b26` | ai | 0.718 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c4592df6-c1ca-4adc-940d-9670cf96b70c` | ai | 0.718 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `42558784-cb5e-4442-bb64-224ebd8f3c42` | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `5bd1608c-cda6-4161-9513-6bafc313f68d` | ai | 0.776 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `8015adb3-430d-433a-9c8a-1d68a4fe2872` | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `8401c63c-2e79-4c4e-b0d6-4ee4cbd18b02` | ai | 0.715 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `8f4d68bb-1bd0-4f6f-99ac-c51c0cbd3b27` | unsure | 0.500 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `00e2b112-2e8d-442c-8931-6b42abb55caa` | unsure | 0.500 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `4435d90f-aa5f-403d-b27c-781f9c3558a7` | human | 0.817 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `ea2bb295-7cad-4d36-a932-1931be38cafb` | unsure | 0.500 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `cd7bfb79-8fbe-4dbf-ae9d-2120d4646b63` | unsure | 0.500 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `e4b04168-c656-4eef-b54d-58ccc7536101` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4f776159-d5a2-4770-9981-4e5110cfa91e` | unsure | 0.500 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `9d0fc47b-8541-4eee-9a92-1d1228b1089a` | human | 0.720 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `4c02d146-84a7-4142-94aa-d90bcd4c7612` | human | 0.793 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `cb642f61-db3c-43b7-b332-b75c3bcee828` | ai | 0.879 | HELD |
| MF06 | malformed | text is emoji only | 200 | `4b25b39c-0a43-49ac-92a7-8388ab9fb992` | ai | 0.798 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `bd2b72f7-e407-4c6b-8782-0510980a5012` | ai | 0.744 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `8b874cfe-35cf-42ae-8509-e937162bc831` | ai | 0.881 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ec004ef9-c327-4592-8ff0-6120683e4729` | human | 0.703 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5a2a86f7-e928-46aa-ac35-1047e7a14fec` | human | 0.703 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2974234c-ace0-48eb-8f15-40b0246fce7d` | human | 0.703 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3bd1d377-83d5-415d-a62f-b86896295f37` | human | 0.703 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `18329f5f-b134-4058-8244-dcfbb21ddbd1` | human | 0.703 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1a477404-91b6-4d4e-bf37-ec8f1b1ec5c5` | human | 0.703 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ffbc0358-5f96-43e5-a2f1-7c18f84d3c43` | human | 0.703 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aae77242-373e-4f4a-8964-960a7f452195` | human | 0.703 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2745f020-5c0f-44db-a1fa-052291801bd2` | human | 0.703 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e504dd0d-9608-41ce-9abb-c284a14cc372` | human | 0.703 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

These ten entries highlight the core structural blind spots, evasion vulnerabilities, injection resistance, and perimeter enforcement of the service:
- **`attacker_FP03` (False positive on ESL writer):** Careful, simple word choices scored high predictability (`model_score: 0.8051`), unjustly triggering a high-confidence AI verdict (`0.7182`).
- **`attacker_FP02` (False positive on formal register):** Academic human prose was misread as synthetic due to standard phrasing (`model_score: 0.7387`, `combined: 0.7178`).
- **`attacker_FP05` (False positive on technical docs):** Clear, structured technical instructions crossed the AI threshold (`0.7761`).
- **`attacker_FP07` (False positive on deliberate repetition):** Intentional human rhetorical repetition lowered burstiness, scoring `0.7152` (AI).
- **`attacker_EV01` (Evasion via typos):** Injected typos artificially inflated lexical diversity, dragging AI text down into the `unsure` band (`0.3521`).
- **`attacker_EV05` (Evasion via heavy editing):** Human editing broke the model and style signals, completely fooling the detector into a confident `"human"` pass (`0.2313`).
- **`attacker_EV10` (Defense held on stanzas):** Despite verse formatting, overwhelming token predictability (`0.9792`) allowed the system to correctly identify AI text (`0.8900`).
- **`attacker_PI02` (Prompt injection treated as text):** The instruction to override the system was treated purely as statistical text and failed to hijack the service.
- **`attacker_MF01` (Perimeter validation rejection):** Whitespace-only submission was rejected with HTTP 400 and recorded in the ledger with `reason: "missing_or_empty_text"`.
- **`attacker_flood` (Rate limit rejection):** Rapid burst submissions past the 10/min threshold were throttled with HTTP 429 and recorded with `reason: "rate_limited"`.

```json
{"timestamp": "2026-11-05T00:28:00+00:00", "content_id": "c4592df6-c1ca-4adc-940d-9670cf96b70c", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.5879, "combined_score": 0.7182, "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.", "status": "decided"}
{"timestamp": "2026-11-05T00:28:00+00:00", "content_id": "999d7828-a04e-497a-a9a1-1241d6193b26", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.6864, "combined_score": 0.7178, "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.", "status": "decided"}
{"timestamp": "2026-11-05T00:28:01+00:00", "content_id": "5bd1608c-cda6-4161-9513-6bafc313f68d", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.7396, "combined_score": 0.7761, "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.", "status": "decided"}
{"timestamp": "2026-11-05T00:28:01+00:00", "content_id": "8401c63c-2e79-4c4e-b0d6-4ee4cbd18b02", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.4657, "combined_score": 0.7152, "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.", "status": "decided"}
{"timestamp": "2026-11-05T00:27:57+00:00", "content_id": "2bb56c79-b76c-48c5-befb-132bea857962", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.6351, "combined_score": 0.3521, "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.", "status": "decided"}
{"timestamp": "2026-11-05T00:27:59+00:00", "content_id": "5502dbab-8fd8-4300-a53f-9549d5d42d43", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.0964, "combined_score": 0.2313, "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.", "status": "decided"}
{"timestamp": "2026-11-05T00:28:00+00:00", "content_id": "95da49ed-a2b5-40d6-9a70-705dc51b2fdf", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.7561, "combined_score": 0.89, "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.", "status": "decided"}
{"timestamp": "2026-11-05T00:28:02+00:00", "content_id": "4435d90f-aa5f-403d-b27c-781f9c3558a7", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.1512, "combined_score": 0.1831, "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.", "status": "decided"}
{"timestamp": "2026-11-05T00:28:03+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "missing_or_empty_text"}
{"timestamp": "2026-11-05T00:28:07+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**Attack FP03 (Content ID: `c4592df6-c1ca-4adc-940d-9670cf96b70c`)** — a non-native English speaker writing carefully and plainly in English. 

The student chose clean, standard words and simple sentence structures to avoid grammatical errors. Because ordinary, straightforward vocabulary is statistically easy for GPT-2 to predict, `detector.py` returned a punishing `model_score` of `0.8051`. Blended with an orderly `style_score` of `0.5879`, the composite score was `0.7182`—crossing our `0.70` threshold and falsely branding the student's authentic work as **High-Confidence AI**. Explaining to an earnest second-language writer that they were accused of cheating precisely *because* they worked hard to write clearly and grammatically is the most damaging failure mode an automated detector can produce.



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False Positive Rate on Human Writing | <= 10% (<= 1 in 10) | 2/10 (20%) | 2/10 (20%) | 2/10 (20%) | FAIL |
| 2. Score Separation (Mean AI - Human) | >= 0.40 separation | 0.1444 gap | 0.1444 gap | 0.1444 gap | FAIL |
| 3. Label Reachability and Coverage | all 3 guesses appear | 0H, 3U, 0A | 0H, 3U, 0A | 0H, 3U, 0A | FAIL |
| 4. Malformed Input Rejection | 100% 4xx (4 of 4) | 3/4 (75%) | 3/4 (75%) | 3/4 (75%) | FAIL |
| 5. Appeal Path Integrity | 100% 200 + log (5 of 5) | 5/5 (100%) | 5/5 (100%) | 5/5 (100%) | PASS |

**Real output for each criterion from one of the runs**, pasted as text, naming the file and function that produced it:

### Criterion 1: False Positive Rate on Human Writing
- **Produced by:** `run_eval.py::main` (calling `app.py::submit` and `scoring.py::combine_signals`)
- **Source file:** `results/run_2026-11-06_1208_before.md` (`my own writing`, Trial 1)

*Sample 1A: False positive on authentic human analysis (Text 5)*
```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.7762,
  "model_score": 0.8149,
  "style_score": 0.7181,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "sent": "I think the issue of whether this constitutes a privacy violation or n"
}
```
> This was a genuine student reflection discussing terms of service and navigation devices. Because the argument uses formal conditional phrasing ("If the privacy policy...", "If the customer hits Agree..."), GPT-2 found the vocabulary sequence highly predictable (`model_score: 0.8149`), and stylometry penalized its uniform sentence cadence (`style_score: 0.7181`), causing a severe false accusation.

*Sample 1B: Clear human pass with lively voice (Text 1)*
```json
{
  "status": 200,
  "guess": "human",
  "confidence": 0.6947,
  "model_score": 0.4569,
  "style_score": 0.0778,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "sent": "So the other day I was walking down this street when 10 really aggress"
}
```
> Conversational storytelling with irregular sentence lengths and dramatic exclamations. The extreme variance in sentence length produced a rock-bottom style score (`0.0778`), correctly driving the verdict into the `"human"` zone.

---

### Criterion 2: Score Separation Between Clear Human and Clear AI Text
- **Produced by:** `run_eval.py::main` (calling `app.py::submit`)
- **Source file:** `results/run_2026-11-06_1208_before.md` (`score separation`, Trial 1)

*Sample 2A: Human technical explanation (Text 2)*
```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4963,
  "style_score": 0.2785,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "sent": "A slightly more advanced encryption method is XOR, which simply takes "
}
```
> A human explanation of XOR encryption in visual novels. Natural human pacing kept `style_score` low (`0.2785`), but technical terminology kept `model_score` near the midpoint (`0.4963`), yielding a combined score of $0.409$.

*Sample 2B: Synthetic text with rare terminology (AI Text 4)*
```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2716,
  "style_score": 0.5706,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "sent": "Machine learning models rely heavily on high-quality training datasets"
}
```
> This illustrates why the separation gap collapsed to $0.1444$: even though this was 100% synthetic prose, specialized terms ("cross-validation", "overfitting", "distribution artifacts") surprised GPT-2, giving an unexpectedly low `model_score` of `0.2716` and dragging the combined score down to $0.3912$.

---

### Criterion 3: Label Reachability and Coverage
- **Produced by:** `run_eval.py::main` (calling `app.py::submit`)
- **Source file:** `results/run_2026-11-06_1208_before.md` (`label coverage`, Trial 1)

*Sample 3: Balanced borderline prose landing in "unsure"*
```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.3376,
  "style_score": 0.4773,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "sent": "Distributed version control systems changed how software development t"
}
```
> The sample successfully tested the middle ground: moderate predictability and balanced clauses produced a combined score of $0.3935$, which landed safely inside the $0.35$–$0.70$ `"unsure"` band without forcing a false binary choice.

---

### Criterion 4: Graceful Rejection of Malformed Input
- **Produced by:** `run_eval.py::main` (calling `app.py::submit`)
- **Source file:** `results/run_2026-11-06_1208_before.md` (`malformed input`, Trial 1)

*Sample 4A: Clean perimeter rejection on missing payload*
```json
{
  "status": 400,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "sent": "{\"creator_id\": \"eval_bad_missing\"}"
}
```
> The route handler intercepted the omitted `text` field at the perimeter, refusing to invoke the scoring pipeline and returning HTTP 400.

*Sample 4B: Input size check failure (50,000-word payload)*
```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.9985,
  "model_score": 0.9975,
  "style_score": 1.0,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "sent": "word word word word word word word word word word word word word word "
}
```
> The service lacked a maximum character/word bound check. Instead of rejecting the massive 50,000-word payload with HTTP 400 or 413, the server processed the entire string, saturating the detector and returning a 200 OK.

---

### Criterion 5: Appeal Path Integrity and State Transition
- **Produced by:** `scratch/test_criterion5.py` (calling `POST /appeal`)
- **Source file:** `results/criterion5_appeals.json` (Trial 1)

*Sample 5: Successful state transition and audit logging*
```json
{
  "content_id": "abf5a367-16d3-4cba-a006-4e6446640b74",
  "creator_id": "appeal_t1_u1",
  "status": 200,
  "response": {
    "content_id": "abf5a367-16d3-4cba-a006-4e6446640b74",
    "message": "Your appeal has been received. Your submission status is now under review.",
    "ok": true,
    "status": "under_review"
  }
}
```
> The appeal route looked up the existing submission in `audit.log`, verified its validity, transitioned its status to `under_review`, and returned HTTP 200, fulfilling the safeguard for contested verdicts.

**Diagnoses**

### Criteria Summary
- **Criterion 1 (False Positive Rate):** **MISSED** (Target $\le 10\%$; Trials produced 20%, 20%, 20%).
- **Criterion 2 (Score Separation):** **MISSED** (Target $\ge 0.40$; Trials produced 0.1444, 0.1444, 0.1444).
- **Criterion 3 (Label Coverage):** **MISSED** (Target all 3 labels; all 3 trials produced only `"unsure"`).
- **Criterion 4 (Malformed Input Rejection):** **MISSED** (Target 100% 4xx; Trials produced 75%, 75%, 75%).
- **Criterion 5 (Appeal Path Integrity):** **MET** (Target 100%; Trials produced 100%, 100%, 100%).

---

### Diagnoses by Criterion Miss

#### 1. Criterion 1 Miss (20% False Positive Rate on Own Writing)
- **Stage:** Signal One (`detector.py::perplexity`) and Combining Rule (`scoring.py::combine_signals`).
- **Mechanism:** Two authentic human samples (Text 3 explaining Yahoo password breaches and Text 5 analyzing terms of service) discussed technical/legal topics using disciplined conditional logic ("If the privacy policy...", "Passwords are secure data..."). Because standard expository phrasing is statistically common in GPT-2 training data, Signal One assigned high AI predictability (`model_score: 0.6946` and `0.8149`). Blended at 60% with moderate style scores ($0.736$ and $0.718$), both exceeded the `0.70` threshold (`0.7112` and `0.7762`), causing false accusations on legitimate analytical writing.

#### 2. Criterion 2 Miss (Score Separation Gap Collapsed to 0.1444)
- **Stage:** Signal One (`detector.py`) and Signal Two (`stylometry.py`).
- **Mechanism:** The separation between clear human prose ($0.3468$) and clear AI prose ($0.4912$) shrank to $0.1444$ due to two symmetric signal distortions:
  1. *Human compression:* Disciplined human explanations (XOR encryption, fair use) produced low sentence spread, elevating their `style_score` into the $0.20$–$0.28$ range.
  2. *AI compression:* Synthetic paragraphs containing domain-specific jargon (machine learning cross-validation, microservices) surprised GPT-2, lowering `model_score` down to $0.2716$. Both distributions collapsed into the middle.

#### 3. Criterion 3 Miss (Label Coverage Limited to "Unsure")
- **Stage:** Label Mapping (`scoring.py::score_to_label`) and Threshold Boundaries (`config.py`).
- **Mechanism:** The test inputs for label coverage scored $0.5670$ (AI testing text), $0.6231$ (dictionary definition of irony), and $0.3935$ (distributed version control). All three fell between `HUMAN_THRESHOLD = 0.35` and `AI_THRESHOLD = 0.70`. Because the combining rule averages two noisy signals, intermediate values dominate unless an input exhibits extreme anomalies across both signals simultaneously. Neither `"human"` nor `"ai"` was triggered in this scenario.

#### 4. Criterion 4 Miss (50,000-Word Payload Accepted)
- **Stage:** Route (`app.py::submit`).
- **Mechanism:** The route perimeter validates missing keys and null values (`if not text or not str(text).strip()`), but lacks an upper bound check on string length or word count. When a 50,000-word payload was submitted, the route processed it completely. Tokenizing 50,000 identical repetitions of `"word"` saturated the perplexity model (`model_score: 0.9975`) and stylometry (`style_score: 1.0`), returning HTTP 200 with an AI verdict instead of a 400 or 413 client error.

---

### Diagnoses of Broken Attacks from the Attack Run

#### 1. Attack MF02 Crash (Single-character input threw HTTP 500)
- **Stage:** Route (`app.py::submit`).
- **Mechanism:** A single character `"x"` passed route validation (`bool("x".strip()) == True`), but `detector.py::perplexity` requires at least two tokens to calculate loss (`if encoded["input_ids"].shape[1] < 2: raise ValueError(...)`). The uncaught `ValueError` escaped the route handler and escalated into an unhandled HTTP 500 Internal Server Error.

#### 2. Evasion Attacks EV01–EV09 (Synthetic text classified as "unsure" or "human")
- **Stage:** Signal Two (`stylometry.py`) and Combining Rule (`scoring.py::combine_signals`).
- **Mechanism:** The evasion attacks applied cheap surface perturbations: injecting typos (EV01), splicing quotations (EV03), or fragmenting clauses (EV02, EV06). Stylometry measures text *as text* without semantic comprehension: typos inflated unique token counts (`type_token_ratio`), and fragmented sentences artificially boosted `sentence_length_spread`. This dragged `style_score` down into the $0.09$–$0.35$ range. Weighted at 40%, this pulled the combined score below `0.70`, letting synthetic text evade the AI label.

#### 3. False Positive Attacks FP02, FP03, FP05, FP07 (Human text classified as "ai")
- **Stage:** Signal One (`detector.py`) and Threshold Setting (`config.py`).
- **Mechanism:** Non-native English speakers writing carefully (FP03) and authors of technical docs (FP05) or formal prose (FP02) deliberately select common, unambiguous words and uniform sentences to ensure clarity. GPT-2 finds ordinary vocabulary statistically easy to predict, scoring `model_score > 0.73`. Because `AI_THRESHOLD` was set at `0.70`, the system punished writers for grammatical discipline.

---

### The Pattern Across the Misses

Two fundamental architectural patterns explain all the misses:
1. **Perimeter Boundary Blindness:** The route (`app.py`) only checked whether text was present, completely ignoring input scale: ultra-short inputs (< 2 tokens) crashed the tokenizer into a 500 error, while ultra-long inputs (> 50,000 words) bypassed validation to consume unconstrained compute.
2. **Predictability Conflated with Authorship:** Signal One relies entirely on statistical likelihood. Anyone writing with plain, disciplined grammar (academic explanations, privacy policies, ESL drafting) scores high on predictability and is penalized. Conversely, Signal Two relies entirely on surface mechanics (length variance, TTR), allowing attackers to bypass detection simply by introducing typos or uneven sentence fragments.



---

## The Improvement

**What I changed:**
Hardened perimeter input validation and error handling on `POST /submit` in [`app.py`](file:///c:/Users/t0mbu/Desktop/ai201/ai201-project4-provenance-guard-starter-v2026/app.py#L221-L235):
1. **Lower-Bound Token Guard:** Added a check requiring at least 2 words (`len(text.strip().split()) < 2`) and wrapped signal calls in `try...except ValueError` to catch any tokenizer bounds errors from `detector.py`, logging rejection reason `"text_too_short"` / `"text_unscoreable"` and returning HTTP 400.
2. **Upper-Bound Payload Guard:** Lowered the oversized payload threshold to reject any text $\ge 10,000$ words with HTTP 400, logging rejection reason `"text_too_large"`.

**Which diagnosis pointed at it:**
1. **Attack MF02 Crash Diagnosis:** Pointed directly at the unhandled `ValueError` when single-character or sub-2-token inputs bypassed route checks and crashed `detector.py::perplexity` with an HTTP 500 error.
2. **Criterion 4 Miss Diagnosis:** Pointed at the lack of an effective upper bound check on submission length, allowing a 50,000-word payload to bypass route validation and return HTTP 200 OK instead of HTTP 400.

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
