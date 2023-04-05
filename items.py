# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import main
from scrapy.item import Item, Field

class Housing_items(Item):
    # define the fields for your item here like:
    basic_info = Field()
    amenities = Field()
    address = Field()
    price = Field()
    

