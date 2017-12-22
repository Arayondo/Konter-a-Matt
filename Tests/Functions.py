#### Functions ####
from classes import Player
from localisation import *
from random import randint, shuffle
import json


def save(opts):
	f = open('options.py', mode='w', encoding='utf-8')
	json.dump(opts, f, indent=2)
	f.close()

def load():
	f = open('options.py', mode='r', encoding='utf-8')
	options = json.load(f)
	f.close()
	return options

def init_players():
	options = load()
	Plr1 = Player(options['Player1'],1, 'bottom_player_')
	Plr2 = Player(options['Player2'],2, 'left_player_')
	Plr3 = Player(options['Player3'],1, 'top_player_')
	Plr4 = Player(options['Player4'],2, 'right_player_')
	All_Players = [Plr1, Plr2, Plr3, Plr4]
	return Plr1, Plr2, Plr3, Plr4, All_Players

def init_MA_cards():
	MA_cards = {}
	Deck_Sort = [k9,k10,kB,kD,kK,kA,r9,r10,rB,rD,rK,rA,s9,s10,sB,sD,sK,sA,h9,h10,hB,hD,hK,hA]
	Deck = [k9,k10,kB,kD,kK,kA,r9,r10,rB,rD,rK,rA,s9,s10,sB,sD,sK,sA,h9,h10,hB,hD,hK,hA]
	for card in Deck_Sort:
		MA_cards[card] = {'Owner':"", 'Value':0, 'Priority':0, 'Trump_Card':False, 'played':False, 'stack_num':0}
	cardnum = 1
	while cardnum<5:
		MA_cards[Deck_Sort[cardnum+1]]['Value'] = cardnum
		MA_cards[Deck_Sort[cardnum+7]]['Value'] = cardnum
		MA_cards[Deck_Sort[cardnum+13]]['Value'] = cardnum
		MA_cards[Deck_Sort[cardnum+19]]['Value'] = cardnum
		cardnum += 1
	MA_cards[sD]['Trump_Card'] = True
	MA_cards[hD]['Trump_Card'] = True
	MA_cards[rD]['Trump_Card'] = True
	MA_cards[sD]['Priority'] = 900
	MA_cards[hD]['Priority'] = 800
	MA_cards[rD]['Priority'] = 700

	MA_cards[k9]['Image'] = 'Images/k9.jpg'
	MA_cards[k10]['Image'] = 'Images/k10.jpg'
	MA_cards[kB]['Image'] = 'Images/kB.jpg'
	MA_cards[kD]['Image'] = 'Images/kD.jpg'
	MA_cards[kK]['Image'] = 'Images/kK.jpg'
	MA_cards[kA]['Image'] = 'Images/kA.jpg'
	MA_cards[r9]['Image'] = 'Images/r9.jpg'
	MA_cards[r10]['Image'] = 'Images/r10.jpg'
	MA_cards[rB]['Image'] = 'Images/rB.jpg'
	MA_cards[rD]['Image'] = 'Images/rD.jpg'
	MA_cards[rK]['Image'] = 'Images/rK.jpg'
	MA_cards[rA]['Image'] = 'Images/rA.jpg'
	MA_cards[s9]['Image'] = 'Images/s9.jpg'
	MA_cards[s10]['Image'] = 'Images/s10.jpg'
	MA_cards[sB]['Image'] = 'Images/sB.jpg'
	MA_cards[sD]['Image'] = 'Images/sD.jpg'
	MA_cards[sK]['Image'] = 'Images/sK.jpg'
	MA_cards[sA]['Image'] = 'Images/sA.jpg'
	MA_cards[h9]['Image'] = 'Images/h9.jpg'
	MA_cards[h10]['Image'] = 'Images/h10.jpg'
	MA_cards[hB]['Image'] = 'Images/hB.jpg'
	MA_cards[hD]['Image'] = 'Images/hD.jpg'
	MA_cards[hK]['Image'] = 'Images/hK.jpg'
	MA_cards[hA]['Image'] = 'Images/hA.jpg'

	rev_MA_cards = {}
	for card in MA_cards:
		rev_MA_cards[MA_cards[card]['Image']] = card
	return Deck, MA_cards, rev_MA_cards

def init_stack():
	stack = {'bottom_player_0': '', 'top_player_0': '', 'left_player_0': '', 'right_player_0': '', 'first_played': ''}
	return stack

