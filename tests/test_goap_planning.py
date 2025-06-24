from goap_python.actions import Action
from goap_python.planning import ActionNode


def test_action_node_equality():
    act1 = Action(name="test")
    node1 = ActionNode(act1, state={}, parameters={})
    node2 = ActionNode(act1, state={}, parameters={})
    assert node1 == node2
    assert hash(node1) == hash(node2)
