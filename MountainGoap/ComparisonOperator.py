# // <copyright file="ComparisonOperator.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from enum import Enum

class ComparisonOperator(Enum):
    """
    List of operators that can be used for comparison.
    """

    Undefined = 0

    Equals = 1

    LessThan = 2

    LessThanOrEquals = 3

    GreaterThan = 4

    GreaterThanOrEquals = 5

