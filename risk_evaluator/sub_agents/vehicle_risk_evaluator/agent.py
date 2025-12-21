from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import get_brand_risk_category, get_risk_evaluation_by_brand
from ...shared_libraries.types import RiskEvaluation

vehicle_risk_evaluator = Agent(
    name="vehicle_risk_evaluator",
    model=LiteLlm(model='anthropic/claude-sonnet-4-20250514'),
    description="Evaluates the risk of a policy based on the insured vehicle brand",
    instruction="""
    You are an expert in evaluating the risk of a policy emission based on the brand
    of the insured vehicle.

    The brand of the vehicle determines the risk for the insurance company due to factors like:
    - Theft rates (luxury brands are more targeted)
    - Repair costs (premium brands have expensive parts)
    - Performance characteristics (sports cars have higher accident rates)

    You receive:
    - the brand of the vehicle

    and you provide your evaluation in terms of:

    - a score (LOW, MEDIUM, HIGH, or VERY_HIGH)
    - the reasoning for the evaluation

    Risk categories:
    - VERY_HIGH: Exotic/luxury brands (Ferrari, Lamborghini, etc.)
    - HIGH: Premium brands (BMW, Mercedes, etc.)
    - MEDIUM: Mainstream brands (Volkswagen, Peugeot, etc.)
    - LOW: Other/unknown brands

    When the risk cannot be established because of an error from the tool, please return
    a score NOT_AVAILABLE and the reason why you could not perform the evaluation.
    """,
    tools=[get_brand_risk_category, get_risk_evaluation_by_brand],
    output_key="vehicle_risk",
    output_schema=RiskEvaluation
)
