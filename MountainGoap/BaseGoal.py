# // <copyright file="BaseGoal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid

class BaseGoal:
    """
    Represents an abstract class for a goal to be achieved for an agent.
    """

    Name: str

    Weight: float

    def __init__(self, name: str = None, weight: float = 1.0):
        """
        Initializes a new instance of the BaseGoal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
        """
        self.Name = name if name is not None else f"Goal {uuid.uuid4()}"
        self.Weight = weight

