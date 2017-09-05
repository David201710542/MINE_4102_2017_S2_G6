import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from taller_1.scrapers.taller_1_g6_p1.items import Taller1G6P1Item
###from taller_1_g6_p1.items import Taller1G6P1Item

class Taller1G6P1(CrawlSpider):
	name = 'Taller1G6P1'
	item_count = 0
	limite_paginas = 100
	allowed_domains = ['uniandes.edu.co']
	start_urls = ['https://www.uniandes.edu.co/']
	
	rules = (
		Rule(LinkExtractor(
			#allow = ('*F*'),
			allow = (),
#			restrict_xpaths = ('//li[@class="leaf"]/a'),
#			restrict_xpaths = ('//li/a[contains(@href, "facultad")]'),
#            restrict_xpaths = ('//a[contains(@href, "facultad")]'),
			restrict_xpaths = ('//a[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "facultades")]'),
			unique = True
		),
		callback = 'filtrar_pagina',
		follow = True),
	)
	
	def filtrar_pagina(self, response):
		#dict_facultades = {}
		for pag in response.xpath('//li[@class="views-row"]'):
			self.item_count += 1
			if self.item_count > self.limite_paginas:
				raise CloseSpider('demasiadas_paginas')
			facultad = Taller1G6P1Item()
			facultad['facultad'] = pag.xpath('.//span[@class="field-content"]/text()').extract_first().strip()
			facultad['url'] = pag.xpath('.//a/@href').extract_first()
			yield facultad
#			dict_facultades[pag.xpath('.//span[@class="field-content"]/text()').extract_first().strip()] = pag.xpath('.//a/@href').extract_first()
#			yield dict_facultades
		#return dict_facultades
'''			yield {
#				'facultad': pag.xpath('.//span[@field-content]/text()').extract_first(),
				'facultad': pag.xpath('.//span[@class="field-content"]/text()').extract_first().strip(),
#				'url': response.url
				'url': pag.xpath('.//a/@href').extract_first()
			}
'''
