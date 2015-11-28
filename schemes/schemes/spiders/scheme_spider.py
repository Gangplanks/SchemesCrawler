import scrapy
import datetime

from schemes.items import SchemeItem
from schemes.loaders import SchemeLoader

class SchemeSpider(scrapy.Spider):
	name = "scheme"
	allowed_domains = ["tn.gov.in"]
	start_urls = [
		"http://www.tn.gov.in/scheme/alpha_view/All"
	]

	def parse(self, response):
		scheme_urls = response.css("div.scheme_list").css('a::attr(href)')
		for scheme_url in scheme_urls:
			url = response.urljoin(scheme_url.extract())
			yield scrapy.Request(url, callback=self.parse_scheme_data)
		scan_for_next_page = 0
		pages = response.css('ul.pager').css('li')
		for page in pages:
			current_page = page.css('li[class*=pager-current]').extract()
			if current_page:
				scan_for_next_page = 1
			if scan_for_next_page == 1:
				next_page = page.css('li[class*=pager-item]')
				if next_page:
					url = response.urljoin(next_page.css('a::attr(href)').extract_first())
					yield scrapy.Request(url, self.parse)


	def parse_scheme_data(self, response):
		scheme_data = self.get_scheme_details(response, '.node_viewlist_odd')
		scheme_data.update(self.get_scheme_details(response, '.node_viewlist_even'))
		scheme_item = self.scheme_item_from(scheme_data)
		return scheme_item
		
	def get_scheme_details(self, response, scheme_selector):
		scheme_data = {}
		for node in response.css(scheme_selector):
			key = node.css('.left_column::text').extract_first()
			value = node.css('.right_column::text')
			if value:
				value = value.extract_first()
			else:
				value = "-"
			scheme_data[key] = value
		return scheme_data

	def scheme_item_from(self, scheme_data):
		scheme_loader = SchemeLoader(item=SchemeItem())
		scheme_loader.add_value('name', scheme_data['Title / Name'])
		scheme_loader.add_value('department', scheme_data['Concerned Department'])
		scheme_loader.add_value('beneficiaries', scheme_data['Beneficiaries'])
		scheme_loader.add_value('funding_pattern', scheme_data['Funding Pattern'])
		scheme_loader.add_value('jurisdiction', scheme_data['Sponsored By'])
		scheme_loader.add_value('age_eligible', scheme_data['Age'])
		scheme_loader.add_value('income_eligible', scheme_data['Income'])
		scheme_loader.add_value('community_eligible', scheme_data['Community'])
		scheme_loader.add_value('others_eligible', scheme_data['Other Details'])
		scheme_loader.add_value('avail_from', scheme_data['How To Avail'])
		scheme_loader.add_value('valid_from', scheme_data['Introduced On'])
		scheme_loader.add_value('valid_till', scheme_data['Valid Upto'])
		scheme_loader.add_value('description', scheme_data['Description'])
		scheme_item = scheme_loader.load_item()
		scheme_item['created_at'] = datetime.datetime.now()
		scheme_item['updated_at'] = datetime.datetime.now()
		return scheme_item