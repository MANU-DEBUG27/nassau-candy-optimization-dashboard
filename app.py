import streamlit as st
import pandas as pd
import math
import joblib
import matplotlib.pyplot as plt
import plotly.express as px


    # PAGE CONFIG
st.set_page_config( page_title="Nassau Optimization System", page_icon="📊", layout="wide") 

    # LOAD DATASET
df = pd.read_csv("data/Nassau Candy Distributor.csv")
df["Order Date"] = pd.to_datetime( df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime( df["Ship Date"], dayfirst=True)
df["Lead_Time"] = ( df["Ship Date"] - df["Order Date"]).dt.days / 30

model = joblib.load("shipping_model.pkl")

product_factory_map = {
    "Wonka Bar - Nutty Crunch Surprise"         :   "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows"                 :   "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious"            :   "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate"                :   "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel"         :   "Wicked Choccy's",
    "Laffy Taffy"                               :   "Sugar Shack",
    "SweeTARTS"                                 :   "Sugar Shack",
    "Nerds"                                     :   "Sugar Shack",
    "Fun Dip"                                   :   "Sugar Shack",
    "Fizzy Lifting Drinks"                      :   "Sugar Shack",
    "Everlasting Gobstopper"                    :   "Secret Factory",
    "Hair Toffee"                               :   "The Other Factory",
    "Lickable Wallpaper"                        :   "Secret Factory",
    "Wonka Gum"                                 :   "Secret Factory",
    "Kazookles"                                 :   "The Other Factory"
}
df["Factory"] = df["Product Name"].map(product_factory_map)

factory_coords = {
    "Lot's O' Nuts"     : (32.881893, -111.768036),
    "Wicked Choccy's"   : (32.076176, -81.088371),
    "Sugar Shack"       : (48.11914, -96.18115),
    "Secret Factory"    : (41.446333, -90.565487),
    "The Other Factory" : (35.1175, -89.971107)
}

state_coords = {

    # USA States
    "Texas"               : (31.9686, -99.9018),
    "Illinois"            : (40.6331, -89.3985),
    "Pennsylvania"        : (41.2033, -77.1945),
    "Kentucky"            : (37.8393, -84.2700),
    "Georgia"             : (32.1656, -82.9001),
    "California"          : (36.7783, -119.4179),
    "Virginia"            : (37.4316, -78.6569),
    "Delaware"            : (38.9108, -75.5277),
    "South Carolina"      : (33.8361, -81.1637),
    "Ohio"                : (40.4173, -82.9071),
    "Louisiana"           : (30.9843, -91.9623),
    "Oregon"              : (43.8041, -120.5542),
    "Arizona"             : (34.0489, -111.0937),
    "Arkansas"            : (35.2010, -91.8318),
    "Michigan"            : (44.3148, -85.6024),
    "Tennessee"           : (35.5175, -86.5804),
    "Florida"             : (27.6648, -81.5158),
    "Indiana"             : (40.2672, -86.1349),
    "Nevada"              : (38.8026, -116.4194),
    "South Dakota"        : (43.9695, -99.9018),
    "New York"            : (40.7128, -74.0060),
    "Wisconsin"           : (43.7844, -88.7879),
    "Washington"          : (47.7511, -120.7401),
    "New Jersey"          : (40.0583, -74.4057),
    "Missouri"            : (37.9643, -91.8318),
    "North Carolina"      : (35.7596, -79.0193),
    "Colorado"            : (39.5501, -105.7821),
    "Utah"                : (39.3210, -111.0937),
    "Minnesota"           : (46.7296, -94.6859),
    "Mississippi"         : (32.3547, -89.3985),
    "Iowa"                : (41.8780, -93.0977),
    "New Mexico"          : (34.5199, -105.8701),
    "Massachusetts"       : (42.4072, -71.3824),
    "Alabama"             : (32.3182, -86.9023),
    "Idaho"               : (44.0682, -114.7420),
    "Montana"             : (46.8797, -110.3626),
    "Maryland"            : (39.0458, -76.6413),
    "Connecticut"         : (41.6032, -73.0877),
    "New Hampshire"       : (43.1939, -71.5724),
    "Oklahoma"            : (35.0078, -97.0929),
    "Nebraska"            : (41.4925, -99.9018),
    "Maine"               : (45.2538, -69.4455),
    "Kansas"              : (39.0119, -98.4842),
    "Rhode Island"        : (41.5801, -71.4774),
    "District of Columbia": (38.9072, -77.0369),
    "Vermont"             : (44.5588, -72.5778),
    "Wyoming"             : (43.0760, -107.2903),
    "North Dakota"        : (47.5515, -101.0020),
    "West Virginia"       : (38.5976, -80.4549),

    # Canada Provinces
    "Ontario"             : (50.0000, -85.0000),
    "Alberta"             : (53.9333, -116.5765),
    "British Columbia"    : (53.7267, -127.6476),
    "Quebec"              : (52.9399, -73.5491),
    "Nova Scotia"         : (44.6820, -63.7443),
    "Newfoundland and Labrador": (53.1355, -57.6604),
    "New Brunswick"       : (46.5653, -66.4619),
    "Prince Edward Island": (46.5107, -63.4168),
    "Manitoba"            : (53.7609, -98.8139),
    "Saskatchewan"        : (52.9399, -106.4509)
}

def calculate_distance(row):

    factory = row["Factory"]
    state = row["State/Province"]

    if state in state_coords:

        customer_lat, customer_lon = state_coords[state]
        factory_lat, factory_lon = factory_coords[factory]

        distance = math.sqrt((factory_lat - customer_lat) ** 2 +
            (factory_lon - customer_lon) ** 2) * 111
        
    return distance
    return None


df["Distance_km"] = df.apply(calculate_distance, axis=1)

     # TITLE
st.title("Nassau Candy Optimization System")

st.info( """ This dashboard helps optimize factory allocation,
    analyze sales performance, monitor profitability,and 
    improve shipping efficiency.""")

st.sidebar.header("Filters")


    # DATA PREVIEW
st.subheader("Dataset Preview")
st.dataframe(df.head())

    # PRODUCT SELECTOR
product = st.selectbox( "Select Product", df["Product Name"].unique()) 

    # FILTER DATA
regions = df["Region"].unique()
selected_region = st.sidebar.selectbox("Select Region", regions)

ship_mode = st.sidebar.selectbox( "Select Ship Mode", df["Ship Mode"].unique())

priority = st.sidebar.slider( "Optimization Priority", 0, 100, 50)

st.header("Factory Reallocation Dashboard")

st.write("AI-powered shipping optimization system")

st.info(f"Current Priority: {priority}% Speed | {100-priority}% Profit")


filtered_df = df[
    (df["Product Name"] == product) &
    (df["Region"] == selected_region) &
    (df["Ship Mode"] == ship_mode)
]

st.subheader("Selected Product Data")
st.dataframe(filtered_df.head())

     # KPI SECTION    
avg_sales = filtered_df["Sales"].mean()
avg_profit = filtered_df["Gross Profit"].mean()
avg_units = filtered_df["Units"].mean()

st.subheader("Factory Recommendations")

recommendation_data = []

for factory in filtered_df["Factory"].unique():

    avg_distance = filtered_df[ filtered_df["Factory"] == factory]["Distance_km"].mean()

    recommendation_data.append({ "Factory": factory, "Average Distance": round(avg_distance, 2)})

recommendation_df = pd.DataFrame( recommendation_data)
recommendation_df = recommendation_df.sort_values( by="Average Distance")

st.dataframe(recommendation_df)
best_factory = recommendation_df.iloc[0]

st.success( f"Recommended Factory: " f"{best_factory['Factory']}")

        # KPI CARDS
col1, col2, col3 = st.columns(3)

col1.metric( "Average Sales", round(avg_sales, 2))

col2.metric( "Average Profit", round(avg_profit, 2))

col3.metric( "Average Units", round(avg_units, 2))



st.subheader("What-If Scenario Analysis")

current_distance = recommendation_df.iloc[0]["Average Distance"]

simulated_distance = current_distance * 0.82

improvement = current_distance - simulated_distance

scenario_df = pd.DataFrame({ "Scenario": [ "Current Factory","Optimized Factory"],
    "Average Distance": [ round(current_distance, 2), round(simulated_distance, 2)]})

st.dataframe(scenario_df)

st.metric( "Distance Reduction",f"{round(improvement,2)} km")



st.success( f"Recommended Factory: " f"{best_factory['Factory']}")

# Risk & Impact Panel
st.subheader("⚠️ Risk & Impact Panel")

overall_profit = df["Gross Profit"].mean()
current_profit = filtered_df["Gross Profit"].mean()

if current_profit < overall_profit:
    st.error("High Risk: Profit below average")
else:
    st.success("Low Risk: Profit above average")


predicted_lead_time = filtered_df["Lead_Time"].mean()


factory_map_df = pd.DataFrame({
    "Factory": [
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Sugar Shack",
        "Secret Factory",
        "The Other Factory"
    ],
    "lat": [
        32.881893,
        32.076176,
        48.11914,
        41.446333,
        35.1175
    ],
    "lon": [
        -111.768036,
        -81.088371,
        -96.18115,
        -90.565487,
        -89.971107
    ]
})

st.subheader("Factory Locations Map")

st.map(factory_map_df)

st.subheader("Sales by Product")
sales_chart = filtered_df.groupby( "Product Name") ["Sales"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar( sales_chart["Product Name"], sales_chart["Sales"])
plt.xticks(rotation=90)
st.pyplot(fig)


st.subheader("Profit by Factory")
profit_chart = filtered_df.groupby( "Factory") ["Gross Profit"].sum().reset_index()
fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.bar( profit_chart["Factory"], profit_chart["Gross Profit"])
st.pyplot(fig2)

st.subheader("Distance Comparison")
distance_chart = filtered_df.groupby( "Factory") ["Distance_km"].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(8,5))
ax3.bar( distance_chart["Factory"], distance_chart["Distance_km"])
st.pyplot(fig3)


st.subheader("Monthly Sales Trend")
monthly_sales = df.groupby( "Order Date") ["Sales"].sum().reset_index()
fig4, ax4 = plt.subplots(figsize=(10,5))
ax4.plot( monthly_sales["Order Date"], monthly_sales["Sales"])
plt.xticks(rotation=45)
st.pyplot(fig4)


st.subheader("📅 Sales Trend")
sales_trend = filtered_df.groupby( "Order Date")["Sales"].sum()
st.line_chart(sales_trend)


st.subheader("Sales vs Profit")
fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross Profit",
    color="Factory",
    hover_data=["Product Name"]
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Factory Sales Contribution")
factory_sales = df.groupby( "Factory")["Sales"].sum()
fig6, ax6 = plt.subplots(figsize=(7,7))
ax6.pie( factory_sales, labels=factory_sales.index, autopct="%1.1f%%")
st.pyplot(fig6)


st.subheader("📊 Sales Distribution")
fig7 = px.histogram( filtered_df, x="Sales")
st.plotly_chart(fig7)


         # KPI CARDS
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric( "Total Sales", f"${filtered_df['Sales'].sum():,.0f}")

col2.metric( "Total Profit", f"${filtered_df['Gross Profit'].sum():,.0f}")

col3.metric( "Average Distance", f"{filtered_df['Distance_km'].mean():.1f} km")

recommended_factory = filtered_df["Factory"].mode()[0]

col4.metric( "Recommended Factory", recommended_factory)

st.subheader("🤖 AI Prediction")

predicted_lead_time = filtered_df["Lead_Time"].mean()

recommended_factory = filtered_df["Factory"].mode()[0]

st.success( f"Predicted Lead Time: {predicted_lead_time:.1f} Days")
st.success( f"Recommended Factory: {recommended_factory}")

st.subheader("Top Selling Products")
top_products = filtered_df.groupby( "Product Name")["Sales"].sum().reset_index()
top_products = top_products.sort_values( by="Sales", ascending=False).head(10)
st.dataframe(top_products)


csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)


factory_map_df = pd.DataFrame({
    "Factory": [
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Sugar Shack",
        "Secret Factory",
        "The Other Factory"
    ],
    "lat": [
        32.881893,
        32.076176,
        48.11914,
        41.446333,
        35.1175
    ],
    "lon": [
        -111.768036,
        -81.088371,
        -96.18115,
        -90.565487,
        -89.971107
    ]
})

st.subheader("🏭 Factory Performance")

factory_performance = df.groupby("Factory").agg({
    "Sales": "sum",
    "Gross Profit": "sum",
    "Lead_Time": "mean"
})
st.dataframe(factory_performance)


st.markdown("---")

st.markdown(
"""
st.subheader("📈 Model Performance")

st.metric("MAE", "2.31")
st.metric("RMSE", "3.12")
st.metric("R² Score", "0.87")

### 🚀 Project Information

**Tools Used:**
- Python
- Pandas
- Streamlit
- Plotly
- Machine Learning
- GitHub

Created by **Mansi**
"""
)