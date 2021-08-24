import requests

class get_auth_id:
    def __init__(self,query,stime,ftime):
        self.query = query
        self.stime = stime
        self.ftime = ftime
        self.authors = {}
        self.apisList = self.get_apis()
        #self.get_all_pages_result()
        
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

    def get_single_page(self,url,param={}):
        header = {'Accept':'application/json','X-ELS-APIKey': self.API_KEY}
        loop_counter = 0
        while (True):
            r = requests.get(url,headers=header,params=param)
            if(r.status_code == 200 ):break
            if(r.status_code == 429 ): self.give_new_key()
            loop_counter +=1
            if(loop_counter == 10):
                print("new error has arrived")
                print (r)
                print (r.json())
        return r.json()['search-results']
    
    def get_first_search_page_link(self):
        url = "https://api.elsevier.com/content/search/scopus?"
        parameter = {'query' : "SRCTITLE("+self.query+")",'date':str(self.stime)+'-'+str(self.ftime),'cursor' : '*','view' : 'COMPLETE'}
        #parameter = {'query' : "SRCTITLE("+self.query+")",'date':str(self.stime)+'-'+str(self.ftime),'view' : 'STANDARD'}

        links = self.get_single_page(url,param=parameter)['link']
        for item in links:
            if (item["@ref"] == "first"):
                return item['@href']
        
    def get_authors_id(self,page):
        entry = page['entry']

        for item in entry:
            if(not('author-count' in item and '$' in item['author-count'] ) or item['author-count']['$']=='0'):
                continue
            try:aut = item['author'][0]['authid']
            except:continue
            self.authors[aut]=[]
        pass

    def get_next_link(self,page):
        for item in page['link']:
            if (item["@ref"] == "next"):
                return item['@href']

    def is_last(self,current_link,page):
        return (current_link == self.get_next_link(page) )

    def get_all_pages_result(self):
        current_link = self.get_first_search_page_link()
        current_page = self.get_single_page(current_link)
        self.page = 1
        while not self.is_last(current_link,current_page):
            self.get_authors_id(current_page)
            current_link = self.get_next_link(current_page)
            if not current_link == None:
                current_page = self.get_single_page(current_link)
                
            print('next')
            self.page+=1


