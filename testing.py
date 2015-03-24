#!/usr/bin/env python

from PIL import Image
import sys
import commands
import re
import os
import json
from difflib import SequenceMatcher

card_text = ""

with open('card_text.txt', 'r') as data:
	card = data.readlines()
	for line in card:
		card_text += line

	card_text = re.sub('[^A-Za-z0-9]+','',card_text)

print card_text
b = "Battlecry: Give a minion +2 Attack this turn."
b = re.sub('[^A-Za-z0-9]+','',b)
print b
print SequenceMatcher(None, card_text, b).ratio()

