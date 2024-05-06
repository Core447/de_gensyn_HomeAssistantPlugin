from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.PluginBase import PluginBase
from .HomeAssistant import HomeAssistantBackend
from .actions.HomeAssistantAction.HomeAssistantAction import HomeAssistantAction


class HomeAssistant(PluginBase):
    def __init__(self):
        super().__init__()

        self.home_assistant_action_holder = ActionHolder(
            plugin_base=self,
            action_base=HomeAssistantAction,
            action_id="de_gensyn_HomeAssistantPlugin::HomeAssistantAction",
            action_name="Home Assistant",
        )
        self.add_action_holder(self.home_assistant_action_holder)

        self.register(
            plugin_name="Home Assistant",
            github_repo="https://github.com/gensyn/de_gensyn_HomeAssistantPlugin",
            plugin_version="0.9.0-beta",
            app_version="1.4.11-beta"
        )

        settings = self.get_settings()
        host = settings.setdefault("host", "")
        port = settings.setdefault("port", "")
        ssl = settings.setdefault("ssl", True)
        token = settings.setdefault("token", "")

        self.backend = HomeAssistantBackend()
        self.backend.set_host(host)
        self.backend.set_port(port)
        self.backend.set_ssl(ssl)
        self.backend.set_token(token)

    def set_settings(self, settings):
        super().set_settings(settings)

        host = settings.setdefault("host", "")
        port = settings.setdefault("port", "")
        ssl = settings.setdefault("ssl", True)
        token = settings.setdefault("token", "")

        self.backend.set_host(host)
        self.backend.set_port(port)
        self.backend.set_ssl(ssl)
        self.backend.set_token(token)
