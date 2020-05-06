# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.utils.markup import remove_tags

from otodom.items import OtodomItem


class OtodomMieszkaniaSpider(scrapy.Spider):
    name = 'otodomSpider'

    def __init__(self, city=None, *args, **kwargs):
        super(OtodomMieszkaniaSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.otodom.pl/sprzedaz/mieszkanie/{city}/']

    def parse(self, response):
        for offer in response.css("header.offer-item-header > h3"):
            link_to_offer = offer.xpath('.//a/@href').get()
            request_to_offer = Request(link_to_offer, callback=self.get_offer_details)
            yield request_to_offer

        next_page_link = response.xpath('//li[@class="pager-next"]/a/@href')
        if next_page_link:
            yield response.follow(next_page_link.extract_first(), callback=self.parse)

    def get_offer_details(self, response):
        offer_item = ItemLoader(item=OtodomItem(), selector=response)

        offer_item.add_value('link', response.url)
        offer_item.add_value('data_pobrania', str(datetime.now()))
        offer_item.add_xpath('tytul', "//h1[@class='css-1ld8fwi']/text()")
        offer_item.add_xpath('cena', '//div[@class="css-1vr19r7"]/text()')

        for script in response.xpath("//script[@type='application/ld+json']"):
            # there is usually a few <scripts> of this type in different order
            # and Im only looking for the one with the coordinates
            if 'GeoCoordinates' in script.get():
                json_offer = json.loads(remove_tags(script.extract()))

                lat = json_offer['@graph'][0]['geo']['latitude']
                lon = json_offer['@graph'][0]['geo']['longitude']
                address = json_offer['@graph'][0]['address']['streetAddress']
                description = json_offer['@graph'][0]['description']

                offer_item.add_value('lat', lat)
                offer_item.add_value('lon', lon)
                offer_item.add_value('address', address)
                offer_item.add_value('opis', description)

        offer_item.add_xpath('powierzchnia', '//li[contains(normalize-space(.), "Powierzchnia:")]/strong/text()')
        offer_item.add_xpath('rodzaj_zabudowy', '//li[contains(normalize-space(.), "Rodzaj zabudowy:")]/strong/text()')
        offer_item.add_xpath('okna', '//li[contains(normalize-space(.), "Okna:")]/strong/text()')
        offer_item.add_xpath('forma_wlasnosci', '//li[contains(normalize-space(.), "Forma własności:")]/strong/text()')
        offer_item.add_xpath('liczba_pokoi', '//li[contains(normalize-space(.), "Liczba pokoi:")]/strong/text()')
        offer_item.add_xpath('pietro', '//li[contains(normalize-space(.), "Piętro:")]/strong/text()')
        offer_item.add_xpath('ogrzewanie', '//li[contains(normalize-space(.), "Ogrzewanie:")]/strong/text()')
        offer_item.add_xpath('rynek', '//li[contains(normalize-space(.), "Rynek:")]/strong/text()')
        offer_item.add_xpath('liczba_pieter', '//li[contains(normalize-space(.), "Liczba pięter:")]/strong/text()')
        offer_item.add_xpath('stan_wykonczenia',
                             '//li[contains(normalize-space(.), "Stan wykończenia:")]/strong/text()')
        offer_item.add_xpath('czynsz',
                             '//li[contains(normalize-space(.), "Czynsz:")]/strong/text()')
        offer_item.add_xpath('forma_wlasnosci',
                             '//li[contains(normalize-space(.), "Forma własności:")]/strong/text()')
        offer_item.add_xpath('rok_budowy',
                             '//li[contains(normalize-space(.), "Rok budowy:")]/strong/text()')
        offer_item.add_xpath('material_budynku',
                             '//li[contains(normalize-space(.), "Materiał budynku:")]/strong/text()')

        extras = {'drzwi_okna_anty': 'drzwi / okna antywłamaniowe',
                  'pom_uzytkowe': 'pom. użytkowe',
                  'garaz_miejsce_park': 'garaż/miejsce parkingowe',
                  'piwnica': 'piwnica',
                  'ogrodek': 'ogródek',
                  'taras': 'taras',
                  'winda': 'winda',
                  'dwupoziomowe': 'dwupoziomowe',
                  'oddzielna_kuchnia': 'oddzielna kuchnia',
                  'klimatyzacja': 'klimatyzacja',
                  'system_alarmowy': 'system alarmowy',
                  'monitoring_ochrona': 'monitoring / ochrona',
                  'balkon': 'balkon',
                  'teren_zamkniety': 'teren zamknięty'}

        extras_list = response.xpath('//div[@class="css-1bpegon"]/ul/li/text()').extract()
        for key, value in extras.items():
            if value in extras_list:
                offer_item.add_value(key, 1)
            else:
                offer_item.add_value(key, 0)

        yield offer_item.load_item()
