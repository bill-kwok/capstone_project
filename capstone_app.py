import streamlit as st
import pandas as pd

def num_to_card(num):
  suit_dict = {0:'Spade', 1:'Heart', 2:'Club', 3:'Diamond'}
  rank_dict = {1:'A', 11:'J', 12:'Q', 13:'K'}
  suit = suit_dict[num // 13]
  rank = num % 13 + 1
  if (rank == 1) | (rank > 10):
    rank = rank_dict[rank]
  return suit + ' ' + str(rank)

df = pd.read_csv("data_for_first_two_cards.csv")
deck = [num_to_card(i) for i in range(52)]

st.header("Welcome!")
st.subheader("Are you going to play Texas Hold'em Poker?")

with st.sidebar:
  table = st.checkbox("Table")

col1, col2 = st.columns(3)
with col1:
  game = st.button("Start a new game")
  if game:
     remaining_deck = deck.copy()
     my_cards = set({})
     community = set({})
     first_selection = st.multiselect("Which two cards do you get:": remaining_deck)
     enter1 = st.button("Confirm")

with col2:
  if table:
    df
