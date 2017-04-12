#coding:utf8
import re 
from bs4 import BeautifulSoup  
import requests

# url="""http://www.chunyuyisheng.com/cooperation/wap/search_doctor_page/?partner=chunyu_wap&clinic_no=2&source_type=chunyu_weixin&from_type=triage_clinic_click"""

url="https://www.guahao.com/hospital/areahospitals?p=%E5%8C%97%E4%BA%AC&pi=1&pageNo=1"

resp=requests.get(url)
text =  resp.text 
soup = BeautifulSoup(text, "lxml")   
line_start=u"北京协和医院,三级甲等,010-69156114,东院]北京市东城区帅府园一号"
line_end=u"北京同仁医院,010-58266699,北京市东城区东交民巷1号(西区)" 




#         
# if is_ul == 1 :
#     lis = table_list.find_all("li")
#     for li in lis :
#         txt = li.get_text().strip()
#         txt = re.sub("\s","$",txt )
#         txt = txt.replace("\n","").replace("\r","$")
#         txt = re.sub("[$]+","$",txt )
#         
#         hrefs =li.find_all("a")
#         urls=set()
#         for url in hrefs :
#             urls.add(url["href"])
#         
#         print "%s$%s" % ( txt, ''.join( list( urls) ) )   

