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
        self.start_touch(index, name, config_name)
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

    def start_zl(self, idx, conf):
        # 通过adb启动紫龙脚本，自动练号
        if not self.launch_mnq(idx):
            return False
        console = self.console

        zl_account = conf['zl_account']
        zl_password = conf['zl_password']
        package = "com.aland.hsz"
        console.stopapp(idx, package)
        console.pressKey(idx, KEY_HOME)
        time.sleep(5)

        console.wait_picture(idx, 60 * 10, RES_ZL_LAUNCH)
        time.sleep(1)
        find, pos = console.check_picture(idx, [RES_ZL_LAUNCH])
        if find is not None:
            console.touch(idx, pos[0], pos[1])
        console.wait_picture(idx, 60 * 10, RES_ZL_SET)
        check_tap(console, idx, [RES_ZL_SET], [[562, 406]])
        time.sleep(1)
        console.touch(idx, 47, 79)
        check_tap(console, idx, [RES_ZL_LOGOUT], [(247, 179), (353, 181)])
        find, pos = console.check_picture(idx, [RES_ZL_LOGIN])
        if find is not None:
            console.touch(idx, 354, 381)
            time.sleep(0.2)
            for i in range(20):
                console.pressKey(idx, KEY_DELETE)
                time.sleep(0.2)

        time.sleep(1)
        console.inputText(idx, zl_account)

        console.touch(idx, 255, 487)
        console.inputText(idx, zl_password)
        time.sleep(0.5)
        console.touch(idx, 362, 660)
        time.sleep(2)
        console.touch(idx, 661, 561)

        check_tap(console, idx, [RES_ZL_MAIN_TASK], [(153, 594)])

        time.sleep(2)
        console.touch(idx, 243, 522)
        time.sleep(0.5)
        console.touch(idx, 264, 642)
        time.sleep(0.5)
        console.touch(idx, 471, 897)
        time.sleep(0.5)
        console.touch(idx, 510, 1018)
        time.sleep(0.5)
        console.touch(idx, 342, 1240)

        time.sleep(5)
        console.touch(idx, 414, 1095)
        cnt = 0
        while True:
            find, pos = console.check_picture(idx, [RES_ZL_SS_LOGIN])
            if find is not None:
                print("找到登录")
                console.touch(idx, 625, 420)
                time.sleep(1)
            find, pos = console.check_picture(idx, [RES_ZL_SS_BIND])
            if find is not None:
                print("找到绑定手机")
                console.touch(idx, 881, 158)
            time.sleep(1)
            cnt += 1
            if cnt > 120:
                break
        return True

    def start_touch(self, index: int, name: str, config_name: str):
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
            self.console.touch(index, 672, xy[1] + 5)

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

    def get_picture(self, index):
        self.console.make_screencap(index, "/sdcard/start_run.png")
        self.console.get_result(index)


RES_ZL_LAUNCH = "res/zl/zl_launch.png"
RES_ZL_SET = "res/zl/set.png"
RES_ZL_LOGOUT = "res/zl/logout.png"
RES_ZL_LOGIN = "res/zl/login.png"
RES_ZL_MAIN_TASK = "res/zl/main_task.png"
RES_ZL_SS_LOGIN = "res/zl/ss_login.png"
RES_ZL_SS_BIND = "res/zl/ss_bind.png"
KEY_DELETE = 67
KEY_HOME = 3


def check_tap(console, idx: int, res: list, poses: list, wait: float = 0.5):
    find, pos = console.check_picture(idx, res)
    if find is not None:
        for p in poses:
            console.touch(idx, p[0], p[1])
            time.sleep(wait)


def main():
    pass
    XYConsole.init("D:/Program Files/Microvirt/MEmu")
    console = XYConsole()
    index = 7
    # console.make_screencap(index, "/sdcard/start_run.png")
    # console.dowload_file(index,"/sdcard/start_run.png","temp/start_run.png")
    console.get_result(index)


if __name__ == '__main__':
    main()
