import ast
from pathlib import Path
import networkx as nx

def build_python_dependency_graph(repo_path: str):
    root = Path(repo_path)
    graph = nx.DiGraph()

    for path in root.rglob("*.py"):
        if ".git" in path.parts or ".venv" in path.parts:
            continue

        rel = str(path.relative_to(root))
        graph.add_node(rel)

        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    graph.add_edge(rel, alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                graph.add_edge(rel, node.module)

    return graph

def dependency_count(graph):
    return int(graph.number_of_edges())
