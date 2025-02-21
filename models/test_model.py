import json
import os
import tweepy
import sys
from flask import Flask, render_template, jsonify

# ✅ Fix UnicodeEncodeError (Forces UTF-8 encoding)
sys.stdout.reconfigure(encoding="utf-8")

# ✅ Load BEARER_TOKEN from config.json
config_path = os.path.join(os.path.dirname(__file__), "config.json")

if not os.path.exists(config_path):
    raise FileNotFoundError(f"❌ config.json not found at {config_path}")

try:
    with open(config_path, "r", encoding="utf-8") as file:  # Ensure UTF-8 encoding
        config = json.load(file)
except json.JSONDecodeError:
    raise ValueError("❌ config.json has an invalid format! Fix the JSON syntax.")

BEARER_TOKEN = config.get("BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("❌ BEARER_TOKEN is missing! Check config.json file.")

print("✅ BEARER_TOKEN Loaded Successfully!")

# ✅ Initialize Flask App
app = Flask(__name__, template_folder="templates", static_folder="static")

# ✅ Twitter Authentication
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# ✅ Home Route (Dashboard)
@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ✅ Sentiment Analysis Results Route
@app.route("/results")
def results():
    return render_template("results.html", sentiment="Positive")  # Example data

# ✅ Fetch Tweets Route
@app.route("/tweets/<keyword>", methods=["GET"])
def get_tweets(keyword):
    """Fetch latest tweets containing the given keyword."""
    try:
        tweets = client.search_recent_tweets(query=keyword, max_results=10, tweet_fields=["created_at", "text"])
        if tweets.data:
            tweet_list = [{"time": tweet.created_at, "text": tweet.text} for tweet in tweets.data]
            return jsonify({"status": "success", "tweets": tweet_list})
        else:
            return jsonify({"status": "success", "tweets": []})  # No tweets found
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ✅ Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
