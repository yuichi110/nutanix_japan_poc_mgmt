from ops_eula import *

def test():
  ops = EulaOps(d)
  ops.set_temporary_password()
  ops.connect_to_prism()
  ops.set_eula()
  ops.set_initial_pulse()
  ops.set_initial_alert()
  ops.change_password()

d = {
  'ip':           '10.149.160.41',
  'user':         'admin',
  'password':     'Nutanix/4u!',
  'eula_name':    'Yuichi Ito',
  'eula_company': 'Nutanix',
  'eula_title':   'DevOps Specialist',
  'enable_pulse': False,
}

if __name__ == '__main__':
  test()