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
      ops = SetupOps(cluster, containers, networks, ipam_networks, images)
      ops.connect_to_prism()
      ops.set_language()
      ops.delete_unused_containers()
      ops.create_containers()
      ops.delete_unused_networks()
      ops.create_networks()
      ops.create_ipam_networks()
      ops.create_images()
    except Exception as e:
      print(e)
  threading.Thread(target=fun).start()

class PowerOps:
  def __init__(self, cluster, node_infos):
    self.session = None
    self.ip =       cluster['ip']
    self.user =     cluster['user']
    self.password = cluster['password']
    self.language = cluster['language']

    self.containers = containers
    self.networks =   networks
    self.ipam_networks = ipam_networks
    self.images = images