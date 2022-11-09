from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

output_file = open("amazon_data.csv","a")
url_data = pd.read_csv("amazon_eye_liner.csv")
HEADERS = ({'User-Agent': 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


## data cleaning

# list of attrs needed = ['productTitle', 'productDescription', 'Rating', 'Price', 'Brand', 'Ingredients', 'About this item',
#                           'Frequently bought together', 'Products related to this item']
url_data = url_data.dropna(subset=['URL'])
for i in range(len(url_data)):
    data = url_data.iloc[i]
    URL = data.URL
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")

    # Extracting Title
    try:
        title = soup.find("span",attrs={"id":'productTitle'})
        title = title.string.strip().replace(',', '')
    except:
        title = np.nan
    
    # Extracting Product Descriptions
    try:
        desc = soup.find("div", attrs={"id":'productDescription'}).find("span").string
    except:
        desc = np.nan

    # Rating and Price
    rating = data.Rating
    price = data.Price

    # No. of reviews
    try:
        reviews = soup.find("span",{"id":"acrCustomerReviewText"}).string
    except:
        reviews = np.nan

    # Brand
    try:
        lis = soup.find("table", attrs={"class":"a-normal a-spacing-micro"}).find_all("span")
        for idx, val in enumerate(lis):
            if(val.string=="Brand"):
                brand = lis[idx+1].string
                break
    except:
        brand = np.nan
        
    # Ingredients
    try:
        flag=0
        lis = soup.find_all("div", attrs={"class" : "a-section content"})
        for idx, val in enumerate(lis):
            st_list = val.find_all(re.compile("h"))
            for idx2, val2 in enumerate(st_list):
                if(val2.string=="Ingredients"):
                    ingredients = lis[idx].text
                    flag=1
                    break
            if(flag):
                break
    except:
        ingredients = np.nan

    
    # About this item
    try:
        lis = soup.find("div", attrs={"id":"feature-bullets"}).find_all("li")
        features = []
        for val in lis:
            features.append(val.string)
    except:
        features = np.nan 
    
    # Frequently bought together
    try:
        fbt = soup.find("div", attrs={"class": "cardRoot bucket"}).find_all("a", href=True)
        fbt_links = []
        for val in fbt:
            fbt_links.append('https://www.amazon.com/'+val['href'])
    except:
        fbt_links = np.nan
        
    # Product related to this item
    try:
        prt = soup.find("div", {"id":"sims-consolidated-2_feature_div"}).find_all("a", href=True)
        dic = {}
        for idx, val in enumerate(prt):
            try:
                temp = val['title']
                dic[temp] = 1
            except:
                temp=1
        
        prt_list_title = list(dic.keys())
    except:
        prt_list_title = np.nan
                                
    

    


    


