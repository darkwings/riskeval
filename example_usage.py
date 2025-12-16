"""
Example usage of the risk evaluator agent with structured input.

This demonstrates how to use the risk evaluation system programmatically
with structured input data, suitable for API integration.
"""

import asyncio
import json
from risk_evaluator.agent import root_agent
from risk_evaluator.shared_libraries.types import PolicyRequest
from google.adk.runners import Runner


async def evaluate_policy_risk(policy_data: dict):
    """
    Evaluate insurance policy risk with structured input data.

    Args:
        policy_data: Dictionary containing:
            - city: str - City where policy holder lives
            - tariff_id: str - Tariff identifier
            - vehicle_brand: str - Vehicle brand
            - fiscal_code: str - Italian fiscal code

    Returns:
        Risk evaluation result with individual and global risk scores
    """
    # Validate input
    request = PolicyRequest(**policy_data)

    # Create structured input message
    input_message = f"""
Please evaluate the insurance risk for the following policy application:

City: {request.city}
Tariff ID: {request.tariff_id}
Vehicle Brand: {request.vehicle_brand}
Fiscal Code: {request.fiscal_code}

Provide a complete risk evaluation.
"""

    # Run the agent
    runner = Runner(agent=root_agent)

    result = {"events": []}
    async for event in runner.run_async(input_message):
        result["events"].append({
            "type": type(event).__name__,
            "data": str(event)
        })

    return result


# Example usage
if __name__ == "__main__":
    # Example 1: High risk case (Ferrari in Milano, person with DUI record)
    high_risk_policy = {
        "city": "Milano",
        "tariff_id": "TARIFF_001",
        "vehicle_brand": "Ferrari",
        "fiscal_code": "RSSMRA80A01H501U"  # Has DUI, reckless driving, license suspension
    }

    # Example 2: Low risk case (Volkswagen in Pavia, clean record)
    low_risk_policy = {
        "city": "Pavia",
        "tariff_id": "TARIFF_001",
        "vehicle_brand": "Volkswagen",
        "fiscal_code": "ABCDEF12G34H567I"  # Clean record (not in mock DB)
    }

    # Example 3: Very high risk (Fraud history in high-risk zone)
    very_high_risk_policy = {
        "city": "Napoli",
        "tariff_id": "TARIFF_001",
        "vehicle_brand": "Lamborghini",
        "fiscal_code": "BNCLRA75D12L219K"  # Insurance fraud, false declaration
    }

    # Run evaluation
    print("=" * 80)
    print("HIGH RISK POLICY EVALUATION")
    print("=" * 80)
    result = asyncio.run(evaluate_policy_risk(high_risk_policy))
    print(json.dumps(high_risk_policy, indent=2))
    print("\nRunning evaluation...")
    print(f"Generated {len(result['events'])} events")

    print("\n" + "=" * 80)
    print("LOW RISK POLICY EVALUATION")
    print("=" * 80)
    result = asyncio.run(evaluate_policy_risk(low_risk_policy))
    print(json.dumps(low_risk_policy, indent=2))
    print("\nRunning evaluation...")
    print(f"Generated {len(result['events'])} events")

    print("\n" + "=" * 80)
    print("VERY HIGH RISK POLICY EVALUATION")
    print("=" * 80)
    result = asyncio.run(evaluate_policy_risk(very_high_risk_policy))
    print(json.dumps(very_high_risk_policy, indent=2))
    print("\nRunning evaluation...")
    print(f"Generated {len(result['events'])} events")
