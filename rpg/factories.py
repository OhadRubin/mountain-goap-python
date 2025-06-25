from goap_python.agent import Agent

class PlayerFactory:
    @staticmethod
    def create(agents, food_positions, name="Player", use_extreme=False):
        return Agent(name=name)
