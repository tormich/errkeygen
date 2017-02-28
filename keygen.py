import os

import subprocess

from errbot import BotPlugin , botcmd


class KeyGen(BotPlugin):
    # def get_configuration_template(self):
    #     return {'ID_TOKEN': '00112233445566778899aabbccddeeff',
    #             'USERNAME':'changeme'}

    @botcmd(admin_only=True)
    def keygen(self, msg, args):
        _s = subprocess.Popen(['ssh-keygen', '-f', args, '-N', ''])
        with open('{}.pub'.format(args), 'r') as pub:
            p = pub.read()
        return '\n'.join([_s, p])
