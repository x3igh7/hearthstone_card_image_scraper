#!/usr/bin/env python

from PIL import Image
import sys
import commands
import re
import os
import json
from pprint import pprint
from difflib import SequenceMatcher

# img = "hearthstone_cards/bananas.png"
# card_text = ""

# commands.getoutput(commands.getoutput('convert {0} -crop 196x75+45+265 -scale 200% -threshold 2% text.tiff'.format(img)))
# # Invoking tesseract from python to extract characters
# commands.getoutput('tesseract text.tiff card_text')
# # Reading the output generated in card_text.txt
# with open('card_text.txt', 'r') as data:
#  	card = data.readlines()

#  	for line in card:
#  		card_text += line
#  		card_text = re.sub('[^A-Za-z0-9]+','',card_text)

# print card_text

with open('download.json') as data_file:
	json_data = json.load(data_file)

pprint(json_data["Basic"][0])

json_data["Basic"][1][u"img"] = u"an image"
pprint(json_data["Basic"][1])

# card_text = ""

# with open('card_text.txt', 'r') as data:
# 	card = data.readlines()
# 	for line in card:
# 		card_text += line

# 	card_text = re.sub('[^A-Za-z0-9]+','',card_text)

# print card_text
# b = "Battlecry: Give a minion +2 Attack this turn."
# b = re.sub('[^A-Za-z0-9]+','',b)
# print b
# print SequenceMatcher(None, card_text, b).ratio()

