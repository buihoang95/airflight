import os

import streamlit as st
import requests

# FastAPI backend URL
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5050")  # Adjust if running on a different host/port
FLIGHT_URL = BACKEND_URL + "/flights"

st.set_page_config(
    page_title="Flights by Country",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Flights by Country")

st.write("""
Enter a **3-character airport code** (e.g., `LAX` for Los Angeles International Airport, `SIN` for Singapore Changi Airport) to see a table of countries from which flights are arriving and the number of flights from each country.
""")

# Input form
with st.form(key='airport_form'):
    airport_code = st.text_input("Airport Code", max_chars=3, help="Enter a valid 3-letter airport code (e.g., LAX, SIN)")
    submit_button = st.form_submit_button(label='Search')

if submit_button:
    airport_code = airport_code.strip().upper()

    if len(airport_code) != 3 or not airport_code.isalpha():
        st.error("Please enter a valid **3-character alphabetic** airport code.")
    else:
        with st.spinner('Fetching flight data...'):
            try:
                response = requests.get(FLIGHT_URL, params={'airport': airport_code}, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    flights = data.get('data', [])

                    if not flights:
                        st.warning(f"No flight data available for airport code `{airport_code}`.")
                    else:
                        # Prepare data for display
                        countries = [flight['country'] for flight in flights]
                        flight_counts = [flight['flight_count'] for flight in flights]

                        flight_data = {
                            'Country': countries,
                            '# of Flights': flight_counts
                        }

                        st.success(f"Flights arriving at **{airport_code}**")
                        st.table(flight_data)
                else:
                    error_detail = response.json().get('detail', 'An error occurred.')
                    st.error(f"Error {response.status_code}: {error_detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while fetching data: {e}")
