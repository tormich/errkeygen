import json
import os

import io
import requests
import subprocess

from errbot import BotPlugin , botcmd


class Ops(BotPlugin):
    def get_configuration_template(self):
        return {'MARATHON_URL': 'http://marathon.mesos:8080'}

    def _get(self, appid:str=None)->dict:
        if not appid:
            appid = ''

        murl = '/'.join([self.config['MARATHON_URL'], 'v2/apps', appid])
        http = requests.session()
        apps = http.get(url=murl)
        return apps.json()

    def _get_apps(self)->dict:
        return self._get()

    @botcmd(admin_only=False)
    def apps(self, msg, args): return 'not implemented!'
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
        stream = self.send_stream_request(msg.frm, io.BytesIO(json.dumps(apps, indent=4).encode('utf-8')), name='apps.json', stream_type='application/json')
        return str('Done')

    @botcmd(admin_only=False)
    def ssh_keygen(self, msg, args):
        _path = '{}/{}'.format(os.getenv('HOME'), args)
        _s = subprocess.Popen(['ssh-keygen', '-f', _path, '-N', ''], stdout=subprocess.PIPE)

        # return '\n'.join([_s.stdout.read().decode(), ls.stdout.read().decode()])
        with open('{}.pub'.format(_path), 'r') as pub:
            p = pub.read()
            stream = self.send_stream_request(msg.frm, io.BytesIO(p.encode('utf-8')), name='{}.pub'.format(args), stream_type='text/plain')
            return '\n'.join(['Public key:', '\n---\n', '```', p, '```', '\n---\n', os.getenv('HOME')])
