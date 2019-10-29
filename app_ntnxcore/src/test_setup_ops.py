from ops_setup import *

def test():
  ops = SetupOps(d)
  ops.set_temporary_password()
  ops.connect_to_prism()
  ops.set_eula()
  ops.set_initial_pulse()
  ops.set_initial_alert()
  ops.change_password()

d = {
  'cluster': {
    'ip':           '10.149.160.41',
    'user':         'admin',
    'password':     'Nutanix/4u!',
    'language':     'ja-JP'
  },

  'containers': [
    {
      'name':'container'
    },
  ],

  'networks': [
    {
      'name': 'vlan168',
      'vlan': '168'
    }
  ],

  'ipam_networks': [
    {
      'name': 'ipam165',
      'vlan': '165',
      'network': '',
      'prefix': '',
      'gateway': '',
      'dns': '',
      'pools': [
      ]
    }
  ],

  'images': [
    {
      'name': 'name',
      'container': 'container',
      'url': 'url'
    }
  ]
}

if __name__ == '__main__':
  test()