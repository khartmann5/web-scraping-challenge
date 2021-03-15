from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
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


    # Quit the browser
    browser.quit()

    return mars_dict