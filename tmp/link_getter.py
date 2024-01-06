from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote

def get_image_url(file_page_url):
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # Go to the page
    driver.get(file_page_url)

    # # Check if a redirect has occurred
    if driver.current_url != file_page_url:
        print(f"Redirect detected: {file_page_url} -> {driver.current_url}")

    # Extract the file name from the URL
    file_name = unquote(file_page_url.split('/')[-1]).replace('File:', '')

    # Get the source of the page
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the image tag with data-src attribute containing the file name
    img_tag = soup.find('img', attrs={'data-src': lambda value: value and file_name in value})

    if img_tag is None:
        print(file_name)

    # If img_tag is None, re-encode the file_name and try again
    if img_tag is None:
        file_name = quote(file_name)
        img_tag = soup.find('img', attrs={'data-src': lambda value: value and file_name in value})

    # Get the URL of the image
    image_url = img_tag['data-src'] if img_tag else None

    if img_tag is None:
        img_tag = soup.find('img', attrs={'src': lambda value: value and file_name in value})
        image_url = img_tag['src'] if img_tag else None

    if image_url is None:
        print(file_name)
        # Find all image tags
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            with open('debug.txt', 'a') as f:
                f.write(str(img_tag) + '\n')
        image_url = 'https://static.wikia.nocookie.net/hotwheels/images/b/b5/Image_Not_Available.jpg'
    else:
        # Split the URL on the filename and keep only the part before it
        image_url = image_url.split(file_name)[0] + file_name

    # print(image_url)

    # Close the browser
    driver.quit()

    return image_url

# # Example usage:
# file_page_url = 'https://hotwheels.fandom.com/wiki/File:HKH31-LOOSE.jpg'
# get_image_url(file_page_url)