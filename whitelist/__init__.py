from mcdreforged.api.all import *

from .interface import register_command


def on_load(server: PluginServerInterface, old):
    register_command(server)
