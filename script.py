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
        brochure = [],
        )

def process():
    "It will start all the process and will return true upon completed"
    
    brand_url = "https://www.pearsondental.com/catalog/product_bybrand_mfg.asp"
    
    brand_links = scrape_brand_links(
        get_soup_object_from_request(
                brand_url
                ))
    
    
    product_links = scrape_product_links(brand_links)
    
    status = scrape_product_info(product_links[3465:])
    
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
    total_links = []
    for link in links:
        p_s = get_soup_object_from_request(link)
        product_links = p_s.find_all('a',class_='subcat')
        product_links = [total_links.append(i.get('href')) for i in product_links]

    
    print("All the product links scraped")    
    
    return total_links



def scrape_product_info(product_links):
    """
    Scrape Product info and appaned into Data Dictornary
    Returns True is completed
    use code like this to append the data -> data_dict['price'].append('data')
    """
    url = "https://www.pearsondental.com"
    #data_soup.find_all(attrs={"data-foo": "value"})
    for index, product_link in enumerate(product_links):
        print((url + product_link))  
        c = get_soup_object_from_request((url + product_link))
        
        try:
            table = c.find(attrs={"style": "background-color: #333333;"}).parent
        except:
            table = c.find(attrs={"bgcolor": "#333333"}).parent
            
        cells = table.find_all("tr", attrs={"valign": "top"})
        for cell in cells:
            data_dict['product_link'].append((url + product_link))
            data_dict['product_name'].append(cell.find("font", class_="link2").text)
            data_dict['mfg_part'].append(cell.find("font", attrs={"color":"000000"}).text.replace("Mfg. Part #: ",""))
            data_dict['item_no'].append(cell.find("td",attrs={"align":"center"}).find("b").text)
            data_dict['price'].append(cell.find("font", class_="maroon").text)
            
            try:
                data_dict['img_url'].append(
                        url + \
                         c.find("a", class_="MagicZoom").get("href"))
            except:
                data_dict['img_url'].append("")
             
            try:
                data_dict['description'].append(c.find("table",class_="link2", attrs={"width":"400"}).text.strip()\
                         .replace("Best Seller",""))
            except:
                data_dict['description'].append("")
             
            
            try:
                data_dict['brand_name'].append(c.find("h1").parent.find("strong").text.replace("(","").replace(")",""))
            except:
                data_dict['brand_name'].append("")
            
            
           
            try:
                data_dict['brochure'].append(c.find(text="Click for Brochure").parent.parent.parent.get('href'))
            except AttributeError:
                data_dict['brochure'].append("")
                
          
        print("Product Left:", str(len(product_links)-index))
        print()
                
                
    
    return True
    
    
    
def export_csv(data_dict):
    """
    Export Data Dictionary into CSV format
    """
    dataFrame = pd.DataFrame(data_dict)
    dataFrame.to_csv("data.csv", mode='w', header=True, index=False)
    print("Data.csv exported")
    return True


# Start the process
process()
