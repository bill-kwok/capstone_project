#-------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from itertools import combinations
#-------------------------------------------------------------------------
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
deck = {i for i in range(52)}
remaining_deck = deck.copy()
my_cards, community = set({}), set({})
df = pd.read_csv("data_for_first_two_cards.csv")
first_col = ["Sample"]
sec_col = [1]
#-------------------------------------------------------------------------
def num_to_card(num):
  suit_dict = {0:'Spade', 1:'Heart', 2:'Club', 3:'Diamond'}
  rank_dict = {1:'A', 11:'J', 12:'Q', 13:'K'}
  suit = suit_dict[num // 13]
  rank = num % 13 + 1
  if (rank == 1) | (rank > 10):
    rank = rank_dict[rank]
  return suit + ' ' + str(rank)

def card_to_num(string):
  suit_dict = {'Spade':0, 'Heart':1, 'Club':2, 'Diamond':3}
  rank_dict = {'A':0, 'J':10, 'Q':11, 'K':12}
  suit_no = int(suit_dict[string.split(" ")[0]])
  rank = string.split(" ")[1]
  if rank.isalpha():
    rank_no = int(rank_dict[rank])
  else:
    rank_no = int(rank)-1
  return 13 * suit_no + rank_no
#-------------------------------------------------------------------------
hand_dict = {0:'High card', 1:'One pair', 2:'Two pairs',
             3:'Three of a kind', 4:'Straight', 5:'Flush',
             6:'Full House', 7:'Four of a kind', 8:'Straight flush', 
             9:'Royal flush'}

hand_list = [hand_dict[9 - i] for i in hand_dict]

def same_rank(list_of_nums):
  result = 0 # High card
  rank = [x % 13 for x in list_of_nums]
  rank_count = [rank.count(i) for i in range(13)]
  if rank_count.count(2) == 1:
    result = 1 # One pair
  if rank_count.count(2) >= 2:
    result = 2 # Two pairs
  if rank_count.count(3) >= 1:
    result = 3 # Three of a kind
    if (rank_count.count(3) >= 2) | ((rank_count.count(3) == 1) & (rank_count.count(2) >= 1)):
      result = 6 # Full house
  if rank_count.count(4) >= 1:
    result = 7 # Four of a kind
  return result

def flush(list_of_nums):
  result = 0 # High card
  suit = [x // 13 for x in list_of_nums]
  for i in range(4):
    if suit.count(i) >= 5:
      result = 5 # Flush
  return result

def five_consecutive(list_of_nums):
  consecutive = False
  rank = sorted([x % 13 for x in list_of_nums])
  diff = [rank[i+1] - rank[i] for i in range(len(rank)-1)]
  if diff.count(1) >= 4:
    consecutive = 'Normal'
  if (0 in rank) & (12 in rank) & (11 in rank) & (10 in rank) & (9 in rank): # 10JQKA
    consecutive = 'Royal'  
  return consecutive

def straight(list_of_nums):
  result = 0 # High card
  consecutive = five_consecutive(list_of_nums)
  if consecutive != False:
    result = 4 # Straight
    spade = [x for x in list_of_nums if x < 13]
    heart = [x for x in list_of_nums if x in range(13,26)]
    club = [x for x in list_of_nums if x in range(26,39)]
    diamond = [x for x in list_of_nums if x >= 39]
    consecutive2 = 0
    if len(spade) >= 5:
      consecutive2 = five_consecutive(spade)     
    if len(heart) >= 5:
      consecutive2 = five_consecutive(heart)
    if len(club) >= 5:
      consecutive2 = five_consecutive(club)
    if len(diamond) >= 5:
      consecutive2 = five_consecutive(diamond)
    if consecutive2 == 'Normal':
      result = 8 # Straight flush
    elif consecutive2 == 'Royal':
      result = 9 # Royal flush
  return result

def get_hand(list_of_nums):
  return max([same_rank(list_of_nums), flush(list_of_nums), straight(list_of_nums)])
#-----------------------------------------------------------------------------------------------------------
def two_cards_name(card1, card2):
  if card1 % 13 == card2 % 13:
    start = 'pair:'
    end = num_to_card(card1).split(' ')[1]
  else:
    big = max([card1 % 13, card2 % 13])
    small = min([card1 % 13, card2 % 13])
    two_cards = num_to_card(small) +' '+ num_to_card(big)
    end = ' '.join(two_cards.split(' ')[1::2])
    if card1 // 13 == card2 // 13:
      start = 'same suit:'
    else:
      start = 'other:'        
  return start + ' ' + end
  
def first_two(card1, card2):
  remaining_deck.difference_update({card1, card2})
  my_cards.update({card1, card2})
  comb_name = two_cards_name(card1, card2)
  filter = df.first_two_cards == comb_name
  rank_rate = np.array(df[filter])[0][1:]
  return rank_rate

def second_flop(card1, card2, card3):
  remaining_deck.difference_update({card1, card2, card3})
  community.update({card1, card2, card3})
  all_possibility = combinations(remaining_deck, 2)
  rank_rate = [0 for i in range(10)]  #From Royal flush to high card
  for two_cards in all_possibility:
    possible_cards = my_cards.union(community)
    possible_cards.update(set(two_cards))
    hand_rank = get_hand(list(possible_cards))
    rank_rate[9-hand_rank] += 1
  total = sum(rank_rate)
  rank_rate = [i/total for i in rank_rate]      
  return rank_rate

def third_turn(card):
  remaining_deck.remove(card)
  community.add(card)

  rank_rate = [0 for i in range(10)]  #From Royal flush to high card
  for one_card in remaining_deck:
    possible_cards = my_cards.union(community)
    possible_cards.add(one_card)
    hand_rank = get_hand(list(possible_cards))
    rank_rate[9-hand_rank] += 1
  total = sum(rank_rate)
  rank_rate = [i/total for i in rank_rate]     
  return rank_rate

def forth_river(card):
  remaining_deck.remove(card)
  community.add(card)
  my_rank = get_hand(list(my_cards.union(community)))
  win_rate = [0 for i in range(3)]  # win, draw, lose

  all_possibility = combinations(remaining_deck, 2)
  for two_cards in all_possibility:
    possible_cards = set(two_cards).union(community)
    hand_rank = get_hand(list(possible_cards))
    if my_rank > hand_rank:
      win_rate[0] += 1
    elif my_rank == hand_rank:
      win_rate[1] += 1
    else:
      win_rate[2] += 1

  total = sum(win_rate)
  win_rate = [i/total for i in win_rate]
  return my_rank, win_rate
#--------------------------------------------------------------------------------------------
st.set_page_config(layout = "wide")
st.subheader("Texas Hold’em Poker Calculator 1.0")
st.subheader("Welcome and Good Luck!")
st.text("")
game = st.button("Start a new game")
if game:
  st.write("The new game will start automatically once you untick all of the options below.")
  st.write("Unfortunately, Streamlit does not allow me to untick for you at this moment.")
  
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

col1, col2, col3, col4 = st.columns([5,5, bar_size, pie_size])

with col1:  
  hand_cards = st.multiselect("Which 2 cards have you got:", [num_to_card(i) for i in remaining_deck])
  enter1 = st.checkbox("Confirm the 2 cards")
  if enter1:
    if len(hand_cards) != 2:
      st.error("You should have 2 cards.")
      st.stop()
    else:
      first_col = hand_list
      sec_col = first_two(card_to_num(hand_cards[0]), card_to_num(hand_cards[1]))
         
  flop = st.multiselect("The flop: first 3 community cards", [num_to_card(i) for i in remaining_deck])
  enter2 = st.checkbox("Confirm the first 3 community cards")
  if enter2:
    if enter1 == False:
      st.error("You have to confirm the 2 cards you get first.")
      st.stop()      
    elif len(flop) != 3:
      st.error("There should be 3 cards.")
      st.stop()
    else:
      first_col = hand_list
      sec_col = second_flop(card_to_num(flop[0]), card_to_num(flop[1]), card_to_num(flop[2]))                    

  turn = st.selectbox("The turn: 4th community card", [num_to_card(i) for i in remaining_deck])
  enter3 = st.checkbox("Confirm the 4th community card")
  if enter3:
    if enter2 == False:
      st.error("You have to confirm the first 3 community cards first.")
      st.stop()      
    else:
      first_col = hand_list
      sec_col = third_turn(card_to_num(turn))

  river = st.selectbox("The river: 5th community card", [num_to_card(i) for i in remaining_deck])
  enter4 = st.checkbox("Confirm the 5th community card")
  if enter4:
    if enter3 == False:
      st.error("You have to confirm the forth community card first.")
      st.stop()      
    else:
      first_col = ['Winning hand rate', 'Drawing hand rate', 'Losing hand rate']
      my_hand, sec_col = forth_river(card_to_num(river))
      st.write('I have "{}".'.format(hand_dict[my_hand]))
      st.write('Note that the table is for 2 players (including you) only, and drawing hand does not mean drawing game.')
             
with col2:
  if table:
    prob = [str(round(i*100, dp)) + ' %' for i in sec_col]
    show_table = pd.DataFrame({'':first_col, 'probability':prob})
    show_table

with col3:
  if bar:
    show_bar = plt.figure(figsize = (bar_size/2, bar_size/2))
    plt.rc('font', size = bar_size + 2)
    sns.barplot(x = first_col, y = sec_col)
    plt.xticks(rotation = 45, horizontalalignment = 'right')
    st.pyplot(show_bar)  

with col4:
  if pie:
    show_pie = plt.figure(figsize = (pie_size/2, pie_size/2))
    plt.rc('font', size = pie_size + 2)
    palette = sns.color_palette('colorblind')
    plt.pie(sec_col, labels = first_col, colors = palette, autopct='%.{}f%%'.format(dp))
    st.pyplot(show_pie)

