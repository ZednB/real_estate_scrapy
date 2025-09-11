import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Estate(scrapy.Spider):
    name = 'estate'
    allowed_domains = ['xn--80az8a.xn--d1aqf.xn--p1ai']
    start_urls = [
        'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D'
        '0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0'
        '%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?objStatus'
        '=0&place=0-44'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=60)

    def parse(self, response):
        driver = response.meta.get('driver')
        if driver is None:
            self.logger.error("Driver not found in response meta!")
            return

        for item in response.css('div.NewBuildingItem__DataRows-sc-o36w9y-12'):
            yield {
                'title': item.css('a.NewBuildingItem__MainTitle-sc-o36w9y-6::text').get(),
                'address': item.css('p.NewBuildingItem__Text-sc-o36w9y-7.iUiqkY::text').get(),
                'id': item.css('p.NewBuildingItem__Text-sc-o36w9y-7.iUiqkY::text').re_first(r'ID:\s*(\d+)'),
                'completion_date': item.css('p.NewBuildingItem__InfoValue-sc-o36w9y-11.geeeKY::text').re_first(
                    r'III кв\. \d{4}'),
                'developer': item.css('p.NewBuildingItem__InfoValue-sc-o36w9y-11.geeeKY::text').re_first(r'ООО\s.+'),
            }
