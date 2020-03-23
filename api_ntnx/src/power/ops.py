import json
import sys
import logging
import time
import os
import traceback
import threading
from power.client import NutanixPowerClient, NutanixClusterClient

_print = print
def print(text):
  _print(text, flush=True)

def on(cluster, nodes, set_status):
  def fun():
    a, b, c, d, e, f, g = 0, 0, 0, 0, 0, 0, 0
    progress = 0
    try:
      is_finished = False
      is_failed = False
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
      ops = PowerOps(cluster, nodes)
      a = 1
      progress = 10
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
      ops.up_all_host()
      b = 1
      progress = 20
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
      ops.wait_till_all_host_becoming_accesible()
      c = 1
      progress = 40
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
      ops.wait_till_all_cvm_up()
      d = 1
      progress = 60
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
      ops.wait_till_all_cvm_accessible()
      e = 1
      f = 1
      progress = 80
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
      ops.up_cluster()
      g = 1
      progress = 100
      is_finished = True
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
    except Exception as exception:
      print(exception)
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
      
  threading.Thread(target=fun).start()

def get_up_status(a, b, c, d, e, f, g):
  s = {
    0: '',
    1: 'Done',
    2: 'Skip',
  }
  up_status = '''power on all host: {}
all hosts are up: {}
all hosts are accessible: {}
all cvm are up: {}
all cvm are accessible: {}
initiate cluster start: {}
cluster is up: {}
'''
  return up_status.format(s[a], s[b], s[c], s[d], s[e], s[f], s[g])


def off(cluster, nodes, set_status):
  def fun():
    a, b, c, d, e, f, g = 0, 0, 0, 0, 0, 0, 0
    progress = 0
    try:
      ops = PowerOps(cluster, nodes)
      is_finished = False
      is_failed = False

      if ops.is_all_cvm_down():
        print('all cvms are already down')
        if ops.is_all_host_down():
          a, b, c, d, e, f, g = 2, 2, 2, 2, 2, 2, 2
          progress = 100
          is_finished = True
          set_status(progress, get_down_status(a, b, c, d, e, f, g), is_finished, is_failed)
        else:
          a, b, c, d, e, f = 2, 2, 2, 2, 2, 1
          progress = 80
          set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
          ops.down_all_hosts()
          g = 1
          progress = 100
          is_finished = True
          set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)

      else:
        if ops.is_cluster_up():
          set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
          ops.down_over_cluster()
          a = 1
          b = 1
          progress = 30
          set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
          ops.down_cluster()
          c = 1
        else:
          a, b, c = 2, 2, 2
        d = 1
        progress = 60
        set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
        ops.down_all_cvms()
        e = 1
        f = 1
        progress = 80
        set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
        ops.down_all_hosts()
        g = 1
        progress = 100
        is_finished = True
        set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
    except Exception as exception:
      print(exception)
      progress = 100
      is_finished = True
      is_failed = True
      set_status(progress, get_up_status(a, b, c, d, e, f, g), is_finished, is_failed)
  threading.Thread(target=fun).start()

def get_down_status(a, b, c, d, e, f, g):
  s = {
    0: '',
    1: 'Done',
    2: 'Skip',
  }
  down_status = '''shutdown guest vms: {}
initiate stopping cluster: {}
cluster is stop: {}
initiate stopping all cvms: {}
cvms are stop: {}
initiate stopping all hosts: {}
hosts are stop: {}
'''
  return down_status.format(s[a], s[b], s[c], s[d], s[e], s[f], s[g])


