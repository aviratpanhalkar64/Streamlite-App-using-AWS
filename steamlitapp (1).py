#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import leafmap.foliumap as leafmap
import requests

st.title("Geospatial Data Visualization")

# Update the center coordinates to Peel Region, Canada
m = leafmap.Map(center=[43.7036, -79.7624], zoom=10, crs="EPSG4326")
m.add_basemap("ROADMAP")

# Define the GeoJSON URLs for Peel Region
geojson_urls = {
    "Population Data": "https://streamliteapp.s3.ap-south-1.amazonaws.com/New_population_bin.geojson",
    "income": "https://streamliteapp.s3.ap-south-1.amazonaws.com/Household_new+(5).geojson",
    "ndbi":"https://streamliteapp.s3.ap-south-1.amazonaws.com/2014-11-10_ndbi_EPSG2.tif"
    # Add other URLs similarly
    # "Layer Name": "URL"
}

# Add a sidebar for layer selection
selected_layers = st.sidebar.multiselect(
    "Select GeoJSON Layers to Display", list(geojson_urls.keys()), default=list(geojson_urls.keys())
)

# Add selected GeoJSON layers to the map
for layer_name in selected_layers:
    url = geojson_urls[layer_name]
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        geojson_content = response.json()
        m.add_geojson(geojson_content, layer_name)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for {layer_name}: {e}")
    except ValueError as e:
        st.error(f"Error parsing JSON for {layer_name}: {e}")

# Display the map
m.to_streamlit(height=600)

