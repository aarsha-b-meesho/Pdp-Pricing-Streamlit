import grpc
from pricing import pricing_service_pb2, pricing_service_pb2_grpc

BATCH_SIZE = 70

def get_pricing_features(user_id, parent_pid, pdp_data, client_id, user_pincode, app_version_code, pricing_features):
    """
    Fetches pricing features for multiple (user_id, product_id) pairs using gRPC in batches of 10.
    Returns a dictionary: {product_id: {feature_name: feature_value, ...}}
    """
    all_pids = [parent_pid] + [pid for pid, *_ in pdp_data]
    results = {}

    # Split into batches of 10
    for i in range(0, len(all_pids), BATCH_SIZE):
        batch = all_pids[i:i+BATCH_SIZE]

        # Call the original logic on each batch
        batch_result = _fetch_pricing_batch(
            user_id=user_id,
            product_ids=batch,
            client_id=client_id,
            user_pincode=user_pincode,
            app_version_code=app_version_code,
            pricing_features=pricing_features
        )
        results.update(batch_result)

    return results


def _fetch_pricing_batch(user_id, product_ids, client_id, user_pincode, app_version_code, pricing_features):
    """
    Internal function to fetch one batch of pricing data via gRPC.
    """
    channel = grpc.insecure_channel('price-aggregator-go.prd.meesho.int:80')

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
        # Prepare IDs
        ids = []
        for pid in product_ids:
            entity_id = pricing_service_pb2.EntityQueries.EntityId(keys=[
                pricing_service_pb2.EntityQueries.EntityId.EntityKey(type="user_id", value=str(user_id)),
                pricing_service_pb2.EntityQueries.EntityId.EntityKey(type="product_id", value=str(pid))
            ])
            ids.append(entity_id)

        # Feature group
        feature_group = pricing_service_pb2.EntityQueries.FeatureGroups(
            label="real_time_product_pricing",
            features=pricing_features
        )

        # Full request
        request = pricing_service_pb2.EntityQueries(
            label="user_product",
            ids=ids,
            featureGroups=[feature_group]
        )

        stub = pricing_service_pb2_grpc.PricingFeatureRetrievalServiceStub(channel)
        response = stub.retrieveFeatures(request=request, metadata=metadata)

        # Parse response
        result = {}
        data = response.data

        if not data or len(data) < 2:
            print("No data received or only headers.")
            return {}

        headers = data[0].features
        print("Headers:", headers)

        for row in data[1:]:
            features = row.features
            if len(features) != len(headers):
                print(f"Skipping row due to mismatched lengths: {features}")
                continue

            feature_map = dict(zip(headers, features))
            product_id = feature_map.get("product_id")

            if not product_id:
                print("No product_id found in row; skipping.")
                continue

            # Remove identifying fields, return only requested features
            filtered = {
                k: v for k, v in feature_map.items()
                if k not in ("user_id", "product_id")
            }

            result[product_id] = filtered

        return result

    except grpc.RpcError as e:
        print(f"[gRPC Error] {e}")
        return {}

    finally:
        channel.close()


if __name__ == "__main__":
    user_id = "326765744"
    parent_pid = 427274849
    pdp_data = [
        (425811861, "source1", ""),
        (427275225, "source2", ""),
        (517156785, "source3", ""),
        (511316437, "source4", ""),
        (536444742, "source5", ""),
        (517263786, "source6", ""),
        (504131719, "source7", ""),
        (445403301, "source8", ""),
        (521966460, "source9", ""),
        (550478849, "source10", ""),
        (427173453, "source11", ""),
        (549666653, "source12", ""),
        (251228364, "source13", "")
    ]

    pricing_features = ["real_time_product_pricing:principle_supplier_id"]

    result = get_pricing_features(
        user_id=user_id,
        parent_pid=parent_pid,
        pdp_data=pdp_data,
        client_id="android",
        user_pincode="560001",
        app_version_code="685",
        pricing_features=pricing_features
    )

    print("\nFinal BATCHED Output:")
    for pid, features in result.items():
        print(f"{pid}: {features}")
