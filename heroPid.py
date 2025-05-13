import requests
import json

def get_heroPid(catalog_id):
    """
    Fetches hero product ID for a given catalog ID.

    Parameters:
    catalog_id (int): The catalog ID to get hero product for

    Returns:
    str: Hero product ID if found, None otherwise
    """
    url = "http://taxonomy-hero.prd.meesho.int/api/v1/products/hero-product"

    headers = {
        "Authorization": "Token bYTFfK5Czo42zfhMmPQoUvXmWiSJ9fV8EbTKdQfDFL4A40tJ",
        "MEESHO-ISO-COUNTRY-CODE": "IN",
        "Content-Type": "application/json"
    }

    payload = {
        "catalog_ids": [catalog_id]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extract hero_pid
        hero_pid = data.get("data", [{}])[0].get("hero_product")
        error = data.get("data", [{}])[0].get("errors")
        if not error:
            return hero_pid
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    catalog_id = 100748726
    hero_pid = get_heroPid(catalog_id)
    print("Hero PID:", hero_pid)