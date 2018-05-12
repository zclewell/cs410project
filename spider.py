#Script that recursively crawls all pages on cs.illinois.edu and then stores the url, title, and html in a csv

import scrapy
from scrapy import Spider
from scrapy.http    import Request

from selenium import webdriver

#object representation of a webpage to be stored in our csv
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
        
    #start with the root url
    def __init__(self):
        self.crawledLinks = ["https://cs.illinois.edu/"]
        self.savedLinks = []
        self.driver = webdriver.Firefox()

    #function to be called recursively
    def parse(self, response):      
        self.driver.get(response.url)
        link_elements = self.driver.find_elements_by_xpath('//a')
        links = list(map(self.get_href, link_elements))
        links2 = response.xpath('//a/@href').extract()
        all_links = links+links2
        
        cur_url = self.driver.current_url
        
        #only crawl sites on cs.illinois.edu
        if '://cs.illinois.edu' in cur_url and (not cur_url in self.savedLinks):
            self.savedLinks.append(cur_url)
            item = ResultItem()
            item["url"] = cur_url
            item["title"] = self.driver.title
            item["text"] = self.driver.find_element_by_tag_name('body').text.encode("unicode_escape").decode("utf-8")
            yield item
        
        for link in all_links:
            if link.startswith('/'):
                link = "https://cs.illinois.edu" + link
            #make sure not to get stuck in a loop
            if (not link in self.crawledLinks) and ('://cs.illinois.edu' in link):
                self.crawledLinks.append(link)
                yield Request(link, self.parse)