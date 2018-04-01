import scrapy
from scrapy import Spider
from scrapy.http    import Request
import html2text

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

    def parse(self, response):
        links = response.xpath('//a/@href').extract()
        
        crawledLinks = []
        
        for link in links:
            if (not link in crawledLinks) and (('://cs.illinois.edu' in link) or link.startswith('/')):
                if link.startswith('/'):
                    link = "https://cs.illinois.edu" + link
                crawledLinks.append(link)
                yield Request(link, self.parse)

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        
        # use css or xpath selectors to extract text
        item = ResultItem()
        item["url"] = response.request.url
        item["title"] = response.xpath('//title/text()').extract()
        item["text"] = converter.handle(response.body.decode("utf8")).encode("unicode_escape").decode("utf-8")
        yield item