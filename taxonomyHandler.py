import requests

def fetch_product_details(product_id_list):
    url = "http://taxonomy-new.prd.meesho.int/api/v2/product/aggregation"
    headers = {"Content-Type": "application/json"}
    payload = {
        "product_ids": product_id_list,
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
        result = []
        for each_product_from_taxonomy in data["catalogs"]:
            extracted_data = {
                "catalog_id": each_product_from_taxonomy["id"],
                "catalog_name": each_product_from_taxonomy["name"],
                "old_sub_sub_category_id": each_product_from_taxonomy["old_category"]["sub_sub_category_id"],
                "sscat_name":each_product_from_taxonomy["old_category"]["sub_sub_category_name"],
                "product_images": [each_product_from_taxonomy["image"]],
                "product_id": each_product_from_taxonomy['id']
            }
            result.append(extracted_data)
        for each_product_from_taxonomy in data["products"]:
            cid = each_product_from_taxonomy['catalog_id']
            idx = next((i for i, item in enumerate(result) if item["catalog_id"] == cid), None)
            if idx is not None:
                result[idx]["product_id"] = each_product_from_taxonomy["id"]
                result[idx]["product_images"] = each_product_from_taxonomy["images"]
        if len(product_id_list)==1:
            return result
        result_pid_to_index = {result[i]['product_id']:i for i in range(len(result))}
        reordered_products = []
        for product_id in product_id_list:
            if product_id in  result_pid_to_index:
                reordered_products.append(result[result_pid_to_index[product_id]])
        return reordered_products
    else:
        raise Exception(f"Failed to fetch product details. HTTP Status: {response.status_code}, Response: {response.text}")

if __name__=="__main__":
    # Example usage:
    product_id = [295954925]
    try:
        details = fetch_product_details(product_id)
        print(details)
    except Exception as e:
        print(e)
