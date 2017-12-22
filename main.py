###   Versioning
__version__ = "17.12.21.1"

###   Modules
from functions			import *
from classes			import Player
from localisation		import *

###   Imports
from random				import randint, shuffle, choice
from time				import sleep
from functools			import partial
import json, pprint
pp = pprint.PrettyPrinter(indent=4)



###   kivy Imports
import kivy
kivy.require('1.10.0')
from kivy.app							import App
from kivy.uix.label						import Label			# uix holds UI Elements like layouts/widgets
from kivy.uix.gridlayout				import GridLayout		# for our Root Widget LoginScreen
from kivy.uix.textinput					import TextInput
from kivy.uix.button					import Button
from kivy.uix.scatter					import Scatter			# handles touch response (resize, move, rotate with fingers)
from kivy.uix.floatlayout				import FloatLayout
from kivy.uix.boxlayout					import BoxLayout
from kivy.properties					import ListProperty, StringProperty
from kivy.graphics.vertex_instructions	import Rectangle, Ellipse, Line
from kivy.graphics.context_instructions	import Color, PopMatrix, PushMatrix
from kivy.uix.scrollview				import ScrollView
from kivy.uix.screenmanager				import ScreenManager, Screen
from kivy.base							import runTouchApp
from kivy.lang							import Builder
from kivy.config						import Config
from kivy.uix.image						import Image
from kivy.uix.behaviors					import ButtonBehavior
from kivy.uix.popup						import Popup
from kivy.graphics						import Rotate

#####   MAIN
class main(App):
	Settings = load()
	def build(self):
		return MyScreenManager()

class MyScreenManager(ScreenManager):
	pass

class MainMenu(Screen):
	pass

class Options(Screen):
	def save_o(self):
		main.Settings['Player1'] = self.ids.PlayerName.text
		main.Settings['Player2'] = self.ids['Player1'].text
		main.Settings['Player3'] = self.ids['Player2'].text
		main.Settings['Player4'] = self.ids['Player3'].text
		main.Settings['Score']   = self.ids.score.text
		save(main.Settings)

#####   GAME
score_them, score_us, Plr1, Plr2, Plr3, Plr4, All_Players, Deck, MA_cards, rev_MA_cards, Dealer, Trumper, Auskommer, stack, Ronn, ready, trump

