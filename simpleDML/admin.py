#!/usr/bin/env python 
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import web 
import re
import json 
import os
render = web.template.render('templates')  
web.config.debug = False
from threading import Thread
from main import Job 
from main import PageInfo
import time
from Config import DOWNLOAD
        
        
urls = (    
   '/', 'LOGIN',
  '/scrapy', 'SCRAPY' ,
  '/result', 'RESULT'
)

app = web.application(urls, globals())


class LOGIN:
    def GET(self): 
        raise web.seeother('/static/index.html')

class RESULT:
    def GET(self): 
        
        server_scrapy_dir=DOWNLOAD.PATH_DOWNLOAD
        dirs = os.listdir(server_scrapy_dir)
        data = []
        for dir in dirs: 
            data.append(  {"page": dir , "count":1} )
        
        return  json.dumps(data)


class SCRAPY:
    def POST(self): 
        job_name = ""
        pages = ""
        job_path=""
        try:
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
            
            job_name = web.input().job_name.strip() 
            job_path = web.input().job_path.strip() 
            
            now = time.strftime("%Y%m%d%H%M%S", time.localtime())
            job_name = "%s_%s"% (job_name,now)  
            server_scrapy_dir=DOWNLOAD.PATH_DOWNLOAD  
            if not job_path:
                job_path = "%s/%s"% (server_scrapy_dir, job_name)
            
            print "first_page_url=[%s]" % ( first_page_url  )
            print "split_page_url=[%s]" % ( split_page_url  )  
            print "job_name=[%s]" % ( job_name  )  
            print "job_path=[%s]" % ( job_path  )  
            args={ 
                  "pages":pages,
                  "split_page_url":split_page_url,
                  "job_name":job_name,
                  "job_path" : job_path
                  }
            pageInfo =PageInfo(first_page_url, first_title,first_link_title  ) 
            job = Job(pageInfo,args)
            job.start()
            
        except Exception,e:
            print e 
        
        data={ "job_name":job_name , "pages":pages,"job_path" : job_path }
        return render.result( data ) 
        
if __name__ == "__main__": 
    app.run() 
    
         