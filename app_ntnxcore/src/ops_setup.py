import json
import sys
import logging
import time
import os
import traceback
from nutanix_restapi import NutanixFoundationClient, NutanixRestApiClient

class SetupOps:
  def __init__(self, cluster, containers, networks, ipam_networks, images):
    self.session = None
    self.ip =       cluster['ip']
    self.user =     cluster['user']
    self.password = cluster['password']
    self.language = cluster['language']

    self.containers = containers
    self.networks =   networks
    self.ipam_networks = ipam_networks
    self.images = images

  def connect_to_prism(self):
    print('connect_to_prism()')
    try:
      self.session = NutanixCoreClient(self.ip, self.user, self.password)
    except:
      print('  Failed with error "Connection or Credential problem"')
      raise ErrorException('Failed to make connection to Prism.')

  def set_language(self):
    print('set_language()')
    print('language={}'.format(self.language))
    language = self.language.lower()
    lmap = {'en-us':'en-US', 'ja-jp':'ja-JP', 'zh-cn':'zh-CN'}
    if language not in ['en-us', 'ja-jp', 'zh-cn']:
      error = 'failed to set language. {} not in {}'.format(self.language, ['en-US', 'ja-JP', 'zh-CN'])
      print(error)
      raise ErrorException(error)

    (success, result) = self.session.change_language(lmap[language])
    if not success:
      error = "failed to set language. reason '{}'".format(response['error'])
      print(error)
      raise ErrorException(error)

  def delete_unused_containers(self):
    print('delete_unused_containers()')
    (success, existing_containers) = self.session.get_container_names()
    if not success:
      raise Exception('Error happens on getting existing container names.')

    for existing_container in existing_containers:
      (success, container_info) = self.session.get_container_info(existing_container)
      if not success:
        raise Exception('Error happens on getting container info "{}".'.format(existing_container))
      if container_info['usage'] != '0':
        continue
      (success, _) = self.session.delete_container(existing_container)
      if not success:
        raise Exception('Error happens on deleting container "{}".'.format(existing_container)) 

  def create_containers(self):
    print('create_containers()')
    (success, existing_containers) = self.session.get_container_names()
    if not success:
      raise Exception('Error happens on getting existing container names.')

    task_list = []
    for container in self.containers:
      if container in existing_containers:
        continue
      (success, taskuuid) = self.session.create_container(container)
      if not success:
        raise Exception('Error happens on creating container "{}".'.format(container))
      task_list.append(taskuuid)

    # wait till end
    self.wait_tasks(task_list)

  def delete_unused_networks(self):
    print('delete_unused_networks()')
    (success, existing_networks) = self.session.get_network_names()
    if not success:
      raise Exception('Error happens on getting existing networks.')

    task_list = []
    for existing_network in existing_networks:
      (success, used) = self.session.is_network_used(existing_network)
      if not success:
        raise Exception('Error happens on getting existing networks.')
      if used:
        continue
      (success, taskuuid) = self.session.delete_network(existing_network)
      if not success:
        raise Exception('Error happens on getting existing networks.')
      task_list.append(taskuuid)

    self.wait_tasks(task_list)

  def create_networks(self):
    print('create_networks()')
    (success, existing_networks) = self.session.get_network_names()
    if not success:
      raise Exception('Error happens on getting existing networks.')

    for network in self.networks:
      name = network['name']
      vlan = network['vlan']
      if name in existing_networks:
        continue
      (success, taskuuid) = self.session.create_network(name, vlan)
      if not success:
        raise Exception('Error happens on creating network "{}"'.format(name))
      task_list.append(taskuuid)

    self.wait_tasks(task_list)

  def create_ipam_networks(self):
    print('create_ipam_networks()')
    (success, existing_networks) = self.session.get_network_names()
    if not success:
      raise Exception('Error happens on getting existing networks.')

    for network in self.ipam_networks:
      name = network['name']
      vlan = network['vlan']
      if name in existing_networks:
        continue
      if hypervisor != 'AHV':
        (success, taskuuid) = self.session.create_network(name, vlan)
        if not success:
          raise Exception('Error happens on creating network "{}"'.format(name))
      else:
        (success, taskuuid) = self.session.create_network_managed(name, vlan, network, 
          prefix, gateway, pools, dns)
        if not success:
          raise Exception('Error happens on creating network "{}"'.format(name))
      task_list.append(taskuuid)

    self.wait_tasks(task_list)

  def create_images(self):
    print('create_images()')
    (success, containers) = self.session.get_container_names()
    if not success:
      raise Exception('Error happens on checking container existance.')
    (success, existing_images) = self.session.get_image_names()
    if not success:
      raise Exception('Error happens on getting existing images names.')

    task_list = []
    for image in self.images:
      name = image['name']
      container = image['container']
      url = image['url']

      if name in existing_images:
        continue
      if image['container'] not in containers:
        raise Exception('Error happens on uploading image.')

      (success, taskuuid) = self.session.upload_image(url, container, name)
      if not success:
        raise Exception('Error happens on uploading image.')
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
