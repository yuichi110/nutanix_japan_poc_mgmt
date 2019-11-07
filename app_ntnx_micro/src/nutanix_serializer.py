import json

class Cluster:
  @classmethod
  def dumps(cls, original):
    if type(original) == dict:
      original = json.dumps(original)
    d = cls.loads(original)
    return json.dumps(d)

  @classmethod
  def loads(cls, s):
    try:
      d = json.loads(s)
    except:
      raise Exception('failed to parse json')
    if 'cluster' not in d:
      raise Exception("key 'cluster' not in json")
    if 'nodes' not in d:
      raise Exception("key 'nodes' not in json")
    if 'basics' not in d:
      raise Exception("key 'basics' not in json")
    if 'fvm' not in d:
      raise Exception("key 'fvm' not in json")
    if 'eula' not in d:
      raise Exception("key 'eula' not in json")
    if 'containers' not in d:
      raise Exception("key 'containers' not in json")
    if 'networks' not in d:
      raise Exception("key 'networks' not in json")
    if 'ipam_networks' not in d:
      raise Exception("key 'ipam_networks' not in json")
    if 'images' not in d:
      raise Exception("key 'images' not in json")    
    nd = {
      'cluster':_get_json_cluster(d['cluster']),
      'nodes':_get_json_nodes(d['nodes']),
      'basics':_get_json_basics(d['basics']),
      'fvm':_get_json_fvm(d['fvm']),
      'eula':_get_json_eula(d['eula']),
      'containers':_get_json_containers(d['containers']),
      'networks':_get_json_networks(d['networks']),
      'ipam_networks':_get_json_ipam_networks(d['ipam_networks']),
      'images':_get_json_images(d['images'])
    }
    return nd

class Foundation:
  @classmethod
  def dumps(cls, original):
    if type(original) == dict:
      original = json.dumps(original)
    d = cls.loads(original)
    return json.dumps(d)

  @classmethod
  def loads(cls, s):
    try:
      d = json.loads(s)
    except:
      raise Exception('failed to parse json')
    if 'cluster' not in d:
      raise Exception("key 'cluster' not in json")
    if 'nodes' not in d:
      raise Exception("key 'nodes' not in json")
    if 'basics' not in d:
      raise Exception("key 'basics' not in json")
    if 'fvm' not in d:
      raise Exception("key 'fvm' not in json")   
    if 'foundation' not in d:
      raise Exception("key 'foundation' not in json") 
    if 'credential' not in d:
      raise Exception("key 'credential' not in json")
    if 'report_server' not in d:
      raise Exception("key 'report_server' not in json")
    nd = {
      'cluster':_get_json_cluster(d['cluster']),
      'nodes':_get_json_nodes(d['nodes']),
      'basics':_get_json_basics(d['basics']),
      'fvm':_get_json_fvm(d['fvm']),
      'foundation':_get_json_foundation(d['foundation']),
      'credential':_get_json_credential(d['credential']),
      'report_server':_get_json_report_server(d['report_server'])
    }
    return nd

class Eula:
  @classmethod
  def dumps(cls, original):
    if type(original) == dict:
      original = json.dumps(original)
    d = cls.loads(original)
    return json.dumps(d)

  @classmethod
  def loads(cls, s):
    try:
      d = json.loads(s)
    except:
      raise Exception('failed to parse json')
    if 'cluster' not in d:
      raise Exception("key 'cluster' not in json")
    if 'eula' not in d:
      raise Exception("key 'eula' not in json")
    if 'credential' not in d:
      raise Exception("key 'credential' not in json") 
    if 'report_server' not in d:
      raise Exception("key 'report_server' not in json")
    nd = {
      'cluster':_get_json_cluster(d['cluster']),
      'eula':_get_json_eula(d['eula']),
      'credential':_get_json_credential(d['credential']),
      'report_server':_get_json_report_server(d['report_server'])
    }
    return nd

class Setup:
  @classmethod
  def dumps(cls, original):
    if type(original) == dict:
      original = json.dumps(original)
    d = cls.loads(original)
    return json.dumps(d)

  @classmethod
  def loads(cls, s):
    try:
      d = json.loads(s)
    except:
      raise Exception('failed to parse json')

    if 'cluster' not in d:
      raise Exception("key 'cluster' not in json")
    if 'basics' not in d:
      raise Exception("key 'basics' not in json")
    if 'containers' not in d:
      raise Exception("key 'containers' not in json")
    if 'networks' not in d:
      raise Exception("key 'networks' not in json")
    if 'ipam_networks' not in d:
      raise Exception("key 'ipam_networks' not in json")
    if 'images' not in d:
      raise Exception("key 'images' not in json")   
    if 'credential' not in d:
      raise Exception("key 'credential' not in json") 
    if 'report_server' not in d:
      raise Exception("key 'report_server' not in json") 
    nd = {
      'cluster':_get_json_cluster(d['cluster']),
      'basics':_get_json_basics(d['basics']),
      'containers':_get_json_containers(d['containers']),
      'networks':_get_json_networks(d['networks']),
      'ipam_networks':_get_json_ipam_networks(d['ipam_networks']),
      'images':_get_json_images(d['images']),
      'credential':_get_json_credential(d['credential']),
      'report_server':_get_json_report_server(d['report_server'])
    }
    return nd

