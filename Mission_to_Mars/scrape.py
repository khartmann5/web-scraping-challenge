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

    # Quit the browser
    browser.quit()

    return mars_dict