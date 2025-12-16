from ...shared_libraries.types import RiskEvaluation

# This should be a call that discriminates zone by tariff
def get_zone(city: str, tariff_id: str) -> dict:
    """Retrieves the geographic zone of a given city

    Args:
        city (str): The name of the city (e.g., "Milano", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'zone ID'
              If 'error', includes an 'error_message' key.
    """
    city_normalized = city.lower().replace(" ", "")

    # At the moment, we do not use the tariff ID as a discriminator, but
    # in a real use case, the tariff ID actually determines the classification
    # of the cities on geographical zones
    mock_zone_db = {
        "milano": {"status": "success", "zone_id": "1"},
        "pavia": {"status": "success", "zone_id": "2"},
        "napoli": {"status": "success", "zone_id": "3"}
    }
    if city_normalized in mock_zone_db:
        return mock_zone_db[city_normalized]
    else:
        return {"status": "success", "zone_id": "4"} 


def get_risk_evaluation_by_zone(zone_id: str) -> RiskEvaluation:
    """Retrieves the risk given a zone

    Args:
        zone_id (str): the identifier of the geographical zone

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes the risk level 'risk_level'
              If 'error', includes an 'error_message' key.
    """
    mock_risk_db = {
        "1": {"status": "success", "risk_level": "HIGH"},
        "2": {"status": "success", "risk_level": "LOW"},
        "3": {"status": "success", "risk_level": "VERY_HIGH"},
        "4": {"status": "success", "risk_level": "LOW"}
    }

    if zone_id in mock_risk_db:
        return mock_risk_db[zone_id]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have risk information for '{zone_id}'."}