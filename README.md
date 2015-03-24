# hearthstone_card_image_scraper

Simple Scraper in Ruby to scrape images of all Hearthstone cards.

JSON file of card stats is also included. Now with image paths.

Image naming convention is card name in all lowercase; all special characters which are converted to spaces; spaces are converted to underscores.

## Install

requires python and ruby

requires imagemagick and tesseract-ocr

helpful guide for installing tesseract-ocr on linux: http://ubuntuforums.org/archive/index.php/t-1647350.html

You need the following gems installed for ruby (Gemfile is included, however)

 gem install scrapifier
 gem install nokogiri
 gem install open-uri
 gem install tesseract-ocr

Thanks to Hearthpwn and HearthstoneJson for their websites and information.
