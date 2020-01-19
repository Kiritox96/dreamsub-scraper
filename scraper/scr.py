import requests
import AdvancedHTMLParser
import datetime 
import pymongo
import time

r = requests.get("https://animeunity.it/anime.php?c=archive&page=*")
parser = AdvancedHTMLParser.AdvancedHTMLParser()
parser.parseStr(r.text)

links = []
children = parser.getElementsByClassName('archive-container visible-xs')[0].getAllNodes().getElementsByTagName('a')
for child in children:
    href = child.attributes.get('href')
    links.append("https://animeunity.it/"+href)

i = 0
for link in links:
    r = requests.get(link)
    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(r.text)
    info = parser.getElementsByClassName('card-body bg-light-gray')[0]
    print("Anime " + str(i) + " of " + str(len(links)))
    # data update
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # image 
    img = info.getAllNodes().getElementsByClassName('thumbnail').getAllNodes().getElementsByTagName('img')[0].attributes.get('src')
    title = " "
    generi = []
    trama = ''
    allIN = info.getAllNodes().getElementsByTagName('p')
    for p in allIN:
        text = p.innerHTML
        # title
        if 'TITOLO:' in text:
            uno = text.replace("\t","")
            due = uno.replace("\n","")
            title = due.replace("<b >TITOLO: </b>","")
        # generi
        if 'GENERI:' in text:
            gen = text.replace("<b >GENERI: </b>","")
            uno = gen.replace("\t","")
            due = uno.replace("\n","")
            tre = due.replace(" ","")
            generi = tre.split(",") 
        # trama
        if 'TRAMA:' in text:
            uno = text.replace("\t","")
            due = uno.replace("\n","")
            trama = due.replace("<b >TRAMA: </b>","")
            
    # episodi
    eps = parser.getElementById('myTabContent').getAllNodes().getElementsByClassName('ep-box col-lg-1 col-sm-1')
    episodi = []
    for ep in eps:
        ll = ep.getAllNodes().getElementsByTagName('a')[0].attributes.get('href')
        string = "https://animeunity.it/"+ll
        episodi.append(string)
    streaming = []
    j = 0
    for stream in episodi:
        print("Episodio " + str(j) + " of " + str(len(episodi)))

        r = requests.get(stream)
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(r.text)
        video = parser.getElementById('video-player').getAllNodes().getElementsByTagName('source')[0].attributes.get('src')
        streaming.append(video)
        time.sleep(1)
        j=j+1

            
    i = i+1
    data = {}
    data['name'] = title
    data['image'] = img
    data['trama'] = trama
    data['last_update'] = dt
    data['generi'] = generi
    data['episodi'] = streaming
    print('========== DATA ==========')
    print(data)      
    
    client = pymongo.MongoClient("mongodb+srv://dai96:tammaro96@anime-mlyde.mongodb.net/")
    db = client['archivi']
    coll = db['unity']
    if(coll.find_one({"name": title}) != None):
        print('========== Anime aggiornato ==========')
        coll.replace_one({"name": title}, data)
    else:
        print('========== Nuovo anime ==========')
        coll.insert_one(data)
    
    time.sleep(2)
