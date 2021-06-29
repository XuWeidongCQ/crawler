

def getFuncList(modelName):
  list = dir(modelName)
  return [x for x in list if not x.endswith('__') and not x.startswith('_')]


  