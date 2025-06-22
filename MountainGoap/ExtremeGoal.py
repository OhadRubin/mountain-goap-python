# // <copyright file="ExtremeGoal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Optional
from .BaseGoal import BaseGoal

class ExtremeGoal(BaseGoal):
    """
    Represents a goal requiring an extreme value to be achieved for an agent.
    """

    DesiredState: Dict[str, bool]

    def __init__(self, name: Optional[str] = None, weight: float = 1.0,
                 desired_state: Optional[Dict[str, bool]] = None):
        """
        Initializes a new instance of the ExtremeGoal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
            desired_state: States to be maximized or minimized.
        """
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}

