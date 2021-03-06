#!/usr/bin/env python

from PIL import Image
import sys
import commands
import re
import os
import json
from difflib import SequenceMatcher
from pprint import pprint
import pipes

class CardReader:

    def __init__(self, img_dir_path = "hearthstone_cards"):
        self.img_dir_path = img_dir_path

    def full_img_path(self, img_path):
        full_path = self.img_dir_path + "/" + img_path + ".png"
        return full_path

    def get_card_name(self, img_path):
        img = self.full_img_path(img_path)
        card_name = ""

        commands.getoutput('convert {0} -crop 210x40+40+200 -threshold 75% name.tiff'.format(pipes.quote(img)))
        # Invoking tesseract from python to extract characters
        commands.getoutput('tesseract name.tiff card_name')
        # Reading the output generated in card_name.txt
        with open('card_name.txt', 'r') as data:
          card = data.readlines()

        for line in card:
            card_name += line

        card_name = re.sub('[^A-Za-z0-9]+','',card_name)

        return card_name

    def get_card_text(self, img_path):
        img = self.full_img_path(img_path)
        card_text = ""

        commands.getoutput(commands.getoutput('convert {0} -crop 196x75+45+265 -scale 200% -threshold 2% text.tiff'.format(img)))
        # Invoking tesseract from python to extract characters
        commands.getoutput('tesseract text.tiff card_text')
        # Reading the output generated in card_text.txt
        with open('card_text.txt', 'r') as data:
            card = data.readlines()

        for line in card:
            card_text += line
        card_text = re.sub('[^A-Za-z0-9]+','',card_text)

        return card_text

    def get_hero_card_name(self, img_path):
        img = self.full_img_path(img_path)
        hero_name = ""

        commands.getoutput('convert {0} -crop 140x35+70+275 -threshold 50% -negate hero_name.tiff'.format(pipes.quote(img)))
        # Invoking tesseract from python to extract characters
        commands.getoutput('tesseract hero_name.tiff hero_name')
        # Reading the output generated in hero_name.txt
        with open('hero_name.txt', 'r') as data:
            card = data.readlines()

        for line in card:
            hero_name += line
        hero_name = re.sub('[^A-Za-z0-9]+','',hero_name)

        return hero_name

    def get_power_card_name(self, img_path):
        img = self.full_img_path(img_path)
        power_card_name = ""

        commands.getoutput('convert {0} -crop 125x25+75+195 -threshold 60% power_name.tiff'.format(pipes.quote(img)))
        # Invoking tesseract from python to extract characters
        commands.getoutput('tesseract power_name.tiff power_card_name')
        # Reading the output generated in power_card_name.txt
        with open('power_card_name.txt', 'r') as data:
            card = data.readlines()

        for line in card:
            power_card_name += line
        power_card_name = re.sub('[^A-Za-z0-9]+','',power_card_name)

        return power_card_name

    def get_hero_card_health(self, img_path):
        img = self.full_img_path(img_path)
        card_health = ""

        commands.getoutput('convert {0} -crop 65x45+220+235 -scale 200% -alpha off -threshold 95% -negate hero_health.tiff'.format(pipes.quote(img)))
        # Invoking tesseract from python to extract characters
        commands.getoutput('tesseract hero_health.tiff hero_card_health')
        # Reading the output generated in card_health.txt
        with open('hero_card_health.txt', 'r') as data:
            card = data.readlines()

        for line in card:
            card_health += line
        card_health = re.sub('[^A-Za-z0-9]+','',card_health)

        return card_health

    def get_power_card_text(self, img_path):
        img = self.full_img_path(img_path)
        power_card_text = ""

        commands.getoutput('convert {0} -crop 160x70+60+260 -scale 200% -threshold 15% power_text.tiff'.format(pipes.quote(img)))        # Invoking tesseract from python to extract characters
        commands.getoutput('tesseract power_text.tiff power_card_text')
        # Reading the output generated in power_card_text.txt
        with open('power_card_text.txt', 'r') as data:
            card = data.readlines()

        for line in card:
            power_card_text += line
        power_card_text = re.sub('[^A-Za-z0-9]+','',power_card_text)

        return power_card_text

    #loop through images to find only duplicate images since those are the only
    #ones we need to match against - the rest are self evident
    def get_duplicate_cards(self, img_names):
        duplicate_cards = []
        img_names_new = []
        previous_name = "no name"

        img_names.sort()

        for name in img_names:
            name = name.split('.')
            img_names_new.append(name[0])
            short_name = re.sub('[^A-Za-z]+', '', name[0])
            previous_short_name = re.sub('[^A-Za-z]+', '', previous_name)

            if short_name == previous_short_name:
                if previous_name not in duplicate_cards:
                    duplicate_cards.append(previous_name)

                duplicate_cards.append(name[0])
            previous_name = name[0]

        results = {
            "img_names": img_names_new,
            "duplicate_cards": duplicate_cards
        }

        return results

    def get_img_files_names(self):
        img_names = next(os.walk(self.img_dir_path))[2]

        results = self.get_duplicate_cards(img_names)

        return results

