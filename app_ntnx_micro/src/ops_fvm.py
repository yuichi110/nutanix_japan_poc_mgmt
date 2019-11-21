import json
import sys
import logging
import time
import os
import traceback
import threading
from server_base import send_report, send_fail_report
from client_fvm import NutanixFoundationClient

def check(cluster, nodes, basics, fvm, foundation, report_server):
  def fun():
    a, b, c, d = 0, 0, 0, 0
    progress = 0
    try:
      print('check: start')
      send_report(report_server, progress, get_check_status(a, b, c, d))
      ops = FvmOps(cluster, nodes, basics, fvm, foundation, report_server)
      a = 1
      progress = 10
      send_report(report_server, progress, get_check_status(a, b, c, d))
      ops.connect_to_fvm()
      b = 1
      progress = 40
      send_report(report_server, progress, get_check_status(a, b, c, d))
      ops.check_ipmi_mac()
      c = 1
      progress = 70
      send_report(report_server, progress, get_check_status(a, b, c, d))
      ops.check_ipmi_ip()
      d = 1
      progress = 100
      send_report(report_server, progress, get_check_status(a, b, c, d))
      print('check: complete')
    except Exception as exception:
      print(exception)
      send_fail_report(report_server, progress, get_check_status(a, b, c, d), exception)

  threading.Thread(target=fun).start()

def get_check_status(a, b, c, d):
  s = {
    0: '',
    1: 'Done',
    2: 'Skip',
  }
  up_status = '''connecting to fvm: {}
start checking ipmi mac exist: {}
start checking ipmi ip has no conflict: {}
check passed: {}
'''
  return up_status.format(s[a], s[b], s[c], s[d])


