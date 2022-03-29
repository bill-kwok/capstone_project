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

st.header("Welcome for using this calculator for Texas Hold'em Poker!")
st.text("")

with st.sidebar:
  table = st.checkbox("Table")
  dp = st.slider("Number of decimal places", 1, 6, 2)
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
  game = st.button("Start a new game")  
  if game:
    remaining_deck = deck.copy()
    my_cards = set({})
    community = set({})
    card_on_hands = ''
    flop = ''
    turn = ''
    river = ''
  
  with st.form('selection1', clear_on_submit = True):
    selection1 = st.multiselect("Which 2 cards have you got:", remaining_deck)
    enter1 = st.form_submit_button("Confirm the 2 cards")
    if enter1:
      card_on_hands = selection1
    st.text(card_on_hands)
      
  with st.form('selection2', clear_on_submit = True):
    selection2 = st.multiselect("The flop: first 3 community cards", remaining_deck)
    enter2 = st.form_submit_button("Confirm the first 3 community cards")
    if enter2:
      flop = selection2
    st.text(flop)
  
  with st.form('selection3', clear_on_submit = True):
    selection3 = st.selectbox("The turn: 4th community card", remaining_deck)
    enter3 = st.form_submit_button("Confirm the 4th community card")
    if enter3:
      turn = selection3
    st.text(turn)
  
  with st.form('selection4', clear_on_submit = True):
    selection4 = st.selectbox("The river: 5th community card", remaining_deck)
    enter4 = st.form_submit_button("Confirm the 5th community card")
    if enter4:
      river = selection4
    st.text(river)
      
with col2:
  if table:
    df
  

