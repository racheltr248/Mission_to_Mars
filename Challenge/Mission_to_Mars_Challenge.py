#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Import Pandas
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


# create a new dataframe from the first html table at index 0
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# assign columns to the new dataframe
df.columns=['description', 'Mars', 'Earth']

# turn the description column into the index in the current dataframe
df.set_index('description', inplace=True)

# look at the new dataframe
df


# In[14]:


# convert dataframe to html
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[17]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
links = browser.find_by_css('a.product-item img')    


# In[18]:


len(links)


# In[19]:


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


# In[20]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# ### Shutdown the automated browsing session

# In[21]:


browser.quit()

