import requests, json

URL_BASE = 'http://127.0.0.1:8081/api/v1'
USER = 'user'
PASSWORD = 'password'

def main():
  #test_check()
  test_image()

def test_check():
  response = requests.post(URL_BASE + '/check/', data=body)
  print(response.text)

def test_image():
  response = requests.post(URL_BASE + '/image/', data=body)
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

  'basics': {
    'gateway': '10.149.160.1',
    'netmask': '255.255.252.0',
    'ntp_server': 'ntp.nict.jp',
    'name_server': '8.8.8.8',
    'language': 'ja-jp'
  },

  "nodes":[
    {
      "host_name":"AHV-1",
      "position":"A",
      "ipmi_mac":"ac:1f:6b:13:4f:a4",
      "ipmi_ip":"10.149.18.11",
      "host_ip":"10.149.18.21",
      "cvm_ip":"10.149.18.31"
    },
    {
      "host_name":"AHV-2",
      "position":"B",
      "ipmi_mac":"ac:1f:6b:13:4f:ac",
      "ipmi_ip":"10.149.18.12",
      "host_ip":"10.149.18.22",
      "cvm_ip":"10.149.18.32"
    },
    {
      "host_name":"AHV-3",
      "position":"C",
      "ipmi_mac":"0c:c4:7a:c9:04:b3",
      "ipmi_ip":"10.149.18.13",
      "host_ip":"10.149.18.23",
      "cvm_ip":"10.149.18.33"
    },
    {
      "host_name":"AHV-4",
      "position":"D",
      "ipmi_mac":"ac:1f:6b:16:96:22",
      "ipmi_ip":"10.149.18.14",
      "host_ip":"10.149.18.24",
      "cvm_ip":"10.149.18.34"
    }
  ],

  "fvm" : {
    "ips" : [
      "10.149.160.5"
    ],
    "user" : "nutanix",
    "password" : "nutanix/4u",
    "nos_packages" : [
      {
        'version':"5.5.7",
        'file':"nutanix_installer_package-release-euphrates-5.5.7-stable.tar"
      },
      {
        'version':"5.10.1",
        'file':"nutanix_installer_package-release-euphrates-5.10.1-stable.tar"
      }
    ]
  },

  "foundation": {
    "aos_version": "5.10.1"
  }
}
body = json.dumps(d)

if __name__ == '__main__':
  main()