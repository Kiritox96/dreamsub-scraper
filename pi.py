import requests
import re
from pymongo import MongoClient
import datetime


class Anime():
    name = ''
    clean = ''
    episodes = []
    image = ''
    
    def __init__(self,name,clean,episodes,image):
        self.name = name
        self.clean = clean
        self.episodes = episodes
        self.image = image
    def str(self):
        return "The name is " + self.name + " and the clean is " + self.clean 

print("Richiesta iniziata")

r = requests.get("https://www.dreamsub.stream/A-Z")
print(r)
l = re.findall(r'<td>.+?</td>',r.text)
animes = []

for i in range(0,len(l)):
    if "href" in l[i]:
        anime = {}
        c = re.findall(r'/anime/.+?">',l[i])
        print("Cerca anime " + l[i])
        if c :
            print("Anime trovato")
            c = c[0].replace('/anime/','')
            c = c.replace('">','')       
            n = re.findall(r'">.+?</a>',l[i])
            n = n[0].replace('">','')
            n = n.replace('</a>','')
            urlInfo = "https://www.dreamsub.stream/anime/"+c
            print("URL anime " + urlInfo)
            if urlInfo != 'https://www.dreamsub.stream/anime/b-daman-crossfire':
                req = requests.get(urlInfo)
                pop = re.findall(r'<li>.+?</li>',req.text)
                episodes = []
                completo = []
                for j in range(0,len(pop)):
                    if "Episodio" in pop[j]:
                        s = re.findall(r'<i>.+?</i>',pop[j])[0]
                        s = s.replace('<i>','')
                        s = s.replace('</i>','')
                        episodes.append(s)
                for k in range(0,len(episodes)-1):
                    urlEp = "https://www.dreamsub.stream/anime/"+c+"/"+str(k+1)
                    print("URL episodio " + urlEp)
                    ret = requests.get(urlEp)
                    frame = re.findall(r'<iframe src=".+?" scrolling',ret.text)
                    if len(frame) > 0:
                        frame = frame[0].replace('<iframe src="','')
                        frame = frame.replace('" scrolling','')
                    else:
                        frame = "NO LINK"
                    if episodes[k] == '':
                        episodes[k] = "Episodio " + str(k+1)
                    completo.append([episodes[k],frame])
                image = re.findall(r'property="og:image".+?/>',req.text)
                image = image[0].replace('property="og:image"         content="','')
                image = image.replace('" />','')
                anime = Anime(n,c,completo,image)

                try: 
                    client = MongoClient("mongodb+srv://dai96:tammaro96@anime-mlyde.mongodb.net/test?retryWrites=true&w=majority")
                    print("Connessione a MongoDB avvenuta con successo") 
                    db = client['db']
                    collection = db['list']
                    post = {
                        "name": anime.name,
                        "clean": anime.clean,
                        "episodi": anime.episodes,
                        "image": anime.image,
                        "date": datetime.datetime.utcnow()
                    }
                    
                    query = { 'name' : anime.name }
                    collection.replace_one(query,post,True)
                    print("Anime aggiornato")
                    
                    print("Fine connessione")
                except:   
                    print("Connessione al DB persa") 
        else:
            print("Anime non disponibile")


                    
            
