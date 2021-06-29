

test = [('对比', 'v'), ('后', 'f'), ('性价比', 'n'), ('高', 'a'), ('产品', 'n'), ('家里', 's'), ('测温', 'nz'), ('试', 'v'), ('速度', 'n'), ('快', 'a'), ('灵敏', 'nr'), ('稳定', 'a'), ('造型', 'n'), ('独特', 'a'), ('时尚', 'n'), ('黑白相间', 'n'), ('小朋友', 'n'), ('上学', 'n'), ('大人', 'n'), ('上班', 'v'), ('都', 'd'), ('家里', 's'), ('先', 'd'), ('测量', 'vn'), ('再', 'd'), ('出门', 'v'), ('确保', 'v'), ('家人', 'n'), ('物流', 'n'), ('速度', 'n'), ('快', 'a'), ('当天', 't'), ('买', 'v'), ('当天', 't'), ('赞', 'v')]
test1 = [('对比', 'v'), ('后', 'f'), ('性价比', 'n'), ('非常', 'd'), ('高', 'a'), ('的', 'uj'), ('产品', 'n'), ('家里', 's'), ('以后', 'f'), ('测温', 'nz'), ('就', 'd'), ('方便', 'a'), ('多', 'm'), ('了', 'ul'), ('试', 'v'), ('了', 'ul'), ('一下', 'm'), ('速度', 'n'), ('非常', 'd'), ('快', 'a'), ('很', 'zg'), ('灵敏', 'nr'), ('很', 'zg'), ('稳定', 'a'), ('造型', 'n'), ('独特', 'a'), ('很', 'zg'), ('时尚', 'n'), ('黑白相间', 'n'), ('以后', 'f'), ('小朋友', 'n'), ('上学', 'n'), ('大人', 'n'), ('上班', 'v'), ('之前', 'f'), ('都', 'd'), ('可以', 'c'), ('在', 'p'), ('家里', 's'), ('先', 'd'), ('测量', 'vn'), ('一下', 'm'), ('再', 'd'), ('出门', 'v'), ('确保', 'v'), ('了', 'ul'), ('家人', 'n'), ('和', 'c'), ('他人', 'r'), ('的', 'uj'), ('安全', 'an'), ('物流', 'n'), ('速度', 'n'), ('非常', 'd'), ('快', 'a'), ('当天', 't'), ('买', 'v'), ('当天', 't'), ('到', 'v'), ('赞', 'v')]
def combine_word(arr):
  l = 0
  r = 0
  tr_lis = ['nda','na']
  markers = ''
  tmp_str = ''
  pos = 0
  while r < len(arr):
    if arr[r][1] == 'n' and markers == '':#起始位置
      markers = markers + 'n'
      tmp_str = tmp_str + arr[r][0]
      pos = r
      r = r + 1
    elif arr[r][1] == 'd' and markers == 'n':
      markers = markers + 'd'
      tmp_str = tmp_str + arr[r][0]
      r = r + 1
    elif arr[r][1] == 'a':#结束位置
      if markers == 'n':
        markers = markers + 'a'
        tmp_str = tmp_str + arr[r][0]
        arr.pop(pos)
        arr.pop(pos)
        arr.insert(pos,(tmp_str,markers))
      elif markers == 'nd':
        markers = markers + 'a'
        tmp_str = tmp_str + arr[r][0]
        arr.pop(pos)
        arr.pop(pos)
        arr.pop(pos)
        arr.insert(pos,(tmp_str,markers))
      else:
        markers = ''
        tmp_str = ''
        r = r + 1
    else:
      markers = ''
      tmp_str = ''
      r = r + 1

def filter_seg(arr):
    filter_set = {'na','nda','n','a'}
    ans = [tup[0] for tup in arr if tup[1] in filter_set]
    ans = set(ans)
    return ' '.join(ans)
combine_word(test)
print(filter_seg(test))
    


