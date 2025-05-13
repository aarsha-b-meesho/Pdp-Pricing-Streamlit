import streamlit as st
import requests
import json
from collections import defaultdict
from displayReco import display_recommendations
from taxonomyHandler import fetch_product_details
from pricing_service import get_pricing_features
from dataprocessing import process_data
from heroPid import get_heroPid
from reco import get_recommendations

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

            # Convert inputs to appropriate types
            try:
                catalog_id_int = int(catalog_id)
                user_id_int = int(user_id)
            except ValueError:
                st.error("Catalog ID and User ID must be valid numbers.")
                st.stop()

            # Make the API call and validate responses
            pdp_data = get_recommendations(catalog_id_int, user_id_int, client_id, 20)
            if not pdp_data:
                st.error("No Recommendation data found for the given Catalog ID.")
                st.stop()

            parent_pid = get_heroPid(catalog_id_int)
            if not parent_pid:
                st.error("Could not retrieve parent product ID.")
                st.stop()

            # Add parent PID to the beginning of the list
            pdp_data.insert(0, parent_pid)

            # Get pricing data
            pricing_data = get_pricing_features(user_id_int, pdp_data, client_id, user_pincode, app_version_code)
            if not pricing_data:
                st.error("Pricing data could not be retrieved.")
                st.stop()

            # Extract parent pricing data
            parent_pricing_data = pricing_data.get(str(parent_pid), {})
            pricing_data.pop(str(parent_pid), None)

            # Get taxonomy data
            taxonomy_data = fetch_product_details(pdp_data)
            if not taxonomy_data:
                st.error("Taxonomy data could not be retrieved.")
                st.stop()

            # Extract parent taxonomy data
            parent_taxonomy_data = next((item for item in taxonomy_data if item.get("product_id") == parent_pid), {})
            taxonomy_data = [item for item in taxonomy_data if item.get("product_id") != parent_pid]

            # Process all data sources and combine features
            pdp_data.pop(0)  # Remove parent PID from the list
            data = process_data(pdp_data, pricing_data, taxonomy_data)
            if not data:
                st.error("Processed data is empty or invalid.")
                st.stop()

            # Display recommendations
            display_recommendations(
                parent_pid,
                parent_pricing_data,
                parent_taxonomy_data,
                data,
                catalog_id_int,
                user_id_int,
                client_id,
                user_pincode,
                app_version_code
            )

        except ValueError as ve:
            st.error(f"Validation error: {str(ve)}")
        except requests.exceptions.RequestException as re:
            st.error(f"Network error: {str(re)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.error("Please check the input values and try again.")
