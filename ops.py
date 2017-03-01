import json
import os

import io
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

    @botcmd(admin_only=False, template='ops')
    def apps(self, msg, args):
        apps = self._get_apps().get('apps')
        _off, _on = [], []
        for app in apps:
            app_string = '{id} ({cpus}; {mem}; {disk}) `{network}` `{img}`'.format()
            if app.get('instances', 0) > 0:
                _on.append(app.get('id'))
            else:
                _off.append(app.get('id'))

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
        _proc = subprocess.Popen(['ssh-keygen', '-f', _path, '-N', ''], stdout=subprocess.PIPE)
        _proc.communicate(timeout=10)

        with open('{}.pub'.format(_path), 'r') as pub:
            p = pub.read()
            stream = self.send_stream_request(msg.frm,
                                              io.BytesIO(p.encode('utf-8')),
                                              name='{}.pub'.format(args), stream_type='text/plain')
