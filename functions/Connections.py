import requests
import sqlite3
from sqlite3 import Error
import functions.FilesOps as Fops
import os
from pprint import pprint
import feedparser
import urllib

# DATABASE ZONE
def CreateDb(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        SQL = """ CREATE TABLE IF NOT EXISTS jobs (
                                                    Empresa text,
                                                    Provincia text,
                                                    Poblacion text,
                                                    Descripcion text,
                                                    Tecnologias text,
                                                    Contrato text,
                                                    Salario text,
                                                    Experiencia text,
                                                    Funciones text,
                                                    Formacion text,
                                                    Titulo text,
                                                    Link text,
                                                    ID text,
                                                    Publicacion text,
                                                    InsercionDB datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
                                                  ); """
        execute(conn, SQL)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def ConnectionDb(db):
    return sqlite3.connect(db)

def execute(conn, SQL):
    c = conn.cursor()
    c.execute(SQL)
    conn.commit()
    return c

    

def mainDb():
    if os.path.isfile(Fops.ParseCfg('AppPaths','app.database')) == False:
        sw = False
        cnt = 0
        while sw == False:
            try:
                print("Zeus DataBase not Found.")
                print("New Database will be created.")
                CreateDb(Fops.ParseCfg('AppPaths','app.database'))
                sw = True
            except:
                print("ERROR DataBase cannot be created, retrying..."+str(cnt))
                cnt-=1
                if cnt == 5:
                    print("ERROR Database cannot be created, check permissions.")
                    exit()
    print("Zeus Database detected, connecting...")
    return ConnectionDb(Fops.ParseCfg('AppPaths','app.database'))

# FEED ZONE
def FeedConnection(url, user):
    feed = None
    if user is not False:
        auth = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        auth.add_password(None, url, user['username'], user['password'])
        feed = feedparser.parse(url, handlers=[auth])
    else:
        feed = feedparser.parse(url)
    return feed

def ZeusConnect(url):
    return requests.get(url)
