import streamlit as st
import pandas as pd

df = pd.read_csv("data_for_first_two_cards.csv")

st.header("Welcome!")
st.subheader("Are you going to play Texas Hold'em Poker?")

with st.sidebar:
  table = st.checkbox("Table")
  
  
col1, col2 = st.columns(2)
with col1:
  game = st.button("Start a new game")

with col2:
  if table:
    df
