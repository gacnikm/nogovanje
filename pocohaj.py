import os
import ssl
import urllib
from urllib.request import Request

from parsel import Selector

from db import db, Igralec, PATH

db.init(os.path.join(PATH, 'db.sqlite'))
db.connect()
db.drop_tables([Igralec])
db.create_tables([Igralec])


def pocohaj_url(url):
    context = ssl.SSLContext()
    context.verify_mode = ssl.CERT_OPTIONAL
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    return response.read()


def pocohaj_igralce(stran):
    content = pocohaj_url(stran)
    num_sodniki = 0

    selector = Selector(content.decode('utf-8'))

    # stevilo sodnikov
    sodniki = selector.xpath("//div[@class='sodniki']/table/tr[1]/td[2]/text()").extract_first("")

    if sodniki:
        num_sodniki = len(sodniki.split(",")) - 1

    # igralci
    tables = selector.xpath("//table")
    tables = tables[1:3]

    for table in tables:
        ekipa = table.xpath(
            "./thead/tr/th/text()").extract_first("").strip()
        rows = table.xpath(
            "./tbody/tr")
        rows = rows[:11]
        for row in rows:
            ime = row.xpath("./td[2]/text()").extract_first("").strip()

            # kapetan = row.xpath("./td[3]/span[contains(@class,'box-blue')]/text()").extract_first(None)
            # if kapetan:
            #  igralec.rokovanj += 11+1+2*num_sodniki

            igralec, created = Igralec.get_or_create(ime=ime, ekipa=ekipa)
            igralec.rokovanj += 11 + num_sodniki
            igralec.save()


def pocohaj_stran(url):
    content = pocohaj_url(url)

    selector = Selector(content.decode('utf-8'))

    rows = selector.xpath(
        "//tr[contains(@class,'hidden-xs odigrano')]/td[contains(@class,'rezultat')]/a/@href").extract()

    for row in rows:
        splitted = row.split("?")
        splitted = splitted[1]
        url = "https://www.prvaliga.si/tekmovanja/default.asp?" + splitted + "&prikaz=4&id_menu=221"
        pocohaj_igralce(url)

pocohaj_stran("https://www.prvaliga.si/tekmovanja/?id_menu=101")
