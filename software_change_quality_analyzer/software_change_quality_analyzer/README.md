# Software Change Quality Analyzer

A B.Tech project that analyzes software changes using change metrics, dependency analysis, and a Random Forest model to estimate change risk.

## Current MVP
- Analyze a local Git repository commit
- Extract basic Git change metrics
- Build a simple Python import dependency graph
- Train a Random Forest model on a generated demo dataset
- Predict Low / Medium / High risk
- Return an explanation based on important risk factors

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python train_model.py
python main.py
```

Then open http://127.0.0.1:8000/docs

## Project structure

- `app/analyzer/metrics.py` - Git/change metrics
- `app/analyzer/dependency_graph.py` - dependency graph
- `app/analyzer/predictor.py` - Random Forest prediction
- `train_model.py` - creates demo training data and trains the model
- `main.py` - FastAPI backend
