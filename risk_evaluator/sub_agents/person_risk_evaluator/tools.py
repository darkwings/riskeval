from shared_libraries.types import RiskEvaluation, RiskScore


def check_judicial_record(fiscal_code: str) -> dict:
    """Simulates a lookup in the Italian justice records (Casellario Giudiziale)

    Args:
        fiscal_code (str): The Italian fiscal code (Codice Fiscale) of the person
                          (e.g., "RSSMRA80A01H501U")

    Returns:
        dict: A dictionary containing the judicial record information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes:
                - 'has_record': boolean indicating if there are records
                - 'offenses': list of offense types found
                - 'severity': overall severity level
              If 'error', includes an 'error_message' key.
    """
    fiscal_code_normalized = fiscal_code.upper().replace(" ", "")

    # Validate basic format (16 characters for Italian fiscal code)
    if len(fiscal_code_normalized) != 16:
        return {
            "status": "error",
            "error_message": f"Invalid fiscal code format. Expected 16 characters, got {len(fiscal_code_normalized)}."
        }

    # Mock database of judicial records
    # In a real scenario, this would query the actual Italian Casellario Giudiziale
    mock_judicial_db = {
        # Person with serious traffic violations
        "RSSMRA80A01H501U": {
            "status": "success",
            "has_record": True,
            "offenses": ["DUI", "reckless_driving", "license_suspension"],
            "severity": "HIGH"
        },
        # Person with minor violations
        "VRDGPP85M15F205Z": {
            "status": "success",
            "has_record": True,
            "offenses": ["speeding"],
            "severity": "LOW"
        },
        # Person with fraud history
        "BNCLRA75D12L219K": {
            "status": "success",
            "has_record": True,
            "offenses": ["insurance_fraud", "false_declaration"],
            "severity": "VERY_HIGH"
        },
        # Person with multiple serious offenses
        "MRNGNN90T20D969P": {
            "status": "success",
            "has_record": True,
            "offenses": ["DUI", "hit_and_run", "insurance_fraud"],
            "severity": "VERY_HIGH"
        },
        # Person with moderate violations
        "FLMPTR88H50A794W": {
            "status": "success",
            "has_record": True,
            "offenses": ["DUI", "speeding"],
            "severity": "MEDIUM"
        }
    }

    if fiscal_code_normalized in mock_judicial_db:
        return mock_judicial_db[fiscal_code_normalized]
    else:
        # Clean record for unknown persons
        return {
            "status": "success",
            "has_record": False,
            "offenses": [],
            "severity": "NONE"
        }


def get_risk_evaluation_by_judicial_record(fiscal_code: str) -> dict:
    """Retrieves the complete risk evaluation based on judicial records

    Args:
        fiscal_code (str): The Italian fiscal code of the person

    Returns:
        dict: A dictionary containing the risk evaluation.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes 'risk_level' and 'evaluation' keys.
              If 'error', includes an 'error_message' key.
    """
    record_result = check_judicial_record(fiscal_code)

    if record_result["status"] == "error":
        return record_result

    has_record = record_result.get("has_record", False)
    offenses = record_result.get("offenses", [])
    severity = record_result.get("severity", "NONE")

    if not has_record:
        return {
            "status": "success",
            "risk_level": "LOW",
            "evaluation": f"Fiscal code {fiscal_code}: Clean judicial record. No previous offenses found."
        }

    # Map severity to risk level
    severity_to_risk = {
        "VERY_HIGH": {
            "risk_level": "VERY_HIGH",
            "evaluation": f"Fiscal code {fiscal_code}: Critical judicial record with serious offenses including {', '.join(offenses)}. High probability of future claims."
        },
        "HIGH": {
            "risk_level": "HIGH",
            "evaluation": f"Fiscal code {fiscal_code}: Significant judicial record with offenses: {', '.join(offenses)}. Elevated risk profile."
        },
        "MEDIUM": {
            "risk_level": "MEDIUM",
            "evaluation": f"Fiscal code {fiscal_code}: Moderate judicial record with offenses: {', '.join(offenses)}. Standard elevated risk."
        },
        "LOW": {
            "risk_level": "LOW",
            "evaluation": f"Fiscal code {fiscal_code}: Minor offenses found ({', '.join(offenses)}). Low impact on risk assessment."
        }
    }

    result = severity_to_risk.get(severity, severity_to_risk["LOW"])
    return {"status": "success", **result}


def validate_fiscal_code(fiscal_code: str) -> dict:
    """Validates the format of an Italian fiscal code

    Args:
        fiscal_code (str): The fiscal code to validate

    Returns:
        dict: A dictionary with validation result.
              Includes 'is_valid' boolean and optional 'message' string.
    """
    fiscal_code_normalized = fiscal_code.upper().replace(" ", "")

    # Basic validation: must be 16 characters, alphanumeric
    if len(fiscal_code_normalized) != 16:
        return {
            "is_valid": False,
            "message": f"Fiscal code must be 16 characters long, got {len(fiscal_code_normalized)}"
        }

    if not fiscal_code_normalized.isalnum():
        return {
            "is_valid": False,
            "message": "Fiscal code must contain only letters and numbers"
        }

    return {
        "is_valid": True,
        "message": "Fiscal code format is valid"
    }
