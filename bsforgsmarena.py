from email import header
from heapq import merge
from attr import attrs
from bs4 import BeautifulSoup as bs
from matplotlib.pyplot import axis
import requests as rq
from time import sleep
import re
import pandas as pd

header={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_***) AppleWebKit/53*** (KHTML, like Gecko) Chrome/83.****** Safari/537.***"}
header2={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"}

for i in range(17):
    r = rq.get(f"https://www.gsmarena.com/samsung-phones-f-9-0-p{i}.php",headers=header)
    
    soup = bs(r.content, "lxml")
    
    whole_table = soup.find("div", attrs={'class':'section-body'})
    items = whole_table.find_all("li")

    head_div = soup.find("div", attrs={'class':'makers'})
    head_li = whole_table.find_all("li")

    for phones in head_li:
        names_features = phones.img.get("title")
        image_links = phones.img.get("src")
        head_a = phones.find("a")
        phones_names = head_a.find("span").text
        features_list=re.split(",|\.",names_features)
        for phone_pages in items:
            items_part_link = phone_pages.a.get("href")
            
            base_link = "https://www.gsmarena.com/"
            items_whole_link = base_link+items_part_link
            phone_page = rq.get(items_whole_link, headers=header2)
            
            phone_soup = bs(phone_page.content, "lxml")
            whole_feature_table = phone_soup.find_all("div", {"id":"specs-list"})
            for feature in whole_feature_table:
                feature_details = feature.find_all("tr")
                
                for rows in feature_details:
                    try:
                        row_name = rows.find("th", attrs={"scope":"row"}).text
                        
                    except AttributeError:
                        print("-")
                    try:    
                        row_head = rows.find("td", attrs={"class":"ttl"}).text
                        
                    except AttributeError:
                        print("-")
                    try:
                        row_info = rows.find("td", attrs={"class":"nfo"}).text
                        
                    except AttributeError:
                        print("-")
                    
                    data_features= {"PhoneName": [phones_names], "HeadFeatures": [features_list[1:]],"ImageLink": [image_links], "RowHead":[row_head], "RowName": [row_name],  "RowInfo":[row_info]}
                    excel_file = pd.DataFrame(data=data_features, index=[features_list[0]])               
                    print(excel_file)
excel_file.to_csv(r'C:\Users\hasan\Desktop\upwork projects\gsmarena.csv',index=False)    