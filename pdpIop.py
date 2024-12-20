import requests

def get_catalog_ids(parent_entity_id):
    """
    Fetches catalog IDs for a given parent entity ID.

    Parameters:
    parent_entity_id (int): The parent entity ID.

    Returns:
    list: List of catalog IDs from the response.
    """
    url = "http://pdp-iop-service-web.prd.meesho.int/api/v1/entities/exploit"
    headers = {
        "MEESHO-USER-ID": "14409845",
        "MEESHO-TENANT-CONTEXT": "organic",
        "Content-Type": "application/json",
        "Authorization": "HrRRsCqQ203i1PVnL1TfNY0Tt9QW9SXzTRE1mEI6B4LhzSdVa2tFqyoDVvnyZV1i",
        "MEESHO-USER-CONTEXT": "logged_in"
    }
    payload = {
        "data": {
            "cursor": None,
            "parent_entity_id": parent_entity_id,
            "parent_entity_type": "catalog",
            "limit": 15
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()

        # Extract catalog IDs from the response
        similar_entities = response_data.get("data", {}).get("similar_entities", [])
        catalog_ids = [entity["id"] for entity in similar_entities]
        return catalog_ids
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return []
    except KeyError as e:
        print(f"Missing key in response: {e}")
        return []

if __name__=="__main__":
    # Example usage
    parent_entity_id_input = 69902829
    catalog_ids = get_catalog_ids(parent_entity_id_input)
    print("Catalog IDs:", catalog_ids)
