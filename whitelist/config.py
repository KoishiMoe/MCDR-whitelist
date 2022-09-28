import json
from typing import List

from mcdreforged.api.types import ServerInterface
from mcdreforged.api.utils import Serializable

from .constants import CONFIG_FILE


class Config(Serializable):
    add_permission_level: int = 1
    remove_permission_level: int = 2
    query_permission_level: int = 2
    admin_permission_level: int = 4
    require_reason: bool = True
    extra_deny: List[str] = []

    def save(self):
        with open(CONFIG_FILE, 'w', encoding='UTF-8') as w:
            json.dump(self.serialize(), w, indent=4)

    @classmethod
    def load(cls) -> 'Config':
        return ServerInterface.get_instance().as_plugin_server_interface().load_config_simple(
            CONFIG_FILE, default_config=cls.get_default().serialize(), in_data_folder=False, echo_in_console=True,
            target_class=cls
        )

    def get_perm_level(self, perm: str) -> int:
        perm_dict = {
            "add": self.add_permission_level,
            "remove": self.remove_permission_level,
            "query": self.query_permission_level,
            "admin": self.admin_permission_level,
            "clear": self.admin_permission_level,
            "allow": self.admin_permission_level,
            "deny": self.admin_permission_level
        }
        return perm_dict.get(perm, 4)


config = Config.load()
