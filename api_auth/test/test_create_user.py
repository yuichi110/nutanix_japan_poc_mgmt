import json
import requests

PORT = 8090
PRIVATE_API = f'http://127.0.0.1:{PORT}/api/private/auth/v1/'
PUBLIC_API = f'http://127.0.0.1:{PORT}/api/public/auth/v1/'

def main():
  '''
  test_get()
  test_create0()
  test_delete_sessions()
  test_login()
  test_get_sessions()
  '''
  test_session()
  
def test_get():
  res = requests.get(PRIVATE_API + 'users/')
  print(res.json())

def test_create0():
  d = {
    'username': 'hello',
    'email': 'hello@example.com',
    'password1': 'nutanix123',
    'password2': 'nutanix123'
  }
  res = requests.post(PRIVATE_API + 'users/', data=json.dumps(d))
  print(res.json())

def test_delete_sessions():
  res = requests.delete(PRIVATE_API + 'sessions/')
  print(res.json())

def test_login():
  d = {
    'username_or_email': 'hello',
    'password': 'nutanix123'
  }
  res = requests.post(PUBLIC_API + 'login/', data=json.dumps(d))
  print(res.json())

  print(res.cookies)

def test_get_sessions():
  res = requests.get(PRIVATE_API + 'sessions/')
  print(res.json())

def test_session():
  test_create0()

  session = requests.Session()
  res = session.get(PRIVATE_API + 'test/private')
  print(res)

  d = {
    'username_or_email': 'hello',
    'password': 'nutanix123'
  }
  res = session.post(PUBLIC_API + 'login/', data=json.dumps(d)) 
  print(res)

  res = session.get(PRIVATE_API + 'test/private')
  print(res)


if __name__ == '__main__':
  main()