import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# === Ensure NLTK Downloads ===
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

# === Load Models ===
model = joblib.load("fake_review_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
lemmatizer = WordNetLemmatizer()

# === Text Preprocessing ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return ' '.join(words)

# === Main Verification Function ===
def verify_review(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    prediction = model.predict(vec)[0]
    confidence = model.predict_proba(vec).max()

    label = "✅ Genuine" if prediction == "OR" else "❌ Fake"
    color = "green" if prediction == "OR" else "red"

    # Influential keywords from vectorizer
    keywords = [w for w in cleaned.split() if w in vectorizer.get_feature_names_out()]

    return {
        "label": label,
        "color": color,
        "confidence": round(confidence * 100, 2),
        "keywords": keywords
    }
