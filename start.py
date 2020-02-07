#!/usr/bin/python

import functions.FilesOps as Fops
import functions.Connections as Conn
import functions.Refine as Ref
from pprint import pprint
import time

def ProgramStart():
    if Conn.ZeusConnect(Fops.ParseCfg('AppConfiguration','app.auth')).status_code == 200:
        print("Hello: " + Fops.ParseCfg('ZeusAccount','zeus.username'))
        print("You are now Connected ;)")
        conn = Conn.mainDb()
        websites = Fops.ReadJson(Fops.ParseCfg('AppPaths','app.websites'))
        print("-----------------------------------")
        print("--> Starting to retrieve RSS Feeds.")
        ok=0
        ko=0
        for x in websites['feeds']:
            if x['process'] == True:
                print("--> Connecting to "+x['webname'])
                print("--> URI: "+x['url'])
                dataFeed = Conn.FeedConnection(x['url'], x['user'])
                if len(dataFeed['entries']) == 0:
                    print("Error - check if its necessary auth or if your user/pass are correct.")
                    print("--> skipping URL")
                    ko+=1
                else:
                    print("--> URL ACCEPTED AND DATA GRABBED.")
                    ok+=1
            else:
                print("--> skipping "+x['webname'])
                print("--> URI: "+x['url'])
            Ref.eval(dataFeed, x['url'], conn)
            print("--> Entry "+x['webname']+" has been Processed.")
        print("-----------------------------------")
        print("["+str(ok) + "] - URL's Has been processed succesfully.")
        print("["+str(ok) + "] - URL's Cannot been processed.")
    else:
        print("Sorry, we cannot comprobate that you are allowed to use this software.")
        if Conn.ZeusConnect(urlAuth).status_code == 404:
            print("Our services are not available. Try later...")

def main():
    while Fops.ParseCfg('AppConfiguration','app.endless') == True:
        ProgramStart()
        time.sleep(int(Fops.ParseCfg('AppConfiguration','app.check')))
    else:
        ProgramStart()

main()
print("-----------------------------------")
print("--> ZeusMail Stopped correctly.")
exit(0)
