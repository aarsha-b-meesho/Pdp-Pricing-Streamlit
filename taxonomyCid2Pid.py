import requests

def get_hero_products(catalog_ids):
    """
    Fetches hero product IDs for the given catalog IDs.

    Parameters:
    catalog_ids (list): List of catalog IDs.

    Returns:
    list: Hero product IDs in the same order as catalog IDs.
    """
    url = "http://taxonomy-read.prd.meesho.int/api/v1/products/hero-product"
    headers = {
        "Authorization": "Token bYTFfK5Czo42zfhMmPQoUvXmWiSJ9fV8EbTKdQfDFL4A40tJ",
        "MEESHO-ISO-COUNTRY-CODE": "IN",
        "Content-Type": "application/json"
    }
    payload = {
        "catalog_ids": catalog_ids
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()

        # Map catalog_id to hero_product
        catalog_to_product = {item["catalog_id"]: item["hero_product"] for item in response_data.get("data", [])}

        # # Ensure hero products are returned in the same order as catalog_ids
        # hero_products = [catalog_to_product.get(catalog_id, None) for catalog_id in catalog_ids]
        return catalog_to_product
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return []
    except KeyError as e:
        print(f"Missing key in response: {e}")
        return []

if __name__=="__main__":
    # Example usage
    catalog_ids_input = [75235810, 50284666, 35960953, 12522103, 108569948, 109918650, 108585357, 129922250]
    hero_products = get_hero_products(catalog_ids_input)
    print("Hero Products:", hero_products)
