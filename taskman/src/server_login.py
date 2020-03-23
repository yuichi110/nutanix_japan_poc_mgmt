import fastapi
import re
import safe
import uuid
from datetime import datetime
from util import *

def private_get_sessions(redis):
  data = {}
  cursor = '0'
  while cursor != 0:
    cursor, keys = redis.scan(cursor=cursor, count=1000000)
    if len(keys) == 0:
      break
    keys = [key.decode() for key in keys]
    values = [value.decode() for value in redis.mget(*keys)]
    data.update(dict(zip(keys, values)))
  return data

def private_delete_sessions(redis):
  cursor = '0'
  while cursor != 0:
    cursor, keys = redis.scan(cursor=cursor, count=1000000)
    if len(keys) == 0:
      break
    keys = [key.decode() for key in keys]
    redis.delete(*keys)

def public_try_login(user_dict, collection, redis):
  username_or_email = user_dict['username_or_email']
  password = user_dict['password']

  user = collection.find_one({'$or':[
    {'username':username_or_email}, {'email':username_or_email}
  ]}, {'_id': False})
  if user is None:
    raise fastapi.HTTPException(status_code=403, 
      detail='authentication failed. user does not exist.')
  if user['validation_uuid'] != '':
    raise fastapi.HTTPException(status_code=403, 
      detail='authentication failed. user is not yet validated.')

  hashed_password = get_hashed_password(password)
  if hashed_password != user['password']:
    raise fastapi.HTTPException(status_code=403, 
      detail='authentication failes. wrong password.')

  user_uuid = user['uuid']
  session_uuid = str(uuid.uuid4())

  # tell 3 hour session. but keep 4 hour in server.
  session_expire = str(int(datetime.utcnow().timestamp()) + 3600 * 3)
  redis.set(user_uuid, session_uuid, ex=3600 * 4)

  return (user_uuid, session_uuid, session_expire)

def public_resession(user_uuid, redis):
  session_uuid = str(uuid.uuid4())

  # tell 3 hour session. but keep 4 hour in server.
  session_expire = int(datetime.utcnow().timestamp()) + 3600 * 3
  redis.set(user_uuid, session_uuid, ex=3600 * 4)

  return (session_uuid, str(session_expire))