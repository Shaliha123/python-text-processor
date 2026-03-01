import re
from collections import Counter

# Word dictionaries
positive_words = {
    "good", "great", "excellent", "amazing",
    "love", "best", "nice", "awesome", "fantastic"
}

negative_words = {
    "bad", "worst", "poor", "terrible",
    "hate", "awful", "disappointing", "boring"
}

negation_words = {"not", "no", "never", "n't"}


def calculate_score(review):
    score = 0

    review = review.lower()

    # Extract proper words only
    words = re.findall(r'\b\w+\b', review)

    word_counts = Counter(words)

    for i, word in enumerate(words):

        multiplier = 1

        # STEP 2 — Negation Handling
        if i > 0 and words[i - 1] in negation_words:
            multiplier = -1

        # STEP 3 — Repetition Control
        # Limit repeated word impact to max 3 times
        repetition_limit = min(word_counts[word], 3)

        if word in positive_words:
            score += multiplier * repetition_limit

        elif word in negative_words:
            score -= multiplier * repetition_limit

    return score


def assign_sentiment(score):
    if score > 1:
        return "Positive"
    elif score < -1:
        return "Negative"
    else:
        return "Neutral"