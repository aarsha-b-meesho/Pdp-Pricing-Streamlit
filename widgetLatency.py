import requests
import time
import threading
from typing import List, Tuple

# Function to make an HTTP request
def make_request(product_id: int) -> Tuple[int,int,int, float]:
    url = "http://reco-engine-web.prd.meesho.int/api/v1/reco/cross-sell/widget"
    headers = {"Content-Type": "application/json"}
    payload = {
        "limit": 10,
        "metadata": {
            "screen": "place_order",
            "product_ids": [product_id]
        },
        "user_id": "390374537"
    }

    start_time = time.time()
    response = requests.post(url, headers=headers, json=payload)
    latency = time.time() - start_time
    jsonResponse = response.json()
    # print(jsonResponse)
    recosLength = 0
    if response.status_code==200:
        recosLength = len(jsonResponse.get("recommendations", []))
    return response.status_code,recosLength,product_id, latency

# Function to process a batch of requests
def process_batch(product_ids: List[int], results: List[Tuple[int, float]]):
    threads = []
    for product_id in product_ids:
        thread = threading.Thread(target=lambda pid: results.append(make_request(pid)), args=(product_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main function to handle requests in batches
def main(product_ids: List[int]):
    batch_size = 2
    results = []

    for i in range(0, len(product_ids), batch_size):
        batch = product_ids[i:i + batch_size]
        process_batch(batch, results)
        time.sleep(1)  # Ensures 10 requests per second

    return results

# Example usage
if __name__ == "__main__":
    # Sample list of product IDs
    product_ids = [i for i in range(1, 1001)]  # Example list of 1000 product IDs
    product_ids = [429077049,
                   124613058,
                   365504383,
                   328813546,
                   416776367,
                   420441629,
                   367585522,
                   224664942,
                   8653029,
                   12533124,
                   373488387,
                   421983350,
                   54993123,
                   140661625,
                   68548412,
                   429481631,
                   426958094,
                   160186373,
                   92319278,
                   420025179,
                   87966039,
                   392591520,
                   73329501,
                   32744446,
                   419947845,
                   406098504,
                   385712523,
                   249192608,
                   417079547,
                   405030443,
                   402223797,
                   72329902,
                   298190494,
                   409123973,
                   232841787,
                   7528882,
                   401156206,
                   17070408,
                   420656433,
                   296071456,
                   241204876,
                   20419085,
                   417683715,
                   374264634,
                   139869673,
                   381452620,
                   417473534,
                   63981102,
                   419339042]
    # product_ids = [243878304]
    # Make requests in batches
    responses = main(product_ids)

    # Print the results
    for status_code,recoLength,productId, latency in responses:
        print(f"Status Code: {status_code}, Reco length: {recoLength}, Product Id: {productId}, Latency: {latency:.2f} seconds")