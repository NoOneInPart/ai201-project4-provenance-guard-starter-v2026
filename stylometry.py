"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    sents = sentences(text)
    if len(sents) < 2:
        return 0.0

    lengths = [len(words(s)) for s in sents if len(words(s)) > 0]
    if len(lengths) < 2:
        return 0.0

    mean_len = statistics.mean(lengths)
    if mean_len == 0:
        return 0.0

    stdev_len = statistics.stdev(lengths)
    return round(stdev_len / mean_len, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words (lexical diversity).

    Returns:
        A float between 0.0 and 1.0. Higher means richer vocabulary with
        less repetition. Returns 0.0 for empty texts.
    """
    token_list = words(text)
    if not token_list:
        return 0.0
    return round(len(set(token_list)) / len(token_list), 4)


def punctuation_density(text: str) -> float:
    """
    Density of expressive punctuation marks per word.

    Counts expressive punctuation (commas, semicolons, colons, dashes,
    question marks, and exclamation marks) relative to total word count.

    Returns:
        A float. Higher density reflects varied, expressive punctuation
        common in human writing. Returns 0.0 for empty texts.
    """
    token_list = words(text)
    if not token_list:
        return 0.0

    marks = re.findall(r"[,;:\-—!?]", text)
    return round(len(marks) / len(token_list), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    token_list = words(text)
    if not token_list:
        return 0.5

    cv = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)

    # Invert and rescale each measure so higher = more AI-like
    # Sentence spread: AI typically clusters at 0.15-0.30; humans often exceed 0.60
    spread_ai = 1.0 - min(max((cv - 0.15) / (0.65 - 0.15), 0.0), 1.0)

    # Type-token ratio: Lower diversity -> more AI-like
    ttr_ai = 1.0 - min(max((ttr - 0.45) / (0.80 - 0.45), 0.0), 1.0)

    # Punctuation density: Lower expressive punctuation -> more AI-like
    punct_ai = 1.0 - min(max((punct - 0.02) / (0.12 - 0.02), 0.0), 1.0)

    # Weighted composite (50% sentence spread, 30% vocab variety, 20% punctuation)
    score = (0.50 * spread_ai) + (0.30 * ttr_ai) + (0.20 * punct_ai)
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")

