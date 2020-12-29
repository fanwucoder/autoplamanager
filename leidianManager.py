# -*- coding: utf-8 -*-
# 注意，请自行导入上面的类代码，否则无法使用
import os

from dnconsole import Dnconsole
import time
import logging
from Log import log
from MNQ import MNQ
from datetime import datetime as dt
from threading import Thread, Lock
from xyconsole import XYConsole

ZL_ACCOUNT = [
    {"zl_account": "13259490164", "zl_password": "fanwu123"},
    {"zl_account": "feiniao123", "zl_password": "feiniao123"},
    {"zl_account": "feiniao124", "zl_password": "feiniao124"},
    {"zl_account": "feiniao125", "zl_password": "feiniao125"}
]


class AutoRunner(Thread):
    def __init__(self, console: Dnconsole = None, mnq: MNQ = None, *args, **kwargs):
        """
        :param max_runner number
        :param except_runner list
        :param args:
        :param kwargs:
        """
        super().__init__()
        self._lock = Lock()
        self.include = kwargs.get("include", [])
        self.max_runner = kwargs.get("max_runner", 1)
        self.except_runner = kwargs.get("except_runner", [])
        self.runner = {}
        self.stop_mnq = {}
        self.task_info = {
            'task': "playGamer",
            "role": [1],
            "副本": "赫顿城, 暮光, 黄昏, 普通, 999, true",
            "副本方式": "指定",
            "分解装备": "true,true,true,true",
            "出售装备": "false,true,true,true",
            "common": {'api_addr': 'http://192.168.0.103:5000'},
        }
        self.runner_name = "default"
        self.running = 0
        self.is_stop = False
        self.last_date = dt.now()
        self._list = None
        self.mnq_path = None
        self.script_path = None
        if console is None:
            self.console = XYConsole()
        else:
            self.console = console
        if mnq is None:
            self.mnq = MNQ(console=self.console)
        else:
            self.mnq = mnq

    def run(self) -> None:
        self.run_app()

    def run_app(self):
        self.get_app_list()
        self.is_stop = False
        log.info("开始运行自动任务")

        while self.is_running():
            if self._lock.acquire(True, timeout=100):
                try:
                    self.start_one()
                    self.check_status()
                except:
                    log.exception("运行出错了")
                finally:
                    self._lock.release()
            time.sleep(10)

    def stop(self):
        for r in self.runner.keys():
            self.mnq.quit(r)
        self.is_stop = True

    def update_config(self, name, config):
        if self._lock.acquire(True, 100):
            try:
                self.runner_name = name
                self.include = config['include']
                self.except_runner = config['except']
                self.max_runner = config['max_runner']
                self.task_info = {
                    'task': config['task'],
                    "role": config['role'],
                    "副本": config["副本"],
                    "副本方式": config['副本方式'],
                    "分解装备": config['分解装备'],
                    "出售装备": config['出售装备'],
                    "common": config['common'],
                    "appType": config["appType"]
                }
                self.mnq_path = config['common']['mnq_path']
                self.script_path = config['common']['script_path']
                self.console.set_mnq_path(self.mnq_path)
                self.mnq.set_script_path(self.script_path)
                if config['clear_stop']:
                    self.clear_stop()
            except:
                log.exception("更新模拟器配置报错")
            finally:

                self._lock.release()
            # self.

    def get_app_list(self):
        self._list = {}
        for x in self.console.get_list():
            if self.check_runner(x.index, x.name):
                self._list[x.index] = x
        return self._list

    def is_running(self):
        return not self.is_stop

    def start_one(self):
        app_list = self.get_app_list()

        if self.running >= self.max_runner:
            log.debug("当前运行了%d个任务，已经超过最大任务数量%d了", self.running, self.max_runner)
            return
        rest = list(set(app_list.keys()) - set(self.runner.keys()) - set(self.stop_mnq.keys()))
        print(rest)
        if len(rest) <= 0:
            log.debug("没有剩余的任务了")
            return
        task = app_list[rest[0]]

        log.info("启动模拟器,index:%d,name:%s", task.index, task.name)
        try:
            config_name = self.write_config(task.index)
            if self.task_info['task'] == "startZL1":
                ret = self.mnq.start_zl(task.index, self.task_info)
            else:
                ret = self.mnq.start_game(task.index, task.name, config_name)
            if not ret:
                log.info("启动模拟器%d失败", task.index)
            else:
                self.runner[task.index] = {"task": task}
        except:
            self.stop[task.index] = task
            # self.mnq.quit(task.index)
            log.exception("模拟器%d启动报错", task.index)
        self.running += 1
        self.mnq.get_picture(task.index)

    def check_status(self):
        self.get_running()
        log.debug("check running status")
        for k, v in list(self.runner.items()):
            status = self.mnq.get_status(index=k)
            if status == "start\n":
                log.info("%d脚本开始运行", k)
            elif status == "finish\n":
                log.info("%d脚本执行完毕", k)
                self.mnq.get_picture(k)
                self.console.quit(k)
                self.remove_stop(k)
                self.stop_mnq[k] = v

            if not self.console.is_running(k):
                self.remove_stop(k)
        date = dt.now()
        if date.strftime("%Y-%m-%d") > self.last_date.strftime("%Y-%m-%d"):
            if date.hour >= 6:
                log.info("时间跳转%s到%s", self.last_date, date)
                self.last_date = date

    def remove_stop(self, k):
        self.running -= 1
        if k in self.runner:
            del self.runner[k]

    def check_runner(self, idx, name):
        if self.include is not None:
            if idx in self.include:
                return True
        elif idx not in self.except_runner and name not in self.except_runner and "-" not in name:
            return True
        return False

    def get_running(self):
        self.runner = {}
        for k in self.console.list_running():
            if self.check_runner(k.index, k.name):
                self.runner[k.index] = k
        self.running = len(self.runner.keys())

    def write_config(self, idx):
        config_name = os.path.join(".", "temp/%s_mnq.config" % self.runner_name)
        self.set_zl_account(idx)
        with open(config_name, mode="w+", encoding="utf-8", newline='\n') as f:
            self.write_info(self.task_info, None, f)
        return config_name

    def set_zl_account(self, idx):
        pos = self.include.index(idx) % len(ZL_ACCOUNT)
        zl = ZL_ACCOUNT[pos]
        self.task_info["zl_account"] = zl['zl_account']
        self.task_info['zl_password'] = zl['zl_password']

    def write_info(self, task_info, parent, f):
        if not parent:
            parent = ""
        for k, v in task_info.items():
            k = parent + k
            if isinstance(v, int):
                f.write(k + "::" + str(v) + "\n")
            if isinstance(v, str):
                f.write(k + "::" + v + "\n")
            if isinstance(v, list):
                f.write(k + "::" + ",".join([str(x) for x in v]) + "\n")
            if isinstance(v, dict):
                self.write_info(v, k, f)

    def clear_stop(self):
        if self.stop_mnq:
            for k in list(self.stop_mnq.keys()):
                del self.stop_mnq[k]


def main():
    from dnconsole import DnPlayer
    from unittest.mock import MagicMock
    # test_list = [
    #     DnPlayer([0, "测试1", 0, 0, 0, 0, 0]),
    #     DnPlayer([1, "测试2", 0, 0, 0, 0, 0]),
    #     DnPlayer([2, "测试3", 0, 0, 0, 0, 0]),
    #     DnPlayer([3, "测试4", 0, 0, 0, 0, 0]),
    #     DnPlayer([4, "测试5", 0, 0, 0, 0, 0]),
    # ]
    # Dnconsole.get_list = MagicMock(return_value=test_list)
    console = Dnconsole()
    auto_runner = AutoRunner(console=console, except_runner=[0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14])
    auto_runner.run_app()


if __name__ == '__main__':
    main()
