'''
这是注释
'''

from getModelInnerFunc import getFuncList
# import math
import datetime
import json
import re
import time
# import jieba
# import gensim
# import pymongo

dic = {'name':'xwd','age':24}
s = {1,2,3}
s1 = {3,4,5}
num = 11
str1 = '1.23'
lis = [0,1,2,3,4]
lis1 = lis.copy()
tup = (1,2,3,2)
bo = True
jstr = '{ "name":"Bill", "age":63, "city":"Seatle"}'
dic = {
  "对比":12
}
str2 = 'xx'

date = datetime.datetime.now()
x = 2

# print(dic.popitem())
# lis.pop(1)
# lis.pop(1)
# lis.insert(1,'#')
print(str2.split(' '))



def outer():
  x = 1
  print(x)
  

def inner():
  print('2')



# s.add(4)

# print(json.dumps(dic,indent=4,separators=(',','=')))

# print(dict(__builtins__))
# print(date.strftime('%x %X'))


# print(dir(re.search('\.',str1)))
# print(s)
# print(s3)
# print(str1[1:10:2])
# print(tup.count(2))
# print(dic.setdefault('name','sd'))
# print(str1.isdigit())
# print(getFuncList(pymongo))
# print(getFuncList(dbClient))
# print(getFuncList(mydb))
# print(getFuncList(mycol))
# print(getFuncList(gensim.models))



