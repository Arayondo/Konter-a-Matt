from random import randint, shuffle, choice
import json, pprint
import sys, time
from localisation import *

class Player:
	def __init__(self, name, team, place):
		self.name = name
		self.hand = {}
		self.streech = []
		self.score = 0
		self.last_played_card = ""
		self.team = team
		self.place = place
	def __repr__(self):
		return self.name
	def debug_all(self):
		return self.name, self.hand, self.streech, self.score, self.last_played_card, self.team, self.place

	def choose_card(self, stack, trump):
		first_played = stack['first_played']
		Deck_k = [k9,k10,kB,kD,kK]
		Deck_r = [r9,r10,rB,rK]
		Deck_s = [s9,s10,sB,sK]
		Deck_h = [h9,h10,hB,hK]

		card = choice(list(self.hand.keys()))
		return card
	def make_trump(self):
		return ["k","r","s","h"][randint(0,3)]



class NPC(Player):
	def __init__(self, name, team, place):
		super(NPC, self).__init__(name, team, place)
	def __repr__(self):
		return self.name
