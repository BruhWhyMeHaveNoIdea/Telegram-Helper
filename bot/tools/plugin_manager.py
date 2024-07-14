import json

from bot.tools.plugins.gtts_text_to_speech import GTTSTextToSpeech
from bot.tools.plugins.auto_tts import AutoTextToSpeech
from bot.tools.plugins.dice import DicePlugin
from bot.tools.plugins.youtube_audio_extractor import YouTubeAudioExtractorPlugin
from bot.tools.plugins.ddg_image_search import DDGImageSearchPlugin
from bot.tools.plugins.ddg_translate import DDGTranslatePlugin
from bot.tools.plugins.spotify import SpotifyPlugin
from bot.tools.plugins.crypto import CryptoPlugin
from bot.tools.plugins.weather import WeatherPlugin
from bot.tools.plugins.ddg_web_search import DDGWebSearchPlugin
from bot.tools.plugins.wolfram_alpha import WolframAlphaPlugin
from bot.tools.plugins.deepl import DeeplTranslatePlugin
from bot.tools.plugins.worldtimeapi import WorldTimeApiPlugin
from bot.tools.plugins.whois_ import WhoisPlugin
from bot.tools.plugins.webshot import WebshotPlugin


class PluginManager:
    """
    A class to manage the plugins and call the correct functions
    """

    def __init__(self, config):
        enabled_plugins = config.get('plugins', [])
        plugin_mapping = {
            'wolfram': WolframAlphaPlugin,
            'weather': WeatherPlugin,
            'crypto': CryptoPlugin,
            'ddg_web_search': DDGWebSearchPlugin,
            'ddg_translate': DDGTranslatePlugin,
            'ddg_image_search': DDGImageSearchPlugin,
            'spotify': SpotifyPlugin,
            'worldtimeapi': WorldTimeApiPlugin,
            'youtube_audio_extractor': YouTubeAudioExtractorPlugin,
            'dice': DicePlugin,
            'deepl_translate': DeeplTranslatePlugin,
            'gtts_text_to_speech': GTTSTextToSpeech,
            'auto_tts': AutoTextToSpeech,
            'whois': WhoisPlugin,
            'webshot': WebshotPlugin,
        }
        self.plugins = [plugin_mapping[plugin]() for plugin in enabled_plugins if plugin in plugin_mapping]

    def get_functions_specs(self):
        """
        Return the list of function specs that can be called by the model
        """
        return [spec for specs in map(lambda plugin: plugin.get_spec(), self.plugins) for spec in specs]

    async def call_function(self, function_name, helper, arguments):
        """
        Call a function based on the name and parameters provided
        """
        plugin = self.__get_plugin_by_function_name(function_name)
        if not plugin:
            return json.dumps({'error': f'Function {function_name} not found'})
        return json.dumps(await plugin.execute(function_name, helper, **json.loads(arguments)), default=str)

    def get_plugin_source_name(self, function_name) -> str:
        """
        Return the source name of the plugin
        """
        plugin = self.__get_plugin_by_function_name(function_name)
        if not plugin:
            return ''
        return plugin.get_source_name()

    def __get_plugin_by_function_name(self, function_name):
        return next((plugin for plugin in self.plugins
                     if function_name in map(lambda spec: spec.get('name'), plugin.get_spec())), None)
