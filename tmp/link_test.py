from selenium import webdriver
from bs4 import BeautifulSoup

def get_image_url(file_page_url):
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # Go to the page
    driver.get(file_page_url)

    # Get the source of the page
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        print(img_tag)

    # Close the browser
    driver.quit()

# Example usage:
file_page_url = 'https://hotwheels.fandom.com/wiki/Manson_Cheung?file=Ain%27tNoSaint.jpg'
get_image_url(file_page_url)