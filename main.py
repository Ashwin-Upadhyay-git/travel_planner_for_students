import streamlit as st
import pydeck as pdk
import google.generativeai as genai
from datetime import date

#  Streamlit Page Configuration

st.set_page_config(page_title="Student Travel Planner", page_icon="🧳", layout="wide")


#  Sidebar: Profile & Settings

st.sidebar.header("👤 Profile Settings")

user_name = st.sidebar.text_input("Name", placeholder="Enter your name")
user_transport = st.sidebar.text_input("Preferred Mode of Transport", placeholder="e.g. Train, Bus")
user_age = st.sidebar.number_input("Age", min_value=16, max_value=60, step=1)
travel_pref = st.sidebar.selectbox(
    "Preferred Travel Type",
    ["Adventure", "Relaxation", "Cultural", "Nature", "Foodie", "Mixed"]
)



st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ App Settings")

api_key = "AIzaSyCdZO9dzJ9LELr-Hr-IBCK8RCB5abfbYVY"

if st.sidebar.button("💾 Save Settings"):
    st.sidebar.success(f"Settings saved for {user_name or 'User'}!")




# Main App

st.title("🧭 Student Travel Planner")
st.write("Plan your next adventure with AI — enter your preferences and get a smart travel itinerary!")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter your Gemini API key from the sidebar to use the AI itinerary generator.")

#  User Inputs

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📍 Destination**")
    destination_option = st.selectbox(
    "Choose from popular destinations or type your own below:",
    [
        "-- Type your own --",
        # 🌆 Tier 1 Cities
        "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad",

        # 🌇 Tier 2 Cities
        "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Patna",
        "Vadodara", "Ludhiana", "Agra", "Nashik", "Coimbatore", "Visakhapatnam", "Madurai",
        "Varanasi", "Meerut", "Rajkot", "Jabalpur", "Amritsar", "Ranchi", "Guwahati",
        "Chandigarh", "Mysore", "Trivandrum", "Bhubaneswar", "Jamshedpur", "Dehradun",
        "Mangalore", "Tiruchirappalli", "Vijayawada", "Gwalior", "Ujjain", "Kolhapur",
        "Salem", "Warangal", "Nellore", "Aligarh", "Ajmer", "Bareilly", "Moradabad",
        "Raipur", "Dhanbad", "Hubli", "Bellary", "Tirunelveli", "Guntur", "Siliguri",
        "Bilaspur", "Jodhpur", "Noida", "Ghaziabad", "Faridabad", "Gurgaon",

        # 🏞️ Tourist / Special Destinations
        "Goa", "Pondicherry", "Andaman", "Manali", "Shimla", "Darjeeling", "Ooty",
        "Munnar", "Udaipur", "Kaziranga", "Rishikesh", "Coorg", "Ranthambore",
    ],
    label_visibility="collapsed"
)

    
    if destination_option == "":
        destination = st.text_input("Enter destination:", placeholder="e.g., Goa, Paris, Tokyo", label_visibility="collapsed")
    else:
        destination = destination_option

with col2:
    st.markdown("**💰 Budget (INR)**")
    budget_option = st.selectbox(
        "Choose a budget range or enter your own below:",
        ["-- Type your own --", "₹5,000 – ₹10,000", "₹11,000 – ₹15,000", 
         "₹16,000 – ₹20,000", "₹21,000 – ₹25,000", "₹25,000+"],
        label_visibility="collapsed"
    )
    
    if budget_option == "-- Type your own --":
        budget = st.text_input("Enter budget:", placeholder="e.g., ₹15,000 or $500", label_visibility="collapsed")
    else:
        budget = budget_option

with col3:
    travel_dates = st.date_input("🗓️ Travel Dates", [date.today(), date.today()])


# Map Section (PyDeck no mapbox or folium) 

