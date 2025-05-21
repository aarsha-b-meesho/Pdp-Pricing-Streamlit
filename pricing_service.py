import grpc
from pricing import pricing_service_pb2, pricing_service_pb2_grpc
from google.protobuf.json_format import MessageToJson

def get_pricing_features(user_id, parent_pid, pdp_data, client_id, user_pincode, app_version_code,pricing_features):
    """
    Fetches pricing features for multiple user ID and product ID pairs using gRPC.

    Parameters:
    user_id (str): User ID for the request
    parent_pid (int): Parent product ID
    pdp_data (list): List of tuples containing (hero_pid, source)
    client_id (str): Client ID (ios/android)
    user_pincode (str): User's pincode
    app_version_code (str): App version code

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

        # Add parent PID first
        user_key = pricing_service_pb2.EntityQueries.EntityId.EntityKey(
            type="user_id",
            value=str(user_id)
        )
        product_key = pricing_service_pb2.EntityQueries.EntityId.EntityKey(
            type="product_id",
            value=str(parent_pid)
        )
        entity_id = pricing_service_pb2.EntityQueries.EntityId(
            keys=[user_key, product_key]
        )
        ids.append(entity_id)

        # Add all hero PIDs from pdp_data
        for hero_pid,_, _ in pdp_data:
            user_key = pricing_service_pb2.EntityQueries.EntityId.EntityKey(
                type="user_id",
                value=str(user_id)
            )
            product_key = pricing_service_pb2.EntityQueries.EntityId.EntityKey(
                type="product_id",
                value=str(hero_pid)
            )
            entity_id = pricing_service_pb2.EntityQueries.EntityId(
                keys=[user_key, product_key]
            )
            ids.append(entity_id)

        # Create FeatureGroups
        feature_group = pricing_service_pb2.EntityQueries.FeatureGroups(
            label="real_time_product_pricing",
            features=pricing_features
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
                        j=2
                        if len(response.data[i+1].features) >= 3:
                            for feature in pricing_features:
                                features[feature] = str(response.data[i+1].features[j])
                                j+=1
                        result[response.data[i+1].features[1]] = features
        return result
    except grpc.RpcError as e:
        print(f"gRPC call failed: {e}")
        return {}
    finally:
        channel.close()

if __name__ == "__main__":
    # Example usage
    user_id = "100000239"
    parent_pid = 138858198
    pdp_data = [(50284666, "source1"), (50284667, "source2")]
    pricing_features = get_pricing_features(user_id, parent_pid, pdp_data, "ios", "122001", "685")

