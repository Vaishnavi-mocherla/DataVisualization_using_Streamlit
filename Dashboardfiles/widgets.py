import streamlit as st  
import pandas as pd

st.write(" ## I/p Widgets")

# Button widget

st.button('Click!', type = 'primary')
if st.button("Say hello!"):
    st.write("Hello!")
else:
    st.write("Goodbye!")

#Click and display
if st.button('Click!', type = 'tertiary'):
    st.write("This is a tertiary button.")



st.balloons()



st.snow()