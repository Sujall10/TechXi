import folium

# Create a map centered at Gujarat, India
m = folium.Map(location=[23.0225, 72.5714], zoom_start=7, tiles="Stamen Terrain")

# Save the map as an HTML file
m.save("gujarat_map.html")
