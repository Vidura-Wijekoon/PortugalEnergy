# Import required libraries# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import warnings
import os
import pydeck as pdk

warnings.filterwarnings('ignore')

# Check for MAPBOX_API_KEY
mapbox_api_key = os.getenv("MAPBOX_API_KEY")
if mapbox_api_key is None:
    raise ValueError("MAPBOX_API_KEY is not set. Please set this environment variable and retry.")

# Coordinates for each region (Replace this with the actual coordinates for your districts)
district_coordinates = {
    'North': [41.6955, -8.8345],
    'Center': [40.2033, -8.4109],
    'Lisbon': [38.7223, -9.1393],
    'Alentejo': [38.6453, -7.9143],
    'Algarve': [37.0179, -7.9304],
    'Azores': [37.7412, -25.6756],
    'Madeira': [32.6669, -16.9241]
}

# Default coordinates for missing districts
default_coordinates = [0, 0]  # replace with suitable values

def load_data():
    # Load the data
    df = pd.read_excel(r"D:\Python\streamlit_env\Scripts\energy_demand_306 (1).xlsx")
    df2 = pd.read_csv(r"D:\Python\streamlit_env\Scripts\cleaned_data.csv")

    # Handle null values
    df2["commissioning_year"] = df2['commissioning_year'].replace(np.nan, df2["commissioning_year"].median())
    df2["district"] = df2["district"].replace(np.nan, df2["district"].mode()[0])
    df2["municipality"] = df2["municipality"].replace(np.nan, df2["municipality"].mode()[0])

    # Replace missing districts with default coordinates
    df2['latitude'] = df2['district'].map(lambda x: district_coordinates.get(x, default_coordinates)[0])
    df2['longitude'] = df2['district'].map(lambda x: district_coordinates.get(x, default_coordinates)[1])

    # Merge the dataframes
    df = pd.concat([df, df2])

    return df

