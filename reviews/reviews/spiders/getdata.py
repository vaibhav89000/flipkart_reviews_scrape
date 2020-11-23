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
            url="https://www.flipkart.com/",
            wait_time=1000,
            screenshot=True,
            callback=self.search,
            dont_filter=True
        )

    def search(self, response):
        driver = response.meta['driver']

        # // div / div / button
        cross_button = driver.find_element_by_xpath("//div/div/button")
        if(cross_button):
            cross_button.click()
            time.sleep(2)

        # time.sleep(50)
        driver.find_element_by_xpath("//form/div/div/input").clear()
        search_input1 = driver.find_element_by_xpath("//form/div/div/input")
        search_input1.send_keys('Note 7')

        time.sleep(3)
        search_button = driver.find_element_by_xpath("//form/div/button")
        search_button.click()
        time.sleep(10)

        first_result = driver.find_element_by_xpath("(//a/div[2]/div[1]/div[1])[1]")
        first_result.click()
        time.sleep(10)
        driver = response.meta['driver']

        driver.switch_to_window(driver.window_handles[1])
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        # next_url = driver.current_url
        # yield SeleniumRequest(
        #     url= next_url,
        #     wait_time=1000,
        #     screenshot=True,
        #     callback=self.parse,
        #     dont_filter=True
        # )
        # time.sleep(60)
        #
        review_click = driver.find_element_by_xpath("//div/span[contains(text(),'reviews')]")
        review_click.click()
        # print()
        time.sleep(10)


        # details = response_obj.xpath("//*[@id='container']/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()").get()

    # def parse(self, response):
    #     time.sleep(50)
    #     print('\n'*2)
    #     print('check',details)
    #     print('\n'*2)

        Reviews_Item = ReviewsItem()
        while(1):
            print('\n'*2)
            print('I am in while loop')
            print('\n' * 2)
            driver = response.meta['driver']
            html = driver.page_source
            response_obj = Selector(text=html)

            details = response_obj.xpath("//*[@id='container']/div/div[3]/div/div/div[2]/div/div/div/div/div/div")

            for idx, detail in enumerate(details):
                rating = detail.xpath(".//div[1]/div[1]/text()").get()
                heading = detail.xpath(".//div[1]/p/text()").get()
                description = detail.xpath(".//div[2]/div/div/div/text()").get()

                Reviews_Item['Rating'] = rating
                Reviews_Item['Heading'] = heading
                Reviews_Item['Description'] = description
                yield Reviews_Item
                print('\n'*3)



            next_page = response_obj.xpath('//a/span[contains(text(), "Next")]').get()
            print('next_page',next_page)
            if(next_page):
                print("true")
                search_button = driver.find_element_by_xpath('//a/span[contains(text(), "Next")]')
                search_button.click()
                time.sleep(5)
            else:
                print('\n'*2)
                print(" now break")
                print('\n' * 2)
                break