demo_locations = {
    # Tier 1 Cities
    "mumbai": [19.0760, 72.8777],
    "delhi": [28.6139, 77.2090],
    "bangalore": [12.9716, 77.5946],
    "chennai": [13.0827, 80.2707],
    "kolkata": [22.5726, 88.3639],
    "hyderabad": [17.3850, 78.4867],
    "pune": [18.5204, 73.8567],
    "ahmedabad": [23.0225, 72.5714],

    # Tier 2 Cities
    "surat": [21.1702, 72.8311],
    "jaipur": [26.9124, 75.7873],
    "lucknow": [26.8467, 80.9462],
    "kanpur": [26.4499, 80.3319],
    "nagpur": [21.1458, 79.0882],
    "indore": [22.7196, 75.8577],
    "bhopal": [23.2599, 77.4126],
    "patna": [25.5941, 85.1376],
    "vadodara": [22.3072, 73.1812],
    "ludhiana": [30.9010, 75.8573],
    "agra": [27.1751, 78.0421],
    "nashik": [19.9975, 73.7898],
    "coimbatore": [11.0168, 76.9558],
    "visakhapatnam": [17.6868, 83.2185],
    "madurai": [9.9252, 78.1198],
    "varanasi": [25.3176, 82.9739],
    "meerut": [28.9845, 77.7064],
    "rajkot": [22.3039, 70.8022],
    "jabalpur": [23.1815, 79.9864],
    "amritsar": [31.6340, 74.8723],
    "ranchi": [23.3441, 85.3096],
    "guwahati": [26.1445, 91.7362],
    "chandigarh": [30.7333, 76.7794],
    "mysore": [12.2958, 76.6394],
    "trivandrum": [8.5241, 76.9366],
    "bhubaneswar": [20.2961, 85.8245],
    "jamshedpur": [22.8046, 86.2029],
    "dehradun": [30.3165, 78.0322],
    "mangalore": [12.9141, 74.8560],
    "tiruchirappalli": [10.7905, 78.7047],
    "vijayawada": [16.5062, 80.6480],
    "gwalior": [26.2183, 78.1828],
    "ujjain": [23.1793, 75.7849],
    "kolhapur": [16.7050, 74.2433],
    "salem": [11.6643, 78.1460],
    "warangal": [17.9784, 79.5941],
    "nellore": [14.4426, 79.9865],
    "aligarh": [27.8974, 78.0880],
    "ajmer": [26.4499, 74.6399],
    "bareilly": [28.3670, 79.4304],
    "moradabad": [28.8386, 78.7733],
    "raipur": [21.2514, 81.6296],
    "dhanbad": [23.7957, 86.4304],
    "hubli": [15.3647, 75.1240],
    "bellary": [15.1394, 76.9214],
    "tirunelveli": [8.7139, 77.7567],
    "guntur": [16.3067, 80.4365],
    "siliguri": [26.7271, 88.3953],
    "bilaspur": [22.0797, 82.1409],
    "jodhpur": [26.2389, 73.0243],
    "noida": [28.5355, 77.3910],
    "ghaziabad": [28.6692, 77.4538],
    "faridabad": [28.4089, 77.3178],
    "gurgaon": [28.4595, 77.0266],

    # Tourist / Special Destinations
    "goa": [15.2993, 74.1240],
    "pondicherry": [11.9416, 79.8083],
    "andaman": [11.7401, 92.6586],
    "manali": [32.2432, 77.1892],
    "shimla": [31.1048, 77.1734],
    "darjeeling": [27.0410, 88.2663],
    "ooty": [11.4064, 76.6932],
    "munnar": [10.0889, 77.0595],
    "udaipur": [24.5854, 73.7125],
    "kaziranga": [26.5775, 93.1711],
    "rishikesh": [30.0869, 78.2676],
    "coorg": [12.3375, 75.8069],
    "ranthambore": [26.0173, 76.5026],
}

if destination:
    dest_key = destination.lower().strip()
    lat, lon = demo_locations.get(dest_key, [20.5937, 78.9629])  

    st.subheader("🌍 Map View")

    
    map_view = pdk.Deck(
        map_style=None,  
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=8, pitch=0),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=[{"lat": lat, "lon": lon}],
                get_position=["lon", "lat"],
                get_color=[255, 0, 0, 200],
                get_radius=8000,
            )
        ],
        tooltip={"text": f"Destination: {destination.title()}"},
    )

    st.pydeck_chart(map_view)



#  Generate Itinerary (Gemini)

if st.button("✨ Generate Itinerary"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not destination or not budget or not travel_dates:
        st.error("Please fill in all fields before generating your itinerary.")
    else:
        st.info("⏳ Generating itinerary... Please wait.")
        try:
            prompt = f"""
Create a detailed student-friendly travel itinerary for {destination}.
Budget range: {budget}.
Dates: {travel_dates}.
Traveler name: {user_name or 'Anonymous'}.
Travel preference: {travel_pref}.
Include accommodation, local food, travel tips, and a day-by-day plan.
"""

            # Initialize the model
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Generate content
            response = model.generate_content(prompt)

            # ✅ Clean output (human-readable)
            st.success("✅ Your AI-generated itinerary:")
            st.text_area("Itinerary", value=response.text, height=400)

        except Exception as e:
            st.error(f"Error generating itinerary: {e}")
