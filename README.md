# RISKEVAL

Insurance risk evaluator agent system based on [Google ADK Framework](https://google.github.io/adk-docs/).

## Overview

This system evaluates insurance policy risk by analyzing three parallel dimensions:
- **Geographic Risk**: Based on the policy holder's city location
- **Vehicle Risk**: Based on the insured vehicle's brand
- **Person Risk**: Based on the policy holder's judicial record (Italian fiscal code)

The system uses a parallel agent architecture that runs all three evaluations simultaneously, then combines them in a global evaluator for a final risk assessment.

## Architecture

```
SequentialAgent (workflow_agent)
├── Stage 1: ParallelAgent (evaluators)
│   ├── geographic_risk_evaluator
│   ├── vehicle_risk_evaluator
│   └── person_risk_evaluator
└── Stage 2: global_evaluator
    └── Combines all three risk assessments
```

## Installation

Create a virtual environment:

```shell
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

## Running the Agent

### Using ADK Web Interface

Start the web interface:

```shell
adk web
```

Then test with this structured message:

```
Evaluate risk for:
- City: Milano
- Tariff ID: TARIFF_001
- Vehicle brand: Ferrari
- Fiscal code: RSSMRA80A01H501U
```

### Programmatic Usage (API Integration)

For API integration, use structured input:

```python
from risk_evaluator.shared_libraries.types import PolicyRequest

# Create structured request
policy_request = PolicyRequest(
    city="Milano",
    tariff_id="TARIFF_001",
    vehicle_brand="Ferrari",
    fiscal_code="RSSMRA80A01H501U"
)
```

See `example_usage.py` for a complete example.

## Input Schema

The system expects the following structured input:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `city` | string | City where the policy holder lives | "Milano", "Roma", "Napoli" |
| `tariff_id` | string | Tariff identifier for the insurance policy | "TARIFF_001" |
| `vehicle_brand` | string | Brand of the insured vehicle | "Ferrari", "BMW", "Volkswagen" |
| `fiscal_code` | string | Italian fiscal code (16 characters) | "RSSMRA80A01H501U" |

## Output Schema

Each evaluator returns a `RiskEvaluation` object:

```json
{
  "score": "LOW" | "MEDIUM" | "HIGH" | "VERY_HIGH" | "NOT_AVAILABLE",
  "evaluation": "Detailed explanation of the risk assessment"
}
```

## Risk Assessment Logic

### Geographic Risk
- **Zone 1 (Milano)**: HIGH - Dense urban traffic, elevated theft rates
- **Zone 2 (Pavia)**: LOW - Moderate traffic, lower crime rates
- **Zone 3 (Napoli)**: VERY_HIGH - High risk metropolitan area
- **Zone 4 (Other)**: LOW - Default for unlisted cities

### Vehicle Risk
- **VERY_HIGH**: Exotic/luxury brands (Ferrari, Lamborghini, Bugatti, McLaren, etc.)
- **HIGH**: Premium brands (BMW, Mercedes, Audi, Porsche, etc.)
- **MEDIUM**: Mainstream brands (Volkswagen, Peugeot, Ford, Toyota, etc.)
- **LOW**: Other/unknown brands

### Person Risk
Based on judicial records:
- **VERY_HIGH**: Insurance fraud, DUI + other serious offenses, hit-and-run
- **HIGH**: Serious traffic violations (DUI, reckless driving, license suspension)
- **MEDIUM**: Moderate violations (multiple speeding tickets, DUI alone)
- **LOW**: Clean record or minor violations

### Global Risk Evaluation
The global evaluator combines all three assessments:
- If ANY score is VERY_HIGH → Final: VERY_HIGH
- If highest is HIGH + another is HIGH/MEDIUM → Final: VERY_HIGH
- If highest is HIGH + others are LOW → Final: HIGH
- If two scores are MEDIUM → Final: HIGH
- If highest is MEDIUM + others are LOW → Final: MEDIUM
- If all scores are LOW → Final: LOW

## Test Cases

The system includes mock data for testing:

**High Risk Example:**
```
City: Milano (HIGH)
Vehicle: Ferrari (VERY_HIGH)
Fiscal Code: RSSMRA80A01H501U (HIGH - DUI, reckless driving)
Expected Result: VERY_HIGH
```

**Low Risk Example:**
```
City: Pavia (LOW)
Vehicle: Volkswagen (MEDIUM)
Fiscal Code: <any not in mock DB> (LOW - clean record)
Expected Result: MEDIUM
```

**Very High Risk Example:**
```
City: Napoli (VERY_HIGH)
Vehicle: Lamborghini (VERY_HIGH)
Fiscal Code: BNCLRA75D12L219K (VERY_HIGH - insurance fraud)
Expected Result: VERY_HIGH
```

## Project Structure

```
risk_evaluator/
├── agent.py                    # Main workflow definition
├── shared_libraries/
│   └── types.py               # Pydantic models (RiskEvaluation, PolicyRequest)
└── sub_agents/
    ├── geographic_risk_evaluator/
    │   ├── agent.py           # Geographic risk agent
    │   └── tools.py           # Zone lookup tools
    ├── vehicle_risk_evaluator/
    │   ├── agent.py           # Vehicle risk agent
    │   └── tools.py           # Brand classification tools
    └── person_risk_evaluator/
        ├── agent.py           # Person risk agent
        └── tools.py           # Judicial record tools
```

## Development

To run the example programmatically:

```shell
python example_usage.py
```

This will evaluate three different risk scenarios and display the results.
