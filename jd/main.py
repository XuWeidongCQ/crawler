
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import time


import utils

BASE_URL = 'https://www.jd.com/'
KEY_WORD = '一次性医用口罩'

def connect_database(address,port,database_name,col_name):
  db_client = pymongo.MongoClient(address,port)
  db_col = db_client[database_name][col_name]
  return db_col


#返回一个字典列表
def handle_page(browser):
  ans = []
  browser.execute_script("window.scrollTo(0,5000)")
  time.sleep(2)
  div_lists = browser.find_elements(By.CSS_SELECTOR,'.gl-i-wrap')
  for div in div_lists:
    try:
      dic = {}
      dic["price"] = div.find_element(By.CSS_SELECTOR,'.p-price strong').get_attribute('textContent').strip()
      dic["product_name"] = div.find_element(By.CSS_SELECTOR,'.p-name > a').get_attribute('title').strip()
      dic["href"] = div.find_element(By.CSS_SELECTOR,'.p-name > a').get_attribute('href').strip()
      dic["shop_name"] = div.find_element(By.CSS_SELECTOR,'.p-shop  a').get_attribute('title').strip()
      dic["commit_num"] = div.find_element(By.CSS_SELECTOR,'.p-commit').get_attribute('textContent').strip()
      ans.append(dic)
    except:
      continue
  next_page_btn = browser.find_element(By.CSS_SELECTOR,'.pn-next') #跳转到下一页
  next_page_btn.click()
  return ans



if __name__ == '__main__':
  count = 0
  page = 1
  options = webdriver.ChromeOptions()
  options.add_experimental_option('prefs',{"profile.managed_default_content_settings.images": 2})
  browser = webdriver.Chrome(options=options)
  

  #0.连接到数据库
  db_col = connect_database('localhost',27017,'jd','medical_mask_shop')

  #1.打开网页
  browser.get(BASE_URL)
  browser.maximize_window()

  #2.找到关键字搜索框并且点击
  input_elm = browser.find_element(By.CSS_SELECTOR,'.form > #key')
  btn = browser.find_element(By.CSS_SELECTOR,'.form > .button')
  input_elm.send_keys(KEY_WORD)
  btn.click()



  #4.处理页面
  while True:
    time.sleep(2)
    print('第{}页'.format(page))
    res = handle_page(browser)
    page = page + 1
    db_col.insert_many(res)
    count = count + len(res)
    if count >= 1000:
      browser.close()
      break

  
  

