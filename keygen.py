import os
from errbot import BotPlugin


class KeyGen(BotPlugin):
    def get_configuration_template(self):
        return {'ID_TOKEN': '00112233445566778899aabbccddeeff',
                'USERNAME':'changeme'}

    def keygen(self):
        return os.getenv('PWD')