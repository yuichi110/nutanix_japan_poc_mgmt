from flask import Flask, jsonify, request
from flask.views import View
import json, uuid

class AppServer:

  def __init__(self, port, debug=False):
    self.app = Flask('')
    self.port = port
    self.debug = debug
    self.tasks_status = {}
    self.register_error_handler()
    self.register_endpoints()

  def get_state(self, task):
    return self.tasks_status.get(task, {'exist':False})

  def run(self):
    self.app.run(debug=self.debug, host='0.0.0.0', port=self.port)

  def add_endpoint(self, url, function, methods):
    methods2 = methods
    class MyView(View):
      methods = methods2
      def dispatch_request(self):
        try:
          return function()
        except Exception as e:
          print(e)
          if isinstance(e, AuthException):
            d = {'error': "user name or password is invalid."}
            return (jsonify(d), 403)
          if isinstance(e, FormatException):
            d = {'error': "json body has problem. reason '{}'".format(e)}
            return (jsonify(d), 400)
          d = {'error': "unexpected error. reason '{}'".format(e)}
          return (jsonify(d), 500)
    self.app.add_url_rule(url, view_func=MyView.as_view(url))

  def get_callbacks(self, task_uuid, report_server={}):
    task_uuid = report_server.get('uuid', str(uuid.uuid4()))
    send = report_server.get('send', False)
    host = report_server.get('host', '')
    port = report_server.get('port', 80)
    self.tasks_status[task_uuid] = {
      'success': True,
      'status': '',
      'progress': 0
    }

    def set_status(success, progress, status, exception=None):
      progress = int(progress)
      if progress < 0:
        print('progress must be <0')
        return
      if progress > 100:
        print('progress must be >100')
        return
      self.tasks_status[task_uuid] = {
        'success': success,
        'status': status,
        'progress': progress
      }
      if exception is not None:
        self.tasks_status[task_uuid]['exception'] = str(exception)

      if not send:
        return
      try:
        url = f'http://{host}:{port}/api/v1/tasks/{task_uuid}'
        d = self.tasks_status[task_uuid]
        response = requests.put(url, data=json.dumps(d))
        if not response.ok:
          raise Exception('got failed response from report server. {}'.format(response.text))
      except Exception as e:
        print(e)

    return (task_uuid, set_status)

  def register_error_handler(self):
    def api_not_found_error(error):
      return (jsonify({'error':"api not found", 'code':404}), 404)
    def method_not_allowed_error(error):
      return (jsonify({'error':'method not allowed', 'code':405}), 405)
    def internal_server_error(error):
      return (jsonify({'error':'server internal error', 'code':500}), 500)
    self.app.register_error_handler(404, api_not_found_error)
    self.app.register_error_handler(405, method_not_allowed_error)
    self.app.register_error_handler(500, internal_server_error)

  def register_endpoints(self):
    @self.app.route('/api/v1/tasks/', methods=['GET'])
    def get_tasks():
      return (jsonify(self.tasks_status), 200)

    @self.app.route('/api/v1/tasks/<task_uuid>', methods=['GET'])
    def get_task(task_uuid):
      if task_uuid not in self.tasks_status:
        return (jsonify({'error':"task not found", 'code':404}), 404)
      return (jsonify(self.tasks_status[task_uuid]), 200)

class AuthException(Exception):
  pass

class FormatException(Exception):
  pass

class MethodException(Exception):
  pass