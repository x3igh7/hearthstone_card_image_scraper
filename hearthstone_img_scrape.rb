require 'scrapifier'
require 'nokogiri'
require 'open-uri'

class Scraper
	attr_accessor :pages, :images

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
		@pages.each do |page|
			Nokogiri::HTML(open(page).read).css("visual-image-cell a").map do |link|
		    if (href = link.attr("href"))
		      @links.push(href)
		    end
	  	end
	  end
	end

	def scrape_img_urls
		image_urls = []

		@links.each do |link|
			link = "http://www.hearthpwn.com" + link
			result = link.scrapify(:images: [:png, :gif])
			card_name = result[:title].slice(" - Heartstone Cards").downcase.tr(" ", "_")
			image_urls.push(card_name => result[:images])
		end

		@images.push(image_urls.flatten)
	end

	def download_imgs
		count = @images[0].length

		@images[0].each_with_index do |card, i|
			card.each_pair do |name, image|
				puts "Downloading image #{i + 1} of #{count}"
				File.open(File.basename(card_name), 'wb') { |f| f.write(open(image).read) }
			end
		end
	end

end

class ImageScrape
	attr_accessor :scraper

	def initialize
		@scraper = Scraper.new
	end

	def run!
		scraper.get_pages
		scraper.scrape_img_urls
		scraper.download_imgs
	end

end

s = ImageScrape.new
s.run!
