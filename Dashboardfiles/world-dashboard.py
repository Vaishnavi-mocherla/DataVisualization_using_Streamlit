import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="World Dashboard", layout="wide")

# --- Load & tidy ---
df = pd.read_csv("worldnew.csv")

# If CSV has an extra index col
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Ensure numeric coords and drop bad rows
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
df["population"] = pd.to_numeric(df["population"], errors="coerce")
df = df.dropna(subset=["lat", "lng", "population"])

# --- Header KPIs ---
with st.container(border=True):
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Cities (unique)", int(df["city"].nunique()))
    col2.metric("Total Countries", int(df["country"].nunique()))
    col3.metric("Rows", len(df))
    col4.metric("Total Population", int(df["population"].sum()))
    col5.metric("Avg City Pop", int(df["population"].mean()))

# --- Sidebar filters ---
with st.sidebar:
    st.header("Filters")

    countries_all = sorted(df["country"].dropna().unique().tolist())
    selected_countries = st.multiselect(
        "Country", options=countries_all, default=countries_all
    )

    min_pop = int(df["population"].min()) if df["population"].notna().any() else 0
    max_pop = int(df["population"].max()) if df["population"].notna().any() else 0

    pop_lo, pop_hi = st.slider(
        "Population range",
        min_value=min_pop,
        max_value=max_pop,
        value=(min_pop, max_pop),
        step=1 if (max_pop - min_pop) < 100_000 else max(1, int((max_pop - min_pop) / 100))
    )

    show_top10 = st.checkbox(
        "Show Top 10 countries by average city population (centroids)",
        value=False
    )

# --- Apply filters ---
mask = df["country"].isin(selected_countries) & df["population"].between(pop_lo, pop_hi)
df_f = df.loc[mask].copy()

st.subheader("Cities")
st.caption("Dots show cities that match your filters.")
# st.map(df_f, latitude="lat", longitude="lng")

# --- Prepare centroids early so tabs can use it safely ---
centroid = pd.DataFrame(columns=["country", "population", "lat", "lng"])

# --- Optional top 10 centroids section ---
if show_top10:
    st.subheader("Top 10 Countries (by average city population)")
    if len(df_f):
        centroid = (
            df_f.groupby("country", as_index=False)
                .agg(
                    population=("population", "mean"),
                    lat=("lat", "mean"),
                    lng=("lng", "mean"),
                )
                .sort_values("population", ascending=False)
                .head(10)
        )

   
# --- Tabs (use the safely-defined `centroid`) ---
tab1, tab2 = st.tabs(["Cities", "Country Centroids"])
with tab1:
    st.map(df_f, latitude="lat", longitude="lng")
with tab2:
    if not centroid.empty:
        st.map(centroid, latitude="lat", longitude="lng")

        st.dataframe(
            centroid.rename(columns={"population": "avg_city_population"})[
                ["country", "avg_city_population", "lat", "lng"]
            ],
            use_container_width=True,
        )

    else:
        st.info("Turn on the checkbox or adjust filters to compute centroids.")



top10 = (
    df_f.groupby("country")["population"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
)

chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X("country", sort="-y", title="Country"),
        y=alt.Y("population", title="Total Population"),
        tooltip=["country", "population"]
    )
    .properties(
        title="Top 10 Countries by City Population"
    )
)

st.altair_chart(chart, use_container_width=True)

# The table (“Top 10 countries by average city population (centroids)”) is sorted by average city population per country → mean(population). That can put Korea, South at #1 if its cities in your dataset are large on average.

# The bar chart is built with df_f.groupby("country")["population"].sum() → total city population per country. That naturally makes China #1.



import pydeck as pdk

st.subheader("City Density Heatmap")

# Controls
c1, c2 = st.columns(2)
radius_px = c1.slider("Point radius (pixels)", 10, 100, 40)
intensity = c2.slider("Intensity", 1, 10, 4)

view = pdk.ViewState(
    latitude=float(df_f["lat"].mean()),
    longitude=float(df_f["lng"].mean()),
    zoom=2, pitch=0
)

