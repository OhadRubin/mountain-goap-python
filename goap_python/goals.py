import uuid
from enum import Enum
from typing import Dict, Optional, Any

from .types import StateDictionary

class BaseGoal:
    Name: str
    Weight: float

    def __init__(self, name: str = None, weight: float = 1.0):
        self.Name = name if name is not None else f"Goal {uuid.uuid4()}"
        self.Weight = weight


class ComparisonOperator(Enum):
    Undefined = 0
    Equals = 1
    LessThan = 2
    LessThanOrEquals = 3
    GreaterThan = 4
    GreaterThanOrEquals = 5


class ComparisonValuePair:
    Value: Optional[Any] = None
    Operator: ComparisonOperator = ComparisonOperator.Undefined

    def __init__(
        self,
        value: Optional[Any] = None,
        operator: ComparisonOperator = ComparisonOperator.Undefined,
    ):
        self.Value = value
        self.Operator = operator


class ComparativeGoal(BaseGoal):
    DesiredState: Dict[str, ComparisonValuePair]

    def __init__(
        self,
        name: Optional[str] = None,
        weight: float = 1.0,
        desired_state: Optional[Dict[str, ComparisonValuePair]] = None,
    ):
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}


class ExecutionStatus(Enum):
    NotYetExecuted = 1
    Executing = 2
    Succeeded = 3
    Failed = 4
    NotPossible = 5


class ExtremeGoal(BaseGoal):
    DesiredState: Dict[str, bool]

    def __init__(
        self,
        name: Optional[str] = None,
        weight: float = 1.0,
        desired_state: Optional[Dict[str, bool]] = None,
    ):
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}


class Goal(BaseGoal):
    DesiredState: StateDictionary

    def __init__(
        self,
        name: Optional[str] = None,
        weight: float = 1.0,
        desired_state: Optional[StateDictionary] = None,
    ):
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}

