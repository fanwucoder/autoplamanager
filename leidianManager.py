# -*- coding: utf-8 -*-
# 注意，请自行导入上面的类代码，否则无法使用
import json
import os
import time
from datetime import datetime as dt
from threading import Thread, Lock
from typing import Union

from Log import log
from MNQ import MNQ
from dnconsole import Dnconsole
from xyconsole import XYConsole
import random

ZL_ACCOUNT = {
    "13259490164": "fanwu123",
    "feiniao123": "feiniao123",
    "feiniao124": "feiniao124",
    "feiniao125": "feiniao125"
}
ret = []
for k, v in ZL_ACCOUNT.items():
    ret.append(k + "/" + v)
print(",".join(ret))


def read_zl_count(name):
    filename = "zl_count_%s.json" % name
    if not os.path.exists(filename):
        return {}
    with open(filename, mode="r") as f:
        data = f.read()
        return json.loads(data)


def write_config(runner_name, zl_config):
    filename = "zl_count_%s.json" % runner_name
    with open(filename, mode="w+", encoding="utf-8") as f:
        f.write(json.dumps(zl_config))


class AutoRunner(Thread):
    def __init__(self, console: Union[Dnconsole, XYConsole] = None, *args, **kwargs):
        """
        :param max_runner number
        :param except_runner list
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self._lock = Lock()
        self.zl_accounts = {}
        self.include = kwargs.get("include", [])
        self.max_runner = kwargs.get("max_runner", 1)
        self.except_runner = kwargs.get("except_runner", [])
        self.runner = {}
        self.account_use = {}
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
        self.all_runner = {}

    def run(self) -> None:
        self.run_app()

    def run_app(self):

        self.is_stop = False
        log.info("开始运行自动任务")

        cnt = 0
        while self.is_running():
            if self._lock.acquire(True, timeout=100):
                try:
                    self.check_status()
                    self.start_one()
                    if cnt % 10 == 0:
                        self.get_pictures()
                except:
                    log.exception("运行出错了")
                finally:
                    self._lock.release()
            cnt += 1
            time.sleep(10)

    def stop(self):
        for k, mnq in self.runner.items():
            mnq.quit()
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
                    "区域":config["区域"],
                    "副本方式": config['副本方式'],
                    "分解装备": config['分解装备'],
                    "出售装备": config['出售装备'],
                    "common": config['common'],
                    "appType": config["appType"]
                }
                zl_accounts = config['zl_accounts']
                if zl_accounts.strip():
                    for a in zl_accounts.split(","):
                        x, y = a.split("/")
                        self.zl_accounts[x] = y
                self.mnq_path = config['common']['mnq_path']
                self.script_path = config['common']['script_path']
                self.console.set_mnq_path(self.mnq_path)
                self.update_instance()

                if config['clear_stop']:
                    self.clear_stop()
            except:
                log.exception("更新模拟器配置报错")
            finally:
                self._lock.release()

    def is_running(self):
        return not self.is_stop

    def get_rest(self):
        app_list = self.include
        if self.running >= self.max_runner:
            log.debug("当前运行了%d个任务，已经超过最大任务数量%d了", self.running, self.max_runner)
            return
        rest = list(set(app_list) - set(self.runner.keys()) - set(self.stop_mnq.keys()))
        zl_runcount = read_zl_count(self.runner_name)
        if self.has_zl():
            rest.sort(key=lambda x: zl_runcount.get(x, 0))
        else:
            rest.sort(key=lambda x: zl_runcount.get(x, 0), reverse=True)
        if len(rest) <= 0:
            log.debug("没有剩余的任务了")
            return
        idx = rest[0]
        return idx

    def start_mnq_by_idx(self, idx):
        mnq = self.get_mnq_instance(idx)
        if not mnq:
            return
        # 忽略已经运行的模拟器
        if mnq.is_running():
            self.runner[idx] = mnq
            log.info("index:%d,name:%s已经开始运行了", mnq.idx, mnq.name)
            return
        log.info("开始启动模拟器,index:%d,name:%s", mnq.idx, mnq.name)
        try:

            mnq.launch()
            mnq.get_picture()
            self.runner[idx] = mnq
            self.running += 1
        except:
            # self.mnq.quit(task.index)
            log.exception("模拟器%d启动报错", mnq.idx)

    def start_one(self):
        idx = self.get_rest()
        if idx:
            self.start_mnq_by_idx(idx)

    def write_task(self, idx, task):
        zl_config = read_zl_count(self.runner_name)
        if task == "zl":
            old_cnt = zl_config.get(idx, 0)
            old_cnt += 1
            zl_config[idx] = old_cnt
            write_config(self.runner_name, zl_config)

    def get_mnq_instance(self, idx):
        return self.all_runner.get(idx, None)

    def get_pictures(self):
        for k, mnq in self.all_runner.items():
            if mnq.is_running():
                mnq.get_picture()

    def check_status(self):
        self.account_use.clear()
        self.running = 0
        log.debug("check running status")
        for k, mnq in self.all_runner.items():
            if mnq.is_running():
                self.running += 1
                # 实时记录账号使用
                if mnq.get_task_type() == "zl":
                    account = mnq.get_zl_account()
                    self.account_use[account] = k
                status = mnq.get_status()
                if status == "start\n":
                    log.info("%d脚本开始运行", k)
                elif status == "finish\n" or mnq.get_runtime() > 7200 or status == 'quit lua\n':
                    log.info("%d脚本执行完毕", k)
                    mnq.get_picture()
                    mnq.quit()
                    self.remove_stop(k)
                    self.stop_mnq[k] = mnq
            elif k in self.runner:
                del self.runner[k]
            # else:
            #     self.remove_stop(k)
            #     self.stop_mnq[k] = mnq

        date = dt.now()
        if date.strftime("%Y-%m-%d") > self.last_date.strftime("%Y-%m-%d"):
            if date.hour >= 6:
                log.info("时间跳转%s到%s", self.last_date, date)
                self.last_date = date
                self.clear_stop()
        log.info("账号使用情况:%s", self.account_use)

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

    def write_config(self, idx):
        config_name = os.path.join(".", "temp/%s_mnq.config" % self.runner_name)
        self.set_zl_account()
        with open(config_name, mode="w+", encoding="utf-8", newline='\n') as f:
            self.write_info(self.task_info, None, f)
        return config_name

    def set_zl_account(self):
        ret = list(set(self.zl_accounts.keys()) - set(self.account_use.keys()))
        if len(ret) > 0:
            self.task_info["zl_account"] = ret[0]
            self.task_info['zl_password'] = self.zl_accounts[ret[0]]
        else:
            self.task_info["zl_account"] = ""
            self.task_info['zl_password'] = ""
        return None

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

    def update_instance(self):
        for k, mnq in list(self.all_runner.items()):
            if k not in self.include and mnq.is_running():
                mnq.quit()
                del self.all_runner[k]
                if k in self.runner:
                    del self.runner[k]
                if k in self.stop_mnq:
                    del self.stop_mnq[k]
        for i in self.include:
            mnq = self.all_runner.get(i, None)
            config_name = self.write_config(idx=i)
            if i not in self.all_runner:
                mnq = MNQ(idx=i, config_name=config_name, console=self.console, runner=self)
                self.all_runner[i] = mnq
            mnq.set_script_path(self.script_path)

    def has_zl(self):
        ret = list(set(self.zl_accounts.keys()) - set(self.account_use.keys()))
        return len(ret) > 0

    def get_task(self):
        # self.get
        self.set_zl_account()
        if self.has_zl():
            return "zl"
        return "auto"

    def get_zl_account(self):
        self.set_zl_account()
        return {
            "zl_account": self.task_info["zl_account"],
            'zl_password': self.task_info["zl_password"],
        }

    def get_DnPlayers(self):
        return [d for d in self.console.get_list() if d.index in self.include]

    def stop_mnq_by_idx(self, idx):
        for k, mnq in self.runner.items():
            if k == idx:
                mnq.quit()
            if k in self.runner:
                del self.runner[k]
                self.stop_mnq[k] = self.get_mnq_instance(k)
            return True
        return False

    def mark_img(self, idx):
        mnq = self.get_mnq_instance(idx)  # type:MNQ
        if mnq.is_running():
            mnq.get_picture()


def main():
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
