#coding:utf8
import re 
from bs4 import BeautifulSoup  
import requests 
from time import ctime,sleep
from threading import Thread

class URLThread(Thread):
    result = []
    
    #(self.url.format(page),self.parent_tag,self.parent_tag_seq, self.dest_tag,  detail_href_seq)  
    def __init__(self, page,url,parent_tag,parent_tag_seq,dest_tag, detail_href_index,job_path, timeout=10, allow_redirects=True):
        super(URLThread, self).__init__()
        self.page = page 
        self.url = url
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.response = None
        self.detail_href_index = detail_href_index 
        self.parent_tag = parent_tag 
        self.parent_tag_seq = parent_tag_seq 
        self.dest_tag  = dest_tag
        self.job_path = job_path
        
        
    def run(self):
        try: 
            print "be downloadding    ,%s" % ( self.url )     
            resp=requests.get(self.url, timeout = self.timeout, allow_redirects = self.allow_redirects)   
            resp.encoding = 'UTF-8' 
            text =  resp.text 
            soup = BeautifulSoup(text, "lxml")    
            trs = soup.select(self.parent_tag)[self.parent_tag_seq] 
            trs = trs.select(self.dest_tag) 
            text=[]
            download_file_full_name="%s/%s" % ( self.job_path,self.page  )
            with open(download_file_full_name,"w") as fw:
                for li in trs  :
                    txt = li.get_text("|").replace("|\n","").replace("\r\n","")
                    txt = re.sub("\|\s*","|",txt )
                    txt = re.sub("\s*\|","|",txt ) 
                        
                    hrefs =li.find_all("a") 
                    href=""
                    if hrefs:
                        href = hrefs[self.detail_href_index]["href"]
                        
                    data =  "%s|%s" % ( txt, href  )  
                    fw.write( data )
                    fw.write("\n")
            
            print "writed %s " % ( download_file_full_name )   
        except Exception,e:
            print e 
            
            
    def get_result(self):
        return self.result
    
class PAPA():
    def __init__(self,*args,**kwargs):   
        print kwargs
        assert "split_page_url" in kwargs 
        self.split_page_url =kwargs["split_page_url"] 
        
        assert "parent_tag" in kwargs 
        self.parent_tag =kwargs["parent_tag"] 
        
        assert "parent_tag_seq" in kwargs 
        self.parent_tag_seq =kwargs["parent_tag_seq"] 
        
        assert "dest_tag" in kwargs 
        self.dest_tag =kwargs["dest_tag"] 
        
        assert "detail_href_index" in kwargs 
        self.detail_href_index =kwargs["detail_href_index"] 
        
        assert "pages" in kwargs 
        self.pages =kwargs["pages"] 
        
         
        assert "job_name" in kwargs 
        self.job_name =kwargs["job_name"]  
        
        assert "job_path" in kwargs 
        self.job_path =kwargs["job_path"]   
        
        try:
            import os  
            if not os.path.exists( self.job_path  ):
                os.mkdir( self.job_path )
        except Exception,e:
            print e 
        
    def run(self): 
        threads = [] 
        pages= int(self.pages)
        detail_href_index = self.detail_href_index 
        for page in range(1,pages): 
            a = URLThread(
                          page,
                          self.split_page_url.format(page),
                          self.parent_tag,
                          self.parent_tag_seq, 
                          self.dest_tag,  
                          detail_href_index,
                          self.job_path
                          )  
            threads.append( a  )

        for t in threads: 
            t.start() 
        for t in threads: 
            t.join()      
        
        print "------"
        data = []
        for t in threads:
            result  = t.get_result()
            for line in result : 
                print  line 
                data.append(line)
        return data
if __name__ == "__main__":
    url="https://www.guahao.com/search/expert?standardDepartmentId=7f67f180-cff3-11e1-831f-5cf9dd2e7135&sort=0&fg=1&standardDepartmentName=%E5%A6%87%E4%BA%A7%E7%A7%91&p=%E5%85%A8%E5%9B%BD&iSq=1&consult=2&pageNo=1"
    papa = PAPA(
                        split_page_url = url,   
                        parent_tag = "html > body > div > div > div > div > div > ul",
                        parent_tag_seq = 1,#1,
                        dest_tag = "li", 
                        detail_href_index =  1,
                        pages = 2,
                        job_name = "job2"
                        
                    ) 
    ret = papa.run()  
