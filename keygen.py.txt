import os

import subprocess

from errbot import BotPlugin , botcmd


class KeyGen(BotPlugin):
    # def get_configuration_template(self):
    #     return {'ID_TOKEN': '00112233445566778899aabbccddeeff',
    #             'USERNAME':'changeme'}

    @botcmd(admin_only=True)
    def keygen(self, msg, args):
        _s = subprocess.Popen(['ssh-keygen', '-f', './{}'.format(args), '-N', ''], stdout=subprocess.PIPE)
        ls = subprocess.Popen(['ls', '-lah', '/root'], stdout=subprocess.PIPE)

        return '\n'.join([_s.stdout.read().decode(), ls.stdout.read().decode()])
        with open('{}.pub'.format(args), 'r') as pub:
            p = pub.read()
            return '\n'.join(['Public key:', '\n---\n', '```', p, '```', '\n---\n', os.getenv('HOME')])