class Power:
  @classmethod
  def dumps(cls, original):
    if type(original) == dict:
      original = json.dumps(original)
    d = cls.loads(original)
    return json.dumps(d)

  @classmethod
  def loads(cls, s):
    try:
      d = json.loads(s)
    except:
      raise Exception('failed to parse json')
    if 'cluster' not in d:
      raise Exception("key 'cluster' not in json")
    if 'nodes' not in d:
      raise Exception("key 'nodes' not in json")
    if 'credential' not in d:
      raise Exception("key 'credential' not in json") 
    if 'report_server' not in d:
      raise Exception("key 'report_server' not in json")
    nd = {
      'cluster':_get_json_cluster(d['cluster']),
      'nodes':_get_json_nodes(d['nodes']),
      'credential':_get_json_credential(d['credential']),
      'report_server':_get_json_report_server(d['report_server'])
    }
    return nd

#####
## Utility
#####

def _get_json_cluster(d):
  if 'ip' not in d:
    raise Exception("key 'ip' not in root.cluster")
  if 'user' not in d:
    raise Exception("key 'user' not in root.cluster")
  if 'password' not in d:
    raise Exception("key 'password' not in root.cluster")
  if 'name' not in d:
    raise Exception("key 'name' not in root.cluster")
  cluster = {
    'ip':d['ip'],
    'user':d['user'],
    'password':d['password'],
    'name':d['name'],
  }
  return cluster

def _get_json_nodes(d):
  nodes = []
  for elem in d:
    if 'host_name' not in elem:
      raise Exception("key 'host_name' not in root.nodes.{}")
    if 'position' not in elem:
      raise Exception("key 'position' not in root.nodes.{}")
    if 'ipmi_mac' not in elem:
      raise Exception("key 'ipmi_mac' not in root.nodes.{}")
    if 'ipmi_ip' not in elem:
      raise Exception("key 'ipmi_ip' not in root.nodes.{}")
    if 'host_ip' not in elem:
      raise Exception("key 'host_ip' not in root.nodes.{}")
    if 'cvm_ip' not in elem:
      raise Exception("key 'cvm_ip' not in root.nodes.{}")
    node = {
      'host_name': elem['host_name'],
      'position': elem['position'],
      'ipmi_mac': elem['ipmi_mac'],
      'ipmi_ip': elem['ipmi_ip'],
      'host_ip': elem['host_ip'],
      'cvm_ip': elem['cvm_ip'],

      'ipmi_user': elem.get('ipmi_user', 'ADMIN'),
      'ipmi_password': elem.get('ipmi_password', 'ADMIN'),
      'host_user': elem.get('host_user', 'root'),
      'host_password': elem.get('host_password', 'nutanix/4u'),
      'cvm_user': elem.get('cvm_user', 'nutanix'),
      'cvm_password': elem.get('cvm_password', 'nutanix/4u')
    }
    nodes.append(node)
  return nodes

def _get_json_basics(d):
  if 'netmask' not in d:
    raise Exception("key 'netmask' not in root.cluster")
  if 'gateway' not in d:
    raise Exception("key 'gateway' not in root.cluster")
  if 'ntp_server' not in d:
    raise Exception("key 'ntp_server' not in root.cluster")
  if 'name_server' not in d:
    raise Exception("key 'name_server' not in root.cluster")
  if 'language' not in d:
    raise Exception("key 'language' not in root.cluster")
  basics = {
    'netmask':d['netmask'],
    'gateway':d['gateway'],
    'ntp_server':d['ntp_server'],
    'name_server':d['name_server'],
    'language':d['language'],    
  }
  return basics

