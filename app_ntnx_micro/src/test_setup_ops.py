from ops_setup import *

def test():
  cluster = d['cluster']
  containers = d['containers']
  networks = d['networks']
  ipam_networks = d['ipam_networks']
  images = d['images']

  ops = SetupOps(cluster, containers, networks, ipam_networks, images)
  ops.connect_to_prism()
  ops.set_language()
  ops.delete_unused_containers()
  ops.create_containers()
  ops.delete_unused_networks()
  ops.create_networks()
  ops.create_ipam_networks()
  ops.create_images()

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

if __name__ == '__main__':
  test()