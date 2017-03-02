import json
import os

import io
from datetime import datetime

import requests
import subprocess

from errbot import BotPlugin , botcmd


class Ops(BotPlugin):
    def get_configuration_template(self):
        return {'MARATHON_URL': 'http://marathon.mesos:8080'}

    def _get(self, appid:str=None, query_param:dict=None)->dict:
        if not appid:
            appid = ''

        murl = '/'.join([self.config['MARATHON_URL'], 'v2/apps', appid])
        if query_param:
            escaped_params = '&'.join(['{}={}'.format(k, v) for k, v in query_param.items()])
            murl = '?'.join([murl, escaped_params])
        http = requests.session()
        apps = http.get(url=murl)
        return apps.json()

    def _get_apps(self)->dict:
        return self._get()

    @botcmd(admin_only=False, template='app_list')
    def apps(self, msg, args):
        """ list apps from marathon
        """
        apps = self._get_apps().get('apps')
        _off, _on = [], []
        for app in apps:
            if app.get('instances', 0) > 0:
                _on.append(app)
            else:
                _off.append(app)
        self.callback_message()
        return {'apps_on': _on, 'apps_off': _off}

    @botcmd(admin_only=False)
    def apps_scale(self, msg, args): return 'not implemented!'
    @botcmd(admin_only=False)
    def apps_restart(self, msg, args): return 'not implemented!'
    @botcmd(admin_only=False)
    def apps_delete(self, msg, args): return 'not implemented!'
    @botcmd(admin_only=False)
    def apps_cp(self, msg, args): return 'not implemented!'

    @botcmd(admin_only=False)
    def apps_groups(self, msg, args):
        return 'not implemented!'

    @botcmd(admin_only=False)
    def apps_vports(self, msg, args):
        return 'not implemented!'

    @botcmd(admin_only=False)
    def apps_snapshot(self, msg, args):
        apps = self._get_apps()
        stream = self.send_stream_request(msg.frm,
                                          io.BytesIO(json.dumps(apps, indent=4).encode('utf-8')),
                                          name='apps.json', stream_type='application/json')
        return str('Done')

    @botcmd(admin_only=False)
    def ssh_keygen(self, msg, args):
        _path = '{}/.ssh/{}'.format(os.getenv('HOME'), args)
        _proc = subprocess.Popen(['ssh-keygen', '-f', _path, '-N', ''], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.send_card(_proc.stdout.read().decode(), in_reply_to=msg)
        self.send_card(_proc.stderr.read().decode(), in_reply_to=msg, color='red')
        _proc.communicate(timeout=10)

        _proc = subprocess.Popen(['chmod', '400', _path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.send_card(_proc.stdout.read().decode(), in_reply_to=msg)
        self.send_card(_proc.stderr.read().decode(), in_reply_to=msg, color='red')
        _proc.communicate(timeout=10)

        proc_env = {}
        _proc = subprocess.Popen(['ssh-agent', '-s'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ssh_agent_strings = _proc.stdout.read().decode()
        self.send_card(ssh_agent_strings, in_reply_to=msg)
        ssh_agent_strings = ssh_agent_strings.split('\n')

        proc_env['SSH_AUTH_SOCK'] = ssh_agent_strings[0].split(';')[0].split('=')[1]
        proc_env['SSH_AGENT_PID'] = ssh_agent_strings[1].split(';')[0].split('=')[1]

        self.send_card(_proc.stderr.read().decode(), in_reply_to=msg, color='red')
        _proc.communicate(timeout=10)


        _proc = subprocess.Popen(['ssh-add', _path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=proc_env)
        self.send_card(_proc.stdout.read().decode(), in_reply_to=msg)
        self.send_card(_proc.stderr.read().decode(), in_reply_to=msg, color='red')
        _proc.communicate(timeout=10)

        _proc = subprocess.Popen(['ssh', '-o StrictHostKeyChecking=no', '-T', 'git@github.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=proc_env)
        self.send_card(_proc.stdout.read().decode(), in_reply_to=msg)
        self.send_card(_proc.stderr.read().decode(), in_reply_to=msg, color='red')
        _proc.communicate(timeout=10)



        with open('{}.pub'.format(_path), 'r') as pub:
            p = pub.read()
            stream = self.send_stream_request(msg.frm,
                                              io.BytesIO(p.encode('utf-8')),
                                              name='{}.pub'.format(args), stream_type='text/plain')
