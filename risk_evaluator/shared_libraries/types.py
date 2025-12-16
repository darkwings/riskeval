
from enum import Enum
from pydantic import BaseModel, Field

class RiskScore(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    NOT_AVAILABLE = "NOT_AVAILABLE"

class RiskEvaluation(BaseModel):
    score: RiskScore
    evaluation: str

class PolicyRequest(BaseModel):
    """Input schema for insurance policy risk evaluation"""
    city: str = Field(..., description="City where the policy holder lives (e.g., 'Milano', 'Roma', 'Napoli')")
    tariff_id: str = Field(..., description="Tariff identifier for the insurance policy (e.g., 'TARIFF_001')")
    vehicle_brand: str = Field(..., description="Brand of the insured vehicle (e.g., 'Ferrari', 'BMW', 'Volkswagen')")
    fiscal_code: str = Field(..., description="Italian fiscal code (Codice Fiscale) of the policy holder - 16 characters (e.g., 'RSSMRA80A01H501U')")    