def image(cluster, nodes, basics, fvm, foundation, report_server):
  def fun():
    a, b, c, d, e, f, g, h, i = 0, 0, 0, 0, 0, 0, 0, 0, ''
    try:
      print('image: start')
      send_report(report_server, 0, get_image_status(a, b, c, d, e, f, g, h, i))
      ops = FvmOps(cluster, nodes, basics, fvm, foundation, report_server)
      a = 1
      send_report(report_server, 10, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.connect_to_fvm()
      b = 1
      send_report(report_server, 20, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.check_ipmi_mac()
      c = 1
      send_report(report_server, 30, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.check_ipmi_ip()
      d = 1
      send_report(report_server, 40, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.set_foundation_settings()
      e = 1
      send_report(report_server, 50, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.configure_ipmi_ip()
      f = 1
      send_report(report_server, 60, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.pre_check()
      g = 1
      send_report(report_server, 70, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.start_foundation()
      h = 1
      send_report(report_server, 80, get_image_status(a, b, c, d, e, f, g, h, i))
      ops.poll_progress()
      i = 'Imaging Success: 100%'
      send_report(report_server, 100, get_image_status(a, b, c, d, e, f, g, h, i))
      print('image: complete')
    except Exception as exception:
      print(exception)
      send_fail_report(report_server, 100, get_image_status(a, b, c, d, e, f, g, h, i), exception)

  threading.Thread(target=fun).start()

def get_image_status(a, b, c, d, e, f, g, h, i):
  s = {
    0: '',
    1: 'Done',
    2: 'Skip',
  }
  up_status = '''connecting to fvm: {}
start checking ipmi mac exist: {}
start checking ipmi ip has no conflict: {}
check passed: {}
set foundation settings: {}
configure ipmi ip: {}
foundation pre check: {}
start foundation: {}

progress: 
{}
'''
  return up_status.format(s[a], s[b], s[c], s[d], s[e], s[f], s[g], s[h], str(i))

def abort(fvmip, user, password):
  def fun():
    pass
  threading.Thread(target=fun).start()


class FvmOps:

  def __init__(self, cluster, nodes, basics, fvm, foundation, report_server):
    print('fvm ops created')
    self.fvm = fvm
    self.nodes = nodes
    self.report_server = report_server

    self.external_ip = cluster['ip']
    self.cluster_name = cluster['name']
    self.netmask = basics['netmask']
    self.gateway = basics['gateway']
    self.name_server = basics['name_server']
    self.ntp_server = basics['ntp_server']
    self.aos_version = foundation['aos_version']
    self.nos_package = ''
    for nos_package in fvm["nos_packages"]:
      if nos_package['version'] == self.aos_version:
        self.nos_package = nos_package['file']
    if self.nos_package == '':
      raise Exception('choosed aos image does not exist.')

    def get_nodeinfo_list(nodes):
      nodeinfo_list = []
      for node in nodes:
        nodeinfo = (node['ipmi_mac'], node['ipmi_ip'], node['host_ip'],
          node['cvm_ip'], node['host_name'], node['position'])
        nodeinfo_list.append(nodeinfo)
      return nodeinfo_list
    self.nodeinfo_list = get_nodeinfo_list(nodes)
    print(self.nodeinfo_list)

    print('fvm ops initialize completed')

  def send_report(self):
    if not self.report_server['send']:
      return
    print()

  def connect_to_fvm(self):
    print('connect_to_fvm()')
    ips = self.fvm['ips']
    user = self.fvm['user']
    password = self.fvm['password']
    print('candidates: {}'.format(ips))
    print('credential: {}, {}'.format(user, password))

    found = False
    for ip in ips:
      try:
        client = NutanixFoundationClient(ip, user, password)

        (success, result) = client.get_progress()
        if not success:
          raise Exception('failed to get progress. {}'.format(json.dumps(result)))
        if not result['imaging_stopped']:
          raise Exception('imaging now')

        (success, nos_packages) = client.get_nos_packages()
        if not success:
          raise Exception('failed to get nos packages. {}'.format(json.dumps(result)))
        if not self.nos_package in nos_packages:
          raise Exception('nos package {} is not in fvm'.format(self.aos_version))

        print('fvm:{} is ready'.format(ip))
        self.client = client
        found = True
        break
      except Exception as e:
        print('fvm:{} is not ready. Reason "{}"'.format(ip, e))

    if not found:
      print('no fvm is available.')
      raise ErrorException('no fvm is available in {}'.format(ips))

  def check_ipmi_mac(self):   
    print('check_ipmi_mac()')
    problem_mac_list = []
    for node in self.nodes:
      position = node['position'].upper()
      print('node position: {}'.format(position))

      # MAC address check
      ipmi_mac = node['ipmi_mac']
      result = self.client.does_mac_exist(ipmi_mac, 'eth0')
      if not result:
        print('ipmi mac "{}" does not exist on the segment'.format(ipmi_mac))
        problem_mac_list.append(ipmi_mac)
      else:
        text = 'ipmi mac "{}" exists on the segment'.format(ipmi_mac)
      print(text)

    if len(problem_mac_list) != 0:
      raise ErrorException('mac {} do not exist'.format(problem_mac_list))

  def check_ipmi_ip(self):
    print('check_ipmi_ip()')
    problem_ip_list = []
    for node in self.nodes:
      position = node['position'].upper()
      print('node position: {}'.format(position))
      
      ipmi_mac = node['ipmi_mac'].lower()
      ipmi_ip = node['ipmi_ip']
      (success, result) = self.client.get_mac_from_ip(ipmi_ip)
      exist = result['exist']
      found_mac = result['mac'].lower()

      if not result['exist']:
        print('ipmi ip "{}" does not exist'.format(ipmi_ip))
      elif ipmi_mac == found_mac:
        print('the ipmi already has ip "{}"'.format(ipmi_ip))
      else:
        print('ipmi ip "{}" is already used by another host "{}".'.format(ipmi_ip, found_mac))
        problems.append(ipmi_ip)

    if len(problem_ip_list) != 0:
      raise ErrorException('unable to use ip {} due to conflict(already used by other host)'.format(problem_ip_list))


  def set_foundation_settings(self):
    print('reset foundation vm')
    (success, result) = self.client.reset_state()
    if not success:
      print('failed to reset')
      raise ErrorException("Failed to reset foundation state.")

    print('get nic address list')
    (success, nics) = self.client.get_nics()
    if not success:
      raise ErrorException("Failed to get nic list")
    primary_nic = ''
    for (nic, nic_info) in nics.items():
      if nic_info['name'].lower() == 'eth0':
        primary_nic = nic
        break
    if primary_nic == '':
      raise ErrorException('foundation vm has no eth0')

    print('set eth0 as primary nic')
    (success, result) = self.client.choose_primary_nic(primary_nic)
    if not success:
      raise ErrorException('failed to set eth0 as primary nic')

  def configure_ipmi_ip(self):
    print('configure ipmi ip. may take few minutes')
    (success, result) = self.client.ipmi_config(
      self.netmask, self.gateway, self.nodeinfo_list, self.cluster_name, 
      self.external_ip, self.name_server, self.ntp_server, self.nos_package)
    if not success:
      error = 'failed to configure ipmi ip. reason "{}"'.format(response['error'])
      print(error)
      raise ErrorException(error)

  def pre_check(self):
    print('pre check. may take few minutes')
    (success, result) = self.client.pre_check(
      self.netmask, self.gateway, self.nodeinfo_list, self.cluster_name, 
      self.external_ip, self.name_server, self.ntp_server, self.nos_package)
    if not success:
      print('failed to pre check. reason "{}"'.format(response['error']))
      raise ErrorException('Failed to do pre check.')

  def start_foundation(self):
    print('kick imaging nodes')
    (success, result) = self.client.image_nodes(
      self.netmask, self.gateway, self.nodeinfo_list, self.cluster_name, 
      self.external_ip, self.name_server, self.ntp_server, self.nos_package)
    if not success:
      error = 'failed to kick imaging. reason "{}"'.format(response['error'])
      print(error)
      raise ErrorException(error)

  def poll_progress(self):
    count = 0
    max_count = 5
    aggregate_percent = 0
    ABORTED = -1
    STOPPED = -2
    ERROR = -3
    print('keep pooling progress till end(finish or error)')
    while True:
      try:
        (success, result) = self.client.get_progress()
        if not success:
          return (False, 0)

        aggregate_percent = result['aggregate_percent_complete']
        print('progress: {}'.format(aggregate_percent))
        if aggregate_percent == 100:
          break
        else:
          if 'abort_session' in result:
            if result['abort_session'] == True:
              aggregate_percent = ABORTED
              break
          elif result['imaging_stopped'] == True:
            aggregate_percent = STOPPED
            break

      except:
        count += 1
        if count > max_count:
          aggregate_percent = ERROR
          break

      time.sleep(5)

    if aggregate_percent == ABORTED:
      print('imaging was aborted')
      raise ErrorException('imaging was aborted.')
    elif aggregate_percent == STOPPED:            
      print('imaging was stopped')
      raise ErrorException('imaging was stopped.')
    elif aggregate_percent == ERROR:
      print('imaging failed with unexpected error')
      raise ErrorException('imaging failed with unexpected error')


class ErrorException(Exception):
  pass