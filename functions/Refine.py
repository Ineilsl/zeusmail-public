import re
import datetime
import hashlib
import functions.Connections as Conn
from pprint import pprint

def eval(data, url, conn):
    web = url.split('/')[2].split('.')
    web = web[len(web)-2]
    entryplus = 0
    entrynegative = 0
    print("--> Checking RSS...")
    if web == "tecnoempleo":
        print("--> Website supported!")
        data = ParseRSSTecno(data)
        SQL = "SELECT * FROM jobs;"
        sw = Conn.execute(conn, SQL)
        if sw is not None:
            SQLHEADER = "INSERT INTO jobs VALUES("
            SQLFOOTER = " julianday('now'));"
            for x in data['feed']:
                ac = ""
                for y in x.keys():
                    if (y == "Empresa:" or y == "Provincia:" or y == "Descripción:" or y == "Tecnologías:" or y == "Tipo de Contrato:"
                        or y == "Salario:" or  y == "Experiencia:" or "Funciones:" or y == "Formación mínima:" or y == "Titulo:"
                        or y == "Link:" or y == "ID" or y == "Publicacion:"):
                        ac = ac +"'"+x[y]+"'"+ ","
                SQL = SQLHEADER + ac + SQLFOOTER
                print("---->"+str(x.keys()))
                res = Conn.execute(conn, SQL)
                #entryplus+=1
                #except:
                #    entrynegative+=1
                #    print(SQL)
            print("--> Database Updated with the new Feed")
            print("Jobs added: "+str(entryplus))
            print("Jobs skipped: "+str(entrynegative))
        else:
            print("--> No changes detected in the Feed")
    else:
        print("--> Website is not supported")

def generateJson(args):
    list = {}
    for x in args:
        x = x.split("${;}")
        if len(x) <= 1:
            list[x[0]]="n/a"
        else:
            list[x[0]]=x[1]
    return list

def ParseRSSTecno(data):
    #feedparser.SANITIZE_HTML = 0
    list = {}
    list['feed'] = []
    cnt = 0
    for x in data.entries:
        #pprint(x['description'])
        cnt+=1
        title = re.sub('<[^<]+?>', '', x['title'])
        title = "Titulo:${;}"+str(title)
        link = re.sub('<[^<]+?>', '', x['link'])
        link = "Link:${;}"+str(link)
        id = str(link)+str(title)
        id = hashlib.md5(id.encode('utf-8')).hexdigest()
        id = "ID:${;}"+str(id)
        published = re.sub('<[^<]+?>', '', x['published']).replace(" +0100","").replace(",","")
        published = datetime.datetime.strptime(published, '%a %d %b %Y %H:%M:%S')
        published = published.strftime("%Y-%m-%d %H:%M:%S %z")
        published = "Publicacion:${;}"+str(published)
        description = re.sub('<[^<]+?>', '', x['description'])
        if cnt==3:
            pprint(description)
            exit()
        description = re.sub("(\\t+)", "${t}", description).replace("&nbsp;", "${;}").replace("\n","").split("${t}")
        description.pop()
        arr = []
        ac = ""
        sw = False
        for y in description:
            if sw == False:
                if y != "Formación mínima:${;}" and y != "Tipo de Contrato:${;}":
                    arr.append(y)
                else:
                    ac = y
                    sw = True
            else:
                dato = ac + y
                arr.append(dato)
                sw = False
        arr.append(title)
        arr.append(link)
        arr.append(id)
        arr.append(published)
        final = generateJson(arr)
        list['feed'].append(final)
    return list
