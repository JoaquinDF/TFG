import scrapy
import hashlib


class SpiderInstance(scrapy.Spider):
    name = 'cdti'
    start_urls = [
        'http://eshorizonte2020.cdti.es/index.asp?MP=7&MS=25&MN=3',
    ]
    collection = 'crawlers.cdti.projects'

    def parse(self, response):
        m = hashlib.sha256()

        for li in response.css('ul.tipo1 li'):
            m.update(li.css('::text').extract()[2])
            yield {
                'nombre_empresa': li.css('::text').extract()[0],
                'titulo_proyecto': li.css('::text').extract()[2],
                'sector': li.css('::text').extract()[3],
                'id': m.hexdigest(),
            }

        next_page = response.css('li.sigpag a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
