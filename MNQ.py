# -*- coding: utf-8 -*-
import os
from typing import Union

from Log import log
import get_proxy
from dnconsole import Dnconsole
import time

from xyconsole import XYConsole


class MNQ:
    script_path = "scripts"
    # script_path = "C:/Users/fan/Documents/TSStudio/Projects/autoplay"
    device_path = "/sdcard/TouchSprite"

    # XYConsole
    def __init__(self, console: Union[Dnconsole, XYConsole] = None, *args, **kwargs):
        """
        :param console
        :param args:
        :param kwargs:
        :return:
        """

        if console is None:
            self.console = Dnconsole()
        else:
            self.console = console

    def start_game(self, index: int, name: str, config_name: str):
        if not self.launch_mnq(index):
            return False
        time.sleep(15)
        self.start_touch(index, name,config_name)
        return True

    def launch_mnq(self, index):
        try:
            log.info("启动模拟器,index:%d", index)
            if not self.console.is_running(index):
                self.console.launch(index)
            cnt = 0
            while cnt < 120:
                time.sleep(3)
                if self.console.is_running(index):
                    log.info("启动模拟器成功,index:%d", index)
                    return True
        except:
            log.exception("模拟器%d启动失败", index)
            self.console.quit(index)

        return False

    def start_touch(self, index: int, name: str,config_name:str):
        # Dnconsole.adb(index, "kill-server",silence=False)
        # Dnconsole.adb(index, "wait-for-device",silence=False)
        # get_proxy.get_proxy(name)

        self.copyScripts(index)
        self.console.adb(index, "push %s %s" % (config_name, MNQ.device_path + "/res/" + "run_config.txt"))
        self.console.adb(index, "push %s %s" % ("temp/test.yaml", "/sdcard/wwww_clash.yaml"))
        self.console.adb(index, "shell echo >/sdcard/touch_status.txt ")
        self.console.invokeapp(index, "com.touchsprite.android")
        self.console.wait_activity(index, "com.touchsprite.android/.activity.MainActivity", 120)
        self.console.swipe(index, (100, 300), (100, 700))
        time.sleep(5)
        ret = self.console.check_picture(index, [os.path.join(os.path.abspath("."), "res/xy_main.png")])
        # ret = self.console.check_picture(index, [os.path.join(os.path.abspath("."), "res\main.png")])
        log.info("main 脚本位置%s", str(ret))
        if ret:
            log.info("开始启动main脚本")
            i, xy = ret
            self.console.touch(index, xy[0], xy[1])
            time.sleep(2)
            self.console.touch(index, 672, xy[1] + 10)
            # time.sleep(2)
            # Dnconsole.touch(index, 672, xy[1] + 160)
            time.sleep(3)
            i, xy = self.console.check_picture(index, [os.path.join(os.path.abspath("."), "res/xy_脚本开始.png")])
            self.console.touch(index, 672, xy[1]+5)

    def copyScripts(self, index):
        script_path = os.path.abspath(MNQ.script_path)
        for f in os.listdir(script_path):
            path = os.path.join(script_path, f)
            if f.endswith("lua"):
                self.console.adb(index, "shell rm %s" % (MNQ.device_path + "/lua/" + f))
                self.console.adb(index, "push %s %s" % (path, MNQ.device_path + "/lua/" + f))
            else:
                self.console.adb(index, "shell rm %s" % (MNQ.device_path + "/res/" + f))
                self.console.adb(index, "push %s %s" % (path, MNQ.device_path + "/res/" + f))

    @staticmethod
    def set_script_path(script_path):
        MNQ.script_path = script_path

    def get_status(self, index):
        self.console.adb(index, "pull %s %s" % ("/sdcard/touch_status.txt", "temp/touch_status.txt"))
        with open("temp/touch_status.txt", mode='r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                return None
            return lines[-1]

    def quit(self, idx):
        self.console.quit(idx)


def main():
    pass
    XYConsole.init("D:/Program Files/Microvirt/MEmu")
    console = XYConsole()
    # mnq = MNQ(console=console)
    # mnq.start_game(3, "test")

    # print(mnq.get_status(4) == "start\n")
    # mnq.start_game(4)
    # Dnconsole.
    # Dnconsole.find_pic()
    # MNQ.copyScripts(4)
    index = 2
    ret = XYConsole.check_picture(index, [os.path.join(os.path.abspath("."), "res/xy_main.png")])
    i, xy = ret
    XYConsole.touch(index, xy[0], xy[1])
    time.sleep(2)
    XYConsole.touch(index, 672, xy[1] + 10)
    time.sleep(2)
    i, xy = XYConsole.check_picture(index, [os.path.join(os.path.abspath("."), "res/xy_脚本开始.png")])
    XYConsole.touch(index, 672, xy[1])
    print(xy)

    # print(os.path.join(os.path.abspath("."), "res/脚本开始.png"))
    # ret = Dnconsole.wait_picture(4, 120, "res/main.png")

    # ret=Dnconsole.adb(5,"input swipe 360, 100 361, 700")
    # Dnconsole.touch(5,30,60)

    # ret = Dnconsole.adb(5, "ls /sdcard/")
    # print(ret)
    # index = 8
    # name = "flybird123"
    # mnq.start_touch(index, name)


if __name__ == '__main__':
    main()
