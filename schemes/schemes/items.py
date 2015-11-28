import scrapy

class SchemeItem(scrapy.Item):
    name = scrapy.Field()
    department = scrapy.Field()
    beneficiaries = scrapy.Field()
    funding_pattern = scrapy.Field()
    jurisdiction = scrapy.Field()
    age_eligible = scrapy.Field()
    income_eligible = scrapy.Field()
    community_eligible = scrapy.Field()
    others_eligible = scrapy.Field()
    avail_from = scrapy.Field()
    valid_from = scrapy.Field()
    valid_till = scrapy.Field()
    description = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    pass
