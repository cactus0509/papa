#coding:utf8
import sys
from __builtin__ import True
reload(sys)
sys.setdefaultencoding('utf-8')

from threading import Thread
import re 
from bs4 import BeautifulSoup  
from bs4.element import NavigableString,Tag
import requests
from pages import PAPA

class Job(Thread): 
    result = []
    
    def __init__(self,  pageInfo,args):  
        super(Job, self).__init__()
        self.pageInfo =pageInfo
        self.args = args
        
    def run(self):  
        try: 
            info = self.pageInfo.parsePageInfo() 
            papa = PAPA(
                            split_page_url = self.args["split_page_url"],   
                            parent_tag = info["parent_tag"], 
                            parent_tag_seq = info["parent_tag_seq"],#1,
                            dest_tag = info["dest_tag"], 
                            detail_href_index = info["detail_href_index"],
                            pages = int(self.args["pages"]),
                            job_name =self.args["job_name"] ,
                            job_path = self.args["job_path"] 
                        ) 
            papa.run() 
        except Exception,e:
            print e 
        
      
class PageInfo():
    
    def __init__(self,first_page_url,first_title,first_link_title):
        #url="https://www.guahao.com/hospital/areahospitals?p=%E5%8C%97%E4%BA%AC&pi=1&pageNo=1"
        self.first_page_url = first_page_url
        self.first_title=first_title
        self.first_link_title = first_link_title
        
    def parsePageInfo(self):
        try:
            print self.first_page_url
            resp=requests.get(self.first_page_url)
            print "response code :  %s " % ( resp.status_code ) 
            resp.encoding = 'utf-8'
            text =  resp.text   
            soup = BeautifulSoup(text, "lxml",fromEncoding="utf-8") 
            
            line_start=self.first_title   
            first_link_title = self.first_link_title
            detail_href_index = 0 
            start_key_arr=line_start.split(",") 
            
            first_key=start_key_arr[0] 
            
            list_tags=["tr","li"]
            dest_tag=None    
            bFind = False 
            mytag = [] 
            
            for child in soup.descendants: 
                if  isinstance(child, NavigableString) :   
                    if child.find(first_key) > -1 :  
                        for parent in  child.parents :
                            for tag in list_tags:  
                                if parent.name == tag and  not bFind :    
                                    for key in start_key_arr:  
                                        key=key.decode('utf-8') 
                                        print key 
                                        if parent.get_text().find(key)< 0   : 
                                            break 
                                        bFind=True
                                        dest_tag =parent.name  
                                        for line in  parent.parents:
                                            mytag.append(line.name) 
                                        
                                        if first_link_title:
                                            hrefs = parent.find_all("a")
                                            bFind = False   
                                            for url in hrefs: 
                                                if url.get_text().find(first_link_title) >-1:
                                                    print "find......" , url
                                                    bFind = True 
                                                if bFind :
                                                    break 
                                                detail_href_index = detail_href_index + 1
                                      
                elif isinstance(child, Tag)   : 
                    pass
                
            sort_tag = [] 
            if mytag: 
                sort_tag = mytag[::-1][1:]
            
            parent_tag =  ' > '.join( sort_tag  ) 
             
            parent_tag_seq = 0  
            if parent_tag:
                tags = soup.select(parent_tag) 
                bFind=False 
                if tags:
                    for tag_ in tags  :   
                        for key in start_key_arr  :  
                          if tag_.find( text=re.compile( key ))  > -1 :
                              bFind=True 
                              break 
                        if  bFind:
                            break 
                        
                        parent_tag_seq = parent_tag_seq + 1
            print parent_tag , dest_tag , parent_tag_seq , detail_href_index
            return {
                    "first_link_title":first_link_title,
                    "parent_tag":parent_tag,
                    "dest_tag":dest_tag,
                    "parent_tag_seq":parent_tag_seq,
                    "detail_href_index":detail_href_index
                   }
        except Exception,e:
            print e 
            
if __name__ == "__main__":
    
    first_page_url="https://www.guahao.com/hospital/areahospitals?sort=region_sort&ipIsShanghai=false&fg=0&c=%E5%B9%BF%E5%B7%9E&ht=all&q=&p=%E5%B9%BF%E4%B8%9C&ci=79&hk=&o=all&pi=29&hl=all&pageNo=2"
    first_title="广州医科大学附属第三医院"
    first_link_title="广州医科大学附属第三医院"
    pageInfo =PageInfo(first_page_url, first_title,first_link_title  )
    info = pageInfo.parsePageInfo()
        