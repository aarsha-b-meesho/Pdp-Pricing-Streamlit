import streamlit as st
import requests
import time
from collections import defaultdict
from widgetHandler import get_cross_sell_recommendations
from taxonomyHandler import fetch_product_details
from feedHandler import  get_cross_sell_feed_with_metadata
from pdpFallback import pdpFallbackThread

# API endpoint
API_URL = "http://reco-engine-web.prd.meesho.int/api/v1/reco/cross-sell/widget"


st.set_page_config(
    page_title="Cross-Sell Recommendations",  # Optional: Set the title of the app
    page_icon="📊",             # Optional: Set an emoji or image as the icon
    layout="wide",              # Enables full-width layout
    initial_sidebar_state="expanded"  # Optional: Sidebar state
)
# Streamlit UI
st.title("Cross-Sell Recommendations")

fallback_response = st.sidebar.checkbox("Enable Fallback Response", value=False)
# Input form for user
with st.form("input_form"):
    st.write("Enter Product Details:")
    product_id = st.text_input("Product ID:", value="326765744")
    limit = st.text_input("Limit:", value="10")
    user_id = st.text_input("UserId:",value="6105390")
    submitted = st.form_submit_button("Submit")

if submitted:
    # Make the API call
    try:
        data = get_cross_sell_recommendations(int(product_id),user_id, int(limit))
        cross_sell_reco = []

        cross_sell_reco = get_cross_sell_feed_with_metadata(int(product_id))

        # SScat based grouping
        crossSellFeedSScat = defaultdict(list)
        if fallback_response==False:
            if cross_sell_reco is not Exception:
                for each_product in cross_sell_reco:
                    crossSellFeedSScat[each_product["old_sub_sub_category_id"]].append(each_product)
        if fallback_response:
            pdpFallbackRecos = pdpFallbackThread(data.get("recommendations",[]))
            for each_widget in data.get("recommendations", []):
                crossSellFeedSScat[each_widget["sscat_id"]] = pdpFallbackRecos[each_widget["product_id"]]

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
                .bordered-column{
                    margin: -10px,
                    padding: 0,
                    background-color: red
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        taxonomyData = fetch_product_details([product_id])
        if  taxonomyData and len(taxonomyData)>0:
            parentCol = st.columns(4)
            with parentCol[0]:
                # Parent Metadata Section
                st.markdown('<div class="center-content">', unsafe_allow_html=True)
                st.header("Product Details")

                # Display catalog name and ID
                st.markdown(
                    f'<p><span class="yellow-highlight">Catalog Name:</span> {taxonomyData[0].get("catalog_name", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight">Catalog ID:</span> {taxonomyData[0].get("catalog_id", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight">SSCat Name:</span> {taxonomyData[0].get("sscat_name", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight">SSCat ID:</span> {taxonomyData[0].get("old_sub_sub_category_id", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
            with parentCol[1]:
                # Display images in a horizontally scrollable gallery
                st.markdown('<div class="center-content">', unsafe_allow_html=True)
                st.markdown('<div style="display: flex; overflow-x: auto;">', unsafe_allow_html=True)
                for image_url in taxonomyData[0].get("product_images", [])[:1]:
                    st.markdown(
                        f'<img src="{image_url}" style="width: 300px; margin-right: 10px;">',
                        unsafe_allow_html=True,
                    )
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        if "parent_metadata" not in data.keys() or data.get("parent_metadata", {}) is None:
            st.markdown("NO CROSS SELL RECOMMENDATION FOR THIS PRODUCT ID")

        else:
            # Group recommendations by sscat_name
            isDuplicateWidgetFeedComing = False
            recommendations = data.get("recommendations", [])
            grouped_recommendations = defaultdict(list)
            sscat_name_2_id_mapping = defaultdict(str)
            for item in recommendations:
                sscat_name_2_id_mapping[item["sscat_name"]] = item["sscat_id"]
                grouped_recommendations[item["sscat_name"]].append(item)
                if len(grouped_recommendations[item["sscat_name"]])>1:
                    isDuplicateWidgetFeedComing = True

            # Display recommendations grouped by SSCat
            st.header("Widget Recommendations")
            if isDuplicateWidgetFeedComing:
                st.markdown("Duplicate Products Coming in Widget Feed")
            for sscat_name, products in grouped_recommendations.items():
                st.markdown(
                    f"""
                    <div class="recommendation-title">
                        <span class="yellow-highlight">
                            <span style="font-size: 25px; margin-right: 10px;">{sscat_name}</span>
                            <span class="yellow-highlight-light"  style="font-size: 18px;">( SSCAT Id:- {sscat_name_2_id_mapping[sscat_name]}) </span>
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                cols = st.columns(3)
                # On left column we will show product data , but on right side we will show feed data based on crossSellFeedSScat["
                for idx, product in enumerate(products[:1]):
                    with cols[0]:
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
                    cross_sell_data = crossSellFeedSScat[product["sscat_id"]]
                    feed_len1 = 2*(len(cross_sell_data)//4 )
                    if len(cross_sell_data)%4 ==1 or len(cross_sell_data)%4 ==2:
                        feed_len1+=len(cross_sell_data)%4
                    if len(cross_sell_data)%4 ==3:
                        feed_len1+=2
                    cross_sell_feed_screen1 = cross_sell_data[:feed_len1]
                    cross_sell_feed_screen2 = cross_sell_data[feed_len1:]
                    with cols[1]:
                        # st.markdown('<div class="bordered-column">', unsafe_allow_html=True)
                        # Display Cross-Sell Products in Rows of 2
                        for i in range(0, len(cross_sell_feed_screen1), 2):
                            row = st.columns(2)  # Create 2 columns for each row
                            for col, item in zip(row, cross_sell_feed_screen1[i:i + 2]):
                                with col:
                                    st.markdown(f"""
                                            <figure style="text-align: center;">
                                                <img src="{item["product_images"][0]}" style="height: 250px; margin-right: 10px;">
                                                <figcaption style="margin-top: 5px; font-size: 14px; color: gray;">{item['catalog_name']}</figcaption>
                                            </figure>
                                            """,unsafe_allow_html=True,
                                                )
                                    st.markdown(f"Product ID: {item['product_id']}")
                                    st.markdown(f"Catalog ID: {item['catalog_id']}")
                        # st.markdown('</div>', unsafe_allow_html=True)
                    with cols[2]:
                        # Display Cross-Sell Products in Rows of 2
                        for i in range(0, len(cross_sell_feed_screen2), 2):
                            row = st.columns(2)  # Create 2 columns for each row
                            for col, item in zip(row, cross_sell_feed_screen2[i:i + 2]):
                                with col:
                                    st.markdown(f"""
                                            <figure style="text-align: center;">
                                                <img src="{item["product_images"][0]}" style="height: 250px; margin-right: 10px;">
                                                <figcaption style="margin-top: 5px; font-size: 14px; color: gray;">{item['catalog_name']}</figcaption>
                                            </figure>
                                            """,unsafe_allow_html=True,
                                                )
                                    st.markdown(f"Product ID: {item['product_id']}")
                                    st.markdown(f"Catalog ID: {item['catalog_id']}")

            # Streamlit layout
            # time.sleep(2)
            st.header("Cross Sell Feed Recommendations")

            #     # Display products in rows of 2
            for i in range(0, len(cross_sell_reco), 5):
                cols = st.columns(5)  # Create two columns
                st.markdown('<div style="border: 1px solid #ccc; padding: 5px; margin-bottom: 10px;">', unsafe_allow_html=True)
                for col, product in zip(cols, cross_sell_reco[i:i + 5]):
                    with col:

                        st.markdown(f"""
                                <figure style="text-align: center;">
                                    <img src="{product['product_images'][0]}" style="height: 250px; margin-right: 10px;">
                                    <figcaption style="margin-top: 5px; font-size: 14px; color: gray;">{product['catalog_name']}</figcaption>
                                </figure>
                                """,unsafe_allow_html=True,
                                    )
                        st.markdown(
                            f'<p><span class="yellow-highlight-light">Product Id:</span> {product["product_id"]}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<p><span class="yellow-highlight-light">Catalog Id:</span> {product["catalog_id"]}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<p><span class="yellow-highlight-light">Sscat Id:</span> {product["old_sub_sub_category_id"]}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<p><span class="yellow-highlight-light">Sscat Name:</span> {product["sscat_name"]}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown('</div>', unsafe_allow_html=True)


    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch recommendations: {e}")
