


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import time


HOST = 'localhost'
PORT = 27017
COLLECTION = 'BDS_0915' #重要!!!每次都要改
BRAND = '保盾（BDS）' #重要!!!每次都要改


def handle_reviews(browser):
  ans = []
  time.sleep(2)
  comment_items = browser.find_elements(By.CSS_SELECTOR,'.comment-item')
  for comment in comment_items:
    try:
      dic = {}
      dic['user'] = comment.find_element(By.CSS_SELECTOR,'.user-column > .user-info').text.strip()
      dic['comment_msg'] = comment.find_element(By.CSS_SELECTOR,'.comment-column > .comment-con').text.strip()
      dic['comment_score'] = comment.find_element(By.CSS_SELECTOR,'.comment-column > .comment-star').get_attribute('class').strip()[-1]
      dic['comment_time'] = comment.find_element(By.CSS_SELECTOR,'.comment-column > .comment-message > .order-info').text.strip()
      ans.append(dic)
    except:
      continue
  return ans





if __name__ == "__main__":
  # 浏览器设置 避免网站检测window.navigator.webdriver 开启无图
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
  browser.maximize_window()

  #链接数据库
  db_client = pymongo.MongoClient(HOST,PORT)
  db_reviews_base_col = db_client['glasses']['reviews_base_info']
  db_reviews_col = db_client['glasses'][COLLECTION]
  db_shop_col = db_client['glasses']['shop_info']

  shop_info = db_shop_col.find({'brand':BRAND},{'_id':0,'href':1,'commit_num':1})
  #把所有的商店信息放到一个列表中，以免游标处理超时
  shop_lis = [{'href':shop['href'],'commit_num':shop['commit_num']} for shop in shop_info]
  #关闭查找的游标
  shop_info.close()

  shop_num = len(shop_lis)
  has_visited_shop = set()
  cnt = 0
  cracker = -1
  for shop in shop_lis:
    cnt = cnt + 1
    href = shop['href']
    print('-----正在处理{}的评论数据---{}/{}---{}'.format(href,cnt,shop_num,shop['commit_num']))
    if href in has_visited_shop:
      print('该商店已经访问过了')
      continue
    has_visited_shop.add(href)
    if cnt < cracker:
      continue
    #1.打开网页
    browser.get(href + '#comment')
    time.sleep(4)
    #2.获取好评 中评 差评的数量
    try:
      label = browser.find_element(By.CSS_SELECTOR,".filter-list > li:last-child > label")
      label.click()
      time.sleep(1)
    except:
      print('--没有找到对应的label按钮--')
      continue

    dic = {}
    dic['brand'] = BRAND
    arr = []
    li_elms = browser.find_elements(By.CSS_SELECTOR,".filter-list > li[data-tab='trigger']")
    for li in li_elms:
      arr.append(li.get_attribute('data-num'))
    dic['reviews_info'] = arr
    # print(dic)
    db_reviews_base_col.insert_one(dic)

    #3.处理评论数据
    try:
      review_page = 1
      while True:
        if review_page > 100:
          print('----{}评论数据处理完了----'.format(href))
          break
        print('第{}页'.format(review_page))
        #处理当前页的评论数据
        ans = handle_reviews(browser)
        db_reviews_col.insert_many(ans)
        #是否存在下一页的按钮 
        next_page_btn = browser.find_element(By.CSS_SELECTOR,".ui-pager-next")
        review_page = review_page + 1
        next_page_btn.click()
      continue
    except:
      print('----{}评论数据处理完了----'.format(href))
      continue

     

  db_client.close()


