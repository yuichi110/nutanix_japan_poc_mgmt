import json
import sys
import threading
import time
import os
import traceback
from client_setup import NutanixSetupClient

def run(cluster, basics, containers, networks, ipam_networks, images, report_server):
  def fun():
    a, b, c, d, e, f, g, h, i = 0, 0, 0, 0, 0, 0, 0, 0, ''
    progress = 0
    try:
      a = 1
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops = SetupOps(cluster, basics, containers, networks, ipam_networks, images, report_server)
      ops.connect_to_prism()
      b = 1
      progress = 10
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops.set_language()
      c = 1
      progress = 20
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops.delete_unused_containers()
      d = 1
      progress = 30
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops.create_containers()
      e = 1
      progress = 40
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops.delete_unused_networks()
      f = 1
      progress = 50
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops.create_networks()
      g = 1
      progress = 60
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops.create_ipam_networks()
      h = 1
      progress = 70
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))
      ops.create_images()
      i = 'upload complete'
      progress = 100
      send_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i))

    except Exception as exception:
      print('failed with error: {}'.format(exception))
      send_fail_report(report_server, progress, get_setup_status(a, b, c, d, e, f, g, h, i), exception)
  threading.Thread(target=fun).start()

def get_setup_status(a, b, c, d, e, f, g, h, i):
  s = {
    0: '',
    1: 'Done',
    2: 'Skip',
  }
  up_status = '''connecting to prism: {}
connected to prism: {}
set language: {}
delete unused containers: {}
create containers: {}
delete unused networks: {}
create networks: {}
create ipam networks: {}
upload images progress:
{}
'''
  return up_status.format(s[a], s[b], s[c], s[d], s[e], s[f], s[g], s[h], str(i))

