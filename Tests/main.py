###   Versioning
__version__ = "17.12.20.0"

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
class Game(Screen):

	def on_pre_enter(self):
		self.score_them = int(main.Settings['Score'])
		self.score_us = int(main.Settings['Score'])
		self.Plr1, self.Plr2, self.Plr3, self.Plr4, self.All_Players = init_players()
		self.Deck, self.MA_cards, self.rev_MA_cards = init_MA_cards()
		self.Dealer = set_first_dealer(self.All_Players)
		self.Trumper = set_trumper(self.All_Players, self.Dealer)
		self.Auskommer = self.Trumper
		self.stack = init_stack()
		self.Ronn = 1

		self.ids.score_them.text = 'Them: ' + main.Settings['Score']
		self.ids.score_us.text = 'Us: ' + main.Settings['Score']
		self.ids.player_left.text = main.Settings['Player2']
		self.ids.player_right.text = main.Settings['Player4']
		self.ids.player_top.text = main.Settings['Player3']
		self.ids.player_bottom.text = main.Settings['Player1']
	def on_enter(self):
		self.Rest_Deck = shuffle_deal3(self.All_Players, self.Trumper, self.Deck, self.MA_cards)
		for card_place in range(1,4):
			self.ids[self.Trumper.place + str(card_place)].source = self.MA_cards[self.Trumper.hand[self.Trumper.place+str(card_place)]]['Image']
		self.ids.info.text = self.Trumper.name + ' makes trump !' + '\n' + self.Plr1.name + ' & ' + self.Plr3.name + '   VS.   ' + self.Plr2.name + ' & ' + self.Plr4.name + '.'

		self.trump = ["k","r","s","h"][randint(0,3)]
		assign_prio_trump(self.trump, self.MA_cards)
		self.load_trump()
		deal_rest_cards(self.All_Players, self.Trumper, self.Rest_Deck, self.MA_cards)
		for card_place in range(1,7):
			for player in self.All_Players:
				self.ids[player.place + str(card_place)].source = self.MA_cards[player.hand[player.place+str(card_place)]]['Image']
		self.ids.info.text = self.Trumper.name + ' chose ' + self.trump + ' as Trump Suit!' + '\n' + 'You may begin playing now.' + '\n' + self.Trumper.name + ' comes out!'

		self.Roundx(self.Auskommer)

		for player in self.All_Players:
			self.ids[player.place + '0'].source = 'Images/card_frame.jpg'
		self.Roundx(self.Auskommer)
		self.winnerteam = determine_Tour_winner(self.All_Players, self.MA_cards)
		self.reset_new_tour()


	def load_trump(self):
		self.ids.trump.source = 'Images/suit_'+self.trump+'.jpg'

	def play_card(self, player, card):
		self.ids[card].disabled = True
		self.ids[player.place + '0'].source = self.ids[card].source
		self.stack[player.place+'0'] = self.rev_MA_cards[self.ids[card].source]
		player.last_played_card = self.rev_MA_cards[self.ids[card].source]
		player.hand.pop(card)
		self.ids[card].source = 'Images/card_frame.jpg'
		self.Roundx_end()

	def play_card_ai(self, player, card):
		self.ids[player.place + '0'].source = self.ids[card].source
		self.stack[player.place+'0'] = self.rev_MA_cards[self.ids[card].source]
		player.last_played_card = self.rev_MA_cards[self.ids[card].source]
		player.hand.pop(card)
		self.ids[card].source = 'Images/card_frame.jpg'

	def Roundx(self, Auskommer):
		if Auskommer == self.Plr1:
			pass
		elif Auskommer == self.Plr2:
			# card = self.choose_card(Plr2)
			card = self.Plr2.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr2, card)
			self.stack['first_played'] = self.Plr2.last_played_card
			# card = self.choose_card(Plr3)
			card = self.Plr3.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr3, card)
			# card = self.choose_card(Plr4)
			card = self.Plr4.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr4, card)
		elif Auskommer == self.Plr3:
			# card = self.choose_card(Plr3)
			card = self.Plr3.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr3, card)
			self.stack['first_played'] = self.Plr3.last_played_card
			# card = self.choose_card(Plr4)
			card = self.Plr4.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr4, card)
		elif Auskommer == self.Plr4:
			# card = self.choose_card(Plr4)
			card = self.Plr4.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr4, card)
			self.stack['first_played'] = self.Plr4.last_played_card
	def Roundx_end(self):
		if self.Auskommer == self.Plr1:
			self.stack['first_played'] = self.Plr1.last_played_card
			# card = self.choose_card(Plr2)
			card = self.Plr2.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr2, card)
			# card = self.choose_card(Plr3)
			card = self.Plr3.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr3, card)
			# card = self.choose_card(Plr4)
			card = self.Plr4.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr4, card)
		elif self.Auskommer == self.Plr2:
			self.stack['first_played'] = self.Plr2.last_played_card
		elif self.Auskommer == self.Plr3:
			self.stack['first_played'] = self.Plr3.last_played_card
			# card = self.choose_card(Plr2)
			card = self.Plr2.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr2, card)
		elif self.Auskommer == self.Plr4:
			self.stack['first_played'] = self.Plr4.last_played_card
			# card = self.choose_card(Plr2)
			card = self.Plr2.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr2, card)
			# card = self.choose_card(Plr3)
			card = self.Plr3.choose_card(self.stack, self.trump)
			self.play_card_ai(self.Plr3, card)
		self.Ronn_winner = determine_Ronn_winner(self.stack, self.MA_cards)
		for player in self.All_Players:
			self.Ronn_winner.streech.append(player.last_played_card)
		self.Auskommer = self.Ronn_winner
		self.Ronn += 1
		self.stack['first_played'] = ""

	def reset_game(self):
		self.ids.trump.source = 'Images/suit_trump.jpg'
		for i in range(1,7):
			self.ids['bottom_player_'+str(i)].disabled = False
			for player in self.All_Players:
				self.ids[player.place+str(i)].source = 'Images/card_frame.jpg'
		for player in self.All_Players:
			self.ids[player.place + '0'].source = 'Images/card_frame.jpg'

	def reset_new_tour(self):
		self.Trumper = update_trumper(self.Trumper, self.All_Players)
		reset_streech(self.All_Players, self.MA_cards)
		self.stack = init_stack()
		reset_prio_trump(self.trump, self.MA_cards)
		self.Ronn = 1
		if self.winnerteam[0].team == 1:
			self.score_us -= 1
			self.ids.score_us.text = 'Us: ' + str(self.score_us)
		elif self.winnerteam[0].team == 2:
			self.score_them -= 1
			self.ids.score_them.text = 'Them: ' + str(self.score_them)
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
