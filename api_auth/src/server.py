import hashlib
import fastapi
import redis
import uuid
import os
import pymongo
from starlette.requests import Request
from starlette.responses import JSONResponse

from util import *
import server_login
import server_user

# REDIS
def get_redis():
  return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
REDIS = get_redis()

# MONGODB
def get_collection():
  client = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/',
    username=MONGO_USERNAME, password=MONGO_PASSWORD)
  col_user = client['api_auth']['user']
  return col_user
COLLECTION = get_collection()

# FASTAPI
app = fastapi.FastAPI()


##################
## login/logout ##
##################

@app.get("/api/public/auth/v1/login/")
async def public_get_login(request: Request):
  logined = is_logined(request)
  return {'logined':logined}

@app.post("/api/public/auth/v1/login/")
async def public_try_login(request: Request):
  try:
    d = await request.json()
    user_dict = {
      'username_or_email': d['username_or_email'].strip(),
      'password':d['password'].strip(),
    }
  except:
    raise fastapi.HTTPException(status_code=400, detail='json format error')
  (user_uuid, session_uuid, session_expire) = server_login.public_try_login(
    user_dict, COLLECTION, REDIS)
  return set_logined(JSONResponse({}), user_uuid, session_uuid, session_expire)

@app.post("/api/public/auth/v1/resession/")
async def public_resession(request: Request):
  if not is_logined(request, REDIS):
    raise fastapi.HTTPException(status_code=401, detail='session already expired')
  ck = request.cookies
  user_uuid = ck['user_uuid']
  (session_uuid, session_expire) = server_login.public_resession(
    user_uuid, REDIS)
  return set_logined(JSONResponse({}), user_uuid, session_uuid, session_expire)

@app.delete("/api/public/auth/v1/login/")
async def public_try_logout(request: Request):
  if not is_logined(request, REDIS):
    raise fastapi.HTTPException(status_code=401, detail='not yet login')
  ck = request.cookies
  user_uuid = ck['user_uuid']
  REDIS.delete(user_uuid)
  return del_logined(JSONResponse({}))


#####################
## create new user ##
#####################

@app.get("/api/private/auth/v1/users/")
async def private_get_users():
  return server_user.private_get_users(COLLECTION)

@app.post("/api/private/auth/v1/users/")
async def private_create_user0(request: Request):
  try:
    d = await request.json()
    user_dict = {
      'uuid': str(uuid.uuid4()),
      'username': d['username'].strip(),
      'email': d['email'].strip(),
      'password1':d['password1'].strip(),
      'password2':d['password2'].strip(),
      'validation_uuid': ''
    }
  except:
    raise fastapi.HTTPException(status_code=400, detail='json format error')
  server_user.create_user01(user_dict, COLLECTION)
  return {}

@app.post("/api/public/auth/v1/users/")
async def public_create_user1(request: Request):
  try:
    d = await request.json()
    validation_uuid = str(uuid.uuid4())
    user_dict = {
      'uuid': str(uuid.uuid4()),
      'username': d['username'].strip(),
      'email': d['email'].strip(),
      'password1':d['password1'].strip(),
      'password2':d['password2'].strip(),
      'validation_uuid': validation_uuid
    }
  except:
    raise fastapi.HTTPException(status_code=400, detail='json format error')
  server_user.create_user01(user_dict, COLLECTION)

  if DEBUG:
    return {'validation_uuid':validation_uuid}
  else:
    server_user.send_validation_email(d['email'], validation_uuid)
    return {}

@app.post("/api/public/auth/v1/users/{validation_uuid}")
async def public_create_user2(request: Request, validation_uuid: str):
  return server_user.create_user2(validation_uuid, COLLECTION)

@app.delete("/api/public/auth/v1/users/{user_uuid}")
async def public_delete_user(request: Request, user_uuid:str):
  if not is_logined(request, REDIS, user_uuid):
    raise fastapi.HTTPException(status_code=403, detail='authentication failed')
    


###############
## user info ##
###############

@app.get("/api/public/auth/v1/users/{user_uuid}")
async def public_get_user(request: Request):
  return {}

@app.put("/api/public/auth/v1/users/{user_uuid}")
async def public_update_user(request: Request):
  return {}

@app.delete("/api/public/auth/v1/users/{user_uuid}")
async def public_delete_user(request: Request):
  return {}


####################
## PRIVATE API ##
####################

@app.get("/api/private/auth/v1/sessions/")
async def private_get_sessions():
  return server_login.private_get_sessions(REDIS)

@app.delete("/api/private/auth/v1/sessions/")
async def private_delete_sessions():
  server_login.private_delete_sessions(REDIS)
  return {}


##########
## test ##
##########

@app.get("/api/public/auth/v1/test/auth/public/")
async def private_test_public(request: Request):
  return {}

@app.get("/api/public/auth/v1/test/auth/private/")
async def private_test_private(request: Request):
  if not is_logined(request, REDIS):
    raise fastapi.HTTPException(status_code=403, detail='requires authentication')
  return {}

@app.get("/api/public/auth/v1/test/auth/users/{user_uuid}")
async def private_test_user(request: Request):
  return {}  