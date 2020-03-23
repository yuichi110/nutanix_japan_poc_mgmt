from ops_power import *
import paramiko

def test():
  test_down()

def test_up():
  ops = PowerOps(d['cluster'], d['nodes'], d['report_server'])
  ops.up_all_host()
  ops.wait_till_all_host_becoming_accesible()
  ops.wait_till_all_cvm_up()
  ops.wait_till_all_cvm_accessible()
  ops.up_cluster()

def test_down():
  ops = PowerOps(d['cluster'], d['nodes'], d['report_server'])
  if ops.is_all_cvm_down():
    print('all cvms are already down')
    if ops.is_all_host_down():
      pass
    else:
      ops.down_all_hosts()
  else:
    if ops.is_cluster_up():
      ops.down_over_cluster()
      ops.down_cluster()
    ops.down_all_cvms()
    ops.down_all_hosts()

d = {
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

if __name__ == '__main__':
  test()