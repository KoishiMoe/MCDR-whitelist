import csv
from io import StringIO
from typing import List, Dict

from mcdreforged.api.all import *

from .config import config
from .constants import PREFIX
from .storage import storage

server = ServerInterface.get_instance().as_plugin_server_interface()


def tr(translation_key: str, *args) -> RTextMCDRTranslation:
    return server.rtr(f'whitelist.{translation_key}', *args)


def process_command(user_input: str) -> Dict[str, str]:
    user_input = user_input.strip()

    f = StringIO(user_input)
    reader = csv.reader(f, delimiter=" ", escapechar="\\", skipinitialspace=True)
    input_list: List[str] = []
    for i in reader:
        input_list += [j for j in i if j]

    out_dict = {}
    i = 0
    while i < len(input_list):
        if input_list[i].startswith("-"):
            try:
                out_dict[input_list[i]] = input_list[i + 1]
                i += 2
                continue
            except IndexError:
                pass
        i += 1

    return out_dict


def register_command(server: PluginServerInterface):
    def get_literal_node(literal):
        perm = config.get_perm_level(literal)
        return Literal(literal).requires(lambda src: src.has_permission(perm))\
            .on_error(RequirementNotMet, lambda src: src.reply(tr('permission_denied'), handled=True))

    server.register_command(
        Literal(PREFIX)
        .on_child_error(UnknownArgument, show_help, handled=True)
        .on_child_error(IllegalArgument, show_help, handled=True)
        .on_child_error(UnknownRootArgument, show_help, handled=True)
        .runs(show_help)
        .then(
            get_literal_node("add")
            .then(
                QuotableText("player")
                .runs(lambda src, ctx: add(src, ctx["player"]))
                .then(GreedyText("reason")
                      .runs(lambda src, ctx: add(src, ctx["player"], ctx["reason"]))
                      )
            )
        )
        .then(
            get_literal_node("remove")
            .then(
                QuotableText("player")
                .runs(lambda src, ctx: remove(src, ctx["player"]))
                .then(GreedyText("reason")
                      .runs(lambda src, ctx: remove(src, ctx["player"], ctx["reason"]))
                      )
            )
        )
        .then(
            get_literal_node("query")
            .runs(lambda src: query(src, ""))
            .then(
                GreedyText("params")
                .runs(lambda src, ctx: query(src, ctx["params"]))
            )
        )
        .then(
            get_literal_node("clear").runs(lambda src: clear(src))
        )
        .then(
            get_literal_node("allow")
            .then(
                QuotableText("player").runs(lambda src, ctx: allow(src, ctx["player"]))
            )
        )
        .then(
            get_literal_node("deny")
            .then(
                QuotableText("player").runs(lambda src, ctx: deny(src, ctx["player"]))
            )
        )
    )


def add(source: CommandSource, target, reason=''):
    if not reason and config.require_reason:
        source.reply(tr('reason_required'))
        return
    if isinstance(source, PlayerCommandSource):
        if source.player in config.extra_deny:
            source.reply(tr('permission_denied'))
            return
        storage.add(source.player, target, reason, True)
    else:
        storage.add('#Console#', target, reason, True)
    server.execute(f"whitelist add {target}")
    source.reply(tr('add_success', target))


def remove(source: CommandSource, target, reason=''):
    if not reason and config.require_reason:
        source.reply(tr('reason_required'))
        return
    if isinstance(source, PlayerCommandSource):
        if source.player in config.extra_deny:
            source.reply(tr('permission_denied'))
            return
        storage.add(source.player, target, reason, False)
    else:
        storage.add('#Console#', target, reason, False)
    server.execute(f"whitelist remove {target}")
    source.reply(tr('remove_success', target))


def query(source: CommandSource, params: str):
    if isinstance(source, PlayerCommandSource):
        if source.player in config.extra_deny:
            source.reply(tr('permission_denied'))
            return
    param_dict = process_command(params)
    number = param_dict.get("-n", "10")
    if number.isdigit():
        number = int(number)
    else:
        number = 10
    result = storage.search(
        param_dict.get("-s", ""),
        param_dict.get("-t", ""),
        number
    )
    resp = RTextList(tr("query_result_title"))
    for i in result:
        resp += "\n" + (RText("+").set_color(RColor.green).set_hover_text(tr("operation_add")) if i.is_add
                 else RText("-").set_color(RColor.red).set_hover_text(tr("operation_remove"))) + "  " \
                + RText(i.source).set_color(RColor.yellow) + "    " + RText(i.target).set_color(RColor.blue) + "    " \
                + RText(i.str_time()).set_color(RColor.gray) + "    " + RText(i.reason).set_color(RColor.white)

    source.reply(resp)


def clear(source: CommandSource):
    storage.clear()
    source.reply(tr('clear_success'))


def allow(source: CommandSource, player: str):
    try:
        config.extra_deny.remove(player)
        config.save()
    except ValueError:
        pass
    source.reply(tr('allow_success', player))


def deny(source: CommandSource, player: str):
    if player not in config.extra_deny:
        config.extra_deny.append(player)
        config.save()
    source.reply(tr('deny_success', player))


def show_help(source: CommandSource):
    source.reply(tr("help"))
