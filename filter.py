import requests
from threading import Thread

class filter_authors():
    def __init__(self, authors, minH, stime, ftime):
        self.authors = authors
        self.stime = stime
        self.ftime = ftime
        self.apisList = self.get_apis()
        self.filterHindex(minH)
        print(self.authors)
        self.filterAge()

        pass

    def filterHindex(self,minH):
        self.authors = dict(filter(lambda x : x[1]['hindex']>= minH,self.authors.items()))
        #print(self.authors)
        pass

    def get_apis(self):
        #init = 'bfd55d016ed308a6de2e9d39e7139dec'
        init = '8579fef278e4149355865b4bcdaed8f9'
        keys_list = open("keys.txt", 'r').readlines()
        self.API_KEY = init
        return keys_list

    def give_new_key(self):
        from random import choice
        self.API_KEY = choice(self.apisList).replace('\n','')

    def get_single_author_age(self,authid,j):
        loop_counter = 0
        url = "http://api.elsevier.com/content/search/scopus?"
        header = {'Accept':'application/json','X-ELS-APIKey': self.API_KEY}
        param = {'query' : 'AU-ID('+authid+')','date' : self.stime+'-'+self.ftime}
        while(True):
            resp = requests.get( url+authid, headers = header, params = param )
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
        self.authors[authid]['inperiod'] =  int(resp.json()['search-results']['opensearch:totalResults'])
    
    def get_all_authors_age(self):
        NUM = 40
        s = list(self.authors.keys())
        thread=[]
        if(NUM>len(s)):NUM = len(s)
        for i in range(len(s)):
            #s[i] = s[i][0:len(s[i])-1]
            print(s[i])
            if(i<NUM):
                thread.append(Thread(target = self.get_single_author_age,args =(s[i],i+1)))
                thread[i].start()
                continue
            f = False
            while(not f):
                for j in range(NUM):
                    if(not thread[j].is_alive()):
                        f = True
                        thread[j]=Thread(target = self.get_single_author_age,args =(s[i],j+1))
                        thread[j].start()
                        break
        for i in range(NUM):
            thread[i].join()

    def filterAge (self):
        self.get_all_authors_age()
        #print(self.authors)
        self.authors = dict(filter(lambda x : x[1]['documents'] == x[1]['inperiod'] ,self.authors.items()))
        print(self.authors)
        pass


