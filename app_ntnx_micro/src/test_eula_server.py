import requests, json

URL_BASE = 'http://127.0.0.1:8082/api/v1'
USER = 'user'
PASSWORD = 'password'

def test():
  response = requests.post(URL_BASE + '/run/', data=body)
  print(response.text)

d = {
  'user': USER,
  'password': PASSWORD,

  'eula': {
    'ip':           '10.149.160.41',
    'user':         'admin',
    'password':     'Nutanix/4u!',
    'eula_name':    'Yuichi Ito',
    'eula_company': 'Nutanix',
    'eula_title':   'DevOps Specialist',
    'enable_pulse': False,
  }

}
body = json.dumps(d)

if __name__ == '__main__':
  test()