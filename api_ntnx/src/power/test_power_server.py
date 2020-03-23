import requests, json

URL_BASE = 'http://127.0.0.1:8084/api/v1'
USER = 'user'
PASSWORD = 'password'

def test():
  test_up()

def test_up():
  response = requests.post(URL_BASE + '/up/', data=body)
  print(response.text)

def test_down():
  response = requests.post(URL_BASE + '/down/', data=body)
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

  "nodes":[
    {
      "host_name":"AHV-1",
      "position":"A",
      "ipmi_mac":"0c:c4:7a:92:95:d4",
      "ipmi_ip":"10.149.160.11",
      "ipmi_user":"ADMIN",
      "ipmi_password":"ADMIN",
      "host_ip":"10.149.160.21",
      "host_user":"root",
      "host_password":"nutanix/4u",
      "cvm_ip":"10.149.160.31",
      "cvm_user":"nutanix",
      "cvm_password":"nutanix/4u",
    },
    {
      "host_name":"AHV-2",
      "position":"B",
      "ipmi_mac":"0c:c4:7a:66:e1:d3",
      "ipmi_ip":"10.149.160.12",
      "ipmi_user":"ADMIN",
      "ipmi_password":"ADMIN",
      "host_ip":"10.149.160.22",
      "host_user":"root",
      "host_password":"nutanix/4u",
      "cvm_ip":"10.149.160.32",
      "cvm_user":"nutanix",
      "cvm_password":"nutanix/4u",
    },
    {
      "host_name":"AHV-3",
      "position":"C",
      "ipmi_mac":"0c:c4:7a:66:e2:95",
      "ipmi_ip":"10.149.160.13",
      "ipmi_user":"ADMIN",
      "ipmi_password":"ADMIN",
      "host_ip":"10.149.160.23",
      "host_user":"root",
      "host_password":"nutanix/4u",
      "cvm_ip":"10.149.160.33",
      "cvm_user":"nutanix",
      "cvm_password":"nutanix/4u",
    },
    {
      "host_name":"AHV-4",
      "position":"D",
      "ipmi_mac":"0c:c4:7a:66:e2:97",
      "ipmi_ip":"10.149.160.14",
      "ipmi_user":"ADMIN",
      "ipmi_password":"ADMIN",
      "host_ip":"10.149.160.24",
      "host_user":"root",
      "host_password":"nutanix/4u",
      "cvm_ip":"10.149.160.34",
      "cvm_user":"nutanix",
      "cvm_password":"nutanix/4u",
    }
  ]
}
body = json.dumps(d)

if __name__ == '__main__':
  test()