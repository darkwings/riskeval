from google.adk.agents.llm_agent import Agent
from google.adk.agents.llm_agent import ParallelAgent
from google.adk.agents.llm_agent import SequentialAgent
from sub_agents.geographic_risk_evaluator.agent import geographic_risk_evaluator
from sub_agents.vehicle_risk_evaluator.agent import vehicle_risk_evaluator
from sub_agents.person_risk_evaluator.agent import person_risk_evaluator
from shared_libraries.types import RiskEvaluation

evaluators = ParallelAgent(
    model='gemini-2.5-flash',
    name='parallel_agent',
    description="Parallel evaluators agent",
    sub_agents=[geographic_risk_evaluator, vehicle_risk_evaluator, person_risk_evaluator]
)

global_evaluator = Agent(
    model='gemini-2.5-flash',
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
    output_schema=RiskEvaluation
)

workflow_agent = SequentialAgent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Insurance risk evaluation workflow orchestrator",
    instruction="""
    You are an insurance risk evaluation assistant that orchestrates the complete risk
    assessment process for auto insurance policy applications.

    Your workflow consists of two sequential stages:

    **Stage 1 - Parallel Risk Evaluation (evaluators)**
    Three specialized agents evaluate different risk dimensions in parallel:
    - Geographic Risk Evaluator: Assesses risk based on the policy holder's city and tariff ID
    - Vehicle Risk Evaluator: Assesses risk based on the insured vehicle's brand
    - Person Risk Evaluator: Assesses risk based on the policy holder's Italian fiscal code
                            (Codice Fiscale) and judicial record

    **Stage 2 - Global Risk Assessment (global_evaluator)**
    The global evaluator combines all three risk assessments into a final comprehensive
    risk evaluation and recommendation.

    **Your Role:**
    1. Collect the required information from the user:
       - City where the policy holder lives
       - Tariff ID for the insurance policy
       - Vehicle brand
       - Policy holder's Italian fiscal code (Codice Fiscale)

    2. Pass this information to the parallel evaluators for assessment

    3. Ensure the global evaluator receives all three risk assessments and produces
       the final risk score and evaluation

    4. Present the final results to the user in a clear, professional manner

    **Input Requirements:**
    - city: String (e.g., "Milano", "Roma", "Napoli")
    - tariff_id: String (e.g., "TARIFF_001")
    - vehicle_brand: String (e.g., "Ferrari", "BMW", "Volkswagen")
    - fiscal_code: String - 16-character Italian fiscal code (e.g., "RSSMRA80A01H501U")

    **Output:**
    Provide the user with a comprehensive risk evaluation that includes:
    - Individual risk scores for geographic, vehicle, and person dimensions
    - The final global risk score (LOW, MEDIUM, HIGH, or VERY_HIGH)
    - A detailed explanation of the risk assessment
    - Clear recommendation for policy underwriting

    Be professional, thorough, and helpful throughout the process. If the user doesn't
    provide all required information, politely ask for the missing details.
    """,
    sub_agents=[evaluators, global_evaluator]
)

root_agent = workflow_agent