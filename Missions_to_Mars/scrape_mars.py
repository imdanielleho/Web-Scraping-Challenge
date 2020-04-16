#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
import requests

def scrape():
    scrape_data = {}
    # ## NASA Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    news_response = requests.get(news_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = BeautifulSoup(news_response.text, 'html.parser')
    
    news_title = news_soup.find('div',class_='slide').find('div',class_='content_title').text
    scrape_data['news_title'] = news_title.replace('\n','')
    news_p = news_soup.find('div',class_='slide').find('div',class_='rollover_description_inner').text
    scrape_data['news_p'] = news_p.replace('\n','')
    

    ## JPL Mars Space Images - Featured Image
    space_url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    space_response = requests.get(space_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    space_soup = BeautifulSoup(space_response.text, 'html.parser')


    base_url='https://www.jpl.nasa.gov'
    image_url = space_soup.find('a',class_='button fancybox')['data-fancybox-href']
    scrape_data['featured_image_url'] = base_url+image_url
    


    # ## Mars Weather
    # URL of page to be scraped
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    weather_response = requests.get(weather_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    weather_soup = BeautifulSoup(weather_response.text, 'html.parser')


    scrape_data['weather'] = weather_soup.find('div',class_='js-tweet-text-container').find('p').text


    # ## Mars Facts
    import pandas as pd
    # URL of page to be scraped
    fact_url = 'https://space-facts.com/mars/'
    
    tables = pd.read_html(fact_url)
    df_fact = tables[0]
    df_fact.columns = ["", "Value"]

    html_table = df_fact.to_html(index=False)
    scrape_data['html_table'] = html_table.replace('\n','')
  
     ## Mars Hemispheres
    # URL of page to be scraped
    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Retrieve page with the requests module
    h_response = requests.get(h_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    h_soup = BeautifulSoup(h_response.text, 'html.parser')

    h_results = h_soup.find_all('a',class_='itemLink product-item')
    h_base_url ='https://astrogeology.usgs.gov'

    h_urls = []

    for h in h_results:
        h_url = h_base_url+ h['href']
        h_urls.append(h_url)

    new_h_response = requests.get(h_url)
    new_h_soup = BeautifulSoup(new_h_response.text, 'html.parser')

    img_url = []
    title = []

    for h_url in h_urls:
        new_h_response = requests.get(h_url)
        new_h_soup = BeautifulSoup(new_h_response.text, 'html.parser')
        img_url.append(new_h_soup.find('div',class_='downloads').find('a')['href'])


    for h in h_results:
        h_title = h.text
        title.append(h_title)

    hemisphere_image_urls = []
        
    for i in range(0,4):
        keyList = ["title","img_url"]
        valueList = [title[i],img_url[i]]
        hemisphere_image_urls.append(dict(zip(keyList, valueList)))
    
    scrape_data['hemisphere_image_urls'] = hemisphere_image_urls
    
    return scrape_data

