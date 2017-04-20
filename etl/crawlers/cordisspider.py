import scrapy
import urllib
from urllib.error import HTTPError
import xmltodict


class SpiderInstance(scrapy.Spider):
    name = 'cordis'
    start_urls = [
        'http://cordis.europa.eu/search/result_es?q=contenttype%3D%27project%27&searchType=advanced',
    ]
    collection = 'crawlers.cordis.projects'

    def parse(self, response):
        # comprobar error en la query
        if response.xpath('//div[@id="searchresult"]/text()').extract_first().find(
                'Failed to execute AciAction to server') is -1:
            for div in response.xpath('//div[@id="matchlist"]/div'):
                xml_page = div.xpath('./div[@class="col-right"]/div/span/a/@href').extract_first()
                xml_page = response.urljoin(xml_page)
                yield scrapy.Request(xml_page, callback=self.parseXml)

            next_page = response.xpath('//div[@id="pagelistbtm"]/a[text()=">"]/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        else:
            # forzar request
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)

    def parseXml(self, response):
        url = response.urljoin(response.xpath('//a[@class="printToXml"]/@href').extract_first())
        try:
            xml = xmltodict.parse(urllib.request.urlopen(url))
            xml['id'] = xml['project']['rcn']
        except HTTPError:
            # error 500
            xml = None
        yield xml
