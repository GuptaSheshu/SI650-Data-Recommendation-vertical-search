from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

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
    

    


    


