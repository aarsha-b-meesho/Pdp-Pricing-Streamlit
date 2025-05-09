import requests
import json

def get_recommendations(catalog_id, user_id,client_id, limit=20, ):
    """
    Fetches recommendations for a given catalog ID and user ID.

    Parameters:
    catalog_id (int): The catalog ID to get recommendations for
    user_id (int): The user ID
    limit (int): Number of recommendations to fetch (default: 5)

    Returns:
    list: List of hero_pids from the recommendations
    """
    url = "http://rx-fa-recommendations.prd.meesho.int/api/v1/recommendations"
    
    headers = {
        "MEESHO-USER-ID": str(user_id),
        "APP-USER-ID": str(user_id),
        "MEESHO-USER-CITY": "Bangalore",
        "MEESHO_USER_CONTEXT": "logged_in",
        "MEESHO-CLIENT-ID": str(client_id),
        "MEESHO-ISO-COUNTRY-CODE": "IN",
        "Content-Type": "application/json"
    }
    
    payload = {
        "catalog_id": catalog_id,
        "user_id": str(user_id),
        "limit": limit,
        "sub_sub_category_id": "",
        "offset": 0
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Extract hero_pids in the same order as they appear in the response
        hero_pids = [catalog["hero_pid"] for catalog in data.get("catalogs", [])]
        return hero_pids
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    catalog_id = 55877126
    user_id = 344572052
    hero_pids = get_recommendations(catalog_id, user_id)
    print("Hero PIDs:", hero_pids) 