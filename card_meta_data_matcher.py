#!/usr/bin/env python

from PIL import Image
import sys
import commands
import re

usr_img = sys.argv[1]
card_name = ""
card_text = ""

commands.getoutput('convert {0} -crop 210x40+40+200 -threshold 75% test.tiff'.format(usr_img))
# Invoking tesseract from python to extract characters
commands.getoutput('tesseract test.tiff data')
# Reading the output generated in data.txt
with open('data.txt', 'r') as data:
    card_name = data.readline().strip().lower().
    card_name = re.sub('[^A-Za-z0-9]+','',card_name)
    card_img_name = card_name.replace(" ", "_")

    #loop through images to find only duplicate images and then check those

    if card_name == "":
    	# check health and attack to match hero or hero power token
    else:
    	# check card text to match


# convert hearthstone_cards/abusive_sergeant.png -crop 210x40+40+200 -fill Black +opaque White test.tiff

# convert hearthstone_cards/abusive_sergeant.png -scale 1000% -blur 1x65535 -blur 1x65535 -blur 1x65535 -contrast -normalize -despeckle -despeckle -type grayscale a_test.tiff

# x = 40px
# y = 200px

# w = 210px
# h = 40px
