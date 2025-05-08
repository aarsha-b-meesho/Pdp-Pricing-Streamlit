# PDP Pricing Streamlit App

A Streamlit application for displaying Product Detail Page (PDP) recommendations with pricing information.

## Features

- Display product recommendations in a clean, modern interface
- Show product details including images, prices, and discounts
- Real-time pricing updates
- Responsive grid layout
- User-friendly form for input parameters

## Setup

1. Clone the repository:
```bash
git clone https://github.com/aarsha-b-meesho/Pdp-Pricing-Streamlit.git
cd Pdp-Pricing-Streamlit
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter the required details in the form:
   - Catalog ID
   - Client ID (ios/android)
   - User ID
   - User Pincode
   - App Version Code

2. Click Submit to view the recommendations

## Dependencies

- Streamlit
- Pandas
- Requests
- Protobuf
- Other dependencies listed in requirements.txt

## License

This project is proprietary and confidential. 