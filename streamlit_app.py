import streamlit as st
import requests
from collections import defaultdict
from handler import get_cross_sell_recommendations
from taxonomyHandler import fetch_product_details

# API endpoint
API_URL = "http://reco-engine-web.prd.meesho.int/api/v1/reco/cross-sell/widget"

# Streamlit UI
st.title("Cross-Sell Recommendations")

# Input form for user
with st.form("input_form"):
    st.write("Enter Product Details:")
    product_id = st.text_input("Product ID:", value="32074483")
    limit = st.text_input("Limit:", value="10")
    user_id = st.text_input("UserId:",value="6105390")
    # user_id = "6105390"  # Predefined user ID for this example
    submitted = st.form_submit_button("Submit")

if submitted:
    # Make the API call
    try:
        data = get_cross_sell_recommendations(int(product_id),user_id, int(limit))
        # Display parent metadata
        st.markdown(
            """
            <style>
                .yellow-highlight {
                    color: yellow;
                    font-weight: bold;
                }
                .yellow-highlight-light {
                    color: #FFFFD3;
                    font-weight: bold;
                }v
                .center-content {
                    text-align: center;
                }
                .center-content img {
                    margin: auto;
                    display: block;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        taxonomyData = fetch_product_details(product_id)
        if "parent_metadata" not in data.keys() or data.get("parent_metadata", {}) is None:
            if  taxonomyData:
                # Parent Metadata Section
                st.markdown('<div class="center-content">', unsafe_allow_html=True)
                st.header("Product Details")

                # Display catalog name and ID
                st.markdown(
                    f'<p><span class="yellow-highlight">Catalog Name:</span> {taxonomyData.get("catalog_name", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight">Catalog ID:</span> {taxonomyData.get("catalog_id", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight">SSCat Name:</span> {taxonomyData.get("sscat_name", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight">SSCat ID:</span> {taxonomyData.get("old_sub_sub_category_id", "N/A")}</p>',
                    unsafe_allow_html=True,
                )

                # Display images in a horizontally scrollable gallery
                st.markdown('<div style="display: flex; overflow-x: auto;">', unsafe_allow_html=True)
                for image_url in taxonomyData.get("product_images", [])[:1]:
                    st.markdown(
                        f'<img src="{image_url}" style="width: 300px; margin-right: 10px;">',
                        unsafe_allow_html=True,
                    )
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("NO CROSS SELL RECOMMENDATION FOR THIS PRODUCT ID")

        else:
            # Parent Metadata
            st.markdown('<div class="center-content">', unsafe_allow_html=True)
            st.header("Parent Metadata")
            parent_metadata = data.get("parent_metadata", {})
            st.markdown(
                f'<img src="{parent_metadata.get("image", "")}" style="height: 600px; margin-right: 10px;">',
                unsafe_allow_html=True,
            )
            # st.image(parent_metadata.get("image", ""), height=600)
            st.markdown(
                f'<p><span class="yellow-highlight">Product ID:</span> {parent_metadata.get("product_id", "N/A")}</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p><span class="yellow-highlight">Catalog ID:</span> {parent_metadata.get("catalog_id", "N/A")}</p>',
                unsafe_allow_html=True,
            )
            if taxonomyData:
                st.markdown(
                    f'<p><span class="yellow-highlight">SSCat Name:</span> {taxonomyData.get("sscat_name", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<p><span class="yellow-highlight">SSCat ID:</span> {parent_metadata.get("sscat_id", "N/A")}</p>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Group recommendations by sscat_name
            recommendations = data.get("recommendations", [])
            grouped_recommendations = defaultdict(list)
            for item in recommendations:
                grouped_recommendations[item["sscat_name"]].append(item)

            # Display recommendations grouped by SSCat
            st.header("Recommendations")
            for sscat_name, products in grouped_recommendations.items():
                st.markdown(f'<div class="recommendation-title"><span class="yellow-highlight">{sscat_name}</span></div>', unsafe_allow_html=True)
                cols = st.columns(len(products))
                for idx, product in enumerate(products):
                    with cols[idx]:
                        st.markdown('<div class="product-container">', unsafe_allow_html=True)
                        st.image(product["widget_metadata"]["image"], width=250)
                        st.markdown(
                            f'<p><span class="yellow-highlight-light">Title:</span> {product["widget_metadata"]["title"]}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<p><span class="yellow-highlight-light">Product ID:</span> {product["product_id"]}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<p><span class="yellow-highlight-light">Catalog ID:</span> {product["catalog_id"]}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown("</div>", unsafe_allow_html=True)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch recommendations: {e}")
