import streamlit as st
import requests
import json
from collections import defaultdict
from widgetHandler import get_cross_sell_recommendations
from displayReco import display_recommendations
from processDsBatchWithDebugApis import  get_widget_and_feed_response
from taxonomyHandler import fetch_product_details
from feedHandler import get_cross_sell_feed_with_metadata_from_widget
st.set_page_config(
    page_title="Cross-Sell Recommendations",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and toggle
st.title("Cross-Sell Recommendations")
debug_mode = st.toggle("Debug DS_BATCH", value=False)

# Debug mode input flow
if debug_mode:

    with st.form("debug_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            parent_catalog_id = st.text_input("Parent Catalog-Id", value="95007398")
        with col2:
            key_version = st.selectbox("DS Key-Version", ["V1", "V2", "V3"],index=1)
        with col3:
            sscat_mapping = st.selectbox("Sscat-Mapping", ["v2"])

        col4, col5, col6 = st.columns(3)

        with col4:
            cvf_enabled = st.selectbox("CVF Enabled", ["Yes", "No"])
        with col5:
            oos_enabled = st.selectbox("OOS Enabled", ["Yes", "No"])

        with col6:
            landingPageLength = st.text_input("Landing Page Length",value="16")

        col7,col8,col9 = st.columns(3)
        with col7:
            minimumCatalogsInLandingPage = st.text_input("Minimum Products(Landing Page)", value = "10")

        with col8:
            userId = st.text_input("User-Id(Req. for CVF Filter)",value="390374537")

        # _,_,_,_,_,col7 = st.columns(6)
        with col9:
            # st.write("")  # Alignment
            # submitted_debug = st.form_submit_button("Submit")
            st.write("")  # Placeholder to align the button properly
            submitted = st.markdown(
                """<style>
                    div.stButton > button {
                        width: 200%;
                        height: 3em;
                        font-size: 1.2em;
                        font-weight: bold;
                    }
                </style>
                """,
                unsafe_allow_html=True
            )
            submitted_debug = st.form_submit_button("Submit")


        if submitted_debug:
            # Make the API call
            try:
                data,cross_sell_reco,debugResp = get_widget_and_feed_response(parent_catalog_id.strip(),key_version,sscat_mapping,cvf_enabled,oos_enabled,minimumCatalogsInLandingPage.strip(),userId.strip())
                if "recommendations" not in data.keys() and (not data["recommendations"]):
                    st.error(f"Failed to fetch recommendations or No recommendations for this ID -   RETRY")
                elif len(cross_sell_reco)==0:
                    st.error(f"Failed to fetch recommendations or No recommendations for this ID -   RETRY")
                else:
                    display_recommendations(data,cross_sell_reco,int(landingPageLength.strip()),isDebug=True,debugResp=debugResp)


            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch recommendations: {e}")

# Normal mode input flow
else:

    with st.form("input_form"):
        st.write("Enter Product Details:")

        col1, col2 = st.columns(2)
        with col1:
            catalogOrProduct = st.selectbox("Product/Catalog", ["Product-Id", "Catalog-Id"])
        with col2:
            product_id = st.text_input("ID", value="326765744")

        col3, col4 = st.columns(2)
        with col3:
            screen = st.selectbox("Select Screen:", ["place_order", "order_details"])
        with col4:
            limit = st.text_input("Limit:", value="6")

        col5, col6 = st.columns(2)
        with col5:
            user_id = st.text_input("UserId:", value="390374537")

        with col6:
            # st.write("")  # For alignment
            # submitted_normal = st.form_submit_button("Submit")
            st.write("")  # Placeholder to align the button properly
            submitted = st.markdown(
                """<style>
                    div.stButton > button {
                        width: 200%;
                        height: 3em;
                        font-size: 1.2em;
                        font-weight: bold;
                    }
                </style>
                """,
                unsafe_allow_html=True
            )
            submitted_normal = st.form_submit_button("Submit")

        if submitted_normal:
            # Make the API call
            try:
                data = get_cross_sell_recommendations(int(product_id),user_id, int(limit),screen,catalogOrProduct=="Product-Id")
                if "recommendations" not in data.keys() and (not data["recommendations"]):
                    st.error(f"Failed to fetch recommendations or No recommendations for this ID -   RETRY")
                cross_sell_reco = []
                cross_sell_reco = get_cross_sell_feed_with_metadata_from_widget(data,user_id)
                if len(cross_sell_reco)==0:
                    st.error(f"Failed to fetch recommendations or No recommendations for this ID -   RETRY")
                else:
                    display_recommendations(data,cross_sell_reco)


            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch recommendations: {e}")

