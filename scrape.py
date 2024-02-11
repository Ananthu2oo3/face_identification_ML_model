import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import requests

# Set up the Selenium webdriver
driver = webdriver.Chrome()  # Set the path to your chromedriver

def scrape_content(name):

    key = name.replace(" ", "+")
    url = f'https://www.google.com/search?q={key}&tbm=isch'
    driver.get(url)

    # Scroll down to load more images
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract image source URLs
    image_tags = soup.find_all('img')

    if not os.path.exists(f'images/{name}'):
        os.makedirs(f'images/{name}')

    for i, img in enumerate(image_tags):
        src = img.get('src')
        if src and src.startswith('http'):
            # Send an HTTP request to download the image
            image_response = requests.get(src)
            
            # Save the image to the 'images' directory with prefixed filename and index
            with open(f'images/{name}/{name}_{i}.jpg', 'wb') as f:
                f.write(image_response.content)
            print(f'Saved image {name}_{i}.jpg successfully.')

    # Close the webdriver
    driver.quit()


if __name__ == '__main__':

    name = input("Enter a persons name: ")
    scrape_content(name)
    