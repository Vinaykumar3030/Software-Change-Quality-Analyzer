import runpy
import sys
from pathlib import Path


def test_main_module_has_uvicorn_entrypoint(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))

    called = {}

    class DummyUvicorn:
        @staticmethod
        def run(app, host=None, port=None, reload=False):
            called["app"] = app
            called["host"] = host
            called["port"] = port
            called["reload"] = reload

    monkeypatch.setitem(sys.modules, "uvicorn", type("Mod", (), {"run": staticmethod(DummyUvicorn.run)}))

    runpy.run_path(str(root / "main.py"), run_name="__main__")

    assert called["app"] == "main:app"
    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8000
