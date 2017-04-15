#!/usr/bin/env python 
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import web 
import re
render = web.template.render('templates')  
web.config.debug = False

urls = (    
   '/', 'LOGIN',
  '/scrapy', 'SCRAPY' 
)

app = web.application(urls, globals())


class LOGIN:
    def GET(self): 
        raise web.seeother('/static/index.html')

class SCRAPY:
    def POST(self): 
        split_page_url = ""
        first_page_url = web.input().first_page_url
        if first_page_url:
            first_page_url = first_page_url.strip().replace("\s","").replace("\r","").replace("\n","").replace("\t","").replace(" ","") 
            split_page_url=first_page_url.replace("{1}","{0}") 
            first_page_url=first_page_url.replace("{1}","1")  
        first_title = web.input().first_title.strip()
        
        first_link_title = web.input().first_link_title.strip()
        pages =web.input().pages.strip() 
        first_page_url = re.sub("[\s \t\r\n]","",first_page_url)
        job_name =web.input().job_name.strip() 
        print "first_page_url=[%s]" % ( first_page_url  )
        print "split_page_url=[%s]" % ( split_page_url  )  
        print "job_name=[%s]" % ( job_name  )  
        
        
        from main import PageInfo
        pageInfo =PageInfo(first_page_url, first_title,first_link_title  )
        info = pageInfo.parsePageInfo()
        
        from pages import PAPA 
        papa = PAPA(
                        split_page_url = split_page_url,   
                        parent_tag = info["parent_tag"], #"html > body > div > div > div > div > div > ul",
                        parent_tag_seq = info["parent_tag_seq"],#1,
                        dest_tag = info["dest_tag"], 
                        detail_href_index = info["detail_href_index"],
                        pages = int(pages),
                        job_name = job_name
                        
                    ) 
             
        ret = papa.run()  
        return render.main( ret )
        
if __name__ == "__main__": 
    app.run() 
    
         