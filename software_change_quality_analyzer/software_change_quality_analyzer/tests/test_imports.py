def test_project_imports():
    import main
    from app.analyzer import metrics, dependency_graph, predictor
    assert main.app is not None
