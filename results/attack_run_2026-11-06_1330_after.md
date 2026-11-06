# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 13:30
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c5c5c8ae-7db6-4c61-a08a-959401076f94` | unsure | 0.500 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `a7ca1ae4-022b-41d2-a87a-cea21c966841` | unsure | 0.500 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d3440de4-b983-4a2f-b2a3-fd25b0c2e7c5` | unsure | 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ff8babd8-ef23-49c3-a534-19e08611bfc1` | unsure | 0.500 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `e6be1541-a4aa-4267-b4d8-f41d685682d0` | human | 0.769 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `e493e54e-7153-470e-90ca-cf8009d1ee6f` | unsure | 0.500 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `03903baf-e76c-4bf8-bf32-bf8937bf4e25` | unsure | 0.500 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `2e6b762c-91e1-4831-9dd9-f3553ea89c63` | unsure | 0.500 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `aad20b51-fc0c-4aca-bf93-63ae28afc9c6` | unsure | 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `f6a68fd5-e658-4527-8936-e2cd4d373e0d` | ai | 0.890 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `8dbd4fff-cbe3-46f6-bd2e-71fa837e65b9` | unsure | 0.500 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `f017e828-dcc8-4936-ae85-173f4d635e18` | ai | 0.718 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c6546f6d-7ae1-4753-9e24-ef0e29844653` | ai | 0.718 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `87f19925-4d59-4bfd-bc95-4cea021508b5` | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `2aef92a7-94be-4874-938e-cf17f88568cd` | ai | 0.776 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `e59366a3-dc0e-41fd-8599-b4aa6c77417c` | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e947ba8e-7eca-4468-bee5-2356bdf65730` | ai | 0.715 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `1360f1ae-43f6-4e2f-8be7-eeab370f23fb` | unsure | 0.500 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `451a1f83-a35c-467d-84b9-301949c72cf4` | unsure | 0.500 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `1435b895-8843-46e1-a9c0-231c4641e39f` | human | 0.817 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1388173d-40c0-425e-a264-665879e8c0df` | unsure | 0.500 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `fe53a8cc-756f-43c3-9b8d-710933f19bc8` | unsure | 0.500 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `bdaad775-6895-4923-9ef4-2f47b3ec73d3` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a5bed71b-0513-4730-b198-5800fc2c1fd1` | unsure | 0.500 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `d3a1017c-3bde-4beb-8ec3-5e53ec6b8710` | human | 0.720 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `b31660ac-8a28-4def-9d5b-9e971b89a82f` | human | 0.793 | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `aa32fa04-f7d5-4aeb-96b0-f6f407e4d8cf` | ai | 0.744 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2bc47ae1-d8b3-438f-8211-73a2627a9756` | human | 0.703 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f00a24bb-942e-4cf7-a23f-890ba3bc45e2` | human | 0.703 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `203f3f9a-d6e4-4286-b8f5-d8c5a6fdfd7b` | human | 0.703 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d7e47f11-f574-44ab-851f-2abaee939833` | human | 0.703 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `19df865f-8cb9-4da7-94b6-d26f667677b0` | human | 0.703 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `33aae632-7e40-490e-a1f5-33c99d9b5d61` | human | 0.703 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2279e7d3-a871-4814-9884-24cbffda64ad` | human | 0.703 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7ee0d349-8497-4362-b126-6854ac8d7a73` | human | 0.703 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2343f57b-76e3-4b55-a8dd-d3fbfbde7030` | human | 0.703 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2c5e7a86-6873-4fa5-8c29-5da6a1d2da1c` | human | 0.703 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c5c5c8ae-7db6-4c61-a08a-959401076f94",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.6351,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "a7ca1ae4-022b-41d2-a87a-cea21c966841",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.152,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "d3440de4-b983-4a2f-b2a3-fd25b0c2e7c5",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6662,
  "style_score": 0.3334,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "ff8babd8-ef23-49c3-a534-19e08611bfc1",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6114,
  "style_score": 0.5998,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "e6be1541-a4aa-4267-b4d8-f41d685682d0",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.7687,
  "model_score": 0.3212,
  "style_score": 0.0964,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "e493e54e-7153-470e-90ca-cf8009d1ee6f",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5727,
  "style_score": 0.2177,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "03903baf-e76c-4bf8-bf32-bf8937bf4e25",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5862,
  "style_score": 0.523,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "2e6b762c-91e1-4831-9dd9-f3553ea89c63",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2452,
  "style_score": 0.5672,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "aad20b51-fc0c-4aca-bf93-63ae28afc9c6",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.7042,
  "style_score": 0.3143,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "f6a68fd5-e658-4527-8936-e2cd4d373e0d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.89,
  "model_score": 0.9792,
  "style_score": 0.7561,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "8dbd4fff-cbe3-46f6-bd2e-71fa837e65b9",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6175,
  "style_score": 0.4708,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "f017e828-dcc8-4936-ae85-173f4d635e18",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7178,
  "model_score": 0.7387,
  "style_score": 0.6864,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c6546f6d-7ae1-4753-9e24-ef0e29844653",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7182,
  "model_score": 0.8051,
  "style_score": 0.5879,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "87f19925-4d59-4bfd-bc95-4cea021508b5",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8329,
  "style_score": 0.4833,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "2aef92a7-94be-4874-938e-cf17f88568cd",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7761,
  "model_score": 0.8005,
  "style_score": 0.7396,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "e59366a3-dc0e-41fd-8599-b4aa6c77417c",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.387,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "e947ba8e-7eca-4468-bee5-2356bdf65730",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7152,
  "model_score": 0.8816,
  "style_score": 0.4657,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "1360f1ae-43f6-4e2f-8be7-eeab370f23fb",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.3223,
  "style_score": 0.417,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "451a1f83-a35c-467d-84b9-301949c72cf4",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4625,
  "style_score": 0.2,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "1435b895-8843-46e1-a9c0-231c4641e39f",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.8169,
  "model_score": 0.2044,
  "style_score": 0.1512,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "1388173d-40c0-425e-a264-665879e8c0df",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.5069,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "fe53a8cc-756f-43c3-9b8d-710933f19bc8",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4998,
  "style_score": 0.4149,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "bdaad775-6895-4923-9ef4-2f47b3ec73d3",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6401,
  "style_score": 0.1786,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "a5bed71b-0513-4730-b198-5800fc2c1fd1",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5583,
  "style_score": 0.4835,
  "label": "We cannot reliably tell whether this was written by a person or an AI; it shows a mix of patterns that could come from either.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "d3a1017c-3bde-4beb-8ec3-5e53ec6b8710",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.72,
  "model_score": 0.0,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "b31660ac-8a28-4def-9d5b-9e971b89a82f",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.7933,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "aa32fa04-f7d5-4aeb-96b0-f6f407e4d8cf",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7438,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We think this was probably generated by an AI, based on highly uniform sentence structures and predictable phrasing.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "2bc47ae1-d8b3-438f-8211-73a2627a9756",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "f00a24bb-942e-4cf7-a23f-890ba3bc45e2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "203f3f9a-d6e4-4286-b8f5-d8c5a6fdfd7b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "d7e47f11-f574-44ab-851f-2abaee939833",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "19df865f-8cb9-4da7-94b6-d26f667677b0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "33aae632-7e40-490e-a1f5-33c99d9b5d61",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "2279e7d3-a871-4814-9884-24cbffda64ad",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "7ee0d349-8497-4362-b126-6854ac8d7a73",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "2343f57b-76e3-4b55-a8dd-d3fbfbde7030",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "2c5e7a86-6873-4fa5-8c29-5da6a1d2da1c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7028,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was probably written by a person, based on the natural rhythm and varied phrasing of the text.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