class CardData:

    def __init__(self, json_path):
        self.reader = CardReader()
        self.json_path = json_path
        self.data = self.load_json()

    def load_json(self):
        json_data = ""

        with open(self.json_path) as data_file:
            json_data = json.load(data_file)

        #flatten the data
        new_json_data = []
        for group in json_data:
            for card in json_data[group]:
                new_json_data.append(card)

        return new_json_data

    def set_img_data(self):
        img_names = self.reader.get_img_files_names()

        for img in img_names["img_names"]:
            print "Processing {0}...".format(img)
            img_name = re.sub('[^A-Za-z]+', '', img)

            for (i, card) in enumerate(self.data):
                card_name =  re.sub('[^A-Za-z]+', '', self.data[i]["name"])

                if card_name.lower() == img_name:
                    self.data[i]["img"] = img
                    break

        for dup in img_names["duplicate_cards"]:
            print "Processing {0}...".format(dup)
            card_name = self.reader.get_card_name(dup)

            if card_name == "":
                # check for hero or power
                img_power_name = self.reader.get_power_card_name(dup).lower()
                img_hero_name = self.reader.get_hero_card_name(dup).lower()

                for (i, card) in enumerate(self.data):
                    card_name =  re.sub('[^A-Za-z]+', '', self.data[i]["name"]).lower()
                    if self.similar(card_name, img_power_name) >= 0.9 or self.similar(card_name, img_hero_name) >= 0.6:

                        if "health" in self.data[i]:
                            img_hero_health = self.reader.get_hero_card_health(dup)
                            card_health = str(self.data[i]["health"])

                            print img_hero_health

                            if self.similar(img_hero_health, card_health) >= 0.5:
                                self.data[i]["img"] = dup
                                break

                        else:
                            #strip any styling tags
                            img_power_txt = self.reader.get_power_card_text(dup)
                            power_text = re.sub('<[^<]+?>', '', self.data[i]["text"]).lower()
                            power_text = re.sub('[^A-Za-z0-9]+', '', power_text).lower()

                            if card_name.lower() == dup and self.similar(power_text, img_power_txt) >= 0.9:
                                self.data[i]["img"] = dup
                                break

            else:
                img_text = self.reader.get_card_text(dup).lower()
                for (i, card) in enumerate(self.data):
                    # check card text to match
                    if "text" in self.data[i]:
                        #strip any styling tags
                        card_text = re.sub('<[^<]+?>', '', self.data[i]["text"])
                        card_text = re.sub('[^A-Za-z0-9]+', '', card_text).lower()

                        if self.similar(card_text, img_text) >= 0.9:
                            self.data[i]["img"] = dup
                            break
        self.write_to_json()
        self.clean_files()

    def write_to_json(self):
        json_file = open('master.json', 'w')
        json_data = json.dumps(self.data)
        json_file.write(json_data)
        json_file.close()

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def clean_files(self):
        os.remove('card_name.txt')
        os.remove('name.tiff')
        os.remove('text.tiff')
        os.remove('card_text.txt')
        os.remove('hero_name.tiff')
        os.remove('hero_name.txt')
        os.remove('power_name.tiff')
        os.remove('power_card_name.txt')
        os.remove('hero_health.tiff')
        os.remove('hero_card_health.txt')
        os.remove('power_text.tiff')
        os.remove('power_card_text.txt')



data = CardData('download.json')
data.set_img_data()

### Text Area ###
# commands.getoutput('convert {0} -crop 196x75+45+265 -scale 200% -threshold 2% text.tiff'.format(img))
# convert hearthstone_cards/abusive_sergeant.png -crop 196x100+45+265 -scale 200% -threshold 2% text.tiff

# x = 45px
# y = 265px

# w = 196px
# h = 75px


### Card Name ###
# x = 40px
# y = 200px

# w = 210px
# h = 40px

### Hero Name ###
# commands.getoutput('convert {0} -crop 140x35+70+275 -threshold 50% -negate hero_name.tiff'.format(img))
# convert hearthstone_cards/kelthuzad_2.png -crop 140x35+70+275 -threshold 50% -negate hero_name.tiff

# x = 70px
# y = 275px

#w = 140px
#h = 35px

### Hero Health ###
# commands.getoutput('convert {0} -crop 65x45+220+235 -scale 200% -alpha off -threshold 95% -negate hero_health.tiff'.format(img)
# convert hearthstone_cards/kelthuzad_2.png -crop 65x45+220+235 -scale 200% -alpha off -threshold 95% -negate hero_health.tiff

# x = 220px
# y = 240px

# w = 55px
# h = 40px

### Power Name ###
# commands.getoutput('convert {0} -crop 125x25+75+195 -threshold 60% power_name.tiff'.format(img))
# convert hearthstone_cards/chains_2.png -crop 125x25+75+195 -threshold 60% power_name.tiff

# x = 75px
# y = 195px

# w = 125px
# h = 25px

### Power Text ###
# commands.getoutput('convert {0} -crop 160x70+60+260 -scale 200% -threshold 15% power_text.tiff'.format(img))
# convert hearthstone_cards/chains_2.png -crop 160x70+60+260 -scale 200% -threshold 15% power_text.tiff

# x = 60px
# y = 260px

# w = 160px
# h = 70px

