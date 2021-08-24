#from PyQt5.QtCore import Null
from mechanize.polyglot import getitem
import requests
import js2py
import mechanize
from threading import Thread


class get_email():
    def __init__(self,authors):
        self.authors = authors
        self.apisList = self.get_apis()
        self.get_all_authors_email()
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

    def get_page(self,authid,j,start):
        loop_counter = 0
        url ="http://api.elsevier.com/content/search/scopus?"
        header = {'Accept':'application/json','X-ELS-APIKey': self.API_KEY}
        param = {'start':str(start),'query' : 'AU-ID('+str(authid)+')','count' : '50','sort':'-coverDate'}
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
        return resp.json()

    def find_paper_urls(self,authid,j):
        start = int(self.papercount/50)*50
        page = self.get_page(authid,j,start)
        if page['search-results']['opensearch:totalResults'] == self.papercount+1: self.signal=2
        return list(map(lambda x : x['link'][2]['@href'],page['search-results']['entry'][:]))   
        
    def find_coded_string(self,document):
        l = "/cdn-cgi/l/email-protection#"
        index = 0 
        if l in document: self.signal=1
        else: 
            return
        index = document.index(l)
        document[index:].index('"')
        href = document[document.index(l):document.index(l)+document[index:].index('"')]
        href = 'file://'+ href
        return href   

    def decode_email(self,coded):
        if coded == None: return 'Null'
        r = js2py.eval_js('''    function r(e, t) {
        var r = e.substr(t, 2);
        return parseInt(r, 16)
            }''')
        n = js2py.eval_js('''    function n(n, c,r) {
                for (var o = "", a = r(n, c), i = c + 2; i < n.length; i += 2) {
                    var l = r(n, i) ^ a;
                    o += String.fromCharCode(l)
                }
                try {
                    o = decodeURIComponent(escape(o))

                } catch (u) {
                    console.log('ddd')
                }
                return o
            }''')
        email = n(coded,35,r) 
        print(email)
        return email

    def find_email(self,authid,j):
        b = mechanize.Browser()
        b.set_handle_robots(False)
        b._factory.is_html = True

        b.addheaders = [('User-agent',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454101'
                        )]

        self.papercount = 0
        self.signal = 0
        while not self.signal==2:
            urls = self.find_paper_urls(authid,j)
            for url in urls:
                res = b.open(url)
                coded = self.find_coded_string(res.read().decode())
                if coded ==None : self.signal=0
                if self.signal ==1 and coded!='':
                    email = self.decode_email(coded)
                    self.authors[authid]['email'] = email
                    return
                if self.signal == 2:
                    self.authors[authid]['email'] = 'Null'
                self.papercount+=1

        
    def get_all_authors_email(self):
        NUM = 40
        s = list(self.authors.keys())
        thread=[]
        if(NUM>len(s)):NUM = len(s)
        for i in range(len(s)):
            #s[i] = s[i][0:len(s[i])-1]
            print(s[i])
            if(i<NUM):
                thread.append(Thread(target = self.find_email,args =(s[i],i+1)))
                thread[i].start()
                continue
            f = False
            while(not f):
                for j in range(NUM):
                    if(not thread[j].is_alive()):
                        f = True
                        thread[j]=Thread(target = self.find_email,args =(s[i],j+1))
                        thread[j].start()
                        break
        for i in range(NUM):
            thread[i].join()

'''
a = {
    '16235591800':{},
    '55340514000':{},
    '49962082100':{},
    '8631242000':{},
    '6504196155':{},
    '57200295973':{},
    '24178954000':{}
}

e = get_email(a)
print(e.authors)'''