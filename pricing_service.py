import grpc
from pricing import pricing_service_pb2, pricing_service_pb2_grpc
from google.protobuf.json_format import MessageToJson

def get_pricing_features(user_id, pdp_data, client_id, user_pincode, app_version_code):
    """
    Fetches pricing features for multiple user ID and product ID pairs using gRPC.

    Parameters:
    user_id (str): User ID for the request
    pdp_data (list): List of product IDs to get pricing for

    Returns:
    dict: Pricing features from the response mapped by product ID
    """
    # Create gRPC channel
    channel = grpc.insecure_channel('price-aggregator-go.prd.meesho.int:80')
    
    # Create metadata (headers)
    metadata = [
        ('meesho-user-id', str(user_id)),
        ('meesho-user-context', 'logged_in'),
        ('meesho-user-city', 'Bangalore'),
        ('meesho_user_context', 'anonymous'),
        ('meesho-client-id', str(client_id)),
        ('meesho-iso-country-code', 'IN'),
        ('meesho-user-pincode', str(user_pincode)),
        ('app-version-code', str(app_version_code))
    ]

    try:
        # Create the request message
        ids = []
        for product_id in pdp_data:
            # Create EntityKey objects for user_id and product_id
            user_key = pricing_service_pb2.EntityQueries.EntityId.EntityKey(
                type="user_id",
                value=str(user_id)
            )
            product_key = pricing_service_pb2.EntityQueries.EntityId.EntityKey(
                type="product_id",
                value=str(product_id)
            )
            
            # Create EntityId with both keys
            entity_id = pricing_service_pb2.EntityQueries.EntityId(
                keys=[user_key, product_key]
            )
            
            ids.append(entity_id)

        # Create FeatureGroups

        feature_group = pricing_service_pb2.EntityQueries.FeatureGroups(
            label="real_time_product_pricing",
            features=["principle_supplier_id", "strike_off_price", "serving_price"]
        )
        
        # Create the complete request
        request = pricing_service_pb2.EntityQueries(
            label="user_product",
            ids=ids,
            featureGroups=[feature_group]
        )

        # Create stub and make the call
        stub = pricing_service_pb2_grpc.PricingFeatureRetrievalServiceStub(channel)
        response = stub.retrieveFeatures(
            request=request,
            metadata=metadata
        )

        # Process response
        result = {}
        # Check if we got data back
        if response.data:
            # Extract features from each data entry
            for i, _ in enumerate(response.data):
                if i < len(ids):  # Make sure we have a corresponding id
                    # Find the product_id from the corresponding EntityId
                    product_id = None
                    for key in ids[i].keys:
                        if key.type == "product_id":
                            product_id = key.value
                            break
                    
                    if product_id:
                        # Extract features
                        features = {}
                        if len(response.data[i+1].features) >= 3:
                            features["principle_supplier_id"] = str(response.data[i+1].features[2])
                            features["strike_off_price"] = str(response.data[i+1].features[3])
                            features["serving_price"] = str(response.data[i+1].features[4])
                        
                        result[product_id] = features
        
        return result
    except grpc.RpcError as e:
        print(f"gRPC call failed: {e}")
        return {}
    finally:
        channel.close()

if __name__ == "__main__":
    # Example usage
    user_id = "100000239"
    product_ids = [138858198, 50284666]
    pricing_features = get_pricing_features(user_id, product_ids)

