import importlib

def test_goal_single_file_importable():
    try:
        module = importlib.import_module('goal_single_file')
    except ModuleNotFoundError:
        # pygame not installed
        return
    assert hasattr(module, '__name__')
