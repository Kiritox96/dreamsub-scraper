import requests
from pymongo import MongoClient
import datetime


class Manga():
    name = ''
    ids = ''
    generi = []
    image = ''
    
    def __init__(self,name,ids,generi,image):
        self.name = name
        self.clean = clean
        self.episodes = episodes
        self.image = image
    def str(self):
        return "The name is " + self.name + " and the id is " + self.ids 



print("Request begin")

r = requests.get("https://www.mangaeden.com/api/list/1/")

l = r.json()['manga']

for i in range(0,len(l)):
    m = l[i]
    req = requests.get("https://www.mangaeden.com/api/manga/" + m['i'])
    m['info'] = req.json()
    print('Manga = ' + m['t'])
    caps = m['info']['chapters']
    capitoli = []
    if len(caps) > 0:
        for j in range(0,len(caps)):
            print('Capitolo ' + str(j+1))
            response = requests.get("https://www.mangaeden.com/api/chapter/" + caps[j][3])
            capitoli.append(response.json())
        m['capitoli'] = capitoli
        try: 
            client = MongoClient("mongodb+srv://admin:admin@manga-71w0f.mongodb.net/test?retryWrites=true&w=majority")
            print("Connected successfully!!!") 
            db = client['db']
            collection = db['list']
            collection.insert_one(m)
            client.close()
            print(m) 
        except:   
            print("Could not connect to MongoDB") 


                    
            
