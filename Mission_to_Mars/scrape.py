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
    mars_dict["paragraph"] = soup.find("div", class_="article_teaser_body").text

    # Featured Mars Image
    jpl_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    featured_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    browser.visit(jpl_image_url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    # Retreive featured image link
    image_url = image_soup.find_all('img')[1]['src']
    mars_dict["featured_image_url"] = featured_url + image_url

    # Mars facts in html table using a for loop
    # read html from website
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    # time.sleep(5)
    # create a Beautfiul Soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_facts=soup.find_all('tr')
    # loop through fact table
    mars_facts_table = []
    count = 0
    for fact in mars_facts:    
        if count == 9:
            break   
        try:
            column = fact.find('td', class_="column-1").text
            print(column)
            value = fact.find('td', class_="column-2").text
            print(value)
            # Create a dictionary
            table_dict = {}
            table_dict["column1"] = column
            table_dict["column2"] = value
            mars_facts_table.append(table_dict)  
        except Exception as e:
            print(e)
        count = count + 1

    mars_dict["mars_facts"] = mars_facts_table

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
    for item in mars_hemispheres:
        # error handling
        try:
            # extract title
            hemi = item.find('div', class_="description")
            title = hemi.h3.text
            print(title)
            # extract image url
            hemisphere_link = hemi.a['href']
            browser.visit(usgs_url + hemisphere_link)
            html = browser.html
            image_soup = BeautifulSoup(html, 'html.parser')
            image_hem = image_soup.find('li').a['href']
            print(image_hem)
            # create dictionary for images and title
            hemisphere_dict = {}
            hemisphere_dict['title'] = title
            hemisphere_dict['img_url'] = image_hem
            hemisphere_images.append(hemisphere_dict)
        except Exception as e:
            print(e)

    mars_dict["mars_hemispheres"] = hemisphere_images
    
    print(mars_dict)



    # Quit the browser
    browser.quit()

    return mars_dict