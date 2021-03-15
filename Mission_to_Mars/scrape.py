from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dict = {}

    # Mars news title and paragraph
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_dict["title"] = soup.find_all("div", class_="content_title")[1].get_text()
    mars_dict["paragraph"] = soup.find_all("div", class_="article_teaser_body")[0].get_text()

    # Featured Mars Image
    jpl_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    featured_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    browser.visit(jpl_image_url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    # Retreive featured image link
    image_url = image_soup.find_all('img')[1]['src']
    mars_dict["featured_image_url"] = featured_url + image_url

    # Mars facts in a html table
    # facts_url = "https://space-facts.com/mars/"
    # browser.visit(facts_url)
    # html = browser.html
    # facts_soup = BeautifulSoup(html, 'html.parser')
    # mars_dict['mars_facts'] = soup.find_all("table", class_="tablepress tablepress-id-p-mars")[0]

    # Mars Hemispheres
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_url = "https://astrogeology.usgs.gov"
    browser.visit(hemisphere_url)
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')
    all_hemispheres = hemisphere_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_hemispheres.find_all('div', class_='item')
    hemisphere_images = []
    # loop through hemisphere images
    for i in mars_hemispheres:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        hemisphere_link = hemisphere.a["href"]
        browser.visit(usgs_url + hemisphere_link)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # create dictionary for images and title
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = image_url
        mars_dict['mars_hemispheres'] = hemisphere_images.append(hemisphere_dict)






    # Quit the browser
    browser.quit()

    return mars_dict