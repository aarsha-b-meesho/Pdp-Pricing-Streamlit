import streamlit as st
from collections import defaultdict
from taxonomyHandler import fetch_product_details

def display_recommendations(data,cross_sell_reco,limit = 16,isDebug=False,debugResp={}):
    feedSource = data["feed_source"]

    # SScat based grouping
    crossSellFeedSScat = defaultdict(list)
    if cross_sell_reco is not Exception:
        for each_product in cross_sell_reco:
            crossSellFeedSScat[each_product["old_sub_sub_category_id"]].append(each_product)
    for each_sscat in crossSellFeedSScat:
        if len(crossSellFeedSScat[each_sscat])>limit:
            crossSellFeedSScat[each_sscat] = crossSellFeedSScat[each_sscat][:limit]

    # Display parent metadata
    st.markdown(
        """
        <style>
            .yellow-highlight {
                color: #2337C6;
                font-weight: bold;
            }
            .yellow-highlight-light {
                color: #4CC9F0;
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

    if data.get('parent_metadata',0)!=0 and data.get('parent_metadata').get("product_id",0)!=0:
        taxonomyData = fetch_product_details([data.get('parent_metadata').get("product_id")])
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
        with parentCol[3]:
            # Parent Metadata Section
            st.markdown('<div class="center-content">', unsafe_allow_html=True)
            st.header("Feed Source")

            # Display catalog name and ID
            st.markdown(
                f'<p><span class="yellow-highlight" style="font-size: 25px;">{feedSource}<span></p>',
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
        colForHorizontalWidget = st.columns(6)
        for i in range(min(6,len(data.get("recommendations",[])))):
            with colForHorizontalWidget[i]:
                st.markdown(f"""
                                        <figure style="text-align: center;">
                                            <img src="{data.get("recommendations")[i]["widget_metadata"]["image"]}" style="height: 250px; margin-right: 10px;">
                                            <figcaption style="margin-top: 5px; font-size: 14px; color: gray;">{data.get("recommendations")[i]["sscat_name"]}</figcaption>
                                        </figure>
                                        """,unsafe_allow_html=True,
                            )
                st.markdown(
                    f'<p><span class="yellow-highlight-light">Product Id:</span> {data.get("recommendations")[i]["product_id"]}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight-light">Catalog Id:</span> {data.get("recommendations")[i]["catalog_id"]}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p><span class="yellow-highlight-light">Sscat Id:</span> {data.get("recommendations")[i]["sscat_id"]}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

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

        if isDebug==True and len(debugResp.keys())>1:
            st.markdown("Ds-Pushed Catalogs")
            st.write(debugResp["ds_pushed_catalogs"])
            st.markdown("CVF Filtered")
            st.write(debugResp["cvf_filter_catalogs"])
            st.markdown("OOS Filtered")
            st.write(debugResp["oos_filtered_catalogs"])
            st.markdown("SSCAT Mappig")
            st.write(debugResp["sscat_mapping"])
            st.markdown("Catalogs After Filtering")
            st.write(debugResp["filtered_catalog_ids"])
        else:
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

