import requests
import json

def call_cross_sell_debug_api(payload: dict) -> dict:
    url = "http://cross-sell-web.prd.meesho.int/api/v1/reco/cross-sell/debug"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


# OOS Filter
def get_oos_filtered_catalogs(catalog_ids: list[int]) -> dict:
    payload = {
        "context": "OOS",
        "keys": [str(cid) for cid in catalog_ids],
        "version": "",
        "userId": ""
    }
    return call_cross_sell_debug_api(payload)

# CVF Filter
def get_cvf_filtered_catalogs(catalog_ids: list[int], user_id: str) -> dict:
    payload = {
        "context": "CVF",
        "keys": [str(cid) for cid in catalog_ids],
        "version": "",
        "userId": user_id
    }
    return call_cross_sell_debug_api(payload)

# DS_BATCH Debug Data
def get_ds_batch_data(catalog_id: int, version: str) -> dict:
    payload = {
        "context": "DS_BATCH",
        "keys": [str(catalog_id)],
        "version": version,
        "userId": ""
    }
    return call_cross_sell_debug_api(payload)

# Metadata for Catalogs
def get_catalogs_metadata(catalog_ids: list[int]) -> dict:
    payload = {
        "context": "METADATA",
        "keys": [str(cid) for cid in catalog_ids],
        "version": "",
        "userId": ""
    }
    return call_cross_sell_debug_api(payload)

# SSCAT Mapping for a given SSCAT ID
def get_sscat_mapping(sscat_id: int, version: str) -> dict:
    payload = {
        "context": "ELIGIBLE_SSCATS",
        "keys": [str(sscat_id)],
        "version": version,
        "userId": ""
    }
    return call_cross_sell_debug_api(payload)


def main():
    print("🔍 Testing OOS Filter...")
    oos_response = get_oos_filtered_catalogs([130021294, 140505736, 134214292])
    print("OOS Response:\n", oos_response, "\n")

    print("🔍 Testing CVF Filter...")
    cvf_response = get_cvf_filtered_catalogs([130021294, 140505736, 134214292], user_id="6567887")
    print("CVF Response:\n", cvf_response, "\n")

    print("🔍 Testing DS_BATCH Data...")
    ds_batch_response = get_ds_batch_data(95007398, "V3")
    print("DS_BATCH Response:\n", ds_batch_response, "\n")

    print("🔍 Testing Catalogs Metadata...")
    metadata_response = get_catalogs_metadata([130021294, 140505736, 134214292])
    print("Metadata Response:\n", metadata_response, "\n")

    print("🔍 Testing SSCAT Mapping...")
    sscat_response = get_sscat_mapping(1001, "v2")
    print("SSCAT Mapping Response:\n", sscat_response, "\n")


if __name__ == "__main__":
    main()

