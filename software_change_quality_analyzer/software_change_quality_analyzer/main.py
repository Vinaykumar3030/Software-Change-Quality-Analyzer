from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.analyzer.metrics import get_commit_metrics
from app.analyzer.dependency_graph import build_python_dependency_graph, dependency_count
from app.analyzer.predictor import predict

app = FastAPI(
    title="Software Change Quality Analyzer",
    version="0.1.0",
    description="Analyzes software changes using metrics, dependency graphs and Random Forest."
)

class AnalyzeRequest(BaseModel):
    repo_path: str
    commit_ref: str = "HEAD"
    complexity: int = 5
    historical_defects: int = 0

@app.get("/")
def home():
    return {
        "project": "Software Change Quality Analyzer",
        "status": "running",
        "docs": "/docs"
    }

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    repo = Path(request.repo_path)

    if not repo.exists():
        raise HTTPException(status_code=400, detail="Repository path does not exist.")

    try:
        metrics = get_commit_metrics(str(repo), request.commit_ref)
        graph = build_python_dependency_graph(str(repo))
        dep_count = dependency_count(graph)

        features = {
            **metrics,
            "complexity": request.complexity,
            "dependency_count": dep_count,
            "historical_defects": request.historical_defects,
        }

        result = predict(features)

        reasons = []
        if features["lines_added"] > 200:
            reasons.append("Large number of lines added")
        if features["files_changed"] > 8:
            reasons.append("Many files changed")
        if features["complexity"] > 15:
            reasons.append("High code complexity")
        if features["dependency_count"] > 10:
            reasons.append("High dependency impact")
        if features["historical_defects"] > 3:
            reasons.append("Affected modules have defect history")

        if not reasons:
            reasons.append("No major threshold-based risk factor detected")

        return {
            "features": features,
            "dependency_nodes": graph.number_of_nodes(),
            "dependency_edges": graph.number_of_edges(),
            "prediction": result,
            "risk_factors": reasons,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
