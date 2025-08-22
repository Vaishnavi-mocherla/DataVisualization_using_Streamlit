
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from numpy.random import default_rng as rng
from datetime import datetime, date
from datetime import time


st.set_page_config(
    page_title="Hackathon Starter",
    layout="wide",
    initial_sidebar_state="expanded",
)

#############################
# Write 
#############################

st.write("Heloo *World* :sunglasses:")

#############################
# Calling it with df 
#############################

df = pd.DataFrame(
    {
        "first_column" : [1,2,3,4],
        "second_column" : [10,20,30,40]
    }
)
st.write('below is the dataframe',df)

#############################
# Headings and text
#############################

st.title ('Main Title')
st.header("Header Example")
st.subheader("Subheader Example")
st.text("This is plain text")
st.markdown("**Bold Text** | _Italic Text_ | [Link](https://streamlit.io)")
st.code("print('Hello Streamlit!')", language="python")                     

#############################
# DataElemnets --> DataColumn --> Part 1 
#############################

df = pd.DataFrame(
    {
        'Avator': ['https://randomuser.me/api/por', 'https://randomuser.me/api/por', 'https://randomuser.me/api/por'],
        'name': ['Madison Obrien', 'Aiden Smith', 'Emma Johnson'],
        'age' : [30, 25, 30],
        'Is_Active': [True, False, True],
        'ListActivity' :  rng(0).integers(0, 5000, size=(3, 30)).tolist(), 
        'Activity' :  rng(0).integers(0, 5000, size=(3, 30)).tolist(), 
        'Homepage': ['https://www.streamlit.io', 'https://www.streamlit.io', 'https://www.streamlit.io'],
        'Appointment_Date': [
            datetime(2025, 1, 15, 10, 30), # (yera, month, day, hour, minute)
            datetime(2025, 2, 20, 14, 0),
            datetime(2025, 3, 5, 9, 15) 
        ] ,
        'birthday' : [
            date(1999, 5, 29) , # (year, month, day)
            date(2000, 8, 15),
            date(1995, 12, 1)
        ] ,
        'my_Time':  [
            time(9, 10), 
            time(12, 30), 
            time(15, 45)] # (hour, minute)
    }
)
st.data_editor(
    df, 
    column_config={
        'Avator': st.column_config.ImageColumn('Avator'),  # Image 

        'name': st.column_config.TextColumn('Name of the person'), # Text Column

        'age': st.column_config.NumberColumn( # Number Column
            'age',
            help="person's age in years",
            format='%d years',
        ),

        'Is_Active': st.column_config.CheckboxColumn('Is Active'), # Checkbox Column

        'ListActivity' : st.column_config.ListColumn(
            'List Activity'
        ),

        'Activity': st.column_config.LineChartColumn(   # Line Chart Column
            'Activity(Daily)',
            help='Daily activity of the person',
            y_max=5000,
            y_min=0,
        ),

        'Homepage': st.column_config.LinkColumn(
            "Homepage URL",
             display_text="Open profile"), # URL/Link Column

        'Appointment_Date' : st.column_config.DatetimeColumn(   # Datetime Column
            'appointment date',
            format = "D MMM YYYY, h:mm a",
            step = 60, # step in seconds
        ),

        'birthday': st.column_config.DateColumn( # Date Column
            'Birthday'
        ), 

        'my_Time':  st.column_config.TimeColumn(
            'Just Time'
        ),
    },
     disabled=["name", "age"], # The editor will give access to edit any column but the disable allow you to disable mentioned columns
    hide_index=True, # removes the index column that is shown by default
)

#############################
# DataElemnets --> DataColumn --> Part 2 
#############################

data_df = pd.DataFrame(
    {
        "sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
        "bar_chart_sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
        "progress_sales": [200, 550, 1000, 80],

    }
)

st.data_editor(
    data_df,
    column_config={

        "sales": st.column_config.AreaChartColumn( # Area Chart Column
            "Sales (last 6 months)",
            width="medium",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
         ),

         "bar_chart_sales": st.column_config.BarChartColumn( # Bar Chart Column
             "Bar Chart" 
            "Sales (last 6 months)",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,),

        "progress_sales": st.column_config.ProgressColumn( # Progress Column
            "Sales volume",
            help="The sales volume in USD",
            format="$%d",
            min_value=0,
            max_value=1000,
        ),
    },
    hide_index=True,
)

#############################
# Metrix 
#############################

st.metric(label='Temperature', value = '20 °C', delta='1 °C')

#col 
col1, col2, col3 = st.columns(3)
col1.metric(label='Temperature', value = '20 °C', delta='1 °C', border=True)
col2.metric(label='Humidity', value = '60 %', delta='-5 %', border=True)
col3.metric(label='Pressure', value = '1013 hPa', delta='2 hPa', border=True)

col4, col5, col6 = st.columns(3)
col1.metric(label='Temperature', value = '20 °C', delta='1 °C', border=True)
col2.metric(label='Humidity', value = '60 %', delta='-5 %', border=True)
col3.metric(label='Pressure', value = '1013 hPa', delta='2 hPa', border=True)