from common import minjson

def obj_to_dict(obj,current_level=0,max_level=5):
  current_level += 1
  if not obj:
    return obj
  if isinstance(obj, (str,int,long,unicode)):
    return obj
  if isinstance(obj, (list,tuple,set)):
    new_list = []
    for item in obj:
      if isinstance(item, (str,int,long,unicode)):
        new_list.append(item)
      else:
        if current_level <= max_level:
          new_list.append(obj_to_dict(item, current_level, max_level))
    return new_list
  if isinstance(obj, dict):
    keys_to_pop = [key for key in obj if key.startswith('_')]
    for key in keys_to_pop:
        obj.pop(key)
    new_dict = {}
    for key,value in obj.iteritems():
      if isinstance(value, (str,int,long,unicode)):
        new_dict[key] = value
      else:
        if current_level <= max_level:
          new_dict[key] = obj_to_dict(value, current_level, max_level)
    return new_dict
  if current_level <= max_level:
    try:
      return obj_to_dict(obj.__dict__, current_level, max_level)
    except:
      pass
  return None


def obj_to_json_for_ajax(obj):
  if isinstance(obj, (list,tuple)):
    data = obj_to_dict(obj[1])
  else:
    data = obj_to_dict(obj)
    return minjson.write(data)
  return minjson.write([obj[0],data])

def obj_to_json(obj):
  return minjson.write(obj_to_dict(obj,max_level=2))