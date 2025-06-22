# // <copyright file="ComparativeGoal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Optional
from .BaseGoal import BaseGoal
from .ComparisonValuePair import ComparisonValuePair

class ComparativeGoal(BaseGoal):
    """
    Represents a goal to be achieved for an agent.
    """

    DesiredState: Dict[str, ComparisonValuePair]

    def __init__(self, name: Optional[str] = None, weight: float = 1.0,
                 desired_state: Optional[Dict[str, ComparisonValuePair]] = None):
        """
        Initializes a new instance of the ComparativeGoal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
            desired_state: Desired state for the comparative goal.
        """
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}

