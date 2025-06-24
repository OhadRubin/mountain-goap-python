from goap_python.goals import ComparisonValuePair, ComparisonOperator, Goal


def test_goal_creation():
    cvp = ComparisonValuePair(operator=ComparisonOperator.Equals, value=5)
    goal = Goal(name="TestGoal", desired_state={"foo": 1})
    assert goal.DesiredState["foo"] == 1
    assert cvp.Operator == ComparisonOperator.Equals
    assert cvp.Value == 5
