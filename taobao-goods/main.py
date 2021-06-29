# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import re

# 打开淘宝并搜索关键字
def search_product(browser,url,key_word):
  # 淘宝会进行登录
  wait = WebDriverWait(browser,15)
  browser.get(url)
  browser.find_element_by_id("q").send_keys(key_word)
  search_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btn-search')))
  search_btn.click()
  browser.maximize_window()
  # 等待15秒，给足时间我们扫码
  # time.sleep(15)
  
  total_page_ele = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'total')))
  page_info = total_page_ele.text
  # 获取所有的页码
  total_page = re.findall('(\d+)',page_info)[0]
  return total_page


# 获取某一页的所有数据
def get_one_page_data(browser,page_num,key_word):
  print('*'*50)
  print('正在爬取第{}页'.format(page_num))
  browser.get('https://s.taobao.com/search?q={}&s={}'.format(key_word, (page_num-1)*44))
  # 等待10s直到页面加载完毕(对于ajax获取的数据需要等待浏览器渲染完毕)
  browser.implicitly_wait(5)
  card_list = browser.find_elements_by_css_selector(".J_MouserOnverReq")
  # print(card_list)
  for item in card_list:
    record = {
      # shopname J_MouseEneterLeave J_ShopInfo
      'price':item.find_element_by_class_name('price').text,
      'people':item.find_element_by_css_selector('.deal-cnt').text,
      'product_name':item.find_element_by_css_selector('.J_ClickStat').text,
      'product_shop':item.find_element_by_css_selector('a.shopname.J_MouseEneterLeave.J_ShopInfo > span:last-child').text,
      'location':item.find_element_by_css_selector('.location').text
    }
    print(record)

if __name__ == "__main__":
  #加快访问速度
  options = webdriver.ChromeOptions()
  #防止被检查出使用selenium
  # options.add_experimental_option('excludeSwitches', ['enable-automation'])
  #不加载图片
  # C:\Users\xwd\AppData\Local\Google\Chrome\User Data\Default
  user_data_dir = (r'--user-data-dir=C:\Users\xwd\AppData\Local\Google\Chrome\User Data\Default')
  options.add_experimental_option('prefs',{"profile.managed_default_content_settings.images": 2})
  # options.add_argument(user_data_dir)
  browser = webdriver.Chrome(options=options)
  
  url = 'https://www.taobao.com/'
  key_word = '口罩'
  page_num = 1
  total_page = search_product(browser,url,key_word)
  print('共{}页'.format(total_page))
  while page_num <= int(total_page):
    get_one_page_data(browser,page_num,key_word)
    page_num += 1
    if page_num == 3:
      break

  
  
