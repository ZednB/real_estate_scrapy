import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Estate(scrapy.Spider):
    name = 'estate'
    allowed_domains = ['xn--80az8a.xn--d1aqf.xn--p1ai']
    start_urls = [
        'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?objStatus=0&place=0-44'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=60)

    def parse(self, response):
        service = Service(executable_path='./chromedriver.exe')
        options = webdriver.ChromeOptions()
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








import time

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse


# class EstateSpider(scrapy.Spider):
#     name = 'estate'
#
#     def __init__(self, *args, **kwargs):
#         super(EstateSpider, self).__init__(*args, **kwargs)
#
#         # Настройки WebDriver
#         options = Options()
#         options.add_argument("--headless")  # Запуск без GUI
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         options.add_argument("accept-language=en-US,en;q=0.9")
#
#         service = Service('/usr/local/bin/chromedriver')  # Путь к вашему chromedriver
#         self.driver = webdriver.Chrome(service=service, options=options)
#
#     def start_requests(self):
#         url = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?objStatus=0&place=0-44'
#         self.driver.get(url)
#         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(15)
#         html = self.driver.page_source
#         response = HtmlResponse(url=url, body=html, encoding='utf-8')
#         yield self.parse(response)
#
#     def parse(self, response):
#         items = response.xpath("//div[contains(@class, 'NewBuildingItem__Inner-sc-o36w9y-1')]")
#
#         for item in items:
#             title = item.xpath(".//div[contains(@class, 'NewBuildingItem__MainTitle-sc-o36w9y-6')]/text()").get()
#             address = item.xpath(".//div[contains(@class, 'NewBuildingItem__Text-sc-o36w9y-7')]/text()").get()
#             publication_date = item.xpath(
#                 ".//div[contains(@class, 'NewBuildingItem__PublicationDateIDWrapper-sc-o36w9y-8')]//p[2]/text()").get()
#
#             yield {
#                 'Title': title or "Title not found",
#                 'Address': address or "Address not found",
#                 'Publication Date': publication_date or "Publication date not found"
#             }
#
#     def closed(self, reason):
#         self.driver.quit()


    # def parse(self, response):
    #     if self.item_counter >= self.max_items:
    #         self.logger.info('Reached max items limit, stopping the spider.')
    #         return
    #
    #     # Извлечение ссылок на детали объявления
    #     for item in response.css('div.NewBuildingItem__Row-sc-o36w9y-13'):
    #         detail_url = item.css('a.NewBuildingItem__MainTitle-sc-o36w9y-6::attr(href)').get()
    #         if detail_url:
    #             yield response.follow(detail_url, self.parse_details)
    #
    #     # Пагинация (если есть страницы)
    #     next_page = response.css('a.next_page::attr(href)').get()
    #     if next_page:
    #         yield SeleniumRequest(url=next_page, callback=self.parse, wait_time=60)
    #
    # def parse_details(self, response):
    #     # Извлечение данных из страницы объявления
    #     yield {
    #         'title': response.css('a.NewBuildingItem__MainTitle-sc-o36w9y-6').get(),
    #         'address': response.css('p.NewBuildingItem__Text-sc-o36w9y-7.iUiqkY::text').get(),
    #         'id': response.css('p.NewBuildingItem__PublicationDateIDWrapper-sc-o36w9y-8 bxxXhO p::text').re_first(r'ID:\s*(\d+)'),
    #         'publication_date': response.css('p.NewBuildingItem__PublicationDateIDWrapper-sc-o36w9y-8 bxxXhO p::text').re_first(r'Опубликован:\s*([\d.]+)'),
    #         'completion_date': response.xpath('//p[contains(text(), "Ввод в эксплуатацию")]/following-sibling::p/text()').get(),
    #         'developer': response.xpath('//p[contains(text(), "Застройщик")]/following-sibling::p/text()').get(),
    #         'company_group': response.xpath('//p[contains(text(), "Группа компаний")]/following-sibling::p/text()').get(),
    #         'key_issuance': response.xpath('//p[contains(text(), "Выдача ключей")]/following-sibling::p/text()').get(),
    #         'avg_price_per_m2': response.xpath('//p[contains(text(), "Средняя цена за 1 м²")]/following-sibling::p/text()').get(),
    #         'sales': response.xpath('//p[contains(text(), "Распроданность квартир")]/following-sibling::p/text()').get(),
    #         'property_class': response.xpath('//p[contains(text(), "Класс недвижимости")]/following-sibling::p/text()').get(),
    #         'number_of_apartments': response.xpath('//p[contains(text(), "Количество квартир")]/following-sibling::p/text()').get(),
    # }