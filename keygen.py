from errbot import BotPlugin

class PluginExample(BotPlugin):
    def get_configuration_template(self):
        return {'ID_TOKEN': '00112233445566778899aabbccddeeff',
                'USERNAME':'changeme'}

    def snapshot(self):
        pass