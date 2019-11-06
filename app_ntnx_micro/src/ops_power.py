import json
import sys
import logging
import time
import os
import traceback
from client_power import NutanixPowerClient

def up():
  def fun():
    try:
      ops = PowerOps(cluster, nodes, report_server)
      ops.all_host_up()
      ops.cluster_up()
    except Exception as e:
      print(e)
  threading.Thread(target=fun).start()

def down():
  def fun():
    try:
      ops = PowerOps(cluster, nodes, report_server)
      ops.all_guestvms_down()
      ops.cluster_down()
      ops.all_cvm_down()
      ops.all_host_down()
    except Exception as e:
      print(e)
  threading.Thread(target=fun).start()


class PowerOps:
  def __init__(self, cluster, nodes):
    self.session = None
    self.ip =       cluster['ip']
    self.user =     cluster['user']
    self.password = cluster['password']

  def all_host_up(self):
    for i in range(5):
      if self.session.is_all_server_power_on():
        return
      for node in self.nodes:
        ipmi_ip = node['ipmi_ip']
        ipmi_user = node['ipmi_user']
        ipmi_password = node['ipmi_password']
        self.session.power_on_server(ipmi_ip, ipmi_user, ipmi_password)
      time.sleep(20)
    raise Exception("Unable to power on servers via IPMI.")

  def cluster_up(self):
    for i in range(30):
      try:
        self.session.is_clusterup(self.prism_ip, self.prism_user, self.prism_password)
        return
      except:
        self.session.clusterup(self.cvm_ips[0], 'nutanix', 'nutanix/4u')
      time.sleep(10)
    raise Exception("failed to start cluster")

  def all_guestvm_down(self):
    for i in range(6):
      try:
        vm_uuids = self.client.get_poweredon_vms()
        if len(vm_uuids) == 0:
          return

        for vm_uuid in vm_uuids:
          if i<5:
            self.client.shutdown_vm(vm_uuid)
          else:
            self.client.poweroff_vm(vm_uuid)
      except:
        pass
      time.sleep(10)

    raise Exception('failed to off all vms')

  def cluster_down(self):
    cluster_stop(self.cvm_list[0])
    for i in range(10):
      is_cluster_stop(self.cvm_list[0])
      time.sleep(5)

  def all_cvm_down(self):
    for cvm_ip in self.cvm_list:
      cvm_stop(cvm_ip)

    for i in range(10):
      all_down = True
      for host_ip in self.host_list:
        if not is_cvm_stop(host_ip):
          all_down = False
      if all_down:
        return
      time.sleep(5)

  def all_host_down(self):
    for host_ip in self.host_list:
      stop_host(host_ip)