import requests

def get_cross_sell_recommendations(product_id, user_id="6105390", limit=10):
    """
    Fetch cross-sell recommendations for a given product ID.

    Args:
        product_id (int): The ID of the product for which recommendations are needed.
        user_id (str): The user ID making the request. Default is "6105390".
        limit (int): The maximum number of recommendations to retrieve. Default is 10.

    Returns:
        dict: The JSON response from the API.
    """
    url = "http://reco-engine-web.prd.meesho.int/api/v1/reco/cross-sell/widget"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "limit": limit,
        "metadata": {
            "screen": "single_product",
            "product_ids": [product_id]
        },
        "user_id": user_id
    }

    # try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    return response.json()


if __name__=="__main__":
    # Example usage
    product_id = 326765744
    response = get_cross_sell_recommendations(product_id)

    if response:
        print(response)

    #(productId=456605192, catalogId=139464093, sscatId=3111) [3111, 1268, 2426, 2066, 2406, 3008, 1580, 1422, 4495, 3009]
