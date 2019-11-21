import requests
import ssl
import re
import pymongo
import datetime
import time

def find_between(s,first,last):
    try:
        start = s.index(first)+len(first)
        end = s.index(last,start)
        return s[start:end]
    except ValueError:
        return ""


while 1:
    print("Richiesta iniziata")
    
    r = requests.get("https://www.dreamsub.stream/")
    print(r)

    l = re.findall(r'<ul class="linkAlternati">.+?</ul>',r.text)
    settimana = []
    for i in range(0,len(l)):
        giorno = []
        li = re.findall(r'">.+?</a>',l[i])
        for j in range(0,len(li)):
            name = ''
            if j == 0 :
                name = find_between(li[j],'Streaming">','</a>')
            else:
                name = find_between(li[j],'">','</a>')
            
            giorno.append(name)
        
        settimana.append(giorno)
    post = {
        "lunedi": settimana[0],
        "martedi": settimana[1],
        "mercoledi": settimana[2],
        "giovedi": settimana[3],
        "venerdi": settimana[4],
        "sabato": settimana[5],
        "domenica": settimana[6],
        "date": datetime.datetime.utcnow(),
        "type": "calendario"
    }
    print(post)
    
    client = pymongo.MongoClient("mongodb+srv://dai96:tammaro96@anime-mlyde.mongodb.net/test?retryWrites=true&w=majority",ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
    print("Connessione a MongoDB avvenuta con successo") 
    db = client['db']
    collection = db['others']

    query = { 'type' : 'calendario' }
    collection.replace_one(query,post,True)
    print("Anime aggiornato")
    
    print("Fine connessione")
    time.sleep(80000) 
    pass
