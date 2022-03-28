import streamlit as st
import pandas as pd

df = pd.read_csv("data_for_first_two_cards.csv")

st.title("Welcome!")
st.header("Are you going to play Texas Hold'em Poker?")
