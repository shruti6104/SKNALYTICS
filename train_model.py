import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

# 1. Sample Training Data (You can replace this with your dataset)
reviews = [
    "This product is amazing and works great",
    "Terrible product, waste of money",
    "Absolutely love it! Highly recommended",
    "Worst product ever, fake and cheap",
    "Satisfied with the purchase",
    "Fake product, totally disappointed"
]
labels = ["OR", "CG", "OR", "CG", "OR", "CG"]  # OR = Original, CG = CopyGenerated (fake)

# 2. Preprocessing + Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(reviews)

# 3. Train Model
model = LogisticRegression()
model.fit(X, labels)

# 4. Save model and vectorizer to model/ directory
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/fake_review_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Model and vectorizer saved in 'model/' folder.")