def main():
    # Title and subheader
    st.title("Energy Communities in Portugal")
    st.subheader("A tool for visualizing energy demand, energy supply and solar potential")

    # Load the data
    df = load_data()

    # Sidebar
    st.sidebar.title("Filters and User Inputs")

    # Filter by district
    district_choice = st.sidebar.multiselect("Select district", df['district'].unique())
    if district_choice:
        df = df[df['district'].isin(district_choice)]

    # Show the Dataframe
    st.text('Dataframe')
    st.dataframe(df)
    district_counts = df["district"].value_counts().reset_index()
    district_counts.columns = ['district', 'count']

    fig1 = px.bar(district_counts, x='district', y='count', color='district', title="Total number of districts in Portugal")
    st.plotly_chart(fig1)


   # Grouping each districts and sum of capacity in each district
   #grouping each districts and sum of capacity in each district
    Capacity_df = df.groupby('district')['capacity_mw'].sum().reset_index()


   # Bar chart between capacity_mw vs district
   #barchart between capacity_mw vs district
    fig2 = px.bar(Capacity_df, x='district', y='capacity_mw',color = "district",
               labels = {"capacity_mw":"Total Energy Capacity in MegaWatt"},
               height= 600,
               title = "Total Energy Capacity In Mega Watt on Each District")
    st.plotly_chart(fig2)

   # Count of energy sources as primary fuel
    fig3 = px.histogram(df, x ="primary_fuel",
                       height = 600,
                       color = "primary_fuel",
                       title = "Total Count of Energy sources as primary fuel")
    st.plotly_chart(fig3)

   # Grouping each primary fuels with energy capacity
    Capacity_energy =  df.groupby('primary_fuel')['capacity_mw'].sum().sort_values(ascending = False).reset_index()

   # Barplot
    fig4 = px.bar(Capacity_energy,
               x ="primary_fuel",
               y = "capacity_mw",
               color="primary_fuel",
               title = "Energy Capacity (MW) vs primary Fuel (Energy Sources)")
    st.plotly_chart(fig4)

   # Grouping each municipality with energy capacity
    Capacity_munici = df.groupby('municipality')['capacity_mw'].sum().sort_values(ascending = False).reset_index()

   # Top 10 municipalities having higher energy capacity
    fig5 = px.bar(Capacity_munici[:10],
               y ="municipality",
               x = "capacity_mw",
               color = "municipality",
               title = "Top 10 Municipalities having higher Energy Capacity(MW)")
    st.plotly_chart(fig5)

   # Municipalities having lower energy capacity
    fig6 = px.bar(Capacity_munici[-20:],
               y ="municipality",
               x = "capacity_mw",
               color = "municipality",
               title = "Municipalities having Low Energy Capcity(MW)")
    st.plotly_chart(fig6)

       # Grouping each Municipality with Energy capacity
    Capacity_munici = df.groupby('municipality')['capacity_mw'].sum().sort_values(ascending = False).reset_index()

   # Top 10 Municipalities having Higher Energy Capacity :
    fig7 = px.bar(Capacity_munici[:10],
                y ="municipality",
                x = "capacity_mw",
                color = "municipality",
                title = "Top 10 Municipalities having higher Energy Capacity(MW)")
    st.plotly_chart(fig7)

   # Municipalities having lower Energy Capacity :
    fig8 = px.bar(Capacity_munici[-20:],
                y ="municipality",
                x = "capacity_mw",
                color = "municipality",
                title = "Municipalities having Low Energy Capcity(MW)")
    st.plotly_chart(fig8)

   # Bar graph of Municipalities of Energy Capacity :
    fig9 = px.bar(Capacity_munici,
                x ="municipality",
                y = "capacity_mw",
                color = "municipality",
                height = 600,width = 1300,
                title = "Energy Capacity(MW) of All Municipalite")
    st.plotly_chart(fig9)

   #Grouping capacity on Commissioning_year
    Capacity_year = df.groupby('commissioning_year')['capacity_mw'].mean().sort_values(ascending = False).reset_index()

   #creating the parameter
    values = Capacity_year["capacity_mw"]
    names = Capacity_year["commissioning_year"]

   # Creating a pie chart for the top 7 commissioning_years with the highest energy capacity (MW)
    fig10 = px.pie(df, values=values[:7],
                names=names[:7],
                height=600,
                title="Top 7 commissioning_year having Higher Energy Capacity (MW)")
    fig10.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig10)

   # Creating a pie chart for the top 15 commissioning_years with the highest energy capacity (MW)
    fig11 = px.pie(df, values=values[:15],
                names=names[:15],
                height=600,
                title="Top 15 commissioning_year Vs Energy Capacity (MW)")
    fig11.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig11)



   # Load the data
    df = load_data()

   # Sidebar for user inputs and filters
    st.sidebar.title("Filters and User Inputs")

   # Filter by district
    district = st.sidebar.multiselect("Select districts", df['district'].unique())
    if district:
       df = df[df['district'].isin(district)]

   # Show the Dataframe
    st.text('Dataframe')
    st.dataframe(df)

    # Prepare the data for the map
# Prepare the data for the map
    df['coordinates'] = df['district'].map(district_coordinates)
    df['latitude'] = df['coordinates'].apply(lambda x: x[0] if isinstance(x, list) else np.nan)
    df['longitude'] = df['coordinates'].apply(lambda x: x[1] if isinstance(x, list) else np.nan)
    map_data = df[['latitude', 'longitude', 'capacity_mw']]



   # Define a layer to display on a map
    layer = pdk.Layer(
       "HeatmapLayer",
       map_data,
       opacity=0.8,
       get_position=['longitude', 'latitude'],
       get_weight='capacity_mw',
       threshold=0.3,
       radiusPixels=50,
    )
   # Set the map's initial viewport
    view_state = pdk.ViewState(
       latitude=39.6395,
       longitude=-7.8492,
       zoom=6,
       max_zoom=15,
       pitch=40.5,
       bearing=-27.36
    )

   # Use PyDeck to create the map
    r = pdk.Deck(
       layers=[layer],
       initial_view_state=view_state,
       map_style="mapbox://styles/mapbox/streets-v11"  # This is the style for a street map
    )

   # Display the map in Streamlit
    st.pydeck_chart(r)


if __name__ == "__main__":
    main()
    mapbox_api_key = os.getenv("MAPBOX_API_KEY")
    if mapbox_api_key is None:
        raise ValueError
