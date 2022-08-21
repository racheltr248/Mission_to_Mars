# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Function to scrape all
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': hemispheres(browser),
        'last_modified': dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Function to visit the Mars NASA News site
def mars_news(browser):

    # Scrape Mars News
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object, quit browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# Function to visit the Mars Space Images site
def featured_image(browser):

    # Scrape Images
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        img_url_rel = img_soup.find('img', class_="fancybox-image").get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Function to visit the Mars Facts site
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    # set column names
    df.columns = ['Description', 'Mars', 'Earth']
    
    # turn the description column into the index in the current dataframe
    df.set_index('Description', inplace=True)

    # convert dataframe to html
    return df.to_html()

# Function to visit Mars Hemispheres site
def hemispheres(browser):
    # Scrape hemispheres site 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    links = browser.find_by_css('a.product-item img') 

    # loop through
    for i in range(len(links)):
    
        # create empty dictionary to store img & title results in
        hemisphere = {}
    
        # find result and click through to next page
        browser.find_by_css('a.product-item img')[i].click()
    
        # find sample image and extract href to jpg
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
    
        # find the title
        hemisphere['title'] = browser.find_by_css('h2.title').text
    
        # append list with dictionary
        hemisphere_image_urls.append(hemisphere)
    
        # browser back for next result
        browser.back()

    return hemisphere_image_urls

if __name__ == '__main__':
    # If running as script, print scraped data
    print(scrape_all())