def shuffle_deal3(Trumper, Deck, MA_cards):
	Rest_Deck = list(Deck)
	shuffle(Rest_Deck)
	for i in range(3):
		MA_cards[Rest_Deck[0]]['Owner'] = Trumper
		Trumper.hand[Trumper.place+str(i+1)] = Rest_Deck.pop(0)
	return Rest_Deck

def set_first_dealer(All_Players):
	return All_Players[randint(0,3)]

def set_trumper(All_Players, Dealer):
	n = All_Players.index(Dealer)+1
	if n == 4:
		n = 0
	return All_Players[n]

def assign_prio_trump(trump, MA_cards):
	if trump == "k":
		MA_cards[kA]['Trump_Card'] = True
		MA_cards[kA]['Priority'] += 1000
		MA_cards[k9]['Trump_Card'] = True
		MA_cards[k9]['Priority'] += 100
		MA_cards[k10]['Trump_Card'] = True
		MA_cards[k10]['Priority'] += 100
		MA_cards[kB]['Trump_Card'] = True
		MA_cards[kB]['Priority'] += 100
		MA_cards[kD]['Trump_Card'] = True
		MA_cards[kD]['Priority'] += 100
		MA_cards[kK]['Trump_Card'] = True
		MA_cards[kK]['Priority'] += 100
	elif trump == "r":
		MA_cards[rA]['Trump_Card'] = True
		MA_cards[rA]['Priority'] += 1000
		MA_cards[r9]['Trump_Card'] = True
		MA_cards[r9]['Priority'] += 100
		MA_cards[r10]['Trump_Card'] = True
		MA_cards[r10]['Priority'] += 100
		MA_cards[rB]['Trump_Card'] = True
		MA_cards[rB]['Priority'] += 100
		MA_cards[rK]['Trump_Card'] = True
		MA_cards[rK]['Priority'] += 100
	elif trump == "s":
		MA_cards[sA]['Trump_Card'] = True
		MA_cards[sA]['Priority'] += 1000
		MA_cards[s9]['Trump_Card'] = True
		MA_cards[s9]['Priority'] += 100
		MA_cards[s10]['Trump_Card'] = True
		MA_cards[s10]['Priority'] += 100
		MA_cards[sB]['Trump_Card'] = True
		MA_cards[sB]['Priority'] += 100
		MA_cards[sK]['Trump_Card'] = True
		MA_cards[sK]['Priority'] += 100
	elif trump == "h":
		MA_cards[hA]['Trump_Card'] = True
		MA_cards[hA]['Priority'] += 1000
		MA_cards[h9]['Trump_Card'] = True
		MA_cards[h9]['Priority'] += 100
		MA_cards[h10]['Trump_Card'] = True
		MA_cards[h10]['Priority'] += 100
		MA_cards[hB]['Trump_Card'] = True
		MA_cards[hB]['Priority'] += 100
		MA_cards[hK]['Trump_Card'] = True
		MA_cards[hK]['Priority'] += 100
	w = 0
	w2 = 5
	Deck_Sort = [k9,k10,kB,kD,kK,kA,r9,r10,rB,rD,rK,rA,s9,s10,sB,sD,sK,sA,h9,h10,hB,hD,hK,hA]
	while w<6:
		MA_cards[Deck_Sort[w]]['Priority'] += w+w2
		MA_cards[Deck_Sort[w+6]]['Priority'] += w+w2
		MA_cards[Deck_Sort[w+12]]['Priority'] += w+w2
		MA_cards[Deck_Sort[w+18]]['Priority'] += w+w2
		w2 += 4
		w += 1

def deal_rest_cards(All_Players, Trumper, Rest_Cards, MA_cards):
	n = All_Players.index(Trumper) + 1
	for i in range(3):
		if n == 4:
			n = 0
		for t in range(1,4):
			MA_cards[Rest_Cards[0]]['Owner'] = All_Players[n]
			All_Players[n].hand[All_Players[n].place+str(t)] = Rest_Cards.pop(0)
		n += 1
	for i in range(4):
		if n == 4:
			n = 0
		for t in range(4,7):
			MA_cards[Rest_Cards[0]]['Owner'] = All_Players[n]
			All_Players[n].hand[All_Players[n].place+str(t)] = Rest_Cards.pop(0)
		n += 1


