from goap_python.agent import Agent


def test_agent_defaults():
    agent = Agent(name="Tester")
    assert agent.Name == "Tester"
    assert agent.Goals == []
    assert agent.Actions == []
    assert agent.Sensors == []
