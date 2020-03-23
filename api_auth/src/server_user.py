import fastapi
import re
import safe
from util import *

def private_get_users(collection):
  result = collection.find({}, {'_id': False})
  return get_json(result)

def create_user01(user_dict, collection):
  user_uuid = user_dict['uuid']
  username = user_dict['username']
  email = user_dict['email']
  password1 = user_dict['password1']
  password2 = user_dict['password2']
  validation_uuid = user_dict['validation_uuid']
  validate_user_dict(username, email, password1, password2, 
    validation_uuid, collection)

  del user_dict['password1']
  del user_dict['password2']
  user_dict['password'] = get_hashed_password(password1)
  collection.insert_one(user_dict)

def send_validation_email(email, validation_uuid):
  ...

def create_user2(validation_uuid):
  if validation_uuid == '':
    raise fastapi.HTTPException(status_code=403, 
      detail='invalid validation_uuid provided')

  result = collection.update_one({'validation_uuid':validation_uuid}, 
    {'$set', {'validation_uuid', ''}})
  if result.matched_count != 1:
    raise fastapi.HTTPException(status_code=403, 
      detail='invalid validation_uuid provided')

  return {}


def validate_user_dict(username, email, password1, password2, validation_uuid, collection):
  def isalnum(text):
    return re.match(r'^[a-zA-Z0-9]+$', text) is not None

  if not isalnum(username):
    raise fastapi.HTTPException(status_code=400, 
      detail='username can have only alphabet number and underber')

  if len(username) < 3:
    raise fastapi.HTTPException(status_code=400, 
      detail='username must have 3 characters at least.')
    
  if password1 != password2:
    raise fastapi.HTTPException(status_code=400, 
      detail='passwords are different')

  if not bool(safe.check(password1, level=2)): # medium
    raise fastapi.HTTPException(status_code=400, 
      detail='password is week')

  # check username
  user = collection.find_one({'username':username}, {'_id': False})
  if user is not None:
    if user['validation_uuid'] == '':
      raise fastapi.HTTPException(status_code=400, 
        detail='username is already taken')
    else:
      collection.delete_one({'username':username})
  
  # check email
  user = collection.find_one({'email':email}, {'_id': False})
  if user is not None:
    if user['validation_uuid'] == '':
      raise fastapi.HTTPException(status_code=400, 
        detail='another user have same email')
    else:
      collection.delete_one({'email':email})