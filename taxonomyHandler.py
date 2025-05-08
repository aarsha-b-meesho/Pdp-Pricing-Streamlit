import requests
from math import ceil

def fetch_product_details(product_id_list):
    url = "http://taxonomy-new.prd.meesho.int/api/v2/product/aggregation"
    headers = {"Content-Type": "application/json"}
    batch_size = 100  # Process in batches of 100
    combined_result = []

    # Split product_id_list into batches
    total_batches = ceil(len(product_id_list) / batch_size)
    for i in range(total_batches):
        batch_start = i * batch_size
        batch_end = min(batch_start + batch_size, len(product_id_list))
        batch = product_id_list[batch_start:batch_end]

        # Prepare payload
        payload = {
            "product_ids": batch,
            "request_flags": {
                "fetch_old_sscat_details": True,
                "fetch_serving_data": True,
                "fetch_taxonomy_attributes": True
            }
        }

        # Send request
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
                    "sscat_name": each_product_from_taxonomy["old_category"]["sub_sub_category_name"],
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

            # Reorder products in the batch
            if len(batch) == 1:
                combined_result.extend(result)
                continue

            result_pid_to_index = {result[i]['product_id']: i for i in range(len(result))}
            reordered_products = []
            for product_id in batch:
                if product_id in result_pid_to_index:
                    reordered_products.append(result[result_pid_to_index[product_id]])

            combined_result.extend(reordered_products)
        else:
            raise Exception(f"Failed to fetch product details. HTTP Status: {response.status_code}, Response: {response.text}")

    return combined_result

if __name__=="__main__":
    # Example usage:
    a = {112569077: 386359262, 126277801: 425811702, 27909875: 97381557, 129297990: 434232186, 117816617: 401701240, 1401871: 8358683, 117892257: 401913520, 118998546: 405237731, 121924211: 413785616, 78522112: 266390648, 129385822: 434520129, 102528547: 353624790, 102093840: 352089873, 103766416: 357843805, 94227719: 323954795, 116700745: 398406628, 91693246: 314906679, 72317847: 241759081, 125105906: 422633165, 129524223: 434930832}
    # a = {95007398: 326765744}
    pids = [a[key] for key in a]
    # product_id = [295954925]
    product_id = pids
    try:
        details = fetch_product_details(product_id)
    except Exception as e:
        print(e)
