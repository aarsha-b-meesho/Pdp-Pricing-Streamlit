import grpc
from pdp_iop_grpc import service_pb2_grpc, request_pb2, response_pb2

def get_catalog_ids(parent_entity_id):
    """
    Fetches catalog IDs for a given parent entity ID using gRPC.

    Parameters:
    parent_entity_id (int): The parent entity ID.

    Returns:
    list: List of catalog IDs from the response.
    """
    # Create gRPC channel
    channel = grpc.insecure_channel('pdp-iop-grpc-service-web.prd.meesho.int:80')
    
    # Create metadata (headers)
    metadata = [
        ('meesho-user-id', '241351057'),
        ('meesho-user-context', 'logged_in')
    ]

    try:
        # Create the request message using the generated proto classes
        request_data = request_pb2.RequestData(
            parentEntityId=parent_entity_id,
            parentEntityType="catalog",
            feedContext="default",
            limit=20
        )
        
        feed_request = request_pb2.GetSimilarEntityFeedRequest(
            data=request_data
        )
        
        request = request_pb2.GetSimilarEntityOrganicFeedRequest(
            request=feed_request
        )
        
        # Create a stub for the PdpIopService
        stub = service_pb2_grpc.PdpIopServiceStub(channel)
        
        # Make the gRPC call using the generated stub
        response = stub.FetchExploitSimilarEntityFeed(request, metadata=metadata)
        
        # Extract catalog IDs from the response
        similar_entities = response.response.data.similarEntities
        catalog_ids = [entity.id for entity in similar_entities]
        return catalog_ids
    except grpc.RpcError as e:
        print(f"gRPC call failed: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        channel.close()

if __name__ == "__main__":
    # Example usage
    parent_entity_id_input = 69902829
    catalog_ids = get_catalog_ids(parent_entity_id_input)