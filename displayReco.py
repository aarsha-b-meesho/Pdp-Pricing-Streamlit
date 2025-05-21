import streamlit as st
from collections import defaultdict

def display_recommendations(parent_pid,parent_pricing_data,parent_taxonomy_data,data, catalog_id, user_id, client_id="ios", user_pincode="110001", app_version_code="1.0.0", limit=16):
    """
    Display product recommendations in Streamlit interface.
    
    Parameters:
    - data: The processed data containing recommendations and parent metadata
    - catalog_id: The catalog ID of the parent product
    - user_id: The user ID for the request
    - client_id: The client ID (ios or android)
    - user_pincode: The user's pincode
    - app_version_code: The app version code
    - limit: Maximum number of recommendations to display
    """

    # Apply dark mode styling
    st.markdown(
        """
        <style>
            /* Global Styles */
            .stApp {
                background-color: rgb(250, 250, 250);  /* Light background */
            }
            
            /* Typography */
            h1, h2, h3 {
                color: #333333;  /* Dark gray text */
                font-family: 'Inter', sans-serif;
                margin-bottom: 1rem;
            }
            
            /* Card Styles */
            .product-card {
                background: #ffffff;  /* White cards */
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s ease;
                border: 1px solid #e0e0e0;  /* Light gray border */
            }
            
            .product-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                border-color: #007bff;  /* Blue accent on hover */
            }
            
            /* Text Styles */
            .label {
                color: #007bff;  /* Blue accent for labels */
                font-size: 0.9rem;
                font-weight: 500;
                margin-bottom: 0.25rem;
            }
            
            .value {
                color: #333333;  /* Dark gray for values */
                font-size: 1rem;
                font-weight: 600;
            }
            
            .price {
                color: #28a745;  /* Green for prices */
                font-weight: 700;
                font-size: 1.1rem;
            }
            
            .discount {
                color: #dc3545;  /* Red for discounts */
                font-weight: 700;
                font-size: 1.1rem;
            }
            
            /* Layout */
            .center-content {
                text-align: center;
                padding: 1rem;
            }
            
            .center-content img {
                border-radius: 8px;
                margin: 1rem auto;
                display: block;
                max-width: 100%;
                height: auto;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            /* Section Headers */
            .section-header {
                color: #333333;  /* Dark gray text */
                font-size: 1.5rem;
                font-weight: 700;
                margin: 2rem 0 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #007bff;  /* Blue accent border */
            }
            
            /* Grid Layout */
            .grid-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1.5rem;
                padding: 1rem 0;
            }

            /* Streamlit specific overrides */
            .stMarkdown {
                color: #333333;  /* Dark gray text */
            }
            
            .stAlert {
                background-color: #ffffff !important;
                color: #333333 !important;
                border: 1px solid #007bff !important;
            }
            
            .stWarning {
                background-color: #fff3cd !important;
                color: #856404 !important;
                border: 1px solid #ffeeba !important;
            }
            
            .stError {
                background-color: #f8d7da !important;
                color: #721c24 !important;
                border: 1px solid #f5c6cb !important;
            }

            /* Form Elements */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            div[data-baseweb="select"] > div,
            div[data-baseweb="select"] div,
            .stTextInput > div > div > input:focus,
            .stSelectbox > div > div > select:focus,
            div[data-baseweb="select"] > div:focus,
            div[data-baseweb="select"] div:focus {
                background-color: #ffffff !important;
                border: 1px solid #ced4da !important;
                color: #333333 !important;
                caret-color: #333333 !important;
            }

            /* Dropdown menu items */
            div[data-baseweb="popover"] * {
                background-color: #ffffff !important;
                color: #333333 !important;
            }

            div[data-baseweb="select"] * {
                background-color: #ffffff !important;
                color: #333333 !important;
            }

            /* Button Styles */
            .stButton > button,
            .stButton > button:focus,
            .stButton > button:active,
            .stButton > button:hover,
            .stButton > button:disabled {
                background: linear-gradient(145deg, #007bff, #0056b3) !important;
                color: white !important;
                border: none !important;
                font-weight: 600 !important;
                padding: 0.5rem 1.5rem !important;
                border-radius: 8px !important;
                transition: all 0.3s ease !important;
            }

            .stButton > button:hover {
                background: linear-gradient(145deg, #0056b3, #007bff) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3) !important;
            }

            /* Override any dark mode styles */
            .stApp [data-testid="stForm"] {
                border-color: #ced4da !important;
                background-color: #ffffff !important;
            }

            /* Style for the form container */
            .stApp [data-testid="stForm"] > div:first-child {
                background-color: #ffffff !important;
                border: 1px solid #ced4da !important;
                border-radius: 8px !important;
                padding: 1rem !important;
            }

            /* Style for select dropdown */
            div[role="listbox"] {
                background-color: #ffffff !important;
            }

            div[role="option"] {
                background-color: #ffffff !important;
                color: #333333 !important;
            }

            div[role="option"]:hover {
                background-color: #f8f9fa !important;
            }

            /* Fix for text input cursor */
            .stTextInput > div > div > input::selection {
                background-color: #007bff !important;
                color: #ffffff !important;
            }

            /* Ensure form elements stay white after submission */
            .stForm > div {
                background-color: #ffffff !important;
            }

            /* Fix for select box after submission */
            div[data-baseweb="select"] > div[aria-expanded="true"] {
                background-color: #ffffff !important;
                color: #333333 !important;
            }

            /* Fix for text input after submission */
            .stTextInput > div > div > input[type="text"] {
                background-color: #ffffff !important;
                color: #333333 !important;
                caret-color: #333333 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display parent product details if available
    parent_metadata = data.get("parent_metadata", {})
    if parent_metadata:
        st.markdown('<h1 class="section-header">Parent Product Details</h1>', unsafe_allow_html=True)

        parent_cols = st.columns([1, 1, 1])
        with parent_cols[0]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.markdown('<h3>Product Information</h3>', unsafe_allow_html=True)

            # Display catalog information with improved styling
            st.markdown(
                f'<p class="label">Catalog ID</p><p class="value">{catalog_id}</p>',
                unsafe_allow_html=True,
            )

            # Display parent pricing information
            if parent_pid:
                st.markdown(
                    f'<p class="label">Parent Hero-Pid</p><p class="price">{parent_pid}</p>',
                    unsafe_allow_html=True,
                )
            if parent_pricing_data:
                # Display all pricing features
                for key, value in parent_pricing_data.items():
                    if value is not None:  # Only display non-None values
                        if key in ["serving_price", "strike_off_price", "special_offers_discounted_price"]:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="price">₹{value}</p>',
                                unsafe_allow_html=True,
                            )
                        elif key in ["applied_offers_discount", "applied_offers_discount_percent", "supplier_discount", 
                                   "brp_discount", "zonal_discount", "cod_discount", "rto_discount"]:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="discount">₹{value}</p>',
                                unsafe_allow_html=True,
                            )
                        elif key in ["zonal_charge", "rto_charge", "delivery_fee_visible", "shipping_price"]:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="value">₹{value}</p>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="value">{value}</p>',
                                unsafe_allow_html=True,
                            )

            st.markdown("</div>", unsafe_allow_html=True)

        with parent_cols[1]:
            if parent_taxonomy_data.get("product_images"):
                st.markdown('<div class="product-card center-content">', unsafe_allow_html=True)
                st.image(
                    parent_taxonomy_data.get("product_images")[0],
                    width=300,
                    caption=parent_taxonomy_data.get("catalog_name", "")
                )
                st.markdown("</div>", unsafe_allow_html=True)

        with parent_cols[2]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.markdown('<h3>User Information</h3>', unsafe_allow_html=True)

            st.markdown(
                f'<p class="label">User ID</p><p class="value">{user_id}</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p class="label">Client ID</p><p class="value">{client_id}</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p class="label">User Pincode</p><p class="value">{user_pincode}</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p class="label">App Version</p><p class="value">{app_version_code}</p>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("No parent metadata available for this product ID")
        return

    # Process and display recommendations
    recommendations = data.get("recommendations", {})
    if not recommendations:
        st.warning("No recommendations available for this product")
        return

    st.markdown('<h1 class="section-header">Product Recommendations</h1>', unsafe_allow_html=True)

    # Process recommendations
    processed_recommendations = []
    for product_id, details in recommendations.items():
        pdp_features = details.get("pdp_features", {})
        pricing_features = details.get("pricing_features", {})
        taxonomy_features = details.get("taxonomy_features", {})

        processed_item = {
            "product_id": product_id,
            "catalog_id": pdp_features.get("catalog_id", "N/A"),
            "sscat_id": taxonomy_features.get("sscat_id", "N/A"),
            "sscat_name": taxonomy_features.get("sscat_name", "Other"),
            "widget_metadata": {
                "image": taxonomy_features.get("images", ["https://via.placeholder.com/250"])[0] if taxonomy_features.get("images") else "https://via.placeholder.com/250",
                "title": taxonomy_features.get("catalog_name", "Product"),
                "price": pricing_features.get("serving_price", "N/A")
            },
            "pricing_features": pricing_features  # Store all pricing features
        }
        processed_recommendations.append(processed_item)

    # Display recommendations in a 4x5 grid
    for i in range(0, len(processed_recommendations), 4):
        row_items = processed_recommendations[i:i+4]
        cols = st.columns(4)

        for idx, product in enumerate(row_items):
            with cols[idx]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)

                # Product Image
                widget_metadata = product.get("widget_metadata", {})
                if image_url := widget_metadata.get("image"):
                    st.image(image_url, width=200)

                # Product Details
                st.markdown(
                    f'<p class="label">Title</p><p class="value">{widget_metadata.get("title", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p class="label">Product ID</p><p class="value">{product.get("product_id", "N/A")}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p class="label">Catalog ID</p><p class="value">{product.get("catalog_id", "N/A")}</p>',
                    unsafe_allow_html=True,
                )

                # Display all pricing features
                pricing_features = product.get("pricing_features", {})
                for key, value in pricing_features.items():
                    if value is not None:  # Only display non-None values
                        if key in ["serving_price", "strike_off_price", "special_offers_discounted_price"]:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="price">₹{value}</p>',
                                unsafe_allow_html=True,
                            )
                        elif key in ["applied_offers_discount", "applied_offers_discount_percent", "supplier_discount", 
                                   "brp_discount", "zonal_discount", "cod_discount", "rto_discount"]:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="discount">₹{value}</p>',
                                unsafe_allow_html=True,
                            )
                        elif key in ["zonal_charge", "rto_charge", "delivery_fee_visible", "shipping_price"]:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="value">₹{value}</p>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<p class="label">{key.replace("_", " ").title()}</p><p class="value">{value}</p>',
                                unsafe_allow_html=True,
                            )

                st.markdown("</div>", unsafe_allow_html=True)

