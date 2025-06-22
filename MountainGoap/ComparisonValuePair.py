# // <copyright file="ComparisonValuePair.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Any, Optional
from .ComparisonOperator import ComparisonOperator

class ComparisonValuePair:
    """
    List of operators that can be used for comparison.
    """

    Value: Optional[Any] = None

    Operator: ComparisonOperator = ComparisonOperator.Undefined

    def __init__(self, value: Optional[Any] = None, operator: ComparisonOperator = ComparisonOperator.Undefined):
        self.Value = value
        self.Operator = operator

