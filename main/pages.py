#coding:utf8
import re 
from bs4 import BeautifulSoup  
import requests 
from time import ctime,sleep
from threading import Thread


class URLThread(Thread):
    def __init__(self, url, timeout=10, allow_redirects=True):
        super(URLThread, self).__init__()
        self.url = url
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.response = None 
    
    def run(self):
        try: 
            print self.url   
            resp=requests.get(self.url, timeout = self.timeout, allow_redirects = self.allow_redirects)  
            print "hello...."
            text =  resp.text 
            soup = BeautifulSoup(text, "lxml")   
             
            trs = soup.find("ul",class_="hos_ul") 
            
            text=[]  
            lis = trs.find_all("li")
            for li in lis :
                txt = li.get_text().strip()
                txt = re.sub("\s","$",txt )
                txt = txt.replace("\n","").replace("\r","$")
                txt = re.sub("[$]+","$",txt )
                    
                hrefs =li.find_all("a")
                urls=set()
                for url in hrefs :
                    urls.add(url["href"])
                    
                print "%s$%s" % ( txt, ''.join( list( urls) ) )   
                    
            print "over "
        except Exception,e:
            print e 
             
# url="""http://www.chunyuyisheng.com/cooperation/wap/search_doctor_page/?partner=chunyu_wap&clinic_no=2&source_type=chunyu_weixin&from_type=triage_clinic_click"""

class Batch():
    
    def __init__(self): 
        pass 
    
    def fetch(self,url,page  ):  
        url =  url.format(page)
        
        
        
    def run(self): 
        threads = []
        url = "https://www.guahao.com/hospital/areahospitals?p=%E5%8C%97%E4%BA%AC&pi=1&pageNo={0}"
        pages= 10
        
        for page in range(1,pages): 
            a = URLThread(url.format(page))  
            threads.append( a  )

        for t in threads: 
            t.start()
            
        
 
if __name__ == "__main__":
    print "begin....."
    batch = Batch()
    batch.run() 
