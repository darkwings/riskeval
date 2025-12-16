
from enum import Enum
from pydantic import BaseModel

class RiskScore(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    NOT_AVAILABLE = "NOT_AVAILABLE"

class RiskEvaluation(BaseModel):
    score: RiskScore
    evaluation: str    