import streamlit as st
import pandas as pd

df = pd.read_csv("data_for_first_two_cards.csv")

st.title("Welcome to Texas Hold'em Poker")
df
