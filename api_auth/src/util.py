import bson.json_util
import fastapi
import json
import os
import hashlib

# environment value
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = int(os.environ['MONGO_PORT'])
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
PASSWORD_ENCKEY = os.environ['API_AUTH_PASSWORD_ENCKEY']
DEBUG = os.environ['API_AUTH_DEBUG']

def get_hashed_password(password):
  text = f'{password}{PASSWORD_ENCKEY}'.encode('utf-8')
  return hashlib.md5(text).hexdigest()

def get_json(mongo_data):
  if mongo_data is None:
    raise fastapi.HTTPException(status_code=404, detail='Resource Not Found')
  return json.loads(bson.json_util.dumps(mongo_data))

def is_logined(request, redis_client, url_user_uuid=None):
  ck = request.cookies
  if 'user_uuid' not in ck:
    return False
  if 'session_uuid' not in ck:
    return False

  user_uuid = ck['user_uuid']
  session_uuid = ck['session_uuid']
  if url_user_uuid is not None:
    if user_uuid != url_user_uuid:
      return False

  value = redis_client.get(user_uuid)
  if value is None:
    return False

  if value.decode() != session_uuid:
    return False

  return True

def set_logined(response, user_uuid, session_uuid, session_expire):
  response.set_cookie('user_uuid', user_uuid)
  response.set_cookie('session_uuid', session_uuid)
  response.set_cookie('session_expire', session_expire)
  return response

def del_logined(response):
  response.delete_cookie('user_uuid')
  response.delete_cookie('session_uuid')
  response.delete_cookie('session_expire')
  return response