#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import leafmap.foliumap as leafmap

st.title("Geospatial Data Visualization")

# Update the center coordinates to Peel Region, Canada
m = leafmap.Map(center=[43.7036, -79.7624], zoom=10, crs="EPSG4326")
m.add_basemap("ROADMAP")

# Define the GeoJSON URLs for Peel Region
geojson_urls = {
    "Population Data": "https://streamliteapp.s3.ap-south-1.amazonaws.com/New_population_bin.geojson",
    "Income Data": "https://streamliteapp.s3.ap-south-1.amazonaws.com/Household_new+(5).geojson",
}

# Add a sidebar for layer selection
selected_layers = st.sidebar.multiselect(
    "Select GeoJSON Layers to Display", list(geojson_urls.keys()), default=list(geojson_urls.keys())
)

# Add a sidebar for basemap selection
basemaps = ["ROADMAP", "SATELLITE", "TERRAIN", "HYBRID"]
selected_basemap = st.sidebar.selectbox("Select Basemap", basemaps)
m.add_basemap(selected_basemap)

# Add styling options
st.sidebar.title("Layer Styling")
layer_styles = {}
for layer_name in selected_layers:
    st.sidebar.subheader(f"{layer_name} Styling")
    color = st.sidebar.color_picker(f"Choose color for {layer_name}", "#FF0000")
    opacity = st.sidebar.slider(f"Choose opacity for {layer_name}", 0.0, 1.0, 0.5)
    layer_styles[layer_name] = {"color": color, "opacity": opacity}

# Function to apply styling to GeoJSON
def apply_styling(geojson_content, style):
    for feature in geojson_content['features']:
        feature['properties']['style'] = {
            "color": style["color"],
            "opacity": style["opacity"]
        }
    return geojson_content

# Add selected GeoJSON layers to the map
for layer_name in selected_layers:
    url = geojson_urls[layer_name]
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        geojson_content = response.json()
        geojson_content = apply_styling(geojson_content, layer_styles[layer_name])
        m.add_geojson(geojson_content, layer_name)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for {layer_name}: {e}")
    except ValueError as e:
        st.error(f"Error parsing JSON for {layer_name}: {e}")

# Display the map
m.to_streamlit(height=600)