def _get_json_fvm(d):
  if 'ips' not in d:
    raise Exception("key 'ip' not in root.fvm.{}")
  if 'user' not in d:
    raise Exception("key 'user' not in root.fvm.{}")
  if 'password' not in d:
    raise Exception("key 'password' not in root.fvm.{}")
  if 'nos_packages' not in d:
    raise Exception("key 'name' not in root.fvm.{}")
  fvm = {
    'ips': [],
    'user': d['user'],
    'password': d['password'],
    'nos_packages': []
  }
  for ip in d['ips']:
    fvm['ips'].append(ip)
  for elem in d['nos_packages']:
    if 'version' not in elem:
      raise Exception("key 'version' not in root.fvm.nos_packages[].{}")
    if 'file' not in elem:
      raise Exception("key 'file' not in root.fvm.nos_packages[].{}")
    nos_package = {
      'version': elem['version'],
      'file': elem['file'],
    }
    fvm['nos_packages'].append(nos_package)
  return fvm

def _get_json_eula(d):
  if 'user' not in d:
    raise Exception("key 'user' not in root.eula.{}")
  if 'company' not in d:
    raise Exception("key 'user' not in root.company.{}")
  if 'title' not in d:
    raise Exception("key 'password' not in root.title.{}")
  eula = {
    'user': d['user'],
    'company': d['company'],
    'title': d['title'],
    'enable_pulse': d.get('enable_pulse', False),
  }

  return eula

def _get_json_containers(d):
  containers = []
  for elem in d:
    if 'name' not in elem:
      raise Exception("key 'name' not in root.containers[].{}")
    container = {
      'name': elem['name']
    }
    containers.append(container)
  return containers

def _get_json_networks(d):
  networks = []
  for elem in d:
    if 'name' not in elem:
      raise Exception("key 'name' not in root.networks[].{}")
    if 'vlan' not in elem:
      raise Exception("key 'name' not in root.networks[].{}")
    network = {
      'name': elem['name'],
      'vlan': elem['vlan']
    }
    networks.append(network)
  return networks

def _get_json_ipam_networks(d):
  ipam_networks = []
  for elem in d:
    if 'name' not in elem:
      raise Exception("key 'name' not in root.ipam_networks[].{}")
    if 'vlan' not in elem:
      raise Exception("key 'vlan' not in root.ipam_networks[].{}")
    if 'network' not in elem:
      raise Exception("key 'network' not in root.ipam_networks[].{}")
    if 'prefix' not in elem:
      raise Exception("key 'prefix' not in root.ipam_networks[].{}")
    if 'gateway' not in elem:
      raise Exception("key 'gateway' not in root.ipam_networks[].{}")
    if 'dns' not in elem:
      raise Exception("key 'dns' not in root.ipam_networks[].{}")
    if 'pools' not in elem:
      raise Exception("key 'pools' not in root.ipam_networks[].{}")
    ipam_network = {
      'name': elem['name'],
      'vlan': elem['vlan'],
      'network': elem['network'],
      'prefix': elem['prefix'],
      'gateway': elem['gateway'],
      'dns': elem['dns'],
      'pools': [],
    }
    for elem2 in elem['pools']:
      if 'from' not in elem2:
        raise Exception("key 'from' not in root.ipam_networks[].pools[].{}")
      if 'to' not in elem2:
        raise Exception("key 'to' not in root.ipam_networks[].pools[].{}")
      pool = {
        'from': elem2['from'],
        'to':   elem2['to']
      }
      ipam_network['pools'].append(pool)
    ipam_networks.append(ipam_network)
  return ipam_networks    

def _get_json_images(d):
  images = []
  for elem in d:
    if 'name' not in elem:
      raise Exception("key 'name' not in root.images[].{}")
    if 'container' not in elem:
      raise Exception("key 'container' not in root.images[].{}")
    if 'url' not in elem:
      raise Exception("key 'url' not in root.images[].{}")
    image = {
      'name': elem['name'],
      'container': elem['container'],
      'url': elem['url']
    }
    images.append(image)
  return images

def _get_json_credential(d):
  if 'user' not in d:
    raise Exception("key 'user' not in root.credential{}")
  if 'password' not in d:
    raise Exception("key 'password' not in root.credential{}")
  credential = {
    'user': d['user'],
    'password': d['password']
  }
  return credential

def _get_json_foundation(d):
  if 'aos_version' not in d:
    raise Exception("key 'aos_version' not in root.foundation{}")
  foundation = {
    'aos_version': d['aos_version']
  }
  return foundation

def _get_json_report_server(d):
  if 'host' not in d:
    raise Exception("key 'host' not in root.report_server{}")
  if 'port' not in d:
    raise Exception("key 'port' not in root.report_server{}")
  report_server = {
    'send': d['send'],
    'host': d['host'],
    'port': d['port'],
    'user': d['user'],
    'password': d['password'],
    'uuid': d['uuid'],
  }
  return report_server