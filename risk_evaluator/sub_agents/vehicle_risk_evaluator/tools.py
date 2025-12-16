from shared_libraries.types import RiskEvaluation, RiskScore


def get_brand_risk_category(brand: str) -> dict:
    """Retrieves the risk category of a vehicle brand

    Args:
        brand (str): The brand of the vehicle (e.g., "Ferrari", "BMW", "Volkswagen").

    Returns:
        dict: A dictionary containing the risk category information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'category' key with the risk category.
              If 'error', includes an 'error_message' key.
    """
    brand_normalized = brand.lower().replace(" ", "").replace("-", "")

    # Very high risk brands (exotic/super sports cars)
    very_high_risk_brands = {
        "ferrari", "lamborghini", "bugatti", "mclaren", "pagani",
        "koenigsegg", "astonmartin", "bentley", "rollsroyce", "maybach"
    }

    # High risk brands (premium/performance brands)
    high_risk_brands = {
        "bmw", "mercedes", "mercedesbenz", "audi", "porsche", "maserati",
        "lexus", "alfa", "alfaromeo", "jaguar", "landrover"
    }

    # Medium risk brands (mainstream brands)
    medium_risk_brands = {
        "volkswagen", "vw", "peugeot", "renault", "citroen", "opel",
        "ford", "chevrolet", "nissan", "mazda", "honda", "toyota",
        "seat", "skoda", "hyundai", "kia", "mitsubishi", "subaru"
    }

    if brand_normalized in very_high_risk_brands:
        return {"status": "success", "category": "VERY_HIGH"}
    elif brand_normalized in high_risk_brands:
        return {"status": "success", "category": "HIGH"}
    elif brand_normalized in medium_risk_brands:
        return {"status": "success", "category": "MEDIUM"}
    else:
        # Default to low risk for unknown/other brands
        return {"status": "success", "category": "LOW"}


def get_risk_evaluation_by_brand(brand: str) -> dict:
    """Retrieves the complete risk evaluation for a vehicle brand

    Args:
        brand (str): The brand of the vehicle

    Returns:
        dict: A dictionary containing the risk evaluation.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes 'risk_level' and 'evaluation' keys.
              If 'error', includes an 'error_message' key.
    """
    category_result = get_brand_risk_category(brand)

    if category_result["status"] == "error":
        return category_result

    category = category_result["category"]

    evaluations = {
        "VERY_HIGH": {
            "risk_level": "VERY_HIGH",
            "evaluation": f"Brand '{brand}' is classified as a luxury/exotic vehicle with very high theft risk and repair costs."
        },
        "HIGH": {
            "risk_level": "HIGH",
            "evaluation": f"Brand '{brand}' is a premium vehicle with elevated theft risk and expensive parts."
        },
        "MEDIUM": {
            "risk_level": "MEDIUM",
            "evaluation": f"Brand '{brand}' is a mainstream vehicle with moderate risk profile."
        },
        "LOW": {
            "risk_level": "LOW",
            "evaluation": f"Brand '{brand}' presents low risk with standard theft rates and affordable repairs."
        }
    }

    result = evaluations.get(category, evaluations["LOW"])
    return {"status": "success", **result}
