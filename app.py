import streamlit as st
import joblib
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from io import BytesIO
from fpdf import FPDF

# === Custom Modules ===
from product_compare import get_product_comparison
from summarizer import summarize_reviews
from review_verifier import verify_review
from sentiment_analyzer import analyze_sentiment
from review_summarizer import summarize_reviews_gpt
from web_scraper import scrape_amazon
from pdf_generator import generate_pdf

# === Streamlit Page Setup ===
st.set_page_config(page_title="Sknalytics - Beauty Review Analyzer", layout="centered", page_icon="💄")
st.title("💄 Sknalytics: Beauty & Skincare Review Analyzer")
st.caption("An AI-powered tool to detect fake reviews, summarize insights, compare prices, and help with smarter product decisions.")

# === Setup NLTK ===
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

lemmatizer = WordNetLemmatizer()

# === Load Model ===
model = joblib.load("model/fake_review_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# === Preprocessing ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return ' '.join(words)

# === Review Authenticity Checker ===
st.markdown("---")
st.header("🧠 Review Authenticity Checker")

user_review = st.text_area("📝 Enter a product review to verify:", height=130)
if st.button("✅ Check Review Authenticity"):
    if user_review.strip():
        result = verify_review(user_review)
        st.markdown(f"### 🎯 <span style='color:{result['color']}'>{result['label']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Confidence Score:** `{result['confidence']}%`")
        st.progress(int(result['confidence']))
        if result['keywords']:
            st.success("Model influenced by: `" + "`, `".join(result['keywords']) + "`")
        else:
            st.info("No keywords matched training data.")
    else:
        st.warning("⚠️ Please enter a valid review.")

# === Sentiment Analysis ===
st.markdown("---")
st.header("🧾 Sentiment Analysis")
sentiment_input = st.text_area("📘 Enter a review to analyze sentiment:", height=120)
if st.button("🧠 Analyze Sentiment"):
    if sentiment_input.strip():
        result = analyze_sentiment(sentiment_input)
        st.markdown(f"### Sentiment: <span style='color:{result['color']}'>{result['sentiment']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Polarity Score:** `{result['polarity']}`")
    else:
        st.warning("⚠️ Please enter a review.")

# === AI Review Summarizer ===
st.markdown("---")
st.header("🧠 AI Review Summarizer")
multi_reviews = st.text_area("Paste multiple product reviews below (1 per line):", height=200)
if st.button("📝 Generate Summary"):
    reviews_list = [r.strip() for r in multi_reviews.split("\n") if r.strip()]
    if reviews_list:
        summary = summarize_reviews_gpt(reviews_list)
        st.markdown("### 📋 Summary:")
        st.success(summary)
    else:
        st.warning("⚠️ Please paste at least 1 review.")

# === Live Amazon Price & Ratings ===
st.markdown("---")
st.header("💸 Live Product Price & Rating Fetcher")
product_query = st.text_input("🔍 Enter a Product Name (e.g. Garnier Vitamin C Serum)")
if st.button("Fetch Results"):
    with st.spinner("🔎 Searching Amazon..."):
        data = scrape_amazon(product_query)
    if data:
        df = pd.DataFrame(data)
        st.subheader("📦 Top Results from Amazon:")
        st.dataframe(df)
        for row in data:
            st.markdown(f"[🔗 {row['Product']}]({row['URL']}) - ₹{row['Price (₹)']} | ⭐ {row['Rating']}")
    else:
        st.error("No results or connection error.")

# === PDF Generation ===
if st.button("📄 Generate PDF Summary"):
    if 'data' in locals():
        pdf_file = generate_pdf(data, product_query, filename="summary.pdf")
        with open(pdf_file, "rb") as file:
            st.download_button("📥 Download Product Summary PDF", data=file, file_name="product_summary.pdf", mime="application/pdf")
    else:
        st.warning("⚠️ No product data available yet. Search first.")

# === Single Review Analysis ===
st.markdown("---")
st.subheader("✍️ Enter a beauty/skincare product review:")
user_input = st.text_area(" ", height=140, placeholder="e.g. This serum worked wonders for my skin...")
if st.button("🔍 Analyze Review") and user_input.strip():
    cleaned = clean_text(user_input)
    vec = vectorizer.transform([cleaned])
    prediction = model.predict(vec)[0]
    confidence = model.predict_proba(vec).max()
    label = "✅ Genuine Review" if prediction == "OR" else "❌ Fake Review"
    color = "green" if prediction == "OR" else "red"
    st.markdown(f"### 🎯 <span style='color:{color}'>{label}</span>", unsafe_allow_html=True)
    st.markdown(f"**Confidence Score:** `{round(confidence * 100, 2)}%`")
    st.progress(int(confidence * 100))
    matched = [word for word in cleaned.split() if word in vectorizer.get_feature_names_out()]
    st.subheader("🧠 Influential Keywords")
    if matched:
        st.success("Matched keywords: `" + "`, `".join(matched) + "`")
    else:
        st.warning("No significant keywords found.")
    summary = summarize_reviews(user_input)
    st.subheader("🧾 AI Review Summary")
    st.success(summary)
    df = pd.DataFrame({
        "Review": [user_input],
        "Prediction": [label],
        "Confidence (%)": [round(confidence * 100, 2)],
        "Summary": [summary]
    })
    st.download_button("📥 Download Result as CSV", df.to_csv(index=False).encode('utf-8'), file_name="review_result.csv", mime='text/csv')

# === Batch Review Analysis ===
with st.expander("📦 Analyze Multiple Reviews (Batch Mode)"):
    batch_input = st.text_area("Paste multiple reviews (one per line):", height=200)
    if st.button("📊 Analyze All"):
        st.subheader("📋 Batch Review Results")
        reviews = [r.strip() for r in batch_input.split("\n") if r.strip()]
        results = []
        for review in reviews:
            cleaned = clean_text(review)
            vec = vectorizer.transform([cleaned])
            pred = model.predict(vec)[0]
            label = "✅ Genuine" if pred == "OR" else "❌ Fake"
            summary = summarize_reviews(review)
            confidence = model.predict_proba(vec).max()
            results.append((review, label, round(confidence*100, 2), summary))
        result_df = pd.DataFrame(results, columns=["Review", "Prediction", "Confidence (%)", "Summary"])
        st.dataframe(result_df)
        st.download_button("📥 Download All as CSV", result_df.to_csv(index=False).encode('utf-8'), file_name="batch_results.csv", mime='text/csv')
        pdf_buf = generate_pdf("Batch Reviews", result_df)
        st.download_button("📄 Download PDF Report", pdf_buf, file_name="batch_report.pdf")

# === Product Comparison Across Platforms ===
st.markdown("---")
st.header("🛍️ Compare Product Across Platforms")
product_query = st.text_input("🔎 Enter Product Name to Compare:", placeholder="e.g., Garnier Vitamin C Serum")
if st.button("🔍 Compare Product"):
    if product_query.strip():
        comparison_data = get_product_comparison(product_query)
        df = pd.DataFrame(comparison_data)
        if not df.empty:
            st.success(f"✅ Showing results for: **{product_query}**")
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Comparison as CSV", data=csv, file_name="product_comparison.csv", mime='text/csv')
        else:
            st.warning("No comparison data found.")
    else:
        st.warning("⚠️ Please enter a valid product name.")

# === Footer ===
st.markdown("---")
st.markdown("Made with ❤️ by **Shrutika** | Project: **Sknalytics**")
