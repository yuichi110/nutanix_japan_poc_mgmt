import json
import requests
import time

URL_BASE = 'http://127.0.0.1:8080/api/v1'

def main():
  #delete_all()
  #uuid = create_cluster()
  #task_uuid = test_foundation(uuid)
  #task_uuid = test_power_down(uuid)
  poll_tasks()

def delete_all():
  response = requests.get(URL_BASE + '/clusters/')
  clusters = response.json()
  for d in clusters:
    uuid = d['uuid']
    response = requests.delete(URL_BASE + '/clusters/' + uuid)
    print(response.text)

  response = requests.get(URL_BASE + '/tasks/')
  tasks = response.json()
  for d in tasks:
    uuid = d['uuid']
    response = requests.delete(URL_BASE + '/tasks/' + uuid)
    print(response.text)

def create_cluster():
  response = requests.post(URL_BASE + '/clusters/', data=body)
  print(response.text)
  return response.json()['uuid']

def test_foundation(uuid):
  d = {
    "aos_version": "5.10.1"
  }
  response = requests.post(URL_BASE + '/ops/foundation/' + uuid, data=json.dumps(d))
  print(response.text)
  return response.json()['uuid']

def poll_tasks():
  while True:
    try:
      response = requests.get(URL_BASE + '/tasks/')
      for task in response.json():
        print(task)
      print()
      time.sleep(3)
    except Exception as e:
      print(e)

d = {
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

  'eula': {
    'user': 'Yuichi Ito',
    'company': 'Nutanix',
    'title': 'Specialist',
    'enable_pulse': False
  },

  'containers': [
    {
      'name':'container'
    },
  ],

  'networks': [
    {
      'name': 'vlan191',
      'vlan': 191
    }
  ],

  'ipam_networks': [
    {
      'name': 'ipam167',
      'vlan': 167,
      'network': '10.149.167.0',
      'prefix': 24,
      'gateway': '10.149.167.1',
      'dns': '8.8.8.8',
      'pools': [
          {
            'from' : '10.149.167.101',
            'to' : '10.149.167.250'
          }
      ]
    }
  ],

  'images': [
    {
      'name': 'ISO_CENT7_MIN',
      'container': 'container',
      'url': 'nfs://10.149.245.50/Public/bootcamp/centos7_min.iso'
    },
    {
      'name': 'IMG_CENT7_JPN',
      'container': 'container',
      'url': 'nfs://10.149.245.50/Public/bootcamp/centos7_jpn_raw'
    },
    {
      'name': 'IMG_CENT7_ENG',
      'container': 'container',
      'url': 'nfs://10.149.245.50/Public/bootcamp/centos7_eng_raw'
    },
    {
      'name': 'IMG_WIN2012R2_ENG',
      'container': 'container',
      'url': 'nfs://10.149.245.50/Public/bootcamp/win2012r2_eng_raw'
    },
  ]
}
body = json.dumps(d)



if __name__ == '__main__':
  main()