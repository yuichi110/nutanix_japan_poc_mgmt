from ops_foundation import *

d = {
  'report_server': {
    'send': False,
    'host': '127.0.0.1:80',
    'user': 'micro_servers',
    'password': 'hello',
  },

  'cluster': {
    'name': 'poc18',
    'netmask': '255.255.252.0',
    'gateway': '10.149.160.1',
    'ntp_server': 'ntp.nict.jp',
    'name_server': '8.8.8.8',
    'external_ip': '10.149.160.41',
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
  },

  "fvm" : {
    "ips" : [
      "10.149.160.5"
    ],
    "user" : "nutanix",
    "password" : "nutanix/4u",
    "nos_packages" : {
      "5.5.7" : "nutanix_installer_package-release-euphrates-5.5.7-stable.tar",
      "5.10.1" : "nutanix_installer_package-release-euphrates-5.10.1-stable.tar"
    }
  },

  "aos_version": "5.10.1"
}

fvm = d['fvm']
cluster = d['cluster']
aos_version = d['aos_version']
report_server = d['report_server']

ops = FoundationOps(fvm, cluster, aos_version, report_server)
ops.connect_to_fvm()
#ops.check_ipmi_mac()
#ops.check_ipmi_ip()
#ops.set_foundation_settings()
#ops.configure_ipmi_ip()
#ops.pre_check()
#ops.start_foundation()
ops.poll_progress()
