# 注意，请自行导入上面的类代码，否则无法使用
from dnconsole import Dnconsole
import time
import logging
from Log import log
from MNQ import MNQ
from datetime import datetime as dt




class AutoRunner:
    def __init__(self, console: Dnconsole = None, mnq: MNQ = None, *args, **kwargs):
        """
        :param max_runner number
        :param except_runner list
        :param args:
        :param kwargs:
        """
        self.max_runner = kwargs.get("max_runner", 3)
        self.except_runner = kwargs.get("except_runner", [])
        self.runner = {}
        self.stop = {}
        self.running = 0
        self.is_stop = False
        self.last_date = dt.now()
        self.list = None
        if console is None:
            self.console = Dnconsole()
        else:
            self.console = console
        if mnq is None:
            self.mnq = MNQ(console=self.console)
        else:
            self.mnq = mnq

    def run_app(self):
        self.init_app_list()
        self.is_stop = False
        log.info("开始运行自动任务")

        while self.is_running():
            self.start_one()
            self.check_status()
            time.sleep(10)

    def init_app_list(self):
        self.list = {}
        for x in Dnconsole.get_list():
            if x.index not in self.except_runner and x.name not in self.except_runner:
                self.list[x.index] = x

    def is_running(self):
        return not self.is_stop

    def start_one(self):
        if self.running >= self.max_runner:
            log.debug("当前运行了%d个任务，已经超过最大任务数量%d了", self.running, self.max_runner)
            return
        rest = list(set(self.list.keys()) - set(self.runner.keys()) - set(self.stop.keys()))
        print(rest)
        if len(rest) <= 0:
            log.debug("没有剩余的任务了")
            return
        task = self.list[rest[0]]
        self.runner[task.index] = {"task": task}
        log.info("启动模拟器,index:%d,name:%s", task.index, task.name)
        if not self.mnq.start_game(task.index):
            log.info("启动模拟器%d失败", task.index)
        self.running += 1

    def check_status(self):
        log.debug("check running status")
        for k, v in self.runner.items():
            status = self.mnq.get_status(index=k)
            if status == "start\n":
                log.info("%d脚本开始运行", k)
            elif status == "finish\n":
                log.info("%d脚本执行完毕", k)
                self.console.quit(k)
                self.running -= 1
                self.stop[k] = v
                del self.runner[k]
        date = dt.now()
        if date.strftime("%Y-%m-%d") > self.last_date.strftime("%Y-%m-%d"):
            if date.hour >= 6:
                log.info("时间跳转%s到%s", self.last_date, date)
                self.last_date = date


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
    auto_runner = AutoRunner(console=console, except_runner=[0, 1, 2, 3,4])
    auto_runner.run_app()


if __name__ == '__main__':
    main()
