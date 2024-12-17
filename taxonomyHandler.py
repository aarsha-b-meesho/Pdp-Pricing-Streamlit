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
        return result
    else:
        raise Exception(f"Failed to fetch product details. HTTP Status: {response.status_code}, Response: {response.text}")
# [352292258, 405099957, 428269549, 414147213, 372416880, 357020004, 119656115, 170425950, 191890524, 295954925, 114300299, 100537408, 370491889, 294221102, 309228505, 406169195, 397253798, 297261478, 234954124, 417043475, 403567197, 371223663, 250850042]
if __name__=="__main__":
    # Example usage:
    product_id = [377791243]
    product_id = [352292258, 405099957, 428269549, 414147213, 372416880, 357020004, 119656115, 170425950, 191890524, 295954925, 114300299, 100537408, 370491889, 294221102, 309228505, 406169195, 397253798, 297261478, 234954124, 417043475, 403567197, 371223663, 250850042]
    try:
        details = fetch_product_details(product_id)
        print(details)
    except Exception as e:
        print(e)
