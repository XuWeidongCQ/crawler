# 处理时间序列(去除序列两端的非法值)
import re

def handle_series(s):
  series = s.split(' ')
  length = len(series)
  if length == 1:
    return '0'
  l = 0
  r = length - 1
  # 从左边找到第一个合法数字的索引
  while l < length:
    if not re.match(r'^[-]?[0-9.]+$',series[l]):
      l = l + 1
    else:
      if float(series[l]) <= 0:
        l = l + 1
      else:
        break
  # 从右边边找到第一个合法数字的索引
  while r > 0:
    if not re.match(r'^[-]?[0-9.]+$',series[r]):
      r = r - 1
    else:
      if float(series[r]) <= 0:
        r = r - 1
      else:
        break
  if l > r:
    return '0'
  else:
    return ' '.join(series[l:r+1])

s = ' We -100 -100 34 5534 -100 0 -9 -3 erw %^ #'
s1 = '1 2 3 4'
s2 = '-1 -3 -4'
s3 = '2'
s4 = '-1'
s5 = '-3 -3 4 -5 0 -9'
print(handle_series(s1))