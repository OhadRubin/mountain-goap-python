from goap_python.actions import Action


def test_action_clone():
    action = Action(name="TestAction", cost=2.5)
    clone = action.copy()
    assert clone.Name == action.Name
    assert clone._cost_base == action._cost_base
