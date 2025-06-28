# review_summarizer.py

import openai
import os

# ✅ Store your API key in environment variable before running
# Example (in terminal): export OPENAI_API_KEY='your-key-here'
openai.api_key = os.getenv("OPENAI_API_KEY")  # Environment variable name only!

def summarize_reviews_gpt(reviews):
    combined = "\n".join(reviews[:10])  # Use first 10 reviews only
    prompt = f"""
You are an expert in product analysis. Summarize the following product reviews clearly and concisely.
Highlight common sentiments, concerns, and feedback:

{combined}

Return a concise paragraph summarizing the overall review sentiment and key takeaways.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        return f"❌ Error generating summary: {str(e)}"
