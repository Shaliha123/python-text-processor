import os

# Positive and negative words
positive = ["good", "nice", "excellent", "happy"]
negative = ["bad", "terrible", "worst", "poor"]

# Get all text files from folder
files = os.listdir()

for file in files:
    if file.endswith(".txt"):   # only read txt files
        with open(file, "r") as f:
            text = f.read().lower()

        score = 0

        # Check positive words
        for word in positive:
            score += text.count(word)

        # Check negative words
        for word in negative:
            score -= text.count(word)

        print("File:", file)
        print("Score:", score)

        if score > 0:
            print("Positive Review 😊")
        elif score < 0:
            print("Negative Review 😞")
        else:
            print("Neutral Review 😐")

        print("--------------------")
