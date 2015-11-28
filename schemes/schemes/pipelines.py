# # -*- coding: utf-8 -*-

# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class SchemesDBPipeline(object):

	def __init__(self, host, port, user, password, db):
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.db = db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			host=crawler.settings.get('DB_HOST'),
			port=crawler.settings.get('DB_PORT'),
			user=crawler.settings.get('DB_USER'),
			password=crawler.settings.get('DB_PASSWORD'),
			db=crawler.settings.get('DB_NAME')
			)

	def open_spider(self, spider):
		self.connection = psycopg2.connect(database=self.db, user=self.user, 
			password=self.password, host=self.host, port=self.port)

	def close_spider(self, spider):
		self.connection.close()

	def process_item(self, item, spider):
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO schemes(name, department, beneficiaries, funding_pattern," +
			" jurisdiction, age_eligible, income_eligible, community_eligible, others_eligible," +
			" avail_from, valid_from, valid_till, description, created_at, updated_at) VALUES" + 
			" (%(name)s, %(department)s, %(beneficiaries)s, %(funding_pattern)s,  %(jurisdiction)s, %(age_eligible)s," +
			" %(income_eligible)s, %(community_eligible)s, %(others_eligible)s, %(avail_from)s," +
			" %(valid_from)s, %(valid_till)s, %(description)s, %(created_at)s, %(updated_at)s)", item)
		self.connection.commit()
		return item