class Game(Screen):

	def on_pre_enter(self):
		print("HEY")
		score_them = int(main.Settings['Score'])
		score_us = int(main.Settings['Score'])
		Plr1, Plr2, Plr3, Plr4, All_Players = init_players()
		Deck, MA_cards, rev_MA_cards = init_MA_cards()
		Dealer = set_first_dealer(All_Players)
		Trumper = set_trumper(All_Players, Dealer)
		Auskommer = Trumper
		stack = init_stack()
		Ronn = 1
		trump = ''
		ready = False

		self.ids.score_them.text = 'Them: ' + main.Settings['Score']
		self.ids.score_us.text = 'Us: ' + main.Settings['Score']
		self.ids.player_left.text = main.Settings['Player2']
		self.ids.player_right.text = main.Settings['Player4']
		self.ids.player_top.text = main.Settings['Player3']
		self.ids.player_bottom.text = main.Settings['Player1']

		self.ids.info.text = "on_pre_enter: Conmpleted"
		print(self.ids.info.text)
		print("on_pre_enter: Conmpleted")
	def on_enter(self):
		Rest_Deck = shuffle_deal3(All_Players, Trumper, Deck, MA_cards)
		self.ids.info.text = "shuffle_deal3: Conmpleted"
		for card_place in range(1,4):
			self.ids[Trumper.place + str(card_place)].source = MA_cards[Trumper.hand[Trumper.place+str(card_place)]]['Image']
		self.ids.info.text = Trumper.name + ' makes trump !' + '\n' + Plr1.name + ' & ' + Plr3.name + '   VS.   ' + Plr2.name + ' & ' + Plr4.name + '.'

		trump = Trumper.make_trump()
		self.ids.info.text = "trump = Trumper.make_trump(): Conmpleted with trump =", trump
		assign_prio_trump(trump, MA_cards)
		self.load_trump()
		deal_rest_cards(All_Players, Trumper, Rest_Deck, MA_cards)
		self.ids.info.text = "deal_rest_cards: Conmpleted"
		for card_place in range(1,7):
			for player in All_Players:
				self.ids[player.place + str(card_place)].source = MA_cards[player.hand[player.place+str(card_place)]]['Image']
		self.ids.info.text = Trumper.name + ' chose ' + trump + ' as Trump Suit!' + '\n' + 'You may begin playing now.' + '\n' + Trumper.name + ' comes out!'

		self.ids.info.text = "Roundx(): BEGIN"
		self.Roundx()
		self.ids.info.text = "Roundx(): Conmpleted"
		while ready:
			print("H1"*15)
			for player in All_Players:
				self.ids[player.place + '0'].source = 'Images/card_frame.jpg'
			self.Roundx()
			print("H2"*15)
			winnerteam = determine_Tour_winner(All_Players, MA_cards)
			self.reset_new_tour()


	def load_trump(self):
		self.ids.trump.source = 'Images/suit_'+trump+'.jpg'

	def info_changed(self):
		print("INFO CHANGE: " + self.ids.info.text)

	def play_card(self, card):
		self.ids[card].disabled = True
		self.ids[Plr1.place + '0'].source = self.ids[card].source
		stack[Plr1.place+'0'] = rev_MA_cards[self.ids[card].source]
		Plr1.last_played_card = rev_MA_cards[self.ids[card].source]
		Plr1.hand.pop(card)
		self.ids[card].source = 'Images/card_frame.jpg'
		self.Roundx_end()

	def play_card_ai(self, player, card):
		self.ids[player.place + '0'].source = self.ids[card].source
		stack[player.place+'0'] = rev_MA_cards[self.ids[card].source]
		player.last_played_card = rev_MA_cards[self.ids[card].source]
		player.hand.pop(card)
		self.ids[card].source = 'Images/card_frame.jpg'

	def Roundx(self):
		if Auskommer == Plr1:
			pass
		elif Auskommer == Plr2:
			card = Plr2.choose_card(stack, trump)
			self.play_card_ai(Plr2, card)
			stack['first_played'] = Plr2.last_played_card
			card = Plr3.choose_card(stack, trump)
			self.play_card_ai(Plr3, card)
			card = Plr4.choose_card(stack, trump)
			self.play_card_ai(Plr4, card)
		elif Auskommer == Plr3:
			card = Plr3.choose_card(stack, trump)
			self.play_card_ai(Plr3, card)
			stack['first_played'] = Plr3.last_played_card
			card = Plr4.choose_card(stack, trump)
			self.play_card_ai(Plr4, card)
		elif Auskommer == Plr4:
			card = Plr4.choose_card(stack, trump)
			self.play_card_ai(Plr4, card)
			stack['first_played'] = Plr4.last_played_card
	def Roundx_end(self):
		if Auskommer == Plr1:
			stack['first_played'] = Plr1.last_played_card
			card = Plr2.choose_card(stack, trump)
			self.play_card_ai(Plr2, card)
			card = Plr3.choose_card(stack, trump)
			self.play_card_ai(Plr3, card)
			card = Plr4.choose_card(stack, trump)
			self.play_card_ai(Plr4, card)
		elif Auskommer == Plr2:
			stack['first_played'] = Plr2.last_played_card
		elif Auskommer == Plr3:
			stack['first_played'] = Plr3.last_played_card
			card = Plr2.choose_card(stack, trump)
			self.play_card_ai(Plr2, card)
		elif Auskommer == Plr4:
			stack['first_played'] = Plr4.last_played_card
			card = Plr2.choose_card(stack, trump)
			self.play_card_ai(Plr2, card)
			card = Plr3.choose_card(stack, trump)
			self.play_card_ai(Plr3, card)
		Ronn_winner = determine_Ronn_winner(stack, MA_cards)
		for player in All_Players:
			Ronn_winner.streech.append(player.last_played_card)
		Auskommer = Ronn_winner
		Ronn = Ronn + 1
		stack['first_played'] = ""

	def reset_game(self):
		self.ids.trump.source = 'Images/suit_trump.jpg'
		for i in range(1,7):
			self.ids['bottom_player_'+str(i)].disabled = False
			for player in All_Players:
				self.ids[player.place+str(i)].source = 'Images/card_frame.jpg'
		for player in All_Players:
			self.ids[player.place + '0'].source = 'Images/card_frame.jpg'

	def reset_new_tour(self):
		Trumper = update_trumper(Trumper, All_Players)
		reset_streech(All_Players, MA_cards)
		stack = init_stack()
		reset_prio_trump(trump, MA_cards)
		Ronn = 1
		if winnerteam[0].team == 1:
			score_us -= 1
			self.ids.score_us.text = 'Us: ' + str(score_us)
		elif winnerteam[0].team == 2:
			score_them -= 1
			self.ids.score_them.text = 'Them: ' + str(score_them)
		for card in range(1,7):
			self.ids['bottom_player_'+str(card)].disabled = False

#####   Custom KIVY
class ImageButton(ButtonBehavior, Image):
	pass
class Options_TextInput(TextInput):
	pass
class Options_Label(Label):
	pass
class MainMenu_Button(Button):
	pass
class Side_Image(Image):
	pass
class Top_Image(Image):
	pass

#####   POPUPS


#####   RUN
if __name__ == '__main__':
	main().run()
