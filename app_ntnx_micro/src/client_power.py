from nutanix_mod_base import Base
from nutanix_mod_clusters import Clusters
from nutanix_mod_hosts import Hosts
from nutanix_mod_vms import Vms
import subprocess
import paramiko

class NutanixPowerClient:

  def __init__(self, prism_ip, prism_user, prism_password, nodes, force=False
   timeout_connection=5, timeout_read=15):
    
    self.prism_ip = prism_ip
    self.prism_user = prism_user
    self.prism_password = prism_password
    self.nodes = nodes
    self.client = None

    self.cluster_down_success = False

  def is_server_power_on(ip, user, password):
    try:
      command = 'ipmitool -I lanplus -U {} -P {} -H {} power status'.format(user, password, ip)
      res_bytes = subprocess.check_output(command.split())
      res_string = res_bytes.decode('utf-8').strip()
    except Exception as e:
      print(e)
      return False

    words = res_string.lower().split()
    if 'off' in words:
      return False
    if 'on' in words:
      return True
    return False

  def is_all_server_power_on(nodes):
    all_up = True
    for node in nodes:
      ipmi_ip = node['ipmi_ip']
      ipmi_user = node['ipmi_user']
      ipmi_password = node['ipmi_password']
      power_on = is_server_power_on(ipmi_ip, ipmi_user, ipmi_password)
      if not power_on:
        all_up = False
        break
    return all_up

  def power_on_server(ip, user, password):
    try:
      command = 'ipmitool -I lanplus -U {} -P {} -H {} chassis power on'.format(user, password, ip)
      res = subprocess.check_output(command.split()).decode('utf-8').strip()
    except Exception as e:
      print(e)

  def issue_cluster_start(cvm_ip, user, password):
    try:
      client = paramiko.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(cvm_ip, username=user, password=password, timeout=3.0)
      command = '/usr/local/nutanix/cluster/bin/cluster start'
      stdin, stdout, stderr = client.exec_command(command)
      print(stdout.read().decode().strip())
      print(stderr.read().decode().strip())
    except Exception as e:
      print(e)

  def cluster_up(self):


    # Try login to Prism. If fails, issue "cluster start" on first CVM
    for i in range(30):
      try:
        _ClusterClient(self.prism_ip, self.prism_user, self.prism_password)
        return
      except:
        issue_cluster_start(self.cvm_ips[0], 'nutanix', 'nutanix/4u')
      time.sleep(10)

    raise Exception("failed to start cluster")

  def guestvm_down(self):
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
    def cluster_stop(cvm_ip):
      try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(cvm_ip, username='nutanix', password='nutanix/4u')
        command = "/home/nutanix/prism/cli/ncli cluster stop"
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode().strip())
      except Exception as e:
        print(e)

    def is_cluster_stop(cvm_ip):
      try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(cvm_ip, username='nutanix', password='nutanix/4u')
        command = "/usr/local/nutanix/cluster/bin/cluster status | grep state"
        stdin, stdout, stderr = client.exec_command(command)
        buf = stdout.read().decode().strip()
        cluster_state = buf.split()
        return cluster_state[-1] == "stop"
      except Exception as e:
        print(e)
      return False

    cluster_stop(self.cvm_list[0])
    for i in range(10):
      is_cluster_stop(self.cvm_list[0])
      time.sleep(5)

  def all_cvm_down(self):
    def cvm_stop(cvm_ip):
      try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(cvm_ip, username='nutanix', password='nutanix/4u')

        command = "sudo /usr/sbin/shutdown -h now"
        stdin, stdout, stderr = client.exec_command(command)
      except Exception as e:
        print(e)

    def is_cvm_stop(host_ip):
      try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host_ip, username='root', password='nutanix/4u')

        command = "bash -c 'virsh list | wc -l'"
        stdin, stdout, stderr = client.exec_command(command)
        buf = stdout.read().decode().strip()
        return buf == '3'
      except Exception as e:
        print(e)
      return False

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
    def stop_host(host_ip):
      try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host_ip, username='root', password='nutanix/4u')

        command = "shutdown -h now"
        stdin, stdout, stderr = client.exec_command(command)
      except Exception as e:
        print(e)

    for host_ip in self.host_list:
      stop_host(host_ip)


class _ClusterClient(Base, Clusters, Hosts, Vms):
  def __init__(self, ip, username, password, timeout_connection=5, timeout_read=15):
    super().__init__(ip, username, password, timeout_connection, timeout_read)
