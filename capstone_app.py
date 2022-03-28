import streamlit as st
import pandas as pd

df = pd.read_csv("data_for_first_two_cards.csv")

st.header("Welcome!")
st.subheader("Are you going to play Texas Hold'em Poker?")
placeholder = st.empty()

# Replace the placeholder with some text:
placeholder.text("Hello")

# Replace the text with a chart:
placeholder.line_chart({"data": [1, 5, 2, 6]})

# Replace the chart with several elements:
with placeholder.container():
     st.write("This is one element")
     st.write("This is another")

# Clear all those elements:
placeholder.empty()

with st.sidebar:
  table = st.checkbox("Table")
  
  
col1, col2, col3 = st.columns(3)
with col1:
  game = st.button("Start a new game")

with col2:
  if table:
    df
with col3:
  st.text("test")
