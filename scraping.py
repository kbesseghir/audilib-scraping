from selenium import webdriver
import pandas as pd 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# options = Options()  # Initialize an instance of the Options class
# options.headless = False # True -> Headless mode activated
# options.add_argument('window-size=1920x1080')  # Set a big window size, so all the data will be displayed


web= "https://www.audible.com/adblbestsellers?ref_pageloadid=dBMdWNF1F5s0xVlX&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=1bb99d4d-8ec8-42a3-bb35-704e849c2bc6&pf_rd_r=NSTW5ST0FYGNW6TXNKCF&pageLoadId=eti2O8Iu2JS9wsKK&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc"
driver=webdriver.Chrome()
driver.get(web)
driver.maximize_window()

pagination = driver.find_element(By.XPATH,"//ul[contains(@class, 'pagingElements')]")
pages_pagination=pagination.find_elements(By.TAG_NAME,'li')
last_page=pages_pagination[-2].text
book_title = []
book_author = []
book_length = []

current_page=1
while current_page <= int(last_page):
    # time.sleep(2)
    container=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'adbl-impression-container')))
    pages=WebDriverWait(container,5).until(EC.presence_of_all_elements_located((By.XPATH,"//li[contains(@class, 'productListItem')]")))


   
    for page in pages:
       
        book_title.append(page.find_element(By.XPATH,".//h3[contains(@class, 'bc-heading')]/a").text)
        book_author.append(page.find_element(By.XPATH,".//li[contains(@class, 'authorLabel')]//a").text)
        book_length.append(page.find_element(By.XPATH,".//li[contains(@class, 'runtimeLabel')]//span").text)

    current_page=current_page+1
    try:
        next_page=driver.find_element(By.XPATH,'.//span[contains(@class , "nextButton")]')
        next_page.click()
    except:
      pass
driver.quit()
# Storing the data into a DataFrame and exporting to a csv file
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('booksanother.csv', index=False)

