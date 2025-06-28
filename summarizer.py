# summarizer.py

from transformers import pipeline
import pandas as pd

# Load summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Summarize a list of reviews
def summarize_reviews(reviews, max_chunk=500):
    full_text = " ".join(reviews)
    chunks = [full_text[i:i+max_chunk] for i in range(0, len(full_text), max_chunk)]

    summary = []
    for chunk in chunks:
        try:
            res = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
            summary.append(res[0]['summary_text'])
        except Exception as e:
            summary.append(f"[Error summarizing chunk] {str(e)}")

    return " ".join(summary)


# Optional: Summarize from CSV directly
def summarize_from_csv(csv_path, text_column="review"):
    df = pd.read_csv(csv_path)
    reviews = df[text_column].dropna().tolist()
    return summarize_reviews(reviews)
