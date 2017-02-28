import json
import os

import io
import requests
import subprocess

from errbot import BotPlugin , botcmd


class Ops(BotPlugin):
    def get_configuration_template(self):
        return {'MARATHON_URL': '00112233445566778899aabbccddeeff'}

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
    def apps_vports(self, msg, args):
        return 'not implemented!'

    @botcmd(admin_only=False)
    def apps_snapshot(self, msg, args):
        apps = self._get_apps()
        stream = self.send_stream_request(msg.frm, io.BytesIO(json.dumps(apps, indent=4).encode('utf-8')), name='apps.json', stream_type='application/json')
        return str('Done')
