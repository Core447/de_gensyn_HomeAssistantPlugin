import os

from plugins.de_gensyn_HomeAssistantPlugin.const import EMPTY_STRING, HOME_ASSISTANT, SETTING_HOST, SETTING_PORT, \
    SETTING_SSL, SETTING_TOKEN

from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.PluginBase import PluginBase
from .actions.HomeAssistantAction.HomeAssistantAction import HomeAssistantAction

def log_method_call(method):
    def wrapper(*args, **kwargs):
        print(f"call {method.__name__}")
        result = method(*args, **kwargs)
        print(f"finished {method.__name__}")
        return result
    return wrapper


class HomeAssistant(PluginBase):
    def __init__(self):
        super().__init__()

        self.home_assistant_action_holder = ActionHolder(
            plugin_base=self,
            action_base=HomeAssistantAction,
            action_id="de_gensyn_HomeAssistantPlugin::HomeAssistantAction",
            action_name=HOME_ASSISTANT,
        )
        self.add_action_holder(self.home_assistant_action_holder)

        self.register(
            plugin_name=HOME_ASSISTANT,
            github_repo="https://github.com/gensyn/de_gensyn_HomeAssistantPlugin",
            plugin_version="0.9.2-beta",
            app_version="1.5.1-beta"
        )

        settings = self.get_settings()
        host = settings.setdefault(SETTING_HOST, EMPTY_STRING)
        port = settings.setdefault(SETTING_PORT, EMPTY_STRING)
        ssl = settings.setdefault(SETTING_SSL, True)
        token = settings.setdefault(SETTING_TOKEN, EMPTY_STRING)

        backend_path = os.path.join(self.PATH, "backend", "HomeAssistant.py")
        self.launch_backend(backend_path=backend_path, open_in_terminal=True)

        self.backend.set_host(host)
        self.backend.set_port(port)
        self.backend.set_ssl(ssl)
        self.backend.set_token(token)


    @log_method_call
    def set_settings(self, settings):
        super().set_settings(settings)

        host = settings.setdefault(SETTING_HOST, EMPTY_STRING)
        port = settings.setdefault(SETTING_PORT, EMPTY_STRING)
        ssl = settings.setdefault(SETTING_SSL, True)
        token = settings.setdefault(SETTING_TOKEN, EMPTY_STRING)

        self.backend.set_host(host)
        self.backend.set_port(port)
        self.backend.set_ssl(ssl)
        self.backend.set_token(token)
