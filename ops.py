import os
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

    def _get_apps(self)->list:
        return self._get().get('apps', [])

    @botcmd(admin_only=True)
    def apps_snapshot(self, msg, args):
        apps = self._get_apps()
        return str(apps)
