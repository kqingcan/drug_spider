# -*- coding: utf-8 -*-
import scrapy
from mysPider.items import MyspiderItem
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup as bs4
import time

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = []
    start_urls = ['https://db.yaozh.com/interaction']
    # def __init__(self):
    #     super(ExampleSpider, self).__init__(name='example')
    #     option = FirefoxOptions()
    #     option.headless = True
    #     self.driver = webdriver.Firefox(options=option)
    
    def parse(self, response):
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        time.sleep(10)
        soup = bs4(driver.page_source,'html.parser')
        h_url = soup.findAll('div',{'class':'responsive-table'})
        list_urls = h_url[0].table.tbody.findAll('tr') 
        # list_urls = response.xpath("//div[@class='main']/div[@class='offset-top table-list']").xpath("./div")
        # print(list_urls)
        for list_url in list_urls:
            item =  MyspiderItem()
            # name = list_url.xpath("./th").extract()
            # related_drug = list_url.xpath("./td").extract[0]
            # effect = list_url.xpath("./td").extract[1]
            th = list_url.find("th")
            name = th.get_text().strip()
            # print("###############name   " ,name)
            tds = list_url.findAll("td")
            related_drug = tds[0].get_text().strip()
            effect = tds[1].get_text().strip()
            detail_url = tds[2].find("a").get("href")
            # print("###############detail_url ", detail_url)


            # detail_url = list_url.xpath("./td")[2].xpath("./a/@href")
            item['name'] = name
            item['related_drug'] = related_drug
            item['effect'] = effect
            # print("#########################################################################effct ",effect)
            yield item
        
        new_urls = soup.findAll("a",{'class':'page'})
        new_url = new_urls[len(new_urls)-1].get('href')
        print("new url : ",new_url)
        if new_url:
            yield scrapy.Request('http://db.yaozh.com'+new_url,callback=self.parse)


        