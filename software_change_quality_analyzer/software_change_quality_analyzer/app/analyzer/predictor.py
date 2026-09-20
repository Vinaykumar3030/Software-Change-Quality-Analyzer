from pathlib import Path
import joblib
import pandas as pd

FEATURES = [
    "lines_added",
    "lines_deleted",
    "files_changed",
    "complexity",
    "dependency_count",
    "historical_defects",
]

MODEL_PATH = Path("models/risk_model.joblib")

def predict(features: dict):
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run: python train_model.py")

    model = joblib.load(MODEL_PATH)
    row = pd.DataFrame([[features[f] for f in FEATURES]], columns=FEATURES)

    label = str(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    classes = list(model.classes_)

    probability_map = {
        str(c): float(p) for c, p in zip(classes, probabilities)
    }

    risk_score = (
        probability_map.get("Low", 0.0) * 20
        + probability_map.get("Medium", 0.0) * 60
        + probability_map.get("High", 0.0) * 100
    )

    return {
        "prediction": label,
        "risk_score": round(risk_score, 2),
        "probabilities": probability_map,
    }
