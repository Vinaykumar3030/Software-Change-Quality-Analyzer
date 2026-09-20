from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

FEATURES = [
    "lines_added",
    "lines_deleted",
    "files_changed",
    "complexity",
    "dependency_count",
    "historical_defects",
]

rng = np.random.default_rng(42)
n = 800

df = pd.DataFrame({
    "lines_added": rng.integers(0, 500, n),
    "lines_deleted": rng.integers(0, 300, n),
    "files_changed": rng.integers(1, 20, n),
    "complexity": rng.integers(1, 30, n),
    "dependency_count": rng.integers(0, 25, n),
    "historical_defects": rng.integers(0, 10, n),
})

risk_score = (
    df.lines_added * 0.015
    + df.lines_deleted * 0.01
    + df.files_changed * 1.8
    + df.complexity * 1.7
    + df.dependency_count * 1.5
    + df.historical_defects * 3.0
)

df["risk"] = pd.cut(
    risk_score,
    bins=[-np.inf, 35, 70, np.inf],
    labels=["Low", "Medium", "High"]
)

X = df[FEATURES]
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred))

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/risk_model.joblib")
df.to_csv("data/demo_training_data.csv", index=False)
print("Saved models/risk_model.joblib")
