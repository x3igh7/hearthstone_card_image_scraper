require 'scrapifier'

class Scraper
	attr_accessor :pages, :images

	def initialize
		@pages = []
		@images = []
	end

	def get_pages
		@pages[0] = "http://www.hearthpwn.com/cards"

		for i in 2..9 do
			page = "http://www.hearthpwn.com/cards?page=#{i}"
			@pages.push(page)
		end
	end

	def scrape_img_urls
		image_urls = []

		@pages.each do |page|
			result = page.scrapify(:images: :png)
			image_urls.push(result[:images])
		end

		@images.push(image_urls.flatten)
	end

	def download_imgs
		count = @images[0].length

		@images[0].each_with_index do |image, i|
			puts "Downloading image #{i + 1} of #{count}"
			File.open(File.basename(image), 'wb') { |f| f.write(open(image).read) }
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
