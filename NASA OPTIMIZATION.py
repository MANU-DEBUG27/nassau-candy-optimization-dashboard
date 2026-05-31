

import pandas as pd
df = pd.read_csv("data/Nassau Candy Distributor.csv") 

print(df.head(5))
print(df)


print(df.info())

print(df.isnull().sum())

print(df.describe())

df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"],   dayfirst=True)
df["Ship Date"] = df["Ship Date"].apply( lambda x: x.replace(year=2024))
df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Lead_Time"] = df["Lead_Time"] / 30
print(df[["Order Date", "Ship Date", "Lead_Time"]].head())
print(df.duplicated().sum()) 
df["Profit_Margin"] = (df["Gross Profit"] / df["Sales"]) * 100
print(df[["Sales", "Gross Profit", "Profit_Margin"]].head(21)) 

        # FACTORY MAPPING
 
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
print(df[["Product Name","Factory"]].head())
print(df[["Product Name","Factory"]].tail())

df.to_csv("data/cleaned_nassau.csv", index=False)

factory_coords = {
    "Lot's O' Nuts"     : (32.881893, -111.768036),
    "Wicked Choccy's"   : (32.076176, -81.088371),
    "Sugar Shack"       : (48.11914, -96.18115),
    "Secret Factory"    : (41.446333, -90.565487),
    "The Other Factory" : (35.1175, -89.971107)
}

print(df["State/Province"].unique())

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
from geopy.distance import geodesic
def calculate_distance(row):

    factory = row["Factory"]
    state = row["State/Province"]

from geopy.distance import geodesic
def calculate_distance(row):

    factory = row["Factory"]
    state = row["State/Province"]

    if (factory in factory_coords and state in state_coords):

        factory_location = factory_coords[factory]
        customer_location = state_coords[state]

        return geodesic(factory_location, customer_location).km
    return None

df["Distance_km"] = df.apply(calculate_distance, axis=1)
print(df[["Factory",  "State/Province",  "Distance_km"]].head(51))

df.to_csv("data/final_nassau.csv", index=False)

    # ORDER MONTH
df["Order_Month"] = df["Order Date"].dt.month
        #ORDER WEEKDAY 
df["Order_Weekday"] = df["Order Date"].dt.weekday
    # COST PER UNIT 
df["Cost_Per_Unit"] = (df["Cost"] / df["Units"])
    # PROFIT PER UNIT 
df["Profit_Per_Unit"] = (df["Gross Profit"] / df["Units"])
print(df.columns)

features = [
   "Distance_km",
   "Sales",
   "Units",
   "Gross Profit",
   "Cost",
   "Profit_Margin",
   "Cost_Per_Unit",
   "Profit_Per_Unit",
   "Order_Month",
   "Order_Weekday",
   "Ship Mode",
   "Division",
   "Region",
   "Factory"
]
                     
X = df[features]
y = df["Lead_Time"]
X = pd.get_dummies(X)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
   X,
   y,
   test_size=0.2,
   random_state=42
)

from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train, y_train)
predictions = model.predict(X_test)

from sklearn.metrics import (
   mean_absolute_error,
   mean_squared_error,
   r2_score
)

mae = mean_absolute_error(y_test, predictions)

rmse = mean_squared_error(y_test, predictions) ** 0.5

r2 = r2_score(y_test, predictions)
print("Linear Regression Results")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)

from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)


rf_r2 = r2_score(y_test, rf_predictions)

rf_mae = mean_absolute_error(y_test, rf_predictions)

print("Random Forest Results")
print("MAE:", rf_mae)
print("R2 Score:", rf_r2)


print(df["Lead_Time"].describe())
print(df["Lead_Time"].value_counts())
df = df[ (df["Lead_Time"] > 0) & (df["Lead_Time"] < 30)]
df = df.dropna()
 
import joblib
joblib.dump(model, "shipping_model.pkl")     
         