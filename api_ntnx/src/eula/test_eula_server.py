import requests, json

URL_BASE = 'http://127.0.0.1:8082/api/v1'
USER = 'user'
PASSWORD = 'password'

def test():
  response = requests.post(URL_BASE + '/run/', data=body)
  print(response.text)

d = {
  'credential': {
    'user': USER,
    'password': PASSWORD,
  },

  'report_server': {
    'send': False,
    'host': '127.0.0.1',
    'port': 8080,
    'user': 'micro_servers',
    'password': 'hello',
    'uuid': '1234567890'
  },

  'cluster': {
    'ip': '10.149.160.41',
    'user': 'admin',
    'password': 'Nutanix/4u!',
    'name': 'poc18',  
  },

  'eula': {
    'user': 'Yuichi Ito',
    'company': 'Nutanix',
    'title': 'Specialist',
    'enable_pulse': False
  },
}
body = json.dumps(d)

if __name__ == '__main__':
  test()