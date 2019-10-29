import json
from nutanix_fvm_client import *

IP = '10.149.160.5'
USER = 'nutanix'
PASSWORD = 'nutanix/4u'
MAC_ADDRESS = '0c:c4:7a:92:95:d4'
IPMI_IP = '10.149.160.11'

def test_constructor():
  try:
    client = NutanixFoundationClient(IP, USER, PASSWORD)
  except:
    assert False, 'login should be success'
  assert True, 'ok'

def test_constructor2():
  try:
    client = NutanixFoundationClient('99.99.99.99', USER, PASSWORD)
  except:
    assert True, 'ok'
    return
  assert False, 'login should fail with wrong IP'

def test_constructor3():
  try:
    client = NutanixFoundationClient(IP, 'user-not-exist', PASSWORD)
  except:
    assert True, 'ok'
    return
  assert False, 'login should fail with wrong credential'

def test_reset_state():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.reset_state()
  assert success, json.dumps(d, indent=2)

def test_abort_session():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.abort_session()
  assert success, json.dumps(d, indent=2)

def test_get_version():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.get_version()
  assert success, json.dumps(d, indent=2)

def test_does_mac_exist():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.does_mac_exist(MAC_ADDRESS, 'eth0')
  assert success, json.dumps(d, indent=2)
  assert d['exist'], json.dumps(d, indent=2)

def test_does_mac_exist2():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.does_mac_exist('11:11:11:11:11:11', 'eth0')
  assert success, json.dumps(d, indent=2)
  assert not d['exist'], json.dumps(d, indent=2)

def test_get_mac_from_ip():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.get_mac_from_ip(IPMI_IP)
  assert success, json.dumps(d, indent=2)
  assert d['exist'], json.dumps(d, indent=2)

def test_get_mac_from_ip2():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.get_mac_from_ip('99.99.99.99')
  assert success, json.dumps(d, indent=2)
  assert not d['exist'], json.dumps(d, indent=2)

def test_get_nos_packages():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.get_nos_packages()
  assert success, json.dumps(d, indent=2)

def test_get_nics():
  client = NutanixFoundationClient(IP, USER, PASSWORD)
  (success, d) = client.get_nics()
  assert success, json.dumps(d, indent=2)

if __name__ == '__main__':
  #test_constructor()
  #test_constructor2()
  #test_constructor3()
  #test_reset_state()
  #test_abort_session()
  #test_get_version()
  #test_does_mac_exist()
  #test_does_mac_exist2()
  #test_get_mac_from_ip()
  #test_get_mac_from_ip2()
  test_get_nos_packages()
  test_get_nics()
