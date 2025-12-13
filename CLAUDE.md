# RISKEVAL

This is a risk evaluator agent system, based on [Google ADK Framework](https://google.github.io/adk-docs/).

Given data about policy holder (a person, with its address) and its vehicle, the system should return the RISK score associated to the user.

We have 3 parallel subagents:

- `geographic_risk_evaluator`: this agent evaluates the risk given the address of the prospect holder, that is the buyer of the policy
- `vehicle_risk_evaluator`: this agent evaluates the risk based on the vehicle (brand, power, yearly mileage, usage type)
- `person_risk_evaluator`: this agent evaluates the risk based on the story of the holder (in a real scenario, it should check the judicial record of the person and stuff like that)

Each agent emits a score and an evaluation.
The score is always one of:

- LOW
- MEDIUM
- HIGH
- VERY_HIGH

The evaluation is the reason of the scoring, for tracing purposes.

The scores are then passed to the final evaluator agent `global_evaluator`. This agent will check the scores and then perform a final evaluation, giving back a global score.