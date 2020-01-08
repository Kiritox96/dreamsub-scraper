import requests
import AdvancedHTMLParser
import pymongo
import datetime
import time

def main():
    updateCalendar("https://dreamsub.stream/")
    
    for i in range(0,64):
        print("Init the anime list " + str(i) + " of 64")
        if(i==0):
            initiate('https://dreamsub.stream/search/?q=')
            
        # ===============================FILTRO====================================
        else:
            initiate('https://dreamsub.stream/search/?q=&page='+str(i))
            
    for anime in results:
        # ===========================FILTRO LETTERA CLEAN ANIME ======================================
        #if(anime.clean[0] == 'o'):
        anime = getInfoEpisodes('https://dreamsub.stream/anime/'+anime.clean,anime)
    
        print("Oggetto risultato:")
        print(anime.__dict__)
        try: 
            client = pymongo.MongoClient("mongodb+srv://dai96:tammaro96@anime-mlyde.mongodb.net/")
            print("Connessione a MongoDB avvenuta con successo") 
            db = client['db']
            coll = db['animes']
            print(coll.find_one({"clean": anime.clean}))
            if(coll.find_one({"clean": anime.clean})):
                coll.replace_one({"clean": anime.clean}, anime.__dict__)
                print("replace")
            else:
                print("insert")
                coll.insert_one(anime.__dict__)
        except:   
            print("Could not connect to MongoDB") 
        #======================================= FINE FILTRO====================================
    
def getInfoEpisodes(url,anime):
    r = requests.get(url)
    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(r.text)

    player = parser.getElementById('media-play')
    if(player):
        if(player.children[0]):
            child = player.children[0]
            if(child):
                listren = child.attributes.get('src')
                if(listren):
                    anime.trailer = listren
       
    trama = parser.getElementById('tramaLong')
    if(trama):
        # TODO = Le stringhe riportate hanno dei caratteri speciali non decodificati
        anime.trama = trama.innerHTML 
  
    list_episodi = []
    children = parser.getElementsByClassName('ep-item')
    i = 1
    for child in children:
        print("Init episodio " + str(i) + " of anime " + anime.name)
        if(child):
            primo = child.getAllNodes().getElementsByTagName('a')[0]
            titolo = primo.innerHTML
            
            href = primo.attributes.get('href')
            
            secondo = child.getAllNodes().getElementsByTagName('span')[0]
            data = secondo.innerHTML
    
            episodio = Episodio(titolo, "https://dreamsub.stream"+href, data)
            # ==================== FILTRO EPISODI TBA =======================
            '''
            if(episodio.titolo != 'TBA'):
            '''
            tupla = getLinksEpisodes(episodio.url,anime,episodio)
            episodio = tupla[0]
            anime = tupla[1]
            #=================FINE TBA===========================

            list_episodi.append(episodio.__dict__)
            i = i + 1
        
  
    anime.episodi = list_episodi
    return anime
  

def getLinksEpisodes(url,anime,episodio):
    r = requests.get(url)
    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(r.text)

    select = parser.getElementById('selectServerSub')
    streamings = []

    if(select):
        for child in select.children:
            value = child.attributes.get('value')
            streamings.append(value)
    select_ita = parser.getElementById('selectServerDub')
    streamings_ita = []

    if(select_ita):
        for child in select_ita.children:
            value = child.attributes.get('value')
            streamings_ita.append(value)
   
  
 
    only = parser.getElementsByClassName('onlyDesktop')
    downloads = []

    if(only):
        children1 = only.getAllNodes()[0]
        if(children1):
            children2 = children1.children[0]
            if(children2):
                children3 = children2.children[0]
                if(children3):
                    elements = children3.getAllNodes().getElementsByTagName('a')
                    if(elements):
                        for elem in elements:
                            href = elem.attributes.get('value')
                            if(href.length>0):
                                downloads.append(href[0])
                         
    episodio.links_streaming = streamings
    episodio.links_streaming_ita = streamings_ita
    episodio.links_download = downloads
    return (episodio,anime)

    
def initiate(url):
    time.sleep( 0.2 )
    r = requests.get(url)
    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(r.text)
    links = parser.getElementsByClassName('tvBlock')
    for link in links:
        name = ''
        if(link.children[0]):
            name = str(link.children[0].getAllNodes()[0].children[0].innerHTML)
        image_url = ''
        clean = ''
        if(link.children[1]):
            child_2 = str(link.children[1].style.background)
            fr = child_2.index('url')+4
            to = child_2.index(')')
            image_url = "https://dreamsub.stream" + child_2[fr:to]
            from_clean = image_url.index('150/')+4
            to_clean = image_url.index('.png')
            clean = image_url[from_clean:to_clean]
        generi = []
        if(link.children[3]):
            child_3 = link.children[3].getAllNodes().getElementsByTagName('a')
            for gen in child_3:
                generi.append(gen.innerHTML)
        anime = Anime(clean,name,image_url,generi)
        results.append(anime)

def updateCalendar(url):
    print("Init calendar")
    try:
        time.sleep( 0.2 )
        r = requests.get(url)
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(r.text)
        link = parser.getElementsByTagName('tbody')
        # giorni
    
        lunedi = []
        martedi = []
        mercoledi = []
        giovedi = []
        venerdi = []
        sabato = []
        domenica = []
    
        if(link[0]):
            gg = link[0].getElementsByClassName('linkAlternati')
            i = 0
            for giorni in gg:
                
                day = giorni.children
                list_day = []
                for an in day:
                    ll = an.getAllNodes().getElementsByTagName('a')[0].attributes.get('href')[7::]
                    list_day.append(ll)
                if(i == 0):
                    lunedi = list_day
                elif (i == 1):
                    martedi = list_day
                elif (i == 2):
                    mercoledi = list_day
                elif (i == 3):
                    giovedi = list_day
                elif (i == 4):
                    venerdi = list_day
                elif (i == 5):
                    sabato = list_day
                elif (i == 6):
                    domenica = list_day
                    
                    
                i = i + 1
                print(list_day)                
                print("=====")
     
        client = pymongo.MongoClient("mongodb+srv://dai96:tammaro96@anime-mlyde.mongodb.net/")
        db = client['db']
        coll = db['others']
        obj = {"type":"calendario","date":datetime.datetime.utcnow(),"lunedi": lunedi,"martedi": martedi,"mercoledi": mercoledi,"giovedi": giovedi,"venerdi": venerdi,"sabato": sabato,"domenica": domenica}
        if(coll.find_one({"type": "calendario"}) != None):
            coll.replace_one({"type": "calendario"}, obj)
        else:
            coll.insert_one(obj)
        



    except:   
        print("Could not connect to MongoDB to update calendar") 
    
        
        
        

class Anime:
    image = ''
    name = ''
    clean = ''
    trailer='' 
    trama=''
    generi = []
    episodi= []

    def __init__(self, clean, name, image, generi):
        self.generi = generi
        self.image = image
        self.name = name
        self.clean = clean
        self.timestamp = datetime.datetime.utcnow()

   
class Episodio:
    titolo = ''
    url = ''
    data = ''
    links_streaming = []
    links_download = []
    links_streaming_ita = []

    def __init__(self, titolo, url, data):
        self.data = data
        self.url = url
        self.titolo = titolo
        self.timestamp = datetime.datetime.utcnow()

        
  

results=[]
main()