import json
import os.path
import time
from typing import List

from mcdreforged.api.types import ServerInterface
from mcdreforged.api.utils import Serializable

from .constants import LOG_FILE

server = ServerInterface.get_instance().as_plugin_server_interface()


class SingleRecord(Serializable):
    source: str
    target: str
    reason: str
    is_add: bool
    time: int

    def __init__(self, source: str = '', target: str = '', reason: str = '', is_add: bool = True,
                 operation_time: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.target = target
        self.reason = reason
        self.is_add = is_add
        self.time = operation_time or int(time.time())

    def str_time(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.time))


class LogStorage:
    def __init__(self):
        self.data: List[SingleRecord] = []

    def load(self):
        self.data = []
        if os.path.isfile(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='UTF-8') as f:
                log: List[dict] = json.load(f)
            for i in log:
                self.data.append(SingleRecord.deserialize(i))
        return self

    def save(self):
        to_save = []
        for i in self.data:
            to_save.append(i.serialize())
        with open(LOG_FILE, 'w', encoding='UTF-8') as w:
            json.dump(to_save, w, indent=4, ensure_ascii=False)

    def search(self, source: str = '', target: str = '', latest: int = 10):
        def check(record: SingleRecord):
            if source and record.source != source:
                return False
            if target and record.target != target:
                return False
            return True

        sorted_list = sorted(self.data, key=lambda x: x.time, reverse=True)
        output = [i for i in filter(check, sorted_list)] if (source or target) else sorted_list

        return output[:latest] or output

    def add(self, source: str, target: str, reason: str = '', is_add: bool = True):
        self.data.append(SingleRecord(source, target, reason, is_add))
        self.save()

    def clear(self):
        self.data = []
        self.save()


storage = LogStorage().load()
