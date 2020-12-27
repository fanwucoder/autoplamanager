# -*- coding: utf-8 -*-
import time

from Log import log
import configparser
import threading
from leidianManager import AutoRunner


class DefaultOption(dict):

    def __init__(self, config, section, **kv):
        self._config = config
        self._section = section
        dict.__init__(self, **kv)

    def items(self):
        _items = []
        for option in self:
            if not self._config.has_option(self._section, option):
                _items.append((option, self[option]))
            else:
                value_in_config = self._config.get(self._section, option)
                _items.append((option, value_in_config))
        return _items


class GroupManager:
    KEY_RUNNER = "runner"

    def __init__(self):
        self._config = "config.ini"
        self._group_runner = {}
        self._group_instance = {}
        self.common = {}
        self.is_stop = False

    def init(self, config="config.ini"):
        self._config = config

        self.is_stop = False

    def quit(self):
        self.is_stop = True
        for name, ins in self._group_instance.items():
            self.stop_group(name)

    def run(self):
        while not self.is_stop:
            try:
                self.update_config()
                self.run_groups()
                self.update_groups()
            except:
                log.exception("运行出错了")

            time.sleep(10)

    def update_config(self):
        config = configparser.ConfigParser()
        config.read(self._config, encoding="utf-8-sig")
        self.common['api_addr'] = config.get("common", "api_addr")
        self.common["mnq_path"] = config.get("common", "mnq_path")
        self.common['script_path'] = config.get("common", "script_path")
        groups = config.get("groups", "group_list").split(",")
        for k in self._group_runner.keys():
            if k not in groups:
                self.stop_group(k)
        for group in groups:
            group_runner = {'task': config.get(group, "task"),
                            'include': self.extend_include(config.get(group, "include")),
                            "max_runner": config.getint(group, "max_runner"),
                            "role": self.extend_include(config.get(group, "role")),
                            "appType": config.get(group, "appType"),
                            "except": self.extend_include(config.get(group, "except", vars={"except": ""})),
                            "副本": config.get(group, "副本"),
                            "副本方式": config.get(group, "副本方式"),
                            "分解装备": config.get(group, "分解装备"),
                            "出售装备": config.get(group, "出售装备"),
                            "clear_stop": config.getboolean(group, "clear_stop", vars={"clear_stop": "False"}),
                            "common": self.common,
                            "runner": None}
            print(group_runner)
            self._group_runner[group] = group_runner

    def run_groups(self):
        log.debug("run groups")
        for k, v in self._group_runner.items():
            self.run_group(k)

    def run_group(self, group):
        if self.get_group(group) is None:
            log.info("start group %s", group)
            self.start_group(group)

    @staticmethod
    def extend_include(param):

        include = []
        if param:
            for x in param.split(","):
                if '-' in x:
                    a, b = x.split("-")
                    a1 = int(a)
                    b1 = int(b)
                    for i in range(a1, b1 + 1, 1):
                        include.append(i)
                else:
                    include.append(int(x))
        return include

    def start_group(self, group):
        runner = AutoRunner()
        self._group_instance[group] = runner
        runner.update_config(group, self._group_runner[group])
        runner.start()

    def stop_group(self, k):
        runner = self.get_group(k)
        if runner:
            runner.stop()
            del self._group_instance[k]

    def update_groups(self):
        for k, v in self._group_runner.items():
            runner = self.get_group(k)  # type:AutoRunner
            runner.update_config(k, v)

    def get_group(self, k):
        runner = self._group_instance.get(k, None)
        return runner
