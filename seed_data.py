"""
Run once to pre-populate sample feedback data.
Usage: python seed_data.py
"""
import json, os
from textblob import TextBlob

DATA_FILE = "data/feedbacks.json"

samples = [
    ("Alice Johnson",  "Product",  "The product quality is outstanding! Really happy with my purchase.", 5),
    ("Bob Smith",      "Support",  "Support team was slow to respond. Took 3 days to get a reply.", 2),
    ("Carol Davis",    "Delivery", "Delivery was super fast and packaging was perfect.", 5),
    ("David Lee",      "Product",  "Average product. Nothing special but does the job.", 3),
    ("Eva Martinez",   "Support",  "Absolutely terrible customer service experience.", 1),
    ("Frank Wilson",   "Delivery", "Package arrived late and was damaged. Very disappointed.", 1),
    ("Grace Kim",      "Product",  "Love it! Best purchase I have made this year.", 5),
    ("Henry Brown",    "Support",  "Support resolved my issue instantly. Very helpful!", 5),
    ("Irene Clark",    "Delivery", "Neutral experience. Delivery was on time, nothing more.", 3),
    ("James White",    "Product",  "Product broke after a week. Horrible quality.", 1),
    ("Karen Hall",     "Billing",  "Billing was straightforward and no hidden fees.", 4),
    ("Leo Turner",     "Billing",  "Got double charged. Still waiting for refund.", 1),
    ("Mia Adams",      "Other",    "Overall a great experience with the company.", 5),
    ("Noah Evans",     "Product",  "Decent product but overpriced for what you get.", 3),
    ("Olivia Scott",   "Support",  "Had to contact support three times for one issue.", 2),
]

os.makedirs("data", exist_ok=True)
data = []
for i, (name, cat, text, rating) in enumerate(samples):
    blob = TextBlob(text)
    pol  = round(blob.sentiment.polarity, 3)
    sub  = round(blob.sentiment.subjectivity, 3)
    label = "Positive" if pol > 0.1 else ("Negative" if pol < -0.1 else "Neutral")
    data.append({
        "id": i + 1,
        "name": name,
        "category": cat,
        "feedback": text,
        "rating": rating,
        "polarity": pol,
        "subjectivity": sub,
        "sentiment": label,
        "timestamp": f"2024-{(i % 12) + 1:02d}-{(i * 2 + 1):02d} 10:00:00",
    })

with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Seeded {len(data)} feedbacks into {DATA_FILE}")
