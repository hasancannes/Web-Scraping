from email import header
from heapq import merge
from attr import attrs
from bs4 import BeautifulSoup as bs
from matplotlib.pyplot import axis
import requests as rq
from time import sleep
import re
import pandas as pd


class webScraping:
    
    def get_adress(self):
        header1={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_***) AppleWebKit/53*** (KHTML, like Gecko) Chrome/83.****** Safari/537.***"}
        for i in range(17):
            r = rq.get(f"https://www.gsmarena.com/samsung-phones-f-9-0-p{i}.php",headers=header1)
            sleep(2)
            soup = bs(r.content, "lxml")
            sleep(6)
            whole_table = soup.find("div", attrs={'class':'section-body'})
            sleep(4)
            items = whole_table.find_all("li")
            sleep(3)
            head_div = soup.find("div", attrs={'class':'makers'})
            sleep(2)
            self.head_li = whole_table.find_all("li")
            sleep(3)
            gsmarena.get_phones()
            gsmarena.get_print_all_values()
            
    def get_phones(self):
        for phones in self.head_li:
            names_features = phones.img.get("title")
            sleep(3)
            self.image_links = phones.img.get("src")
            sleep(2)
            self.head_a = phones.find("a")
            sleep(4)
            self.phones_names = self.head_a.find("span").text
            sleep(5)
            self.features_list=re.split(",|\.",names_features)
            sleep(2)
            gsmarena.get_phone_pages()

    def get_phone_pages(self):
        for phone_pages in self.head_li:
            items_part_link = phone_pages.a.get("href")
            sleep(2)
            base_link = "https://www.gsmarena.com/"
            items_whole_link = base_link+items_part_link
            sleep(6)
            phone_page = rq.get(items_whole_link)
            sleep(4)
            phone_soup = bs(phone_page.content, "lxml")
            sleep(3)
            self.whole_feature_table = phone_soup.find_all("div", {"id":"specs-list"})
            sleep(7)
            gsmarena.get_phone_features()

    def get_phone_features(self):
        for feature in self.whole_feature_table:
                feature_details = feature.find_all("tr")
                sleep(2)
                for rows in feature_details:
                    try:
                        self.row_name = rows.find("th", attrs={"scope":"row"}).text
                        sleep(3)    
                    except AttributeError:
                        print("-")
                        sleep(5)
                    try:    
                        self.row_head = rows.find("td", attrs={"class":"ttl"}).text
                        sleep(2)    
                    except AttributeError:
                        print("-")
                        sleep(4)
                    try:
                        self.row_info = rows.find("td", attrs={"class":"nfo"}).text
                        sleep(4)   
                    except AttributeError:
                        print("-")
                        sleep(7)
    def get_print_all_values(self):
        data_features= {"PhoneName": [self.phones_names], "HeadFeatures": [self.features_list[1:]],"ImageLink": [self.image_links], "RowHead":[self.row_head], "RowName": [self.row_name],  "RowInfo":[self.row_info]}
        sleep(4)
        excel_file = pd.DataFrame(data=data_features, index=[self.features_list[0]])               
        print(excel_file)
        excel_file.to_csv(r'C:\Users\hasan\Desktop\upwork projects\gsmarena.csv',index=False)

gsmarena = webScraping()
gsmarena.get_adress()
