import json
from pprint import pprint
import configparser
import feedparser
import time

def ParseCfg(head, arg):
    #username = CfgP.ParseCfg('ZeusAccount','zeus.username')
    config = configparser.RawConfigParser()
    config.read('resources/app.ini')
    return config.get(head, arg)

def ReadJson(file):
	with open(file, 'r') as json_file:
	    return json.load(json_file)

def ParseRSS(RSS):

    result = None

    return result
