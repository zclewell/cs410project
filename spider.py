import scrapy
from scrapy import Spider
from scrapy.http    import Request
import html2text

from selenium import webdriver

class ResultItem(scrapy.Item):
  url = scrapy.Field()
  title = scrapy.Field()
  text = scrapy.Field()
  
class Foo(Spider):
    # start urls executed at the beginning
    # with default callback "parse"
    start_urls = ["https://cs.illinois.edu/"]
    name = "basic_spider"
    custom_settings = {
    'FEED_EXPORT_FIELDS': ["url", "title", "text"],
    }
    
    def get_href(self, element):
        return element.get_attribute('href')
        
    def __init__(self):
        self.crawledLinks = []
        self.driver = webdriver.Firefox()

    def parse(self, response):      
        self.driver.get(response.url)
        link_elements = self.driver.find_elements_by_xpath('//a')
        links = map(self.get_href, link_elements)
        
        for link in links:
            if (not link in self.crawledLinks) and (('://cs.illinois.edu' in link) or link.startswith('/')):
                if link.startswith('/'):
                    link = "https://cs.illinois.edu" + link
                self.crawledLinks.append(link)
                yield Request(link, self.parse)

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        
        item = ResultItem()
        item["url"] = response.request.url
        item["title"] = response.xpath('//title/text()').extract()
        item["text"] = self.driver.find_element_by_tag_name('body').text.encode("unicode_escape").decode("utf-8")
        yield item