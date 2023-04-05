import scrapy
#from ..items import DeSpiderItem
#from items import Housing_items
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class DataExtractionSpider(scrapy.Spider):
    name = "test_spider"
    start_urls = ["http://www.rentalhomebd.com/properties?page=1"]
    website_main_url = "http://www.rentalhomebd.com/"

    
    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        #url_context_names = response.css("li article div a._287661cb::attr(href)").getall()
        url_context_names = response.xpath('//*[@id="grid-image"]/a[1]/@href').getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]

        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

#       next_page = response.xpath('//div/a[contains(@alt, "Next")]').xpath('@href').get()
        #next_page = response.xpath('//div/ul/li/a[contains(@title, "Next")]').xpath('@href').get()

#        if next_page is not None:

#            new_url = self.website_main_url+next_page
#            yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)


    def parse_details_page(self, response):
#        item = Housing_items()
        yield {'basic_info' : 'response.xpath("//*[@id="propertiesDiv"]/div[2]/div[1]/div/div[2]/p[1]/text").get()',
        'amenities' : 'response.xpath("//*[@id="property-details"]/div[3]/text").get()',
        'address' : 'response.xpath("//*[@id="propertiesDiv"]/div[2]/div[1]/div/div[2]/p[2]/text").get()'}

#    item = Housing_items()
#        yield {'basic_info' : response.css("p.property-basic-info::text").get(),
#        'amenities' : response.css("div.features-box::text").get(),
#        'address' : response.css("p.property-address text-wrap::text").get()}
#       'price' : response.css("div.bd-highlight flex-price::text").get()}
    #    item['basic_info'] = response.css("p.property-basic-info::text").get()
    #    item['amenities'] = response.css("div.features-box::text").get()
    #    item['address'] = response.css("p.property-address text-wrap::text").get()
    #    item['price'] = response.css("div.bd-highlight flex-price::text").get()
        

#        yield item

    def errback_httpbin(self, failure):
        # logs failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)