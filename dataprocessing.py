def process_data(pdp_data, pricing_data, taxonomy_data):
    """
    Process and combine data from different sources.
    
    Parameters:
    pdp_data (list): List of product IDs
    pricing_data (dict): Dictionary of pricing features by product ID
    taxonomy_data (list): List of taxonomy data for products
    
    Returns:
    dict: Combined data with recommendations and parent metadata
    """
    try:
        combined_data = {}

        # Initialize structure for each product ID
        for product_id in pdp_data:
            combined_data[str(product_id)] = {
                "pdp_features": {},
                "pricing_features": {},
                "taxonomy_features": {}
            }

        # Create a mapping from product_id to catalog_id
        product_to_catalog = {
            str(item.get("product_id")): item.get("catalog_id")
            for item in taxonomy_data
            if item.get("product_id") and item.get("catalog_id")
        }

        # Add PDP data using the taxonomy mapping
        for product_id in pdp_data:
            product_id_str = str(product_id)
            catalog_id = product_to_catalog.get(product_id_str)
            if catalog_id:
                combined_data[product_id_str]["pdp_features"] = {
                    "catalog_id": catalog_id
                }

        # Add pricing features
        for product_id in combined_data:
            price_info = pricing_data.get(product_id)
            if price_info:
                combined_data[product_id]["pricing_features"] = {
                    "strike_off_price": price_info.get("strike_off_price"),
                    "serving_price": price_info.get("serving_price"),
                    "principle_supplier_id": price_info.get("principle_supplier_id")
                }

        # Add taxonomy features
        for product in taxonomy_data:
            product_id = str(product.get("product_id"))
            if product_id in combined_data:
                combined_data[product_id]["taxonomy_features"] = {
                    "catalog_name": product.get("catalog_name"),
                    "sscat_id": product.get("old_sub_sub_category_id"),
                    "sscat_name": product.get("sscat_name"),
                    "images": product.get("product_images", [])
                }

        return {
            "recommendations": combined_data,
            "parent_metadata": taxonomy_data[0] if taxonomy_data else None
        }
    except Exception as e:
        print(f"Error in process_data: {str(e)}")
        return None
