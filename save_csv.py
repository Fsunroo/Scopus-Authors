import csv

class savecsv():
    def __init__(self,authors,fname,lname,email,aff,country,doc,cit,hind,id,output_name):
        self.authors = authors
        self.fname = fname
        self.lname = lname
        self.email = email
        self.aff = aff
        self.country = country
        self.doc = doc
        self.cit = cit
        self.hind = hind
        self.id = id
        self.output_name = output_name
        self.save()
    
    def save(self):
        for i in self.authors:
            self.authors[i]['id'] = str(i)

        header = ['id']
        if self.fname : header.append('name')
        if self.lname : header.append('surname')
        if self.aff : header.append('affilliation')
        if self.country : header.append('country')
        if self.doc : header.append('documents') 
        if self.cit : header.append('citation') 
        if self.hind : header.append('hindex') 
        if self.email : header.append('email') 

        with open (self.output_name,'w',newline='',encoding = 'utf-8') as f:
            w = csv.DictWriter(f,fieldnames = header, extrasaction='ignore')
            w.writeheader()
            w.writerows(list(self.authors.values()))
            f.close()


        
        
        
