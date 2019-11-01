import json
import requests

URL_BASE = 'http://127.0.0.1:8000/api/v1'

def main():
  delete_all_clusters()
  uuid = create_cluster()
  test_power_up(uuid)
  test_power_down(uuid)

def delete_all_clusters():
  response = requests.get(URL_BASE + '/clusters/')
  clusters = response.json()
  for d in clusters:
    uuid = d['uuid']
    response = requests.delete(URL_BASE + '/clusters/' + uuid)
    print(response.text)

def create_cluster():
  response = requests.post(URL_BASE + '/clusters/', data=body)
  print(response.text)
  return response.json()['uuid']

def test_power_up(uuid):
  response = requests.post(URL_BASE + '/ops/power/up/' + uuid, data=body)
  print(response.text)

def test_power_down(uuid):
  response = requests.post(URL_BASE + '/ops/power/down/' + uuid, data=body)
  print(response.text)

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
      "host_ip":"10.149.160.21",
      "cvm_ip":"10.149.160.31"
    },
    {
      "host_name":"AHV-2",
      "position":"B",
      "ipmi_mac":"0c:c4:7a:66:e1:d3",
      "ipmi_ip":"10.149.160.12",
      "host_ip":"10.149.160.22",
      "cvm_ip":"10.149.160.32"
    },
    {
      "host_name":"AHV-3",
      "position":"C",
      "ipmi_mac":"0c:c4:7a:66:e2:95",
      "ipmi_ip":"10.149.160.13",
      "host_ip":"10.149.160.23",
      "cvm_ip":"10.149.160.33"
    },
    {
      "host_name":"AHV-4",
      "position":"D",
      "ipmi_mac":"0c:c4:7a:66:e2:97",
      "ipmi_ip":"10.149.160.14",
      "host_ip":"10.149.160.24",
      "cvm_ip":"10.149.160.34"
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