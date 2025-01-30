import  requests
from taxonomyHandler import fetch_product_details
from concurrent.futures import ThreadPoolExecutor


def get_cross_sell_feed_recommendations(parent_product_id,clicked_product,clicked_sscat,user_id,limit=16,screen="place_order"):
    url = "http://reco-engine-web.prd.meesho.int/api/v1/reco/cross-sell/feed"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "widget_parent_product_id":parent_product_id,
        "click_context": {
            "product_id": clicked_product,
            "sscat_id": clicked_sscat
        },
        "limit": limit,
        "screen": screen,
        "user_id": str(user_id),
        "tenant": "CROSS_SELL"
    }
    # try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    return response.json()


def get_cross_sell_feed_with_metadata(parent_product_id,clicked_pid,clicked_sscat_id,user_id,screen="place_order"):
    try:
        cross_sell_feed = get_cross_sell_feed_recommendations(parent_product_id,clicked_pid,clicked_sscat_id,user_id,16,screen)
        # print("cross_sell_feed = get_cross_sell_feed_recommendations(product_id)",cross_sell_feed)
        if "entities" in cross_sell_feed:
            metadata = fetch_product_details(cross_sell_feed["entities"])
            return metadata
        return []
    except Exception as e:
        print("Error while fetching cross_sell_feed_recommendations")

def get_cross_sell_feed_with_metadata_from_widget_response(recommendations, parent_product_id, user_id,screen="place_order"):
    input_data_for_each_sscat = [
        [parent_product_id, each_tiles["product_id"], each_tiles["sscat_id"], user_id,screen]
        for each_tiles in recommendations
    ]

    # Execute calls in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_cross_sell_feed_with_metadata, *input_data) for input_data in input_data_for_each_sscat]

        # Wait for all futures to complete and collect responses
        responses = [future.result() for future in futures]

    # Merge responses
    merged_response = []
    for each_tiles_resp in responses:
        merged_response.extend(each_tiles_resp)

    return merged_response

def get_cross_sell_feed_with_metadata_from_widget(widget_response,user_id,screen="place_order"):
    recommendations = widget_response["recommendations"]
    parent_pid = widget_response["parent_metadata"]["product_id"]
    return get_cross_sell_feed_with_metadata_from_widget_response(recommendations,parent_pid,user_id,screen)


if __name__=="__main__":
    # Example usage
    # parent_product_id = 341933586
    # clicked_pid = 391963241
    # clicked_sscat_id = 1093
    # user_id =  251078202
    widget_resp = {
        "recommendations": [
            {
                "product_id": 394240561,
                "catalog_id": 115240667,
                "sscat_id": 5090,
                "sscat_name": "Cross Body Bags & Sling Bags",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/394240561/mijkq.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Cross Body Bags & Sling Bags"
                }
            },
            {
                "product_id": 106381581,
                "catalog_id": 30740942,
                "sscat_id": 1039,
                "sscat_name": "Palazzos",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/106381581/9rh4y.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Palazzos"
                }
            },
            {
                "product_id": 159720126,
                "catalog_id": 48282358,
                "sscat_id": 1853,
                "sscat_name": "Dupatta Sets",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/159720126/2r52u.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Dupatta Sets"
                }
            },
            {
                "product_id": 383014579,
                "catalog_id": 111498868,
                "sscat_id": 1091,
                "sscat_name": "Earrings & Studs",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/383014579/lwpis.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Earrings & Studs"
                }
            },
            {
                "product_id": 85630166,
                "catalog_id": 24359256,
                "sscat_id": 1093,
                "sscat_name": "Jewellery Set",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/85630166/cisnh.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Jewellery Set"
                }
            },
            {
                "product_id": 31959729,
                "catalog_id": 7651410,
                "sscat_id": 1034,
                "sscat_name": "Trousers & Pants",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/31959729/rj4nc.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Trousers & Pants"
                }
            },
            {
                "product_id": 364586199,
                "catalog_id": 105823868,
                "sscat_id": 1094,
                "sscat_name": "Bangles & Bracelets",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/364586199/x0ieq.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Bangles & Bracelets"
                }
            },
            {
                "product_id": 68649156,
                "catalog_id": 18598191,
                "sscat_id": 1035,
                "sscat_name": "Leggings & Tights ",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/68649156/vjgzy.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Leggings & Tights "
                }
            },
            {
                "product_id": 295232413,
                "catalog_id": 85937417,
                "sscat_id": 1032,
                "sscat_name": "Jeans",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/295232413/mew55.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Jeans"
                }
            },
            {
                "product_id": 324726367,
                "catalog_id": 94442941,
                "sscat_id": 1006,
                "sscat_name": "Dupattas",
                "widget_metadata": {
                    "image": "https://images.meesho.com/images/products/324726367/ua5ic.jpg",
                    "price": None,
                    "rating": None,
                    "title": "Dupattas"
                }
            }
        ],
        "parent_metadata": {
            "product_id": 40669725,
            "catalog_id": 9765072,
            "sscat_id": 1001,
            "sscat_name": None,
            "image": "https://images.meesho.com/images/products/40669725/s39nn.jpg"
        },
        "feed_source": "DS_BATCH"
    }
    response = get_cross_sell_feed_with_metadata_from_widget(widget_resp,14086668)

    if response:
        print(response)
