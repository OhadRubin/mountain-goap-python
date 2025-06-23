import importlib

def test_example_has_run():
    try:
        module = importlib.import_module('rpg.example')
    except ModuleNotFoundError:
        return
    assert hasattr(module, 'RpgExampleComparativePygame')
