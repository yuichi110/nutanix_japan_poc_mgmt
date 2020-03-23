from modules.base import Base
from modules.alerts import Alerts
from modules.clusters import Clusters
from modules.containers import Containers
from modules.images import Images
from modules.networks import Networks
from modules.tasks import Tasks
from modules.users import Users
from modules.vms import Vms

class NutanixSetupClient(Base, Alerts, Clusters, Containers, Images, Networks, Tasks, Users, Vms):

  def __init__(self, ip, username, password, timeout_connection=5, timeout_read=15):
    super().__init__(ip, username, password, timeout_connection, timeout_read)
