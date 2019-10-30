from nutanix_mod_base import Base
from nutanix_mod_clusters import Clusters
from nutanix_mod_hosts import Hosts
from nutanix_mod_vms import Vms

class NutanixPowerClient:

  def __init__(self, prism_ip, prism_user, prism_password, node_infos,
   timeout_connection=5, timeout_read=15):
    
    self.prism_ip = prism_ip
    self.prism_user = prism_user
    self.prism_password = prism_password
    self.node_infos = node_infos

  def get_cluster_status():
    pass

  def all_host_up():
    pass

  def cluster_up():
    pass

  def cluster_down():
    pass

  def all_cvm_down():
    pass

  def all_host_down():
    pass


class _ClusterClient(Base, Clusters, Hosts, Vms):
  def __init__(self, ip, username, password, timeout_connection=5, timeout_read=15):
    super().__init__(ip, username, password, timeout_connection, timeout_read)
