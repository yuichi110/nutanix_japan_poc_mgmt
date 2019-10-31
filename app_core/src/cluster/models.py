from django.db import models
from django.core.exceptions import ValidationError
from common.errors import *

import uuid
import json

class Cluster(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100, unique=True)
  data = models.TextField()

  def __str__(self):
    return 'NAME:{}, UUID:{}'.format(self.name, self.uuid)

  @classmethod
  def exists(cls, cluster_uuid):
    return Cluster.objects.filter(uuid=cluster_uuid).exists()

  @classmethod
  def create(cls, json_text):
    d = cls._get_normalize_json(json_text)
    name = d['cluster']['name']
    if Cluster.objects.filter(name=name).exists():
      raise Exception400('same name cluster already exist')

    cluster_object = Cluster.objects.create(name=d['cluster']['name'], data='')
    d['uuid'] = str(cluster_object.uuid)
    cluster_object.data = json.dumps(d, indent=2)
    cluster_object.save()
    return d

  @classmethod
  def read(cls, cluster_uuid):
    cluster_object = Cluster.objects.filter(uuid=cluster_uuid)[0]
    return json.loads(cluster_object.data)

  @classmethod
  def read_all(cls):
    cluster_objects = Cluster.objects.all()
    cluster_list = [json.loads(cluster_object.data) for cluster_object in cluster_objects]
    return cluster_list

  @classmethod
  def update(cls, cluster_uuid, json_text):
    cluster_object = Cluster.objects.filter(uuid=cluster_uuid)[0]
    d = cls._get_normalize_json(json_text)
    new_name = d['cluster']['name']
    if new_name != cluster_object.name:
      if Cluster.objects.filter(name=new_name).exists():
        raise Exception400('same name cluster already exist')

    d['uuid'] = str(cluster_uuid)
    cluster_object.name = new_name
    cluster_object.data = json.dumps(d, indent=2)
    cluster_object.save()
    return d

  @classmethod
  def delete_(cls, cluster_uuid):
    cluster_object = Cluster.objects.filter(uuid=cluster_uuid)[0]
    cluster_object.delete()
    return {}

  @classmethod
  def _get_normalize_json(cls, json_text):
    try:
      d = json.loads(json_text)
    except:
      raise Exception('failed to parse json')

    if 'cluster' not in d:
      raise Exception400("key 'cluster' not in json")
    if 'nodes' not in d:
      raise Exception400("key 'cluster' not in json")
    if 'fvm' not in d:
      raise Exception400("key 'fvm' not in json")
    if 'eula' not in d:
      raise Exception400("key 'eula' not in json")
    if 'containers' not in d:
      raise Exception400("key 'fvm' not in json")
    if 'networks' not in d:
      raise Exception400("key 'fvm' not in json")
    if 'ipam_networks' not in d:
      raise Exception400("key 'fvm' not in json")
    if 'images' not in d:
      raise Exception400("key 'fvm' not in json")    

    d = {
      'cluster':cls._get_json_cluster(d['cluster']),
      'nodes':cls._get_json_nodes(d['nodes']),
      'fvm':cls._get_json_fvm(d['fvm']),
      'eula':cls._get_json_eula(d['eula']),
      'containers':cls._get_json_containers(d['containers']),
      'networks':cls._get_json_networks(d['networks']),
      'ipam_networks':cls._get_json_ipam_networks(d['ipam_networks']),
      'images':cls._get_json_images(d['images'])
    }
    return d

  @classmethod
  def _get_json_cluster(cls, d):
    if 'ip' not in d:
      raise Exception400("key 'ip' not in root.cluster")
    if 'user' not in d:
      raise Exception400("key 'user' not in root.cluster")
    if 'password' not in d:
      raise Exception400("key 'password' not in root.cluster")
    if 'name' not in d:
      raise Exception400("key 'name' not in root.cluster")
    if 'netmask' not in d:
      raise Exception400("key 'netmask' not in root.cluster")
    if 'gateway' not in d:
      raise Exception400("key 'gateway' not in root.cluster")
    if 'ntp_server' not in d:
      raise Exception400("key 'ntp_server' not in root.cluster")
    if 'name_server' not in d:
      raise Exception400("key 'name_server' not in root.cluster")
    if 'language' not in d:
      raise Exception400("key 'language' not in root.cluster")

    cluster = {
      'ip':d['ip'],
      'user':d['user'],
      'password':d['password'],
      
      'name':d['name'],
      'netmask':d['netmask'],
      'gateway':d['gateway'],
      'ntp_server':d['ntp_server'],
      'name_server':d['name_server'],
      'language':d['language'],
    }
    return cluster

  @classmethod
  def _get_json_nodes(cls, d):
    nodes = []
    for elem in d:
      if 'host_name' not in elem:
        raise Exception400("key 'host_name' not in root.nodes.{}")
      if 'position' not in elem:
        raise Exception400("key 'position' not in root.nodes.{}")
      if 'ipmi_mac' not in elem:
        raise Exception400("key 'ipmi_mac' not in root.nodes.{}")
      if 'ipmi_ip' not in elem:
        raise Exception400("key 'ipmi_ip' not in root.nodes.{}")
      if 'host_ip' not in elem:
        raise Exception400("key 'host_ip' not in root.nodes.{}")
      if 'cvm_ip' not in elem:
        raise Exception400("key 'cvm_ip' not in root.nodes.{}")

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
        'cvm_password': elem.get('nutanix/4u')
      }
      nodes.append(node)
    return nodes

  @classmethod
  def _get_json_fvm(cls, d):
    if 'ips' not in d:
      raise Exception400("key 'ip' not in root.fvm.{}")
    if 'user' not in d:
      raise Exception400("key 'user' not in root.fvm.{}")
    if 'password' not in d:
      raise Exception400("key 'password' not in root.fvm.{}")
    if 'nos_packages' not in d:
      raise Exception400("key 'name' not in root.fvm.{}")

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
        raise Exception400("key 'version' not in root.fvm.nos_packages[].{}")
      if 'file' not in elem:
        raise Exception400("key 'file' not in root.fvm.nos_packages[].{}")

      nos_package = {
        'version': elem['version'],
        'file': elem['file'],
      }
      fvm['nos_packages'].append(nos_package)

    return fvm

  @classmethod
  def _get_json_eula(cls, d):
    if 'user' not in d:
      raise Exception400("key 'user' not in root.eula.{}")
    if 'company' not in d:
      raise Exception400("key 'user' not in root.company.{}")
    if 'title' not in d:
      raise Exception400("key 'password' not in root.title.{}")
    eula = {
      'user': d['user'],
      'company': d['company'],
      'title': d['title']
    }
    return eula

  @classmethod
  def _get_json_containers(cls, d):
    containers = []
    for elem in d:
      if 'name' not in elem:
        raise Exception("key 'name' not in root.containers[].{}")
      container = {
        'name': elem['name']
      }
      containers.append(container)
    return containers

  @classmethod
  def _get_json_networks(cls, d):
    networks = []
    for elem in d:
      if 'name' not in elem:
        raise Exception400("key 'name' not in root.networks[].{}")
      if 'vlan' not in elem:
        raise Exception400("key 'name' not in root.networks[].{}")
      network = {
        'name': elem['name'],
        'vlan': elem['vlan']
      }
      networks.append(network)
    return networks

  @classmethod
  def _get_json_ipam_networks(cls, d):
    ipam_networks = []
    for elem in d:
      if 'name' not in elem:
        raise Exception400("key 'name' not in root.ipam_networks[].{}")
      if 'vlan' not in elem:
        raise Exception400("key 'vlan' not in root.ipam_networks[].{}")
      if 'network' not in elem:
        raise Exception400("key 'network' not in root.ipam_networks[].{}")
      if 'prefix' not in elem:
        raise Exception400("key 'prefix' not in root.ipam_networks[].{}")
      if 'gateway' not in elem:
        raise Exception400("key 'gateway' not in root.ipam_networks[].{}")
      if 'dns' not in elem:
        raise Exception400("key 'dns' not in root.ipam_networks[].{}")
      if 'pools' not in elem:
        raise Exception400("key 'pools' not in root.ipam_networks[].{}")

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
          raise Exception400("key 'from' not in root.ipam_networks[].pools[].{}")
        if 'to' not in elem2:
          raise Exception400("key 'to' not in root.ipam_networks[].pools[].{}")
        pool = {
          'from': elem2['from'],
          'to':   elem2['to']
        }
        ipam_network['pools'].append(pool)

      ipam_networks.append(ipam_network)
    return ipam_networks    

  @classmethod
  def _get_json_images(cls, d):
    images = []
    for elem in d:
      if 'name' not in elem:
        raise Exception400("key 'name' not in root.images[].{}")
      if 'container' not in elem:
        raise Exception400("key 'container' not in root.images[].{}")
      if 'url' not in elem:
        raise Exception400("key 'url' not in root.images[].{}")
      image = {
        'name': elem['name'],
        'container': elem['container'],
        'url': elem['url']
      }
      images.append(image)
    return images