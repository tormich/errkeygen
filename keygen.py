import os
from errbot import BotPlugin , botcmd


class KeyGen(BotPlugin):
    # def get_configuration_template(self):
    #     return {'ID_TOKEN': '00112233445566778899aabbccddeeff',
    #             'USERNAME':'changeme'}

    @botcmd('repo_name', admin_only=True)
    def keygen(self, repo_name):
        return repo_name
