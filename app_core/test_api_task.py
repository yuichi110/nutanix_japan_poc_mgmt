import json
import requests

URL_BASE = 'http://127.0.0.1:8000/api/v1'

def main():
  print(1)
  test_delete_all()
  print(2)
  parent_uuid = test_create_task()
  print(3)
  child_uuid = test_create_child_task(parent_uuid)
  child_uuid = test_create_child_task(parent_uuid)
  test_update1(child_uuid)
  test_update3(child_uuid)
  test_update2(child_uuid)
  '''
  print(4)
  test_get(child_uuid)
  print(5)
  test_get_all()
  test_delete(parent_uuid)
  print(6)
  test_get_all()
  print(7)
  '''

def test_delete_all():
  response = requests.get(URL_BASE + '/tasks/')
  clusters = response.json()
  for d in clusters:
    uuid = d['uuid']
    response = requests.delete(URL_BASE + '/tasks/' + uuid)
    print('delete: ' + response.text)

def test_create_task():
  response = requests.post(URL_BASE + '/tests/')
  print('create: ' + response.text)
  return response.json()['uuid']

def test_create_child_task(parent_uuid=''):
  if parent_uuid == '':
    response = requests.get(URL_BASE + '/tasks/')
    parent_uuid = response.json()[0]['uuid']
  response = requests.post(URL_BASE + '/tests/' + parent_uuid)
  print('create: ' + response.text)
  return response.json()['uuid']

def test_get_all():
  response = requests.get(URL_BASE + '/tasks/')
  clusters = response.json()
  print('len: {}'.format(len(clusters)))
  for d in clusters:
    print('get: ' + str(d))

def test_get(uuid):
  response = requests.get(URL_BASE + '/tasks/' + uuid)
  print('get: ' + response.text)

def test_delete(uuid):
  response = requests.delete(URL_BASE + '/tasks/' + uuid)
  print('delete: ' + response.text)

def test_update1(uuid):
  d = {
    'progress':50,
  }
  response = requests.put(URL_BASE + '/tasks/' + uuid, data=json.dumps(d))
  print('update: ' + response.text)

def test_update2(uuid):
  d = {
    'progress':100,
  }
  response = requests.put(URL_BASE + '/tasks/' + uuid, data=json.dumps(d))
  print('update: ' + response.text)

def test_update3(uuid):
  d = {
    'failed':True,
  }
  response = requests.put(URL_BASE + '/tasks/' + uuid, data=json.dumps(d))
  print('update: ' + response.text)

if __name__ == '__main__':
  main()