import streamlit as st
import requests
import json
from collections import defaultdict
from displayReco import display_recommendations
from pdpIop import get_catalog_ids
from taxonomyHandler import fetch_product_details
from pricing_service import get_pricing_features
from dataprocessing import process_data

st.set_page_config(
    page_title="PDP Recommendations",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("PDP Recommendations")

with st.form("input_form"):
    st.write("Enter Details:")

    # Create three columns for inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        catalog_id = st.text_input("Catalog ID", value="126277899")
        client_id = st.selectbox("Client ID", options=["ios", "android"], index=0)
    with col2:
        user_id = st.text_input("User ID", value="326765744")
        user_pincode = st.text_input("User Pincode", value="122001")
    with col3:
        app_version_code = st.text_input("App Version Code", value="685")

    submitted = st.form_submit_button("Submit", use_container_width=True)

    if submitted:
        try:
            # Validate required inputs
            if not catalog_id.strip() or not user_id.strip():
                st.warning("Catalog ID and User ID are required.")
                st.stop()

            # Make the API call and validate responses
            pdp_data = get_catalog_ids(int(catalog_id))
            if not pdp_data:
                raise ValueError("No Recommendation data found for the given Catalog ID.")

            pricing_data = get_pricing_features(user_id, pdp_data, client_id, user_pincode, app_version_code)
            if not pricing_data:
                raise ValueError("Pricing data could not be retrieved.")

            taxonmy_data = fetch_product_details(pdp_data)
            if not taxonmy_data:
                raise ValueError("Taxonomy data could not be retrieved.")

            # Process all data sources and combine features
            data = process_data(pdp_data, pricing_data, taxonmy_data)
            if not data:
                raise ValueError("Processed data is empty or invalid.")

            display_recommendations(data, catalog_id, user_id, client_id, user_pincode, app_version_code)

        except ValueError as ve:
            st.error(f"Validation error: {ve}")
        except requests.exceptions.RequestException as re:
            st.error(f"Network error: {re}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
