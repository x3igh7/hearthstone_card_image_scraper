require 'scrapifier'
require 'nokogiri'
require 'open-uri'
require 'fileutils'
require 'rubygems'

class Scraper
	attr_accessor :pages, :links, :images

	def initialize
		@pages = []
		@links = []
		@images = []
	end

	def get_pages
		@pages[0] = "http://www.hearthpwn.com/cards"

		for i in 2..9 do
			page = "http://www.hearthpwn.com/cards?page=#{i}"
			@pages.push(page)
		end
	end

	def get_page_links
		puts "Grabbing card pages..."
		@pages.each do |page|
			page = Nokogiri::HTML(open(page))
			links = page.css(".visual-image-cell a")
			links.each do |link|
	      @links.push(link['href'])
	  	end
	  end
	end

	def scrape_img_urls
		puts "Grabbing image paths..."
		image_urls = []
		last_card_name = ""
		card_name = ""

		# need to handle the special conditions for these naxx heroes,
		# where there is a card as well as multiple hero tokens
		maexxna_count = 1
		loatheb_count = 1
		baron_rivendare_count = 1
		thaddius_count = 1
		kelthuzad_count = 1

		@links.each do |link|
			link = "http://www.hearthpwn.com" + link
			result = link.scrapify(images: [:png])
			card_name = derive_card_name(result[:title])
			last_card_name = card_name
			puts "#{card_name} => #{result[:images][0]}"
			image_urls.push(card_name => result[:images][0])
		end

		@images.push(image_urls.flatten)
	end

	def download_imgs
		count = @images[0].length

		@images[0].each_with_index do |card, i|
			card.each_pair do |name, image|
				puts "Downloading image #{i + 1} of #{count}"

				basename = File.basename(image)
				ext = basename.split(".")
				ext = ext[1]
				name = name + "." + ext

				File.open(File.basename(image), 'wb') { |f| f.write(open(image).read) }
				File.rename(basename, name)
				FileUtils.mv(name, "hearthstone_cards/" + name)
			end
		end
	end

	protected

	def derive_card_name(card_name)
		card_name.slice!(" - Hearthstone Cards")
		card_name = card_name.strip.downcase.tr(" ", "_").gsub(/[!@%&"'.,-:]/,'')

		if(card_name.tr("_", "") == "maexxna")
			card_name = "maexxna_#{maexxna_count}"
			maexxna_count += 1
		elsif(card_name.tr("_", "") == "loatheb")
			card_name = "loatheb_#{loatheb_count}"
			loatheb_count += 1
		elsif(card_name.tr("_", "") == "baronrivendare")
			card_name = "baron_rivendare_#{baron_rivendare_count}"
			baron_rivendare_count += 1
		elsif(card_name.tr("_", "") == "thaddius")
			card_name = "thaddius_#{thaddius_count}"
			thaddius_count += 1
		elsif(card_name.tr("_", "") == "kelthuzad")
			card_name = "kelthuzad_#{kelthuzad_count}"
			kelthuzad_count += 1
		elsif(card_name.tr("_", "") == last_card_name.tr("0-9_", ""))
			if(last_card_name.tr("A-Za-z_", "") == "")
				card_name = card_name + "_2"
			else
				number = last_card_name.tr("A-Za-z_", "").to_i + 1
				card_name = card_name + "_#{number.to_s}"
			end
		end

		return card_name
	end

end

class ImageScrape
	attr_accessor :scraper

	def initialize
		@scraper = Scraper.new
	end

	def run!
		scraper.get_pages
		scraper.get_page_links
		scraper.scrape_img_urls
		scraper.download_imgs
	end

end

s = ImageScrape.new
s.run!
