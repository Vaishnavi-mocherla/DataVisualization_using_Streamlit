import streamlit as st 
import pandas as pd 
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Uber Dashboard",
    page_icon="📊",
    layout="wide",       # "centered" or "wide"
    initial_sidebar_state="expanded"
)


df = pd.read_csv('newuber.csv')

with st.container(border=True):
    count_booking = df['booking_id'].nunique()
    max_customer_rating = df['customer_rating'].mean()
    avg_booking_price = df['booking_value'].mean()
    vehicle_types = df['vehicle_type'].nunique()

    col1, col2,col3, col4 = st.columns(4)

    col1.metric("Total Bookings", count_booking, border=True)
    col2.metric("Avg Ratings", f'{max_customer_rating:1f}', border=True)
    col3.metric("Avg Booking Value", f'{avg_booking_price:2f}', border=True)
    col4.metric("# Vehicle Types", vehicle_types, border=True)


col1, col2 = st.columns(2)
with col1: 
    with st.container(border=True):
        
        df['customer_rating'] = pd.to_numeric(df['customer_rating'])
        avg_by_type = (
            df.groupby(['vehicle_type'], as_index=False)['customer_rating']
            .mean()
            .rename(columns={'customer_rating': 'avg_rating'})
            .sort_values('avg_rating', ascending = True)
        )


        st.bar_chart(
            avg_by_type,
            x = 'vehicle_type',
            y= 'avg_rating'
        )   
       

    with col2:
        with st.container(border=True):
            # Ensure "date" is datetime
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            # Count bookings per day
            bookings_over_time = (
                df.groupby(df["date"].dt.date)["booking_id"]
                .count()
                .reset_index(name="bookings")
            )

            # Plot line chart
            st.line_chart(
                bookings_over_time,
                x="date",
                y="bookings"
            )

col1, col2 = st.columns(2)
with col1: 
    tab1, tab2 = st.tabs(["Customer", "Driver"])


    with tab1:
        with st.container():
            st.table(
                pd.DataFrame(df['reason_for_cancelling_by_customer'].unique(),
                columns=['Cancellation Reason by Customer']
            ))
    with tab2:
        with st.container():
            st.table(
                pd.DataFrame(df['driver_cancellation_reason'].unique(),
                columns=['Cancellation Reason by Driver']
            ))

with col2:
        with st.container(border = True):
            st.bar_chart(df, x="vehicle_type", y="cancelled_rides_by_customer", color="reason_for_cancelling_by_customer", horizontal=True)



col1, col2 = st.columns(2)

top10 = df.nlargest(1000, "booking_value")   # by largest values

with col1:
    with st.container(border=True):
        st.scatter_chart(
        top10,
        x="booking_value",
        y="ride_distance",
        color = 'customer_rating'
)

with col2: 
    with st.container(border=True):
        df["cutomer_rating"] = pd.to_numeric(df['customer_rating'])
        avg_by_payment = (
        df.groupby(['payment_method'], as_index=False)['customer_rating']
        .count()
        .rename(columns={'customer_rating': 'count_customer_rating'})
        .sort_values('count_customer_rating', ascending = True)
        )
        st.bar_chart(
        avg_by_payment,
        x="payment_method",
        y=["count_customer_rating"]
)

filtered = df.copy()
chart_kind = st.selectbox("Chart type", ["Bar", "Line"])
grouped = (
    filtered.groupby("vehicle_type", as_index=False)["booking_value"].count().rename(columns={"booking_value":"avg_value"})
)
if chart_kind == "Bar":
    st.bar_chart(grouped, x="vehicle_type", y="avg_value")
else:
    st.line_chart(grouped, x="vehicle_type", y="avg_value")



bins = st.slider("Bins for booking value", 5, 100, 30)
hist = alt.Chart(filtered).mark_bar().encode(
    x=alt.X("booking_value:Q", bin=alt.Bin(maxbins=bins)),
    y="count()"
)
st.altair_chart(hist, use_container_width=True)


