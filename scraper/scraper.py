import requests
import AdvancedHTMLParser
import datetime 
import pymongo
import time

while(1):
    
    links = []

    for i in range(1,119): # 1..119
        r = requests.get("https://www.animeworld.cc/az-list?page=" + str(i))
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(r.text)
        children = parser.getElementsByClassName('items')[0].getElementsByClassName('item')
        for i in range(1,len(children)-1):
            ch = children[i].getElementsByClassName('name')[0].attributes.get('href')
            links.append(ch)

    for link in links:
        r = requests.get(link)
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(r.text) 
        
        # div delle info
        info = parser.getElementsByClassName('widget info')[0]
        # name anime
        name = info.getElementsByClassName('thumb col-md-5 hidden-sm hidden-xs')[0].getAllNodes().getElementsByTagName('img')[0].attributes.get('alt')
        # link image
        img = info.getElementsByClassName('thumb col-md-5 hidden-sm hidden-xs')[0].getAllNodes().getElementsByTagName('img')[0].attributes.get('src')
        # trama
        trama = info.getElementsByClassName('desc')[0].innerHTML
        # data update
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # generi
        lista_generi = []
        genere = info.getElementsByClassName('info col-md-19')[0].getElementsByClassName('meta col-sm-12')[0].getAllNodes().getElementsByTagName('a')
        for gen in genere:
            lista_generi.append(gen.innerHTML)
        # lista episodi  
        streaming = []
        try:
            # vedere su vvvid
            isVVVID = False
            alertVVVID = parser.getElementById('animeId').getElementsByClassName('tab active')[0].innerHTML
            if 'VVVVID' in alertVVVID:
                print("========== Anime su vvvid ==========")
                isVVVID = True
            # streaming episodi
            anime = parser.getElementById('animeId').
            active = parser.getElementById('animeId').getElementsByClassName('server active')[0].getAllNodes().getElementsByTagName('a')
            #print(active)
            
            for stream in active:
                episode = stream.attributes.get('data-id')
                if isVVVID:
                
                    streaming.append("https://www.vvvvid.it/channel/0/you&r")
                else:
                    streaming.append("https://www.animeworld.cc/ajax/episode/serverPlayer?id="+str(episode))
            
        except:
            print("========== Serie non disponibile ==========")
            print(name)
        data = {}
        data['name'] = name
        data['image'] = img
        data['last_update'] = dt
        data['generi'] = lista_generi
        data['episodi'] = streaming
        print('========== DATA ==========')
        print(data)
        
        client = pymongo.MongoClient("mongodb+srv://dai96:tammaro96@anime-mlyde.mongodb.net/")
        db = client['archivi']
        coll = db['world']
        if(coll.find_one({"name": name}) != None):
            print('========== Anime aggiornato ==========')
            coll.replace_one({"name": name}, data)
        else:
            print('========== Nuovo anime ==========')
            coll.insert_one(data)
        

    time.sleep(1000)
        
    