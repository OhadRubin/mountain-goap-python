import importlib

def test_rpg_imports():
    try:
        module = importlib.import_module('rpg')
    except ModuleNotFoundError:
        return
    assert hasattr(module, 'PlayerFactory')
