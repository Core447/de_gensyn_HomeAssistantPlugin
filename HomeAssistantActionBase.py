# Import gtk modules
import gi
from plugins.de_gensyn_HomeAssistantPlugin.const import CONNECT_NOTIFY_TEXT, CONNECT_NOTIFY_ACTIVE, LABEL_HOST_KEY, \
    LABEL_PORT_KEY, LABEL_SSL_KEY, LABEL_TOKEN_KEY, SETTING_HOST, SETTING_PORT, SETTING_TOKEN, LABEL_SETTINGS_KEY, \
    SETTING_SSL

from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.PluginManager.PluginBase import PluginBase

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository.Adw import EntryRow, PasswordEntryRow, PreferencesGroup, SwitchRow


class HomeAssistantActionBase(ActionBase):
    host_entry: EntryRow
    port_entry: EntryRow
    ssl_switch: SwitchRow
    token_entry: PasswordEntryRow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_config_rows(self) -> list:
        lm = self.plugin_base.locale_manager

        self.host_entry = EntryRow(title=lm.get(LABEL_HOST_KEY))

        self.port_entry = EntryRow(title=lm.get(LABEL_PORT_KEY))

        self.ssl_switch = SwitchRow(title=lm.get(LABEL_SSL_KEY))

        self.token_entry = PasswordEntryRow(title=lm.get(LABEL_TOKEN_KEY))

        self.load_config_defaults_base()

        self.host_entry.connect(CONNECT_NOTIFY_TEXT, self.on_change_entry, SETTING_HOST)
        self.port_entry.connect(CONNECT_NOTIFY_TEXT, self.on_change_entry, SETTING_PORT)
        self.ssl_switch.connect(CONNECT_NOTIFY_ACTIVE, self.on_change_ssl)
        self.token_entry.connect(CONNECT_NOTIFY_TEXT, self.on_change_entry, SETTING_TOKEN)

        group = PreferencesGroup()
        group.set_title(lm.get(LABEL_SETTINGS_KEY))
        group.set_margin_top(20)
        group.add(self.host_entry)
        group.add(self.port_entry)
        group.add(self.ssl_switch)
        group.add(self.token_entry)

        return [group]

    def load_config_defaults_base(self):
        settings = self.plugin_base.get_settings()
        host = settings.setdefault(SETTING_HOST, "")
        port = settings.setdefault(SETTING_PORT, "")
        ssl = settings.setdefault(SETTING_SSL, True)
        token = settings.setdefault(SETTING_TOKEN, "")

        self.host_entry.set_text(host)
        self.port_entry.set_text(port)
        self.ssl_switch.set_active(ssl)
        self.token_entry.set_text(token)

    def on_change_entry(self, entry, *args):
        settings = self.plugin_base.get_settings()
        settings[args[1]] = entry.get_text()
        self.plugin_base.set_settings(settings)

    def on_change_ssl(self, switch, _):
        settings = self.plugin_base.get_settings()
        settings[SETTING_SSL] = bool(switch.get_active())
        self.plugin_base.set_settings(settings)
