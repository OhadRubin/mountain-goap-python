import goap


def test_package_imports():
    assert hasattr(goap, 'Action')
    assert hasattr(goap, 'Agent')
