import requests
import sqlite3
import os
import feedparser
import urllib
import re
from pprint import pprint
from sqlite3 import Error
import functions.FilesOps as Fops

def eval(data, url):
    web = url.split('/')[2].split('.')
    web = web[len(web)-2]
    if web == "tecnoempleo":
        print("La pagina web que ha definido esta soportada.")
        # data = ParseRSSTecno(data)
    else:
        print("La pagina web que ha definido no esta soportada.")

def ParseRSSTecno(data):
    feedparser.SANITIZE_HTML = 0
    for x in data.entries:
        title = re.sub('<[^<]+?>', '', x['title'])
        link = re.sub('<[^<]+?>', '', x['link'])
        guid = re.sub('<[^<]+?>', '', x['guid'])
        description = re.sub('<[^<]+?>', '', x['description'])
        published = re.sub('<[^<]+?>', '', x['published'])
        pprint(title)
        pprint(link)
        pprint(guid)
        pprint(description)
        pprint(published)
        exit()
