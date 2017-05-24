import re
from scrapy import Spider, Request


def parse_project(response):
    well = response.xpath('//div[@class="well"]')
    table = well.xpath('.//table')
    n = len(table[1].xpath('.//tr/td/text()').extract())

    data = dict()
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


class SpiderInstance(Spider):
    name = 'h2020'
    start_urls = [
        'https://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/master_calls.html',
    ]
    collection = 'crawlers.h2020.topics'

    def parse(self, response):
        for a in response.xpath('//div//li/a[contains(@href, "topics")]'):
            url = a.xpath('./@href').extract_first()
            url = response.urljoin(url)
            yield Request(url, callback=parse_project)
