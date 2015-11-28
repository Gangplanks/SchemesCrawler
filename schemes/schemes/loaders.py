from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import replace_escape_chars

def strip_dashes(x):
	if "--" in x:
		return "-"
	else:
		return x

class SchemeLoader(ItemLoader):
	default_input_processor = MapCompose(strip_dashes, replace_escape_chars)
	default_output_processor = TakeFirst()