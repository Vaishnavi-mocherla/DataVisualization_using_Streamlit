
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from numpy.random import default_rng as rng
from datetime import datetime, date
from datetime import time
import plotly.figure_factory as ff

###############################
# Set up the page configuration
############################### 
st.set_page_config(
    page_title="Hackathon Starter",
    layout="wide",
    initial_sidebar_state="expanded",
)

#############################
# Uploading a csv 
#############################

df = pd.read_excel('Data/Adidas.xlsx')
st.write(df.head())

#############################
# Area Charts
#############################

df1 = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=['A', 'B', 'C'])
st.area_chart(df1)


df = df.sort_values("InvoiceDate")
st.area_chart(df.set_index("InvoiceDate")[["TotalSales", "OperatingProfit"]])
                                                                             
#############################
# Bar Charts
#############################

# Suppose you already read your CSV

# Group by State and take the maximum PriceperUnit
df_max = df.groupby("State", as_index=False)["PriceperUnit"].max()

# Set State as index for plotting
df_max = df_max.set_index("State")

# Bar chart of max price per unit per state
st.bar_chart(df_max)

# Top 2 
# Step 1: Group by State and take max PriceperUnit
df_max = df.groupby("State", as_index=False)["PriceperUnit"].max()

# Step 2: Sort by PriceperUnit descending
df_max = df_max.sort_values("PriceperUnit", ascending=False)

# Step 3: Keep only top 2
df_top2 = df_max.head(10)

# Step 4: Set State as index for plotting
df_top2 = df_top2.set_index("State")

# Plot
st.bar_chart(df_top2)

# import streamlit as st
# from vega_datasets import data

# source = data.barley()

st.bar_chart(df, x="Product", y="UnitsSold", color="SalesMethod", horizontal=True)

#############################
# Line Charts
#############################

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.sort_values("InvoiceDate")

graph_sales = df.resample("M", on="InvoiceDate")["UnitsSold"].max()
graph_sales_1 = df.resample("M", on="InvoiceDate")["PriceperUnit"].max()
combined_df = pd.concat([graph_sales, graph_sales_1], axis=1)
st.line_chart(combined_df)


#############################
# Maps
#############################

import streamlit as st
import pandas as pd

dfsf = pd.DataFrame({
    "lat": [37.7749, 40.7128],   # San Francisco, New York
    "lon": [-122.4194, -74.0060]
})

st.map(dfsf)

import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

dfsd = pd.DataFrame(
    {
        "col1": rng(0).standard_normal(1000) / 50 + 37.76,
        "col2": rng(1).standard_normal(1000) / 50 + -122.4,
        "col3": rng(2).standard_normal(1000) * 100,
        "col4": rng(3).standard_normal((1000, 4)).tolist(),
    }
)

st.map(dfsd, latitude="col1", longitude="col2", size="col3", color = "col4", zoom=10)

import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

# sample data
df33 = pd.DataFrame({
    "lat": np.random.normal(37.76, 0.01, 1000),
    "lon": np.random.normal(-122.4, 0.01, 1000),
    "category": np.random.choice(["A", "B", "C"], 1000)
})

#############################
#Altair scatter plot
#############################


df22 = pd.DataFrame({
    "Retailer": ["A", "B", "C", "D", "E"],
    "RetailerID": [101, 102, 103, 104, 105],
    "InvoiceDate": pd.date_range("2023-01-01", periods=5, freq="M"),
    "Region": ["North", "South", "East", "West", "North"],
    "State": ["CA", "TX", "NY", "WA", "CA"],
    "City": ["San Jose", "Houston", "NYC", "Seattle", "LA"],
    "Product": ["Laptop", "Phone", "Tablet", "Monitor", "Printer"],
    "PriceperUnit": [1200, 800, 500, 300, 150],
    "UnitsSold": [10, 25, 40, 15, 30],
    "TotalSales": [12000, 20000, 20000, 4500, 4500],
    "OperatingProfit": [3000, 5000, 6000, 800, 1200],
    "OperatingMargin": [0.25, 0.20, 0.30, 0.18, 0.27],
    "SalesMethod": ["Online", "Retail", "Retail", "Online", "Online"]
})

chart = (
    alt.Chart(df22)
    .mark_circle()
    .encode(
        x="TotalSales:Q",
        y="UnitsSold",
        size="OperatingProfit:Q",
        color="Product:N",
        tooltip=[
            "Retailer",
            "City",
            "Product",
            "UnitsSold",
            "TotalSales",
            "OperatingProfit",
            "SalesMethod"
        ]
    )
    .properties(title="Sales Scatter Plot by Region")
).interactive()

st.altair_chart(chart, theme=None, use_container_width=True)



#############################
# Histograms
#############################

df_melt = df.melt(
    value_vars=["TotalSales","OperatingProfit"],
    var_name="Metric", value_name="Value"
)
fig = px.histogram(
    df_melt, x="Value", color="Metric",
    barmode="overlay", opacity=0.6, nbins=60,
    histnorm="probability density",  # comparable scales
    marginal="box")
st.plotly_chart(fig, use_container_width=True)


#############################
#Plotly Chart with configuratio
#############################
import plotly.graph_objects as go   

fig = go.Figure()

# Scatter: Total Sales vs Units Sold
fig.add_trace(
    go.Scatter(
        x=df["UnitsSold"],
        y=df["TotalSales"],
        mode="markers",
        text=df["Product"],   # hover tooltip
        marker=dict(size=10, color=df["OperatingProfit"], colorscale="Viridis", showscale=True)
    )
)

fig.update_layout(
    title="Sales vs Units Scatter",
    xaxis_title="Units Sold",
    yaxis_title="Total Sales"
)

st.plotly_chart(fig, config={'scrollZoom': True})




fig = px.scatter(df, x="OperatingProfit", y="TotalSales")

event = st.plotly_chart(fig, key="iris", on_select="rerun")


fig = px.scatter(
    df,
    x="UnitsSold",
    y="TotalSales",
    color="SalesMethod",
    size="OperatingProfit",
    hover_data=["OperatingMargin"], 
)

event = st.plotly_chart(fig)

