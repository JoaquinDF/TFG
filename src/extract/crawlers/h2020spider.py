import re
import time
from scrapy import Spider, Request
from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException


class SpiderInstance(Spider):
    name = 'h2020'
    start_urls = [
        'https://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/master_calls.html',
    ]
    collection = 'crawlers.h2020.topics'

    def parse(self, response):
        for a in response.xpath('//div//li/a[contains(@href, "calls")]'):
            url = a.xpath('./@href').extract_first()
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_challenge)

    def parse_challenge(self, response):
        with Xvfb() as xvfb:
            driver = webdriver.Chrome()
            try:
                driver.get(response.url)
                elements = []
                flag = True
                nxt = False
                while flag:
                    try:
                        elements = driver.find_elements_by_xpath('//div[@class="well-white"]')
                        if len(elements) is not 0 or nxt:
                            flag = False
                    except (NoSuchElementException, StaleElementReferenceException):
                        time.sleep(10)
                        nxt = True
                for elem in elements:
                    status = elem.find_element_by_css_selector('span.label').text
                    url = elem.find_element_by_css_selector('a').get_property('href')
                    yield Request(url, callback=self.parse_project, meta={'status': status})
            except WebDriverException:
                yield Request(response.url, callback=self.parse_challenge, dont_filter=True)
            finally:
                driver.quit()

    def parse_project(self, response):
        well = response.xpath('//div[@class="well"]')
        table = well.xpath('.//table')
        n = len(table[1].xpath('.//tr/td/text()').extract())

        data = dict()
        data['status'] = response.meta['status']
        data['topic'] = well.xpath('.//h3/text()').extract_first()
        data['topic_id'] = table[0].xpath('.//tr/td/text()').extract()[0]
        data['publication_date'] = table[0].xpath('.//tr/td/text()').extract()[1]
        data['types_of_action'] = re.sub(r'\s+', ' ', table[1].xpath('.//tr/td/text()').extract()[0])
        data['deadline_model'] = re.sub(r'\s+', ' ', table[1].xpath('.//tr/td/text()').extract()[4].split('\n')[1])
        data['opening_date'] = re.sub(r'\s+', ' ', table[1].xpath('.//tr/td/text()').extract()[4].split('\n')[2])
        if n > 9:
            data['deadline'] = re.sub(r'\s+', ' ', table[1].xpath('.//tr/td/text()').extract()[8])
            data['2nd_stage_deadline'] = re.sub(r'\s+', ' ', table[1].xpath('.//tr/td/text()').extract()[9])
        else:
            data['deadline'] = re.sub(r'\s+', ' ', table[1].xpath('.//tr/td/text()').extract()[7])
        data['id'] = data['topic_id']
        yield data
