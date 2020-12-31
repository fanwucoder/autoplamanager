# -*- coding: utf-8 -*-
# 注意，请自行导入上面的类代码，否则无法使用
import os
import time
from datetime import datetime as dt
from threading import Thread, Lock

from Log import log
from MNQ import MNQ
from dnconsole import Dnconsole
from xyconsole import XYConsole

ZL_ACCOUNT = {
    "13259490164": "fanwu123",
    # "feiniao123": "feiniao123",
    # "feiniao124": "feiniao124",
    # "feiniao125": "feiniao125"
}
account_use = {

}


class AutoRunner(Thread):
    def __init__(self, console: Dnconsole = None, *args, **kwargs):
        """
        :param max_runner number
        :param except_runner list
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self._lock = Lock()
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

    def run(self) -> None:
        self.run_app()

    def run_app(self):

        self.is_stop = False
        log.info("开始运行自动任务")

        while self.is_running():
            if self._lock.acquire(True, timeout=100):
                try:
                    self.check_status()
                    self.start_one()
                except:
                    log.exception("运行出错了")
                finally:
                    self._lock.release()
            time.sleep(10)

    def stop(self):
        for k, mnq in self.runner:
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
                    "副本方式": config['副本方式'],
                    "分解装备": config['分解装备'],
                    "出售装备": config['出售装备'],
                    "common": config['common'],
                    "appType": config["appType"]
                }
                self.mnq_path = config['common']['mnq_path']
                self.script_path = config['common']['script_path']
                self.console.set_mnq_path(self.mnq_path)
                self.update_scripts(self.script_path)

                if config['clear_stop']:
                    self.clear_stop()
            except:
                log.exception("更新模拟器配置报错")
            finally:
                self._lock.release()

    def is_running(self):
        return not self.is_stop

    def start_one(self):
        app_list = self.include
        if self.running >= self.max_runner:
            log.debug("当前运行了%d个任务，已经超过最大任务数量%d了", self.running, self.max_runner)
            return
        rest = list(set(app_list) - set(self.runner.keys()) - set(self.stop_mnq.keys()))
        if len(rest) <= 0:
            log.debug("没有剩余的任务了")
            return
        idx = rest[0]
        config_name = self.write_config(idx)
        mnq = self.runner.setdefault(idx, MNQ(idx, config_name=config_name, runner=self, console=self.console))

        # 忽略已经运行的模拟器
        if mnq.is_running():
            log.info("index:%d,name:%s已经开始运行了", mnq.idx, mnq.name)
            return
        log.info("开始启动模拟器,index:%d,name:%s", mnq.idx, mnq.name)
        try:

            mnq.launch()
            mnq.get_picture()
            self.running += 1
        except:
            # self.mnq.quit(task.index)
            log.exception("模拟器%d启动报错", mnq.idx)

    def check_status(self):

        self.account_use.clear()
        self.running = 0
        log.debug("check running status")
        for k, mnq in list(self.runner.items()):
            if mnq.is_running():
                self.running += 1
                # 实时记录账号使用
                if mnq.get_task_type() == "zl":
                    account = mnq.get_zl_account()
                    self.account_use[account] = k
                status = mnq.get_status()
                if status == "start\n":
                    log.info("%d脚本开始运行", k)
                elif status == "finish\n":
                    log.info("%d脚本执行完毕", k)
                    mnq.get_picture()
                    mnq.quit()
                    self.remove_stop(k)
                    self.stop_mnq[k] = mnq

            else:
                self.remove_stop(k)

        date = dt.now()
        if date.strftime("%Y-%m-%d") > self.last_date.strftime("%Y-%m-%d"):
            if date.hour >= 6:
                log.info("时间跳转%s到%s", self.last_date, date)
                self.last_date = date
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
        ret = list(set(ZL_ACCOUNT.keys()) - set(self.account_use.keys()))
        if len(ret) > 0:
            self.task_info["zl_account"] = ret[0]
            self.task_info['zl_password'] = ZL_ACCOUNT[ret[0]]
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

    def update_scripts(self, script_path):
        for k, mnq in self.runner.items():
            mnq.set_script_path(script_path)

    def has_zl(self):
        ret = list(set(ZL_ACCOUNT.keys()) - set(self.account_use.keys()))
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
