import  requests
from taxonomyHandler import fetch_product_details

def get_cross_sell_feed_recommendations(product_id,user_id="6105390",limit=100):
    url = "http://reco-engine-web.prd.meesho.int/api/v1/reco/cross-sell/feed"
    productMetaData = fetch_product_details([product_id])
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "parent_product_ids":[product_id],
        "click_context": {
            "product_id": product_id,
            "sscat_id": productMetaData[0]["old_sub_sub_category_id"]
        },
        "limit": limit,
        "screen": "place_order",
        "product_ids": [product_id],
        "user_id": user_id
    }
    # try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    return response.json()


def get_cross_sell_feed_with_metadata(product_id):
    try:
        cross_sell_feed = get_cross_sell_feed_recommendations(product_id)
        if "entities" in cross_sell_feed:
            metadata = fetch_product_details(cross_sell_feed["entities"])
            return metadata
        return []
    except Exception as e:
        return "Error while fetching cross_sell_feed_recommendations"

if __name__=="__main__":
    # Example usage
    product_id = 32074483
    response = get_cross_sell_feed_with_metadata(product_id)

    if response:
        print(response)
