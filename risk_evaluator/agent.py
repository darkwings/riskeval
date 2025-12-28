from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from .sub_agents.geographic_risk_evaluator.agent import geographic_risk_evaluator
from .sub_agents.vehicle_risk_evaluator.agent import vehicle_risk_evaluator
from .sub_agents.person_risk_evaluator.agent import person_risk_evaluator
from .shared_libraries.types import RiskEvaluation
from .shared_libraries.callbacks import rate_limit_callback

evaluators = ParallelAgent(
    name='parallel_agent',
    description="Parallel evaluators agent",
    sub_agents=[geographic_risk_evaluator, vehicle_risk_evaluator, person_risk_evaluator]
)

global_evaluator = Agent(
    model=LiteLlm(model='anthropic/claude-sonnet-4-20250514'),
    name='global_evaluator',
    description="Final evaluators agent that combines all risk assessments",
    instruction="""
    You are the final risk evaluator for insurance policy emission. Your role is to analyze
    the risk assessments from three specialized evaluators and produce a comprehensive final
    risk evaluation.

    You receive evaluations from three parallel agents:
    1. **geographic_risk**: Risk assessment based on the policy holder's address/location
    2. **vehicle_risk**: Risk assessment based on the insured vehicle's brand
    3. **person_risk**: Risk assessment based on the policy holder's judicial record

    Each evaluation contains:
    - score: One of LOW, MEDIUM, HIGH, VERY_HIGH, or NOT_AVAILABLE
    - evaluation: The reasoning behind the score

    Your task is to:
    1. Analyze all three risk scores
    2. Determine the final overall risk score using the following logic:
       - If ANY score is VERY_HIGH, the final score should be VERY_HIGH
       - If ANY score is NOT_AVAILABLE, mention this in your evaluation but proceed with available data
       - If the highest score is HIGH and another is HIGH or MEDIUM, the final score should be VERY_HIGH
       - If the highest score is HIGH and others are LOW, the final score should be HIGH
       - If the highest score is MEDIUM and another is MEDIUM, the final score should be HIGH
       - If the highest score is MEDIUM and others are LOW, the final score should be MEDIUM
       - If all scores are LOW, the final score should be LOW
    3. Provide a comprehensive evaluation that:
       - Summarizes the key risk factors from each dimension (geographic, vehicle, person)
       - Explains the final risk score decision
       - Highlights the most critical risk factors
       - Provides a clear rationale for the insurance underwriting decision

    Be thorough and professional in your evaluation, as this will be used to determine
    whether to issue the insurance policy and at what premium rate.

    Output format:
    - score: The final overall risk score (LOW, MEDIUM, HIGH, or VERY_HIGH)
    - evaluation: A detailed explanation of your decision, referencing all three risk dimensions
    """,
    output_key="global_risk",
    output_schema=RiskEvaluation,
    before_model_callback=rate_limit_callback
)

workflow_agent = SequentialAgent(
    name='root_agent',
    description="Insurance risk evaluation workflow: runs parallel evaluators (geographic, vehicle, person) then combines results in global evaluator",
    sub_agents=[evaluators, global_evaluator]
)

root_agent = workflow_agent