def reset_prio_trump(trump, MA_cards):
	Deck_k = [k9,k10,kB,kD,kK]
	Deck_r = [r9,r10,rB,rK]
	Deck_s = [s9,s10,sB,sK]
	Deck_h = [h9,h10,hB,hK]
	if trump == "k":
		for card in Deck_k:
			MA_cards[card]['Trump_Card'] = False
			MA_cards[card]['Priority'] -= 100
		MA_cards[kA]['Trump_Card'] = False
		MA_cards[kA]['Priority'] -= 1000
	elif trump == "r":
		for card in Deck_r:
			MA_cards[card]['Trump_Card'] = False
			MA_cards[card]['Priority'] -= 100
		MA_cards[rA]['Trump_Card'] = False
		MA_cards[rA]['Priority'] -= 1000
	elif trump == "s":
		for card in Deck_s:
			MA_cards[card]['Trump_Card'] = False
			MA_cards[card]['Priority'] -= 100
		MA_cards[sA]['Trump_Card'] = False
		MA_cards[sA]['Priority'] -= 1000
	elif trump == "h":
		for card in Deck_h:
			MA_cards[card]['Trump_Card'] = False
			MA_cards[card]['Priority'] -= 100
		MA_cards[hA]['Trump_Card'] = False
		MA_cards[hA]['Priority'] -= 1000
	w = 0
	w2 = 5
	Deck_Sort = [k9,k10,kB,kD,kK,kA,r9,r10,rB,rD,rK,rA,s9,s10,sB,sD,sK,sA,h9,h10,hB,hD,hK,hA]
	while w<6:
		MA_cards[Deck_Sort[w]]['Priority'] -= w+w2
		MA_cards[Deck_Sort[w+6]]['Priority'] -= w+w2
		MA_cards[Deck_Sort[w+12]]['Priority'] -= w+w2
		MA_cards[Deck_Sort[w+18]]['Priority'] -= w+w2
		w2 += 4
		w += 1

def determine_Ronn_winner(stack, MA_cards):
	first_played = stack['first_played']
	Deck_k = [k9,k10,kB,kD,kK,kA]
	Deck_r = [r9,r10,rB,rK,rA]
	Deck_s = [s9,s10,sB,sK,sA]
	Deck_h = [h9,h10,hB,hK,hA]
	if first_played in Deck_k:
		for card in Deck_k:
			MA_cards[card]['Priority'] += 50
	elif first_played in Deck_r:
		for card in Deck_r:
			MA_cards[card]['Priority'] += 50
	elif first_played in Deck_s:
		for card in Deck_s:
			MA_cards[card]['Priority'] += 50
	elif first_played in Deck_h:
		for card in Deck_h:
			MA_cards[card]['Priority'] += 50
	liste2 = []
	liste3 = []
	for i in stack:
		liste2.append(MA_cards[stack[i]]['Owner'])
		liste3.append(MA_cards[stack[i]]['Priority'])
	highest_prio_index = liste3.index(max(liste3))
	winner = liste2[highest_prio_index]
	if first_played in Deck_k:
		for card in Deck_k:
			MA_cards[card]['Priority'] -= 50
	elif first_played in Deck_r:
		for card in Deck_r:
			MA_cards[card]['Priority'] -= 50
	elif first_played in Deck_s:
		for card in Deck_s:
			MA_cards[card]['Priority'] -= 50
	elif first_played in Deck_h:
		for card in Deck_h:
			MA_cards[card]['Priority'] -= 50
	return winner

def determine_Tour_winner(All_Players, MA_cards):
	for player in All_Players:
		for card in player.streech:
			player.score += MA_cards[card]['Value']
	print(All_Players[0].score + All_Players[2].score)
	print(All_Players[1].score + All_Players[3].score)
	if All_Players[0].score + All_Players[2].score > 20:
		return All_Players[0], All_Players[2]
	else:
		return All_Players[1], All_Players[3]

def update_trumper(Trumper, All_Players):
	new_trumper = All_Players.index(Trumper)+1
	if new_trumper == 4:
		new_trumper = 0
	return All_Players[new_trumper]

def reset_streech(All_Players, MA_cards):
	for player in All_Players:
		player.streech = []
		player.score = 0
		player.last_played_card = ''
		for card in player.hand:
			MA_cards[card]['Owner'] = ""
