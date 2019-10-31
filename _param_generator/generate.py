import json

PARAM_FILE = 'param.json'

class Generator:
  def __init__(self):
    self.cluster_assets = {}
    self.basics = {}
    self.containers = {}
    self.eulas = {}
    self.fvms = {}
    self.images = {}
    self.ipam_networks = {}
    self.networks = {}

  def generate(self):
    pass

  def load_cluster_assets(self):
    pass
