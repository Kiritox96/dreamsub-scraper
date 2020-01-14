import requests
import AdvancedHTMLParser
import pymongo

while(1):
    
    ultimi = []
    r = requests.get('https://www.animeworld.cc/updated')
    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(r.text)
    children = parser.getElementsByClassName('film-list')[0].getElementsByClassName('item')
    for child in children:
        name = child.getElementsByClassName('name')[0].innerHTML
        ep = child.getElementsByClassName('ep')[0].innerHTML
        img = child.getAllNodes().getElementsByTagName('img')[0].attributes.get('src')
        data = {}
        data['name'] = name
        data['numero'] = ep
        ultimi.append(data)    
    obj = {}
    obj['data'] = ultimi
    obj['type'] = 'new'
    print(obj)

    client = pymongo.MongoClient("mongodb+srv://dai96:tammaro96@anime-mlyde.mongodb.net/")
    db = client['archivi']
    coll = db['nuovi']
    if(coll.find_one({"type": 'new'}) != None):
        print('========== Dati aggiornati ==========')
        coll.replace_one({"type": 'new'}, obj)
    else:
        print('========== Nuovi dati ==========')
        coll.insert_one(obj)
        
    time.sleep(1000)

