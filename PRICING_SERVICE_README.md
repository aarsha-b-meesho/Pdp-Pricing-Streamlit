# Price Aggregator Service Client

This directory contains the implementation of a gRPC client for the Price Aggregator service.

## Overview

The Price Aggregator service provides pricing information for products based on user and product IDs. This client implementation uses gRPC to communicate with the service.

## Files

- `pricing_service.proto`: Proto definition file that defines the service interface, requests, and responses
- `pricing_service_pb2.py`: Auto-generated Python code from the proto file (messages)
- `pricing_service_pb2_grpc.py`: Auto-generated Python code from the proto file (services)
- `pricing.py`: Main implementation of the client (updated to use new proto definitions)
- `pricing_service.py`: Alternative implementation with same interface
- `test_pricing_service.py`: Test script to verify the implementation

## Usage

```python
from pricing import get_pricing_features

# Example usage
user_id = "100000239"
product_ids = ["2653067", "82360953"]

pricing_features = get_pricing_features(user_id, product_ids)
print("Pricing Features:", pricing_features)
```

## Service Parameters

### Request

The service accepts the following parameters in the gRPC request:

- `label`: A string identifier for the request (e.g., "user_product")
- `ids`: A list of EntityId objects, each containing:
  - `keys`: A list of key-value pairs where:
    - `type`: The type of key (e.g., "user_id", "product_id")
    - `value`: The value for the key
- `featureGroups`: A list of feature groups, each containing:
  - `label`: Identifier for the feature group (e.g., "real_time_product_pricing")
  - `features`: List of feature names to request (e.g., "principle_supplier_id", "strike_off_price", "serving_price")

### Response

The service returns an EntityPayload object containing:

- `entityLabel`: The label of the entity
- `data`: A list of data entries, each containing:
  - `features`: A list of feature values
- `keySize`: The number of keys in the request

## Notes

- The service is accessed at `price-aggregator-go.prd.meesho.int:80`
- The implementation includes necessary metadata headers for the request
- Error handling is included for gRPC communication issues

## Regenerating Proto Files

If you need to update the proto definition and regenerate the Python code:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pricing_service.proto
``` 