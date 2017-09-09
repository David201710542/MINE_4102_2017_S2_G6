import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from taller_1.scrapers.taller_1_g6_p1.items import Taller1G6P1Item
###from taller_1_g6_p1.items import Taller1G6P1Item
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import re

class Taller1G6P1(CrawlSpider):
	name = 'Taller1G6P1'
	item_count = 0
	limite_paginas = 1000
	url_base = 'https://uniandes.edu.co'
	allowed_domains = ['uniandes.edu.co']
	start_urls = ['https://www.uniandes.edu.co/']

	def parse(self, response):
		v_orden = 1
		v_nivel = 1
		for pag in response.xpath('//div[contains(@class, "menu-ppal")]//ul[contains(@class, "dropdown-menu")]'):
			self.item_count += 1
			if self.item_count > self.limite_paginas:
				raise CloseSpider('demasiadas_paginas')
			facultad = Taller1G6P1Item()
			url = self.url_base + pag.xpath('.//a/@href').extract_first() if pag.xpath('.//a/@href').extract_first()[:1] == '/' else pag.xpath('.//a/@href').extract_first()
			facultad['facultad'] = pag.xpath('.//a/text()').extract_first().strip()
			facultad['url'] = url
			facultad['fuente'] = response.url
			facultad['orden'] = str(v_orden)
			facultad['origen'] = 0
			facultad['nivel'] = v_nivel
			yield facultad
			#url = urlparse.urljoin(response.url, url)
			yield scrapy.Request(url, callback = self.filtrar_facultades, meta = { 'origen': str(v_orden), 'nivel': v_nivel })
			v_orden += 1

	def filtrar_facultades(self, response):
		v_orden = 1
		v_origen = response.meta['origen']
		v_nivel = response.meta['nivel'] + 1
		for pag in response.xpath('//div[contains(@class, "view-vista-lista-departamentos")]//ul/li[contains(@class, "views-row")]'):
			self.item_count += 1
			if self.item_count > self.limite_paginas:
				raise CloseSpider('demasiadas_paginas')
			facultad = Taller1G6P1Item()
			url = self.url_base + pag.xpath('.//a/@href').extract_first() if pag.xpath('.//a/@href').extract_first()[:1] == '/' else pag.xpath('.//a/@href').extract_first()
			facultad['facultad'] = pag.xpath('.//span[@class="field-content"]/text()').extract_first().strip()
			facultad['url'] = url
			facultad['fuente'] = response.url
			facultad['orden'] = v_orden
			facultad['origen'] = str(v_origen)
			facultad['nivel'] = v_nivel
			yield facultad
			yield scrapy.Request(url, callback = self.filtrar_noticias, meta = { 'origen': str(v_origen) + '-' + str(v_orden), 'nivel': v_nivel })
			v_orden += 1

	def filtrar_noticias(self, response):
		v_orden = 1
		v_origen = response.meta['origen']
		v_nivel = response.meta['nivel'] + 1
		for pag in response.xpath('//div[contains(@class, "noticia-list")]//a[contains(@class, "item-nl")]'):
			self.item_count += 1
			if self.item_count > self.limite_paginas:
				raise CloseSpider('demasiadas_paginas')
			fecha_noticia = '<b>' + pag.xpath('.//div[contains(@class, "date-nl")]/p/text()').extract_first().strip() + '</b>'
			titulo_noticia = pag.xpath('.//div[contains(@class, "info-nl")]//p/text()').extract_first().strip()
			facultad = Taller1G6P1Item()
			facultad['facultad'] = fecha_noticia + ': ' + titulo_noticia
			facultad['url'] = ''
			facultad['fuente'] = response.url
			facultad['orden'] = v_orden
			facultad['origen'] = str(v_origen)
			facultad['nivel'] = v_nivel
			yield facultad
			v_orden += 1
