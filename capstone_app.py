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
st.text("")

with st.sidebar:
  table = st.checkbox("Table")
  st.title("")
  st.title("")
  bar = st.checkbox("Bar chart")
  bar_size = st.slider("Size of bar chart", 1, 10, 5)
  st.title("")
  st.title("")
  pie = st.checkbox("Pie chart")
  pie_size = st.slider("Size of pie chart", 1, 10, 5)

col1, col2 = st.columns([1,3])
with col1:
  remaining_deck = deck.copy()
  my_cards = set({})
  community = set({})
  with st.form(selection1, clear_on_submit=True):
    selection1 = st.multiselect("Which 2 cards have you got:", remaining_deck)
  enter1 = st.button("Confirm the 2 cards")
  if enter1:
    a = 1
  
  st.text("")
  selection2 = st.multiselect("The flop: first 3 community cards", remaining_deck)
  enter2 = st.button("Confirm the first 3 community cards")
  
  st.text("")
  selection3 = st.selectbox("The turn: 4th community card", remaining_deck)
  enter3 = st.button("Confirm the 4th community card")
  
  st.text("")
  selection4 = st.selectbox("The river: 5th community card", remaining_deck)
  enter4 = st.button("Confirm the 5th community card")
  
  
  game = st.form_submit_button("Start a new game")  
  if game:
    remaining_deck = deck.copy()
    my_cards = set({})
    community = set({})
    
with col2:
  if table:
    df
