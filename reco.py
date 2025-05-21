import requests
import json
import grpc
from feed_aggregator import api_pb2, api_pb2_grpc

def get_recommendations_grpc(catalog_id, user_id, client_id, limit=70):
    """Fetches recommendations using gRPC for a given catalog ID.

    Parameters:
    catalog_id (int): The catalog ID to get recommendations for
    user_id (int): The user ID for the request
    client_id (str): The client ID for metadata
    limit (int): Number of recommendations to fetch (default: 70)

    Returns:
    list: List of tuples containing (hero_pid, source) from the recommendations
    """
    # Create gRPC channel
    channel = grpc.insecure_channel('feed-aggregator-web.prd.meesho.int:80')
    stub = api_pb2_grpc.PdpFeedHandlerStub(channel)

    # Create request data
    request = api_pb2.RecommendationsRequest(
        catalog_id=catalog_id,
        limit=limit,
        offset=0,
        cursor=""
    )
    metadata = [
        ('meesho-user-id', str(user_id)),
        ('meesho-user-context', 'logged_in'),
        ('meesho-client-id', str(client_id)),
    ]

    try:
        # Make gRPC call
        response = stub.FetchPdpFeed(
            request=request,
            metadata=metadata
        )

        # Extract hero_pids and sources from catalogs
        recommendations = []
        for catalog in response.catalogs:
            hero_pid = catalog.hero_pid
            source = catalog.source
            id=catalog.id
            if hero_pid:
                recommendations.append((hero_pid,id, source))

        return recommendations

    except grpc.RpcError as e:
        print(f"Error making gRPC request: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    catalog_id = 55877126
    user_id = 12345678
    client_id = "ios"

    # Get recommendations using gRPC
    recommendations = get_recommendations_grpc(catalog_id, user_id, client_id)
    print("Recommendations (hero_pid, source):", recommendations)

    # Optional: implement legacy REST version as needed
    # hero_pids = get_recommendations(catalog_id, user_id, client_id)
    # print("Hero PIDs (legacy):", hero_pids)