class SetupOps:
  def __init__(self, cluster, basics, containers, networks, ipam_networks, images, report_server):
    self.session = None
    self.ip =       cluster['ip']
    self.user =     cluster['user']
    self.password = cluster['password']
    self.language = basics['language']

    self.containers = containers
    self.networks =   networks
    self.ipam_networks = ipam_networks
    self.images = images

  def connect_to_prism(self):
    print('connect_to_prism()')
    print('ip={}, user={}, password={}'.format(self.ip, self.user, self.password))
    try:
      self.session = NutanixSetupClient(self.ip, self.user, self.password)
    except:
      error = "failed to connect to prism"
      print(error)
      raise ErrorException(error)

  def set_language(self):
    print('set_language()')
    print('language={}'.format(self.language))
    language = self.language.lower()
    lmap = {'en-us':'en-US', 'ja-jp':'ja-JP', 'zh-cn':'zh-CN'}
    if language not in ['en-us', 'ja-jp', 'zh-cn']:
      error = 'failed to set language. {} not in {}'.format(self.language, ['en-US', 'ja-JP', 'zh-CN'])
      print(error)
      raise ErrorException(error)

    (success, result) = self.session.change_language('admin', lmap[language])
    if not success:
      error = "failed to set language. reason '{}'".format(response['error'])
      print(error)
      raise ErrorException(error)

  def delete_unused_containers(self):
    print('delete_unused_containers()')
    (success, existing_containers) = self.session.get_container_names()
    if not success:
      error = "get container names failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)

    for existing_container in existing_containers:
      (success, container_info) = self.session.get_container_info(existing_container)
      if not success:
        error = "get container info failed. reason '{}'".format(result['error'])
        print(error)
        raise ErrorException(error)
      if container_info['usage'] != '0':
        continue

      (success, _) = self.session.delete_container(existing_container)
      if not success:
        error = "delete container failed. reason '{}'".format(result['error'])
        print(error)
        raise ErrorException(error)
      else:
        print("delete container '{}'".format(existing_container))

  def create_containers(self):
    print('create_containers()')
    (success, existing_containers) = self.session.get_container_names()
    if not success:
      edict = existing_containers
      error = "get container names failed. reason '{}'".format(edict['error'])
      print(error)
      raise ErrorException(error)

    task_list = []
    for container in self.containers:
      name = container['name']
      if name in existing_containers:
        continue
      (success, taskuuid) = self.session.create_container(name)
      if not success:
        edict = taskuuid
        error = "create container failed. reason '{}'".format(edict)
        print(error)
        raise ErrorException(error)
      else:
        print("create container '{}'".format(name))
      task_list.append(taskuuid)

    # wait till end
    self.wait_tasks(task_list)

  def delete_unused_networks(self):
    print('delete_unused_networks()')
    (success, existing_networks) = self.session.get_network_names()
    if not success:
      error = "session.get_network_names() failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)

    task_list = []
    for existing_network in existing_networks:
      (success, used) = self.session.is_network_used(existing_network)
      if not success:
        error = "session.is_network_used() failed. reason '{}'".format(result['error'])
        print(error)
        raise ErrorException(error)
      if used:
        continue

      (success, taskuuid) = self.session.delete_network(existing_network)
      if not success:
        error = "session.delete_network() failed. reason '{}'".format(result['error'])
        print(error)
        raise ErrorException(error)
      else:
        print("delete network '{}'".format(existing_network))
      task_list.append(taskuuid)

    self.wait_tasks(task_list)

  def create_networks(self):
    print('create_networks()')
    (success, existing_networks) = self.session.get_network_names()
    if not success:
      error = "session.get_network_names() failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)

    task_list = []
    for network in self.networks:
      name = network['name']
      vlan = network['vlan']
      if name in existing_networks:
        continue
      (success, taskuuid) = self.session.create_network(name, vlan)
      if not success:
        error = "session.create_network() failed. reason '{}'".format(result['error'])
        print(error)
        raise ErrorException(error)
      else:
        print("create network '{}'".format(name))
      task_list.append(taskuuid)

    self.wait_tasks(task_list)

  def create_ipam_networks(self):
    print('create_ipam_networks()')
    (success, hypervisor) = self.session.get_hypervisor()
    if not success:
      error = "session.get_hypervisor() failed. reason '{}'".format(result['error'])
      print(error)
      raise ErrorException(error)
    if hypervisor.lower() != 'ahv':
      return

    (success, existing_networks) = self.session.get_network_names()
    if not success:
      edict = existing_networks
      error = "session.get_network_names() failed. reason '{}'".format(edict)
      print(error)
      raise ErrorException(error)

    task_list = []
    for ipam_network in self.ipam_networks:
      name = ipam_network['name']
      if name in existing_networks:
        continue

      vlan = ipam_network['vlan']
      network = ipam_network['network']
      prefix = ipam_network['prefix']
      gateway = ipam_network['gateway']
      pools = ipam_network['pools']
      dns = ipam_network['dns']
      (success, taskuuid) = self.session.create_network_managed(name, vlan, network, 
        prefix, gateway, pools, dns)
      if not success:
        edict = taskuuid
        error = "session.create_network_managed() failed. reason '{}'".format(edict)
        print(error)
        raise ErrorException(error)
      else:
        print("create ipam network '{}'".format(name))
      task_list.append(taskuuid)

    self.wait_tasks(task_list)

  def create_images(self):
    print('create_images()')
    (success, existing_images) = self.session.get_image_names()
    if not success:
      edict = existing_images
      error = "session.get_image_names() failed. reason '{}'".format(edict)
      print(error)
      raise ErrorException(error)

    (success, containers) = self.session.get_container_names()
    if not success:
      error = "session.get_container_names() failed. reason '{}'".format(edict)
      print(error)
      raise ErrorException(error)

    task_list = []
    for image in self.images:
      name = image['name']
      container = image['container']
      url = image['url']

      if name in existing_images:
        continue
      if container not in containers:
        error = "container does not exist. '{}'".format(container)
        print(error)
        raise ErrorException(error)

      (success, taskuuid) = self.session.upload_image(url, container, name)
      if not success:
        edict = taskuuid
        error = "session.upload_image() failed. reason '{}'".format(edict)
        print(error)
        raise ErrorException(error)
      task_list.append(taskuuid)

    self.wait_tasks(task_list)

  def wait_tasks(self, uuids, interval=5):
    first = True
    while(True):
      (success, tasks) = self.session.get_tasks_status()
      if not success:
        print(tasks)
        continue
        #raise Exception('Error happens on getting tasks status.')

      finished = True
      for task in tasks:
        if task['uuid'] in uuids:
          if first:
            print('Wait till all tasks end. Polling interval {}s.'.format(interval))
            first = False
          print('{} {}% : {}'.format(task['method'], task['percent'], task['uuid']))
          finished = False
        else:
          # Child or other task
          pass

      if finished:
        break
      else:
        print('--')
      time.sleep(interval)

    if not first:
      print('All tasks end.')

class GotoException(Exception):
  pass

class ErrorException(Exception):
  pass
