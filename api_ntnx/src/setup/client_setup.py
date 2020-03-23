from nutanix_mod_base import Base
from nutanix_mod_alerts import Alerts
from nutanix_mod_clusters import Clusters
from nutanix_mod_containers import Containers
from nutanix_mod_images import Images
from nutanix_mod_networks import Networks
from nutanix_mod_tasks import Tasks
from nutanix_mod_users import Users
from nutanix_mod_vms import Vms

class NutanixSetupClient(Base, Alerts, Clusters, Containers, Images, Networks, Tasks, Users, Vms):

  def __init__(self, ip, username, password, timeout_connection=5, timeout_read=15):
    super().__init__(ip, username, password, timeout_connection, timeout_read)