heat = pdk.Layer(
    "HeatmapLayer",
    data=df_f,
    get_position='[lng, lat]',
    get_weight="population",     # heavier cities glow more
    radiusPixels=radius_px,
    intensity=intensity,
)

r = pdk.Deck(layers=[heat], initial_view_state=view, tooltip={"text": "{city}, {country}\nPop: {population}"})
st.pydeck_chart(r)


import pydeck as pdk

st.subheader("Hexagon Density (3D)")

elev = st.slider("Elevation scale", 1, 50, 10)
radius_m = st.slider("Hexagon radius (meters)", 10000, 150000, 50000, step=5000)

view = pdk.ViewState(
    latitude=float(df_f["lat"].mean()),
    longitude=float(df_f["lng"].mean()),
    zoom=2.2, pitch=40, bearing=15
)

hex_layer = pdk.Layer(
    "HexagonLayer",
    data=df_f,
    get_position='[lng, lat]',
    radius=radius_m,
    elevation_scale=elev,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=0.9,
    get_weight="population",
    pickable=True,
)

r = pdk.Deck(layers=[hex_layer], initial_view_state=view,
             tooltip={"text": "Cells aggregated by nearby cities\nHeight ~ density"})
st.pydeck_chart(r)

import numpy as np

st.subheader("Nearby Cities Finder")

if not df_f.empty:
    # Pick a reference city
    home_city = st.selectbox("Select a city", sorted(df_f["city"].unique()))
    max_km = st.slider("Radius (km)", 50, 3000, 500, step=50)

    # Fetch the home city coords
    home_row = df_f.loc[df_f["city"] == home_city].iloc[0]
    lat0, lng0 = float(home_row["lat"]), float(home_row["lng"])

    # Haversine distance (km)
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        p1, p2 = np.radians(lat1), np.radians(lat2)
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dlon/2)**2
        return 2*R*np.arcsin(np.sqrt(a))

    df_near = df_f.copy()
    df_near["km"] = haversine(lat0, lng0, df_near["lat"].values, df_near["lng"].values)
    df_near = df_near[df_near["km"] <= max_km].sort_values("km")

    st.caption(f"Found {len(df_near)} cities within {max_km} km of {home_city}.")
    st.map(df_near, latitude="lat", longitude="lng")
    st.dataframe(df_near[["city","country","population","km"]].reset_index(drop=True), use_container_width=True)
else:
    st.info("No cities available with current filters.")


import pydeck as pdk

st.subheader("Country Hub → Top Cities (Arcs)")

if not df_f.empty:
    pick_country = st.selectbox("Choose a country to highlight", sorted(df_f["country"].unique()))
    k = st.slider("Top N cities by population", 3, 30, 10)

    df_c = df_f[df_f["country"] == pick_country].copy()
    if not df_c.empty:
        # ✅ Correct way: mean lat/lng as floats
        hub_lat = float(df_c["lat"].mean())
        hub_lng = float(df_c["lng"].mean())

        # Top N destination cities
        top_cities = df_c.sort_values("population", ascending=False).head(k).copy()
        top_cities["hub_lat"] = hub_lat
        top_cities["hub_lng"] = hub_lng

        arcs = pdk.Layer(
            "ArcLayer",
            data=top_cities,
            get_source_position='[hub_lng, hub_lat]',
            get_target_position='[lng, lat]',
            get_width=2,
            get_source_color=[10, 120, 255],
            get_target_color=[255, 80, 0],
            pickable=True,
        )
        hub_point = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lng": hub_lng, "lat": hub_lat}],
            get_position='[lng, lat]',
            get_radius=60000,
            get_fill_color=[0,0,0,200]
        )
        city_points = pdk.Layer(
            "ScatterplotLayer",
            data=top_cities,
            get_position='[lng, lat]',
            get_radius=30000,
            get_fill_color=[255, 140, 0, 160],
            pickable=True
        )

        view = pdk.ViewState(latitude=hub_lat, longitude=hub_lng, zoom=3, pitch=30)
        r = pdk.Deck(
            layers=[hub_point, city_points, arcs],
            initial_view_state=view,
            tooltip={"text": "{city}, Pop: {population}"}
        )
        st.pydeck_chart(r)
    else:
        st.info("No cities for that country under current filters.")
