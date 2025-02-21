import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# ✅ Step 1: Load and Check Dataset
dataset_path = "sentimentdataset.csv"  
df = pd.read_csv(dataset_path)

if 'Text' not in df.columns or 'Sentiment' not in df.columns:
    raise ValueError("❌ Dataset must contain 'Text' and 'Sentiment' columns.")

# ✅ Step 2: Preprocessing Function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

df['Text'] = df['Text'].apply(preprocess_text)

# ✅ Step 3: Split Data
X = df['Text']
y = df['Sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Step 4: Use TF-IDF for Better Representation
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words='english', max_features=5000)),  # TF-IDF instead of CountVectorizer
    ('classifier', MultinomialNB())  
])

# ✅ Step 5: Train Model
pipeline.fit(X_train, y_train)

# ✅ Step 6: Evaluate Model
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Improved Model Accuracy: {accuracy:.2f}")

# ✅ Step 7: Save Model
model_path = "models/sentiment_model.pkl"
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

print(f"Model saved at {model_path}")
