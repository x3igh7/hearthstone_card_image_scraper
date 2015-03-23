#!/usr/bin/env python

from PIL import Image
import sys
import commands
import re
import os
import json

class CardReader:

	def __init__(img_dir_path = "hearthstone_cards"):
		self.img_dir_path = img_dir_path

	def get_card_name(self, img_path):
		img = path
		card_name = ""

		commands.getoutput('convert {0} -crop 210x40+40+200 -threshold 75% name.tiff'.format(img))
		# Invoking tesseract from python to extract characters
		commands.getoutput('tesseract name.tiff card_name')
		# Reading the output generated in card_name.txt
		with open('card_name.txt', 'r') as data:
	  	card_name = data.readline().strip().lower()
	  	card_name = re.sub('[^A-Za-z0-9]+','',card_name)

	  return card_name

	def get_card_text(self, img_path):
		img = path
		card_text = ""

		commands.getoutput('convert {0} -crop 210x40+40+200 -threshold 75% text.tiff'.format(img))
		# Invoking tesseract from python to extract characters
		commands.getoutput('tesseract text.tiff card_text')
		# Reading the output generated in card_text.txt
		with open('card_text.txt', 'r') as data:
	  	card_text = data.readline().strip().lower()
	  	card_text = re.sub('[^A-Za-z0-9]+','',card_text)

	  return card_text

	def get_alt_card_name(self, img_path):
		img = path
		card_name = ""

		commands.getoutput('convert {0} -crop 210x40+40+200 -threshold 75% alt_name.tiff'.format(img))
		# Invoking tesseract from python to extract characters
		commands.getoutput('tesseract alt_name.tiff card_alt_name')
		# Reading the output generated in card_alt_name.txt
		with open('card_alt_name.txt', 'r') as data:
	  	card_alt_name = data.readline().strip().lower()
	  	card_alt_name = re.sub('[^A-Za-z0-9]+','',card_alt_name)

	  return card_alt_name

	def get_alt_card_health(self, img_path):
		img = path
		card_health = ""

		commands.getoutput('convert {0} -crop 210x40+40+200 -threshold 75% health.tiff'.format(img))
		# Invoking tesseract from python to extract characters
		commands.getoutput('tesseract health.tiff card_health')
		# Reading the output generated in card_health.txt
		with open('card_health.txt', 'r') as data:
	  	card_health = data.readline().strip().lower()
	  	card_health = re.sub('[^A-Za-z0-9]+','',card_health)

	  return card_health

  def get_alt_card_cost(self, img_path):
  	img = path
		card_cost = ""

		commands.getoutput('convert {0} -crop 210x40+40+200 -threshold 75% cost.tiff'.format(img))
		# Invoking tesseract from python to extract characters
		commands.getoutput('tesseract cost.tiff card_cost')
		# Reading the output generated in card_cost.txt
		with open('card_cost.txt', 'r') as data:
	  	card_cost = data.readline().strip().lower()
	  	card_cost = re.sub('[^A-Za-z0-9]+','',card_cost)

	  return card_cost

	#loop through images to find only duplicate images since those are the only
	#ones we need to match against - the rest are self evident
	def get_duplicate_cards(img_names):
		duplicate_cards = []
		previous_name = ""

		for name in img_names:
			short_name = re.sub('[^A-Za-z]+', '', name)
		 	previous_short_name = re.sub('[^A-Za-z]+', '', previous_name)

		 	if short_name == previous_short_name:
		   	if duplicate_cards[-1] != previous_name:
					duplicate_cards.append(previous_name)

				duplicate_cards.append(name)
		  previous_name = name

		return duplicate_cards

	def get_img_files_names(self):
		img_names = next(os.walk(self.get_img_files_names))[2]
		duplicate_cards = self.get_duplicate_cards(img_names)

		results = {
			"img_names": img_names,
			"duplicate_cards": duplicate_cards
		}

		return results

class CardData:

	def __init__(json_path):
		self.reader = CardReader()
		self.data = self.load_json(json_path)

	def load_json(json_path):
		json_data = ""
		new_json_data = ""

		with open(json_path) as data_file:
			json_data = json.load(data_file)

		#flatten the data
		new_json_data = [item for sublist in json_data for item in sublist]
		return new_json_data

	def set_img_data(self):
		img_names = self.reader.get_img_file_names()

		for img in img_names["img_names"]:
			img_name = re.sub('[^A-Za-z]+', '', img)

			for card in self.data:
				card_name =  re.sub('[^A-Za-z]+', '', card["name"])

				if card_name.lower() == img_name:
					card["img"] = img

		for dup in img_names["duplicate_cards"]:
			card_name = self.reader.get_card_name(dup)
			card_health = "0"
			card_cost = "0"
			card_text = ""

			if card_name == "":
				# check health or cost attack to match hero
				img_health = self.reader.get_alt_card_health(dup)

				for (i, card) in enumerate(self.data):
					card_name =  re.sub('[^A-Za-z]+', '', card["name"])
					if "health" in card:
						card_health = str(card["health"])

					if card_name.lower() == dup && card_health == img_health:
						card["img"] = dup

			else:
				# check card text to match
				if "text" in card:
					#strip any styling tags
					card_text = re.sub('<[^<]+?>', '', card["text"])
					img_text = self.reader.get_card_text(dup)

					if card_text == img_text:
						card["img"] = dup

				# if no txt check for naxx hero power token
				else:
					if "cost" in card:
						card_cost = str(card["cost"])
						img_cost = self.reader.get_alt_card_cost(dup)

						if card_cost == img_cost:
							card["img"] = dup

# if card_name == "":
 	# check health and attack to match hero or hero power token
# else:
 	# check card text to match

# x = 40px
# y = 200px

# w = 210px
# h = 40px
