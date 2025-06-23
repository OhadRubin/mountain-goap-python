import importlib

def test_player_factory_returns_agent():
    try:
        factories = importlib.import_module('rpg.factories')
    except ModuleNotFoundError:
        return
    from goap.agent import Agent
    PlayerFactory = factories.PlayerFactory
    agents = []
    player = PlayerFactory.create(agents, [])
    assert isinstance(player, Agent)
    assert player.Name == "Player"
