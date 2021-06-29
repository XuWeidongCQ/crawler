# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import re


#解析一个电影列表页面的信息
def parse_film_page(browser,start):
  film_infos = []
  browser.get(BASE_URL + '?start={}'.format(start))
  film_lists = browser.find_elements_by_css_selector('.info')
  for film in film_lists:
    film_infos.append({
      'film_name':film.find_element_by_css_selector('.info > .hd .title').text,
      'film_desc':film.find_element_by_css_selector('.info > .bd > p').text,
      'review_link':film.find_element_by_css_selector('.info > .hd > a').get_attribute('href')
    })
  return film_infos

#解析一部电影的评论
def parse_film_reviews(browser,review_link,start):
  reviews_infos = []
  browser.get(review_link  + '/comments?start={}'.format(start))
  time.sleep(2)
  reviews_lists = browser.find_elements_by_css_selector('.comment-item')
  for review in reviews_lists:
    reviews_infos.append(review.find_element_by_css_selector('.short').text)
  return reviews_infos


if __name__ == "__main__":

  BASE_URL = 'https://movie.douban.com/top250'
  # 电影页数 最大为10页 每页都是25个
  FILM_PAGE = 1
  # 每部电影的评论页 每页都是20条 最大只能看500条 也就是25页
  REVIEWS_PAGE = 5

  #加快访问速度 不加载图片
  options = webdriver.ChromeOptions()
  options.add_experimental_option('prefs',{"profile.managed_default_content_settings.images": 2})
  browser = webdriver.Chrome(options=options)
  #指定最长的等待时间
  wait = WebDriverWait(browser,10)

  #对电影的每一页 
  for i in range(FILM_PAGE):
    ret = {}
    print('#'*50)
    print('开始爬取第{}页'.format(i+1))
    films = parse_film_page(browser,i*25)
    #解析这一页所有电影的评论
    for film in films:
      print('获取['+film['film_name']+']的评论')
      ret = film
      ret['reviews'] = []
      #获取这部电影的评论
      for j in range(REVIEWS_PAGE):
        reviews_infos = parse_film_reviews(browser,film['review_link'],j*20)
        ret['reviews'].append(reviews_infos)
      print(ret)



