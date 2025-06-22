# // <copyright file="Goal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional
from .BaseGoal import BaseGoal

class Goal(BaseGoal):
    """
    Represents a goal to be achieved for an agent.
    """

    DesiredState: Dict[str, Optional[Any]]

    def __init__(self, name: Optional[str] = None, weight: float = 1.0,
                 desired_state: Optional[Dict[str, Optional[Any]]] = None):
        """
        Initializes a new instance of the Goal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
            desired_state: Desired end state of the goal.
        """
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}

