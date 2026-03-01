import re

# Positive and Negative word lists
positive_words = ["good", "great", "excellent", "amazing", "love", "nice", "awesome", "fantastic"]
negative_words = ["bad", "poor", "terrible", "worst", "hate", "awful", "disappointing"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    return words

def calculate_score(text):
    words = clean_text(text)
    score = 0

    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    return score

def get_sentiment(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"