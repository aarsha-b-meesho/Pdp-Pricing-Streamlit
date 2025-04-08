from debugApis import *
from collections import defaultdict
import json
import uuid

def apply_oos_filter(catalog_ids: list[int], oos_response: dict) -> list[int]:
    """Filter catalog_ids using OOS response while maintaining order."""
    filtered_set = set(oos_response.get("data", {}).get("oosFilteredCatalogs", []))
    return [cid for cid in catalog_ids if cid in filtered_set]


def apply_cvf_filter(catalog_ids: list[int], cvf_response: dict) -> list[int]:
    """Filter catalog_ids using CVF response while maintaining order."""
    filtered_set = set(cvf_response.get("data", {}).get("cvfFilteredCatalogs", []))
    return [cid for cid in catalog_ids if cid in filtered_set]


def process_catalogs_with_filters(
        parent_catalog_id: str,
        key_version: str,
        sscat_mapping: str,
        cvf_enabled: str,
        oos_enabled: str,
) -> dict:
    ds_batch_response = get_ds_batch_data(int(parent_catalog_id), key_version)
    ds_batch_catalogs = ds_batch_response.get("data", {}).get("complementaryCatalogs", [])
    catalog_ids = ds_batch_catalogs

    cvf_response,oos_response = [],[]
    if cvf_enabled.lower() == "yes":
        cvf_response = get_cvf_filtered_catalogs(ds_batch_catalogs, user_id="6567887")
        catalog_ids = apply_cvf_filter(catalog_ids, cvf_response)
        cvf_response = list(set(cvf_response.get("data", {}).get("cvfFilteredCatalogs", [])))

    if oos_enabled.lower() == "yes":
        oos_response = get_oos_filtered_catalogs(ds_batch_catalogs)
        catalog_ids = apply_oos_filter(catalog_ids, oos_response)
        oos_response = list(set(oos_response.get("data", {}).get("oosFilteredCatalogs", [])))

    metadata_response = get_catalogs_metadata(catalog_ids+[parent_catalog_id])
    metadata_map = metadata_response.get("data", {}).get("metaDataResponse", {})

    parent_sscat_id = metadata_response.get("data", {}).get("metaDataResponse", {}).get(parent_catalog_id, {}).get("sscatId")

    sscat_mapping_response = get_sscat_mapping(parent_sscat_id, sscat_mapping)
    eligible_sscats = sscat_mapping_response.get("data", {}).get("eligiblesscats", [])

    # Step: Group catalogs by SSCAT ID
    grouped_by_sscat = defaultdict(list)
    for cid in catalog_ids:
        meta = metadata_map.get(str(cid))
        if meta:
            grouped_by_sscat[meta["sscatId"]].append({
                "catalogId": cid,
                "productId": meta["productId"],
                "sscatId": meta["sscatId"],
                "sscatName": meta["sscatName"],
                "image": meta["image"]
            })

    # Step: Sort groups in the order of eligible SSCAT mapping
    ordered_grouped_catalogs = []
    for sscat in eligible_sscats:
        sid = sscat.get("id")
        if sid in grouped_by_sscat:
            ordered_grouped_catalogs.append({
                "sscatId": sid,
                "sscatName": sscat.get("name"),
                "catalogs": grouped_by_sscat[sid]
            })

    return {
        "filtered_catalog_ids": catalog_ids,
        "ds_pushed_catalogs":ds_batch_catalogs,
        "metadata": metadata_map,
        "sscat_mapping": eligible_sscats,
        "grouped_catalogs": ordered_grouped_catalogs,
        "cvf_filter_catalogs":list(set(ds_batch_catalogs) - set(cvf_response)) if cvf_enabled.lower() == "yes" else [],
        "oos_filtered_catalogs":list(set(ds_batch_catalogs) - set(oos_response)) if oos_enabled.lower() == "yes" else [],
    }

def format_grouped_widget_response(ordered_grouped_catalogs: list, parent_metadata: dict, minProductForLandingPage: int) -> dict:
    recommendations = []

    for group in ordered_grouped_catalogs:
        if not group["catalogs"] or len(group["catalogs"])<minProductForLandingPage:
            continue

        catalog = group["catalogs"][0]  # Pick only the first one
        recommendations.append({
            "product_id": catalog["productId"],
            "catalog_id": catalog["catalogId"],
            "sscat_id": catalog["sscatId"],
            "sscat_name": catalog["sscatName"],
            "widget_metadata": {
                "image": catalog["image"],
                "price": None,
                "rating": None,
                "title": catalog["sscatName"]
            }
        })

    parent_meta_obj = {
        "product_id": parent_metadata.get("productId"),
        "catalog_id": int(parent_metadata.get("catalogId", 0)),
        "sscat_id": parent_metadata.get("sscatId"),
        "sscat_name": parent_metadata.get("sscatName", None),
        "image": parent_metadata.get("image")
    }

    return {
        "recommendations": recommendations,
        "parent_metadata": parent_meta_obj,
        "feed_source": "DS_BATCH",
        "tracking": {
            "tracking_id": str(uuid.uuid4())
        }
    }


def convert_to_flattened_feed_response(ordered_grouped_catalogs: list) -> list:
    flattened_response = []

    for group in ordered_grouped_catalogs:
        sscat_id = group.get("sscatId")
        sscat_name = group.get("sscatName")
        catalogs = group.get("catalogs", [])

        for catalog in catalogs:
            flattened_response.append({
                "catalog_id": catalog["catalogId"],
                "catalog_name": catalog.get("catalogName", "Others"),
                "old_sub_sub_category_id": sscat_id,
                "sscat_name": sscat_name,
                "product_images": [catalog.get("image")] if catalog.get("image") else [],
                "product_id": catalog.get("productId")
            })

    return flattened_response


def get_widget_and_feed_response(parent_catalog_id,key_version,sscat_mapping,cvf_enabled,oos_enabled,minProductForLandingPage):
    debugResponse = process_catalogs_with_filters(parent_catalog_id,key_version,sscat_mapping,cvf_enabled,oos_enabled)
    widgetResponse = format_grouped_widget_response(debugResponse["grouped_catalogs"],debugResponse["metadata"][parent_catalog_id],int(minProductForLandingPage))
    feedResponse = convert_to_flattened_feed_response(debugResponse["grouped_catalogs"])
    return (widgetResponse,feedResponse,debugResponse)

if __name__ == "__main__":
    result = process_catalogs_with_filters(
        parent_catalog_id="95007398",
        key_version="V3",
        sscat_mapping="v2",
        cvf_enabled="Yes",
        oos_enabled="Yes"
    )