class PowerOps:
  def __init__(self, cluster, nodes):
    self.ip =       cluster['ip']
    self.user =     cluster['user']
    self.password = cluster['password']
    self.nodes = nodes
    self.session = NutanixPowerClient()

  ###
  ## Check
  ###

  def is_all_host_down(self):
    all_down = True
    for node in self.nodes:
      ipmi_ip = node['ipmi_ip']
      ipmi_user = node['ipmi_user']
      ipmi_password = node['ipmi_password']
      (success, is_down) = self.session.is_host_down(ipmi_ip, ipmi_user, ipmi_password)
      if not success:
        raise Exception('error happens')
      print('host {} is down:{}'.format(node['host_ip'], is_down))
      if not is_down:
        all_down = False
    return all_down

  def is_all_host_up(self):
    all_up = True
    for node in self.nodes:
      ipmi_ip = node['ipmi_ip']
      ipmi_user = node['ipmi_user']
      ipmi_password = node['ipmi_password']
      (success, is_down) = self.session.is_host_down(ipmi_ip, ipmi_user, ipmi_password)
      if not success:
        raise Exception('error happens')
      print('host {} is down:{}'.format(node['host_ip'], is_down))
      if is_down:
        all_up = False
    return all_up

  def is_all_host_accessible(self):
    all_accessible = True
    for node in self.nodes:
      host_ip = node['host_ip']
      host_user = node['host_user']
      host_password = node['host_password']
      (_, accessible) = self.session.is_host_accessible(host_ip, host_user, host_password)
      print('host {} is accessible:{}'.format(host_ip, accessible))
      if not accessible:
        all_accessible = False
    return all_accessible

  def is_all_cvm_down(self):
    all_down = True
    for node in self.nodes:
      host_ip = node['host_ip']
      host_user = node['host_user']
      host_password = node['host_password']
      (success, is_down) = self.session.is_cvm_down(host_ip, host_user, host_password)
      if not success:
        raise Exception('error happens')
      print('cvm {} is down:{}'.format(node['cvm_ip'], is_down))
      if not is_down:
        all_down = False
    return all_down

  def is_all_cvm_up(self):
    all_up = True
    for node in self.nodes:
      host_ip = node['host_ip']
      host_user = node['host_user']
      host_password = node['host_password']
      (success, is_down) = self.session.is_cvm_down(host_ip, host_user, host_password)
      if not success:
        raise Exception('error happens')
      print('cvm {} is down:{}'.format(node['cvm_ip'], is_down))
      if is_down:
        all_up = False
        break
    return all_up

  def is_all_cvm_accessible(self):
    all_accessible = True
    for node in self.nodes:
      cvm_ip = node['cvm_ip']
      cvm_user = node['cvm_user']
      cvm_password = node['cvm_password']
      (_, accessible) = self.session.is_host_accessible(cvm_ip, cvm_user, cvm_password)
      print('cvm {} is accessible:{}'.format(cvm_ip, accessible))
      if not accessible:
        all_accessible = False
    return all_accessible

  def is_cluster_down(self):
    for node in self.nodes:
      ip = node['cvm_ip']
      user = node['cvm_user']
      password = node['cvm_password']
      (success, down) = self.session.is_cluster_down(ip, user, password)
      if not success:
        continue
      return down

    # failed to get cluster status from all cvms.
    # judge cluster is down 
    return True

  def is_cluster_up(self):
    return not self.is_cluster_down()


  ###
  ## UP
  ###

  def up_all_host(self):
    print('up_all_host()')
    for i in range(5):
      if self.is_all_host_up():
        return
      for node in self.nodes:
        ipmi_ip = node['ipmi_ip']
        ipmi_user = node['ipmi_user']
        ipmi_password = node['ipmi_password']
        host_ip = node['host_ip']
        print('power on host {} through ipmi'.format(host_ip))
        (success, _) = self.session.up_host(ipmi_ip, ipmi_user, ipmi_password)
        if not success:
          print('failed to power on host: {}'.format(host_ip))
      time.sleep(20)
    raise Exception("Unable to power on hosts via IPMI.")

  def wait_till_all_host_becoming_accesible(self):
    print('wait_till_all_host_becoming_accesible()')
    for i in range(60):
      if self.is_all_host_accessible():
        return
      print('waiting all host become accessible. {}/60'.format(i))
      time.sleep(5)
    raise Exception("Failed to see all CVMs are up")

  def wait_till_all_cvm_up(self):
    print('wait_till_all_cvm_up()')
    for i in range(12):
      try:
        if self.is_all_cvm_up():
          return
      except:
        pass
      print('waiting all cvm up. {}/12'.format(i))
      time.sleep(5)
    raise Exception("Failed to see all CVMs are up")

  def wait_till_all_cvm_accessible(self):
    print('wait_till_all_cvm_accessible()')
    for i in range(24):
      try:
        if self.is_all_cvm_accessible():
          return
      except:
        pass
      print('waiting all cvm become accessible. {}/24'.format(i))
      time.sleep(5)
    raise Exception("Failed to see all CVMs are up")

  def up_cluster(self):
    print('up_cluster()')
    node = self.nodes[0]
    ip = node['cvm_ip']
    user = node['cvm_user']
    password = node['cvm_password']

    for i in range(30):
      (success, is_down) = self.session.is_cluster_down(ip, user, password)
      if success:
        if not is_down:
          return
        else:
          self.session.up_cluster(ip, user, password)
      time.sleep(10)
    raise Exception("failed to start cluster")


  ####
  ## Down Over Cluster
  ####

  def down_over_cluster(self):
    print('down_over_cluster()')
    self.down_all_guestvms()

  def down_all_guestvms(self):
    print('down_all_guestvms()')
    client = NutanixClusterClient(self.ip, self.user, self.password)
    for i in range(6):
      try:
        (_, vm_uuids) = client.get_poweredon_vms()
        if len(vm_uuids) == 0:
          return
        else:
          print('power on vms: {}'.format(vm_uuids))
        for vm_uuid in vm_uuids:
          if i<5:
            client.shutdown_vm(vm_uuid)
          else:
            client.poweroff_vm(vm_uuid)
      except:
        pass
      time.sleep(10)

    raise Exception('failed to off all vms')

  def down_cluster(self):
    print('down_cluster()')
    if self.is_cluster_down():
      return

    for node in self.nodes:
      cvm_ip = self.nodes[0]['cvm_ip']
      cvm_user = self.nodes[0]['cvm_user']
      cvm_password = self.nodes[0]['cvm_password']
      (success, _) = self.session.down_cluster(cvm_ip, cvm_user, cvm_password)
      if success:
        break

    for i in range(12):
      if self.is_cluster_down():
        time.sleep(10)
        return
      time.sleep(5)
    raise Exception('failed to stop cluster')

  def down_all_cvms(self):
    print('down_all_cvms()')
    for node in self.nodes:
      cvm_ip = node['cvm_ip']
      cvm_user = node['cvm_user']
      cvm_password = node['cvm_password']
      (success, _) = self.session.down_cvm(cvm_ip, cvm_user, cvm_password)
      print('cvm {} down request success:{}'.format(cvm_ip, success))

    for i in range(36):
      if self.is_all_cvm_down():
        return
      print('waiting all cvms are down {}/36'.format(i))
      time.sleep(5)
    raise Exception('failed to down all cvms')

  def down_all_hosts(self):
    print('down_all_hosts()')
    for node in self.nodes:
      host_ip = node['host_ip']
      host_user = node['host_user']
      host_password = node['host_password']
      (success, _) = self.session.down_host(host_ip, host_user, host_password)
      print('host {} down request success:{}'.format(host_ip, success))

    for i in range(24):
      if self.is_all_host_down():
        return
      print('waiting all hosts are down {}/24'.format(i))
      time.sleep(5)

    self.down_all_hosts_force()

  def down_all_hosts_force(self):
    print('down_all_hosts_force()')
    for node in self.nodes:
      ipmi_ip = node['ipmi_ip']
      ipmi_user = node['ipmi_user']
      ipmi_password = node['ipmi_password']
      self.session.down_host_force(ipmi_ip, ipmi_user, ipmi_password)
