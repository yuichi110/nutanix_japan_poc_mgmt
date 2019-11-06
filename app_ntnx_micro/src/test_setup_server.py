import requests, json

URL_BASE = 'http://127.0.0.1:8083/api/v1'
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

  'basics': {
    'gateway': '10.149.160.1',
    'netmask': '255.255.252.0',
    'ntp_server': 'ntp.nict.jp',
    'name_server': '8.8.8.8',
    'language': 'ja-jp'
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
  test()