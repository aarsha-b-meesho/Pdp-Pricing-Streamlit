import requests

def fetch_product_details(product_id):
    url = "http://taxonomy-new.prd.meesho.int/api/v2/product/aggregation"
    headers = {"Content-Type": "application/json"}
    payload = {
        "product_ids": [product_id],
        "request_flags": {
            "fetch_old_sscat_details": True,
            "fetch_serving_data": True,
            "fetch_taxonomy_attributes": True
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()

        # Extract the required fields
        extracted_data = {
            "catalog_id": data["catalogs"][0]["id"],
            "catalog_name": data["catalogs"][0]["name"],
            "old_sub_sub_category_id": data["catalogs"][0]["old_category"]["sub_sub_category_id"],
            "sscat_name":data["catalogs"][0]["old_category"]["sub_sub_category_name"],
            "product_images": data["products"][0]["images"]
        }

        return extracted_data
    else:
        raise Exception(f"Failed to fetch product details. HTTP Status: {response.status_code}, Response: {response.text}")

if __name__=="__main__":
    # Example usage:
    product_id = 389003792
    try:
        details = fetch_product_details(product_id)
        print(details)
    except Exception as e:
        print(e)
