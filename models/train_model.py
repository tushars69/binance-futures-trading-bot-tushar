# models/train_model.py

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")


BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
DATA_PATH = os.path.join(BASE_DIR, "data", "candles_BTCUSDT.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

# ---------------------------------------------------------------------
# 🧩 Load and preprocess the data
# ---------------------------------------------------------------------
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Data file not found at: {DATA_PATH}\nPlease run collect_candles.py first.")

print(f"📂 Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

# Basic data check
if df.empty:
    raise ValueError("❌ Loaded CSV is empty. Please check your data collector output.")

print(f"✅ Data loaded: {len(df)} rows")

# ---------------------------------------------------------------------
# 🧮 Feature engineering (simple example)
# ---------------------------------------------------------------------
df["ma3"] = df["close"].rolling(window=3).mean()
df["ma8"] = df["close"].rolling(window=8).mean()
df["ret"] = df["close"].pct_change()
df.dropna(inplace=True)

# Create target variable: 1 if price increases next step, else 0
df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)

features = ["close", "ma3", "ma8", "ret"]
X = df[features]
y = df["target"]

print(f"🧾 Feature matrix shape: {X.shape}, Target shape: {y.shape}")

# ---------------------------------------------------------------------
# 🤖 Train/test split
# ---------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# ---------------------------------------------------------------------
# 🚀 Train model
# ---------------------------------------------------------------------
print("🚀 Training RandomForestClassifier...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

# ---------------------------------------------------------------------
# 📊 Evaluate model
# ---------------------------------------------------------------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Model training complete — Accuracy: {acc:.2%}")

# ---------------------------------------------------------------------
# 💾 Save model
# ---------------------------------------------------------------------
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"✅ Model saved successfully at: {MODEL_PATH}")
print("🎉 Training pipeline complete!")
