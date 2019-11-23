# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def filter_price(value):
    # \xa0 - space
    value = value.replace('zł', "").replace("\xa0", "").replace(",", ".").replace(".00", "") \
        .replace("\n", "").replace(" ", "")
    try:
        float(value)
        return value
    except ValueError:
        return None


def filter_powierzchnia(value):
    value = value.replace(' m²', "").replace("\xa0", "").replace(",", ".").replace(".00", "") \
        .replace("\n", "").replace(" ", "")
    try:
        float(value)
        return value
    except ValueError:
        return None


class OtodomItem(scrapy.Item):
    tytul = scrapy.Field(output_processor=TakeFirst())
    cena = scrapy.Field(input_processor=MapCompose(filter_price), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst())
    lat = scrapy.Field(output_processor=TakeFirst())
    lon = scrapy.Field(output_processor=TakeFirst())
    powierzchnia = scrapy.Field(input_processor=MapCompose(filter_powierzchnia), output_processor=TakeFirst())
    rodzaj_zabudowy = scrapy.Field(output_processor=TakeFirst())
    czynsz = scrapy.Field(input_processor=MapCompose(filter_price), output_processor=TakeFirst())
    okna = scrapy.Field(output_processor=TakeFirst())
    forma_wlasnosci = scrapy.Field(output_processor=TakeFirst())
    liczba_pokoi = scrapy.Field(input_processor=MapCompose(str.strip),
                                output_processor=TakeFirst())
    pietro = scrapy.Field(input_processor=MapCompose(str.strip),
                          output_processor=TakeFirst())
    ogrzewanie = scrapy.Field(output_processor=TakeFirst())
    rynek = scrapy.Field(output_processor=TakeFirst())
    liczba_pieter = scrapy.Field(output_processor=TakeFirst())
    stan_wykonczenia = scrapy.Field(output_processor=TakeFirst())
    opis = scrapy.Field(input_processor=MapCompose(str.strip),
                        output_processor=TakeFirst())
    rok_budowy = scrapy.Field(input_processor=MapCompose(str.strip),
                              output_processor=TakeFirst())
    material_budynku = scrapy.Field(output_processor=TakeFirst())

    balkon = scrapy.Field(output_processor=TakeFirst())
    drzwi_okna_anty = scrapy.Field(output_processor=TakeFirst())
    pom_uzytkowe = scrapy.Field(output_processor=TakeFirst())
    garaz_miejsce_park = scrapy.Field(output_processor=TakeFirst())
    piwnica = scrapy.Field(output_processor=TakeFirst())
    ogrodek = scrapy.Field(output_processor=TakeFirst())
    taras = scrapy.Field(output_processor=TakeFirst())
    winda = scrapy.Field(output_processor=TakeFirst())
    dwupoziomowe = scrapy.Field(output_processor=TakeFirst())
    oddzielna_kuchnia = scrapy.Field(output_processor=TakeFirst())
    klimatyzacja = scrapy.Field(output_processor=TakeFirst())
    system_alarmowy = scrapy.Field(output_processor=TakeFirst())
    monitoring_ochrona = scrapy.Field(output_processor=TakeFirst())
    teren_zamkniety = scrapy.Field(output_processor=TakeFirst())

    data_pobrania = scrapy.Field(output_processor=TakeFirst())
