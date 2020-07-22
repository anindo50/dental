# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 00:06:38 2020

@author: Surface Laptop
"""

#Import Libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests as req



data_dict = dict(
        product_name = [],
        brand_name = [],
        description = [],
        mfg_part = [],
        item_no = [],
        price = [],
        img_url = [],
        product_link = [],
        )

def process():
    "It will start all the process and will return true upon completed"
    brand_url = "https://www.pearsondental.com/catalog/product_bybrand_mfg.asp"
    brand_links = scrape_brand_links(
        get_soup_object_from_request(
                brand_url
                ))
    
    
    product_links = scrape_product_links(brand_links)
    
    status = scrape_product_info(product_links)
    
    if status:
        export_csv(data_dict)
        
        return True
    else:
        return False

def get_soup_object_from_request(url):
    """
    Takes URL and return Soup object
    """
    resp = req.get(url)
    data = resp.text
    soup = BeautifulSoup(data,'html.parser')
    
    return soup
    

def scrape_brand_links(soup_object):
    """
    It will scrape all the brand links and will return list of all brand links
    """
    tr = soup_object.find_all('table',class_='subcat') 
    
    for i in tr:
        x = i.find_all('a')
        link_list = []
        for i in x:
            link = "https://www.pearsondental.com/catalog/" + i.get('href')
            link_list.append(link)
     
    print("All the brand links scraped")
    
    return link_list
  
 
def scrape_product_links(links):
    """
    Takes list of links of brands
    return all the products link in a list
    """
    for link in links:
        p_s = get_soup_object_from_request(link)
        product_links = p_s.find_all('a',class_='subcat')
        product_links = [i.get('href') for i in product_links]

    
    print("All the product links scraped")    
    
    return product_links



def scrape_product_info(product_links):
    """
    Scrape Product info and appaned into Data Dictornary
    Returns True is completed
    use code like this to append the data -> data_dict['price'].append('data')
    """
    
    # Enter Loop for product_links
    
    # Enter loop for Description/Package field(multiple products)
    
    # Append All the stuff
    
    return True
    
    
    
def export_csv(data_dict):
    """
    Export Data Dictionary into CSV format
    """
    dataFrame = pd.DataFrame(data_dict)
    dataFrame.to_csv("data.csv", mode='w', header=True, index=False)
    print("Data.csv exported")
    return True
