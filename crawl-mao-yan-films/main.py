import requests
from requests.exceptions import RequestException
import time
import csv
from pyquery import PyQuery as pq

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
  }

def get_one_page(url,headers):
  try:
    res = requests.get(url,headers=headers)
    if res.status_code == 200:
      return res.text
  except RequestException:
    return None

def parse_one_page(html):
  lis = []
  doc = pq(html)
  div = doc('.board-wrapper > dd').items()
  for item in div:
    idx = item('.board-index').text()
    name = item('.name').children().text()
    actor = item('.star').text()[3:]
    releasetime = item('.releasetime').text()[5:]
    score = item('.integer').text() + item('.fraction').text()
    # print(data)
    lis.append([idx,name,actor,releasetime,score])
  write_to_file(lis)

def write_to_file(content):
  with open('../data/mao_yan_top_100_films_v.csv','a',newline='',errors='ignore') as csvfile:
    f = csv.writer(csvfile)
    f.writerows(content)

def main(offset):
  url = 'https://maoyan.com/board/4?offset=' + str(offset)
  html = get_one_page(url,headers)
  parse_one_page(html)

if __name__ == "__main__":
    print('开始爬虫了')
    for i in range(1):
      print('爬取' + str(i))
      main(offset=i * 10)
      time.sleep(1)
    print('爬虫结束了')
