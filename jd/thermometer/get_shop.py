

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import time


BASE_URL = 'https://www.jd.com/'
KEY_WORD = '电子体温计'
Brands = '欧姆龙（OMRON）' #重要 一定要改
HOST = 'localhost'
PORT = 27017
MAX_PAGE = 5 #重要 一定要改



def connect_database(address,port,database_name,col_name):
  db_client = pymongo.MongoClient(address,port)
  db_col = db_client[database_name][col_name]
  return db_col

def get_shop_info(browser):
  browser.execute_script("window.scrollTo(0,8000)") #先把所有的商店加载出来
  time.sleep(2)
  shop_lists = browser.find_elements(By.CSS_SELECTOR,'.gl-i-wrap')
  shop_res = []
  for shop in shop_lists:
    try: 
      dic = {}
      dic["price"] = shop.find_element(By.CSS_SELECTOR,'.p-price strong').text.strip()
      dic["product_name"] = shop.find_element(By.CSS_SELECTOR,'.p-name > a').get_attribute('title').strip()
      dic["href"] = shop.find_element(By.CSS_SELECTOR,'.p-name > a').get_attribute('href').strip()
      dic["shop_name"] = shop.find_element(By.CSS_SELECTOR,'.p-shop  a').get_attribute('title').strip()
      dic["commit_num"] = shop.find_element(By.CSS_SELECTOR,'.p-commit').text.strip()
      dic["brand"] = Brands
      if dic["commit_num"][0] == '0':
        continue
      shop_res.append(dic)
    except:
      continue
  next_page_btn = browser.find_element(By.CSS_SELECTOR,'.pn-next') #跳转到下一页
  next_page_btn.click()
  return shop_res

  



if __name__ == "__main__":
  
  #浏览器设置 避免网站检测window.navigator.webdriver 开启无图
  option = webdriver.ChromeOptions()
  option.add_experimental_option('excludeSwitches',['enable-automation'])
  option.add_experimental_option('prefs',{"profile.managed_default_content_settings.images": 2})
  browser = webdriver.Chrome(options=option)
  browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
  })
  

  #1.打开网页
  browser.get(BASE_URL)
  browser.maximize_window()

  #2.在搜索框中输入关键字
  input_elm = browser.find_element(By.CSS_SELECTOR,'.form > #key')
  btn = browser.find_element(By.CSS_SELECTOR,'.form > .button')
  input_elm.send_keys(KEY_WORD)
  btn.click()

  #3.获取品牌的链接
  time.sleep(2)
  brand_lists = browser.find_element(By.CSS_SELECTOR,".J_valueList")
  link = brand_lists.find_element(By.CSS_SELECTOR,"a[title='{}']".format(Brands))
  link.click()

  #4.找到所有商铺的链接
  db_client = pymongo.MongoClient(HOST,PORT)
  db_col = db_client['thermometer']['shop_info']
  # cnt = 0
  for page in range(1,MAX_PAGE+1):
    time.sleep(2)
    print('第{}页'.format(str(page)))
    res = get_shop_info(browser)
    db_col.insert_many(res)
    print('第{}页处理完成'.format(str(page)))
  db_client.close()