import json
import os
import tweepy
import sys
from flask import Flask, render_template, jsonify

# ✅ Fix UnicodeEncodeError (For Windows)
sys.stdout.reconfigure(encoding="utf-8")

# ✅ Load BEARER_TOKEN from config.json
config_path = r"C:\Users\harshitha\OneDrive\Desktop\Social Media\models\dashboard\config.json"

if not os.path.exists(config_path):
    raise FileNotFoundError(f"❌ config.json not found at {config_path}")

try:
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)
except json.JSONDecodeError:
    raise ValueError("❌ config.json has an invalid format! Fix the JSON syntax.")

BEARER_TOKEN = config.get("BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("❌ BEARER_TOKEN is missing! Check config.json file.")

print("✅ BEARER_TOKEN Loaded Successfully!")

# ✅ Initialize Flask App
app = Flask(__name__, template_folder="template", static_folder="static")

# ✅ Twitter Authentication
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# ✅ Fetch Tweets and Perform Sentiment Analysis
@app.route("/tweets/<keyword>", methods=["GET"])
def get_tweets(keyword):
    """Fetch tweets and analyze sentiment."""
    try:
        tweets = client.search_recent_tweets(query=keyword, max_results=100, tweet_fields=["created_at", "text"])
        
        # Simulated Sentiment Analysis (Replace with actual model)
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        
        for tweet in tweets.data:
            text = tweet.text.lower()
            if "good" in text or "love" in text or "amazing" in text:
                sentiment_counts["positive"] += 1
            elif "bad" in text or "hate" in text or "worst" in text:
                sentiment_counts["negative"] += 1
            else:
                sentiment_counts["neutral"] += 1
        
        total = sum(sentiment_counts.values())
        if total > 0:
            sentiment_percentages = {k: round(v / total * 100, 2) for k, v in sentiment_counts.items()}
        else:
            sentiment_percentages = {"positive": 0, "negative": 0, "neutral": 0}

        return jsonify({"status": "success", "sentiments": sentiment_percentages})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ✅ Home & Dashboard Route
@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ✅ Results Route (Pass Sentiment Data)
@app.route("/results")
def results():
    """Pass sentiment data to results page."""
    sentiment_data = {
        "positive": 65,  # Example: 65% Positive
        "negative": 20,  # Example: 20% Negative
        "neutral": 15    # Example: 15% Neutral
    }
    return render_template("results.html", sentiment_data=sentiment_data)

# ✅ Run Flask
if __name__ == "__main__":
    app.run(debug=True)
