import scrapy
import time
import os
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
from ..items import ReviewsItem

class GetdataSpider(scrapy.Spider):
    name = 'getdata'


    def start_requests(self):
        index = 0
        yield SeleniumRequest(
            url="https://www.flipkart.com/infinix-note-7-aether-black-64-gb/product-reviews/itmec535fbb60714?pid=MOBFVEGAJPYVPAZQ&lid=LSTMOBFVEGAJPYVPAZQ7CMIIK&marketplace=FLIPKART&page=1",
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        Reviews_Item = ReviewsItem()
        while(1):
            driver = response.meta['driver']
            html = driver.page_source
            response_obj = Selector(text=html)

            details = response_obj.xpath("//div[@class='_3gijNv col-12-12']/div/div/div[@class='col _390CkK _1gY8H-']")

            for idx, detail in enumerate(details):
                rating = detail.xpath(".//div[1]/div[1]/text()").get()
                heading = detail.xpath(".//div[1]/p/text()").get()
                description = detail.xpath(".//div[2]/div/div/div/text()").get()

                Reviews_Item['Rating'] = rating
                Reviews_Item['Heading'] = heading
                Reviews_Item['Description'] = description
                yield Reviews_Item
                print('\n'*3)



            next_page = response_obj.xpath('//a[@class="_3fVaIS"]/span[contains(text(), "Next")]').get()
            print('next_page',next_page)
            if(next_page):
                print("true")
                search_button = driver.find_element_by_xpath('//a[@class="_3fVaIS"]/span[contains(text(), "Next")]')
                search_button.click()
                time.sleep(5)
            else:
                break




