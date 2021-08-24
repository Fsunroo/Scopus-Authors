import requests
from threading import Thread

class get_info():
    def __init__(self,authors):
        self.authors = authors
        self.apisList = self.get_apis()
        self.get_all_authors_info()


    def get_apis(self):
        #init = 'bfd55d016ed308a6de2e9d39e7139dec'
        init = '8579fef278e4149355865b4bcdaed8f9'
        keys_list = open("keys.txt", 'r').readlines()
        self.API_KEY = init
        return keys_list

    def give_new_key(self):
        from random import choice
        self.API_KEY = choice(self.apisList).replace('\n','')

    def load_single_author_info(self,authid,j):
        loop_counter = 0
        url = "https://api.elsevier.com/content/author/author_id/"
        header = {'Accept':'application/json','X-ELS-APIKey': self.API_KEY}
        while(True):
            resp = requests.get( url+authid, headers = header, params = {'view':'ENHANCED'} )
            if(resp.status_code == 200 ):break
            if(resp.status_code == 429 and j == 1): self.give_new_key()
            if(resp.status_code == 429):continue
            if(resp.status_code == 404):break
            
            loop_counter +=1
            if(loop_counter > 0):
                print("new error has arrived" + authid)
                print (resp)
                print (resp.json())
                break
        if(resp.status_code == 404):return
        if(not isinstance(resp.json()['author-retrieval-response'], list)):return
        return resp.json()
    
    def get_singe_author_info(self,authid,j):
        j = self.load_single_author_info(authid,j)

        surname = j["author-retrieval-response"][0]['author-profile']['preferred-name']['surname']
        givenName = j["author-retrieval-response"][0]['author-profile']['preferred-name']['given-name']
        documents = j["author-retrieval-response"][0]["coredata"]["document-count"]
        citation = j["author-retrieval-response"][0]["coredata"]["citation-count"]
        HIndex = j["author-retrieval-response"][0]["h-index"]
        if 'affiliation-current' not in j['author-retrieval-response'][0]['author-profile'] :
            affiliation = "NotGIVEN"
        else:
            if(not isinstance(j['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation'], list)):
                affiliation = j['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']['ip-doc']
            else:
                affiliation = j['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation'][0]['ip-doc']
        if('afdispname' not in affiliation):
            affiliation = "NotGIVEN"
            country = "NotGIVEN"
        else:
            if('address' not in affiliation or affiliation['address']==None or'country' not in affiliation['address']):
                country = "NotGIVEN"
            else:
                country = affiliation['address']['country']
            affiliation=affiliation['afdispname']

        if(givenName==None):givenName = "NotGIVEN"
        if(surname==None):surname = "NotGIVEN"
        if(documents == None):documents = "0"
        if(citation == None):citation = "0"
        if(HIndex == None):HIndex = "0"
        self.authors[authid] = {'name':givenName,
                'surname':surname,
                'documents':int(documents),
                'citation':int(citation),
                'hindex':int(HIndex),
                'affilliation':affiliation,
                'country':country}
    
    def get_all_authors_info(self):
        NUM = 40
        s = list(self.authors.keys())
        thread=[]
        if(NUM>len(s)):NUM = len(s)
        for i in range(len(s)):
            #s[i] = s[i][0:len(s[i])-1]
            print(s[i])
            if(i<NUM):
                thread.append(Thread(target = self.get_singe_author_info,args =(s[i],i+1)))
                thread[i].start()
                continue
            f = False
            while(not f):
                for j in range(NUM):
                    if(not thread[j].is_alive()):
                        f = True
                        thread[j]=Thread(target = self.get_singe_author_info,args =(s[i],j+1))
                        thread[j].start()
                        break
        for i in range(NUM):
            thread[i].join()
'''
file = open("c_out.txt", "r") 
s = file.readlines()

auths = get_info(s)
print(auths.authors)'''