# -*- coding: utf-8 -*-
import json
import os
import time
from datetime import datetime as dt
from typing import Union

from lxml import etree
import lxml
import Utils
from Log import log
from dnconsole import Dnconsole
from xyconsole import XYConsole


def launch_thread(mnq):
    mnq.launch_()


class MNQ:
    # script_path = "scripts"
    # script_path = "C:/Users/fan/Documents/TSStudio/Projects/autoplay"
    device_path = "/sdcard/TouchSprite"

    # XYConsole
    def __init__(self, idx: int, config_name: str, console: Union[Dnconsole, XYConsole] = None,
                 runner=None, *args,
                 **kwargs):
        """
        :param console
        :param args:
        :param kwargs:
        :return:
        """
        self.start_date = dt.now()
        self.idx = idx
        self.script_path = "scripts"
        self.runner = runner
        self.zl_block_cnt = 0
        self.zl_block_lasttime = dt.now()
        self.zl_login_cnt = 0
        self.last_status = ""
        self.last_status_time = dt.now()
        self.zl_login = False
        # self.device_path = "/sdcard/TouchSprite"
        self.set_config_name(config_name)

        if console is None:
            self.console = Dnconsole()
        else:
            self.console = console
        self.dnplayer = self.console.get_dnplayer(idx)

    def set_config_name(self, config_name):
        my_config_name = config_name + "%d_t" % self.idx
        with open(config_name, mode="r", encoding="utf-8", newline="\n") as f:
            with open(my_config_name, mode="w+", encoding="utf-8", newline="\n") as f1:
                f1.write(f.read())
        self.config_name = my_config_name

    @property
    def name(self):
        return self.dnplayer.name

    def start_game(self):
        log.info("运行内置脚本")
        index = self.idx
        name = self.name
        config_name = self.config_name
        if not self.launch_mnq(index):
            return False
        time.sleep(15)
        self.console.pressKey(self.idx, KEY_BACK)
        time.sleep(2)
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

    def start_zl(self, conf):
        log.info("运行紫龙脚本")
        idx = self.idx
        config_name = self.config_name
        # 通过adb启动紫龙脚本，自动练号
        if not self.launch_mnq(idx):
            return False
        self.console.pressKey(self.idx, KEY_BACK)
        time.sleep(2)

        zl_account = conf['zl_account']
        zl_password = conf['zl_password']
        # self.console.adb(idx, "push %s %s" % (config_name, MNQ.device_path + "/res/" + "run_config.txt"))
        self.console.adb(idx, "shell echo >/sdcard/touch_status.txt ")
        self.console.adb(idx, "shell echo zl >/sdcard/task_info.txt ")
        self.console.adb(idx, "shell echo zlaccount:%s >/sdcard/zlaccount.txt " % zl_account)
        console = self.console

        package = "com.aland.hsz"
        console.stopapp(idx, package)
        console.pressKey(idx, KEY_HOME)
        time.sleep(5)

        console.wait_picture(idx, 60 * 10, RES_ZL_LAUNCH)
        time.sleep(1)
        find, pos = console.check_picture(idx, [RES_ZL_LAUNCH])
        if find is not None:
            console.touch(idx, pos[0], pos[1])
        cnt = 600
        while cnt > 0:
            find, pos = console.check_picture(idx, [RES_ZL_SET])
            if find is not None:
                console.pressKey(idx, KEY_BACK)
            find, pos = console.check_picture(idx, [RES_ZL_SET1])
            if find is not None:
                break
            cnt = cnt - 1
            time.sleep(1)
        if cnt <= 0:
            return False
        time.sleep(1)
        console.touch(idx, 65, 107)
        check_tap(console, idx, [RES_ZL_LOGOUT], [(234, 235), (373, 232)])
        find, pos = console.check_picture(idx, [RES_ZL_LOGIN])
        if find is not None:
            console.touch(idx, 452, 516)
            time.sleep(0.2)
            for i in range(20):
                console.pressKey(idx, KEY_DELETE)
                time.sleep(0.2)

        time.sleep(1)
        console.inputText(idx, zl_account)

        console.touch(idx, 582, 655)
        for i in range(20):
            console.pressKey(idx, KEY_DELETE)
            time.sleep(0.2)

        console.inputText(idx, zl_password)
        time.sleep(0.5)
        console.touch(idx, 357, 889)
        time.sleep(2)
        console.touch(idx, 686, 510)

        path = "//node[@text='角色选择']"
        self.tap_path(path)
        time.sleep(2)
        path = "//node[@text='主线任务']"
        self.tap_checked(path)
        time.sleep(2)
        path = "//node[@text='通用版']"
        if self.tap_path(path):
            time.sleep(2)
            path = "//node[@text='上士']"
            self.tap_path(path)
            time.sleep(2)
        else:
            self.start_zl(conf)
            return
        path = "//node[@text='功能设置']"
        self.tap_path(path)
        time.sleep(2)
        path = "//node[@text='刷完关闭游戏']"
        if self.tap_path(path):
            time.sleep(2)
            path = "//node[@text='等待重启']"
            self.tap_path(path)
        time.sleep(2)
        path = "//node[@text='启动脚本']"
        self.tap_path(path)
        time.sleep(5)
        path = "//node[@text='运行脚本']"
        self.tap_path(path)
        time.sleep(5)

        return True

    def check_login(self):
        """
        检测是否卡登录页面
        """
        if self.get_runtime() < self.zl_login_cnt * 60:
            return
        self.zl_login_cnt += 1
        idx = self.idx
        console = self.console
        find, pos = console.check_picture(idx, [RES_ZL_SS_LOGIN])
        if find is not None:
            log.info("找到登录")
            console.touch(idx, 625, 420)
            time.sleep(1)
        find, pos = console.check_picture(idx, [RES_ZL_SS_BIND])
        if find is not None:
            log.info("找到绑定手机")
            console.touch(idx, 881, 158)
        time.sleep(1)

    def start_touch(self, index: int, name: str, config_name: str):
        # Dnconsole.adb(index, "kill-server",silence=False)
        # Dnconsole.adb(index, "wait-for-device",silence=False)
        # get_proxy.get_proxy(name)

        self.copyScripts(index)
        self.console.adb(index, "push %s %s" % (config_name, MNQ.device_path + "/res/" + "run_config.txt"))
        self.console.adb(index, "push %s %s" % ("temp/test.yaml", "/sdcard/wwww_clash.yaml"))
        self.console.adb(index, "shell echo >/sdcard/touch_status.txt ")
        self.console.adb(index, "shell echo zl >/sdcard/task_info.txt ")
        self.console.invokeapp(index, "com.touchsprite.android")
        self.console.wait_activity(index, "com.touchsprite.android/.activity.MainActivity", 120)
        self.console.swipe(index, (100, 300), (100, 700))
        time.sleep(5)
        area = self.get_area("//node[@text='main.lua']")
        self.console.touch(self.idx, int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2))
        time.sleep(2)
        self.console.touch(self.idx, 672, area[1] + 20)
        time.sleep(2)
        area = self.get_area("//node[@text='立即运行']")
        time.sleep(2)
        self.console.touch(self.idx, int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2))
        time.sleep(2)

    def copyScripts(self, index):
        script_path = os.path.abspath(self.script_path)
        for f in os.listdir(script_path):
            path = os.path.join(script_path, f)
            print(path)
            if f.endswith("lua"):
                self.console.adb(index, "shell rm -r -f %s" % (MNQ.device_path + "/lua/" + f))
                self.console.adb(index, "push %s %s" % (path, MNQ.device_path + "/lua/" + f))
            else:
                self.console.adb(index, "shell rm -r -f%s" % (MNQ.device_path + "/res/" + f))
                self.console.adb(index, "push %s %s" % (path, MNQ.device_path + "/res/" + f))

    def set_script_path(self, script_path):
        self.script_path = script_path

    def get_status(self):

        self.console.adb(self.idx, "pull %s %s" % ("/sdcard/touch_status.txt", "temp/touch_status.txt"))
        with open("temp/touch_status.txt", mode='r', encoding="utf-8") as f:
            lines = f.readlines()

            if len(lines) == 0:
                return None
            status = lines[-1]
            if status == "start\n":
                log.info("%d脚本开始运行", self.idx)
            if status != self.last_status:
                self.last_status = status
                self.last_status_time = dt.now()
            return status

    def is_finish(self):
        status = self.get_status()
        result = status == "finish\n" or self.get_runtime() > 7200 or status == 'quit lua\n'
        if result:
            log.info("%d脚本执行完毕", self.idx)
        return result

    def is_block(self, timeout=10 * 60):
        if self.get_task_type() == "zl":
            return False
        last_time = dt.now().timestamp() - self.last_status_time.timestamp()
        result = last_time >= timeout
        if result:
            log.info("模拟器%d运行卡住了", self.idx)
        return result

    def quit(self):
        self.console.adb(self.idx, "shell echo >/sdcard/touch_status.txt ")
        self.console.quit(self.idx)

    def get_picture(self, ):
        self.console.make_screencap(self.idx, "/sdcard/start_run.png")
        self.console.get_result(self.idx)
        cwd = os.path.join(os.path.abspath("."), "finish_result")
        Utils.execute_command("delete_old.bat", cwd)

    def get_zl_account(self):
        ret = self.console.adb(self.idx, " shell cat /sdcard/zlaccount.txt")
        for acc in ret.split("\n"):
            acc = acc.strip()
            if acc.startswith("zlaccount"):
                return acc.split(":")[1]
        return None

    def is_running(self):
        return self.console.is_running(self.idx)

    def get_runtime(self):
        return dt.now().timestamp() - self.start_date.timestamp()

    def get_area(self, path):
        data = self.ui_by_path(path)
        return self.ele_area(data)

    @staticmethod
    def ele_area(ele):
        if ele is not None:
            ret = ele.attrib.get("bounds")
            pos = ret.replace("][", ",").replace("[", "").replace("]", "").split(",")
            return [int(x.strip()) for x in pos]

    def ui_by_path(self, path):
        ui_tree = self.dup_ui()
        data = ui_tree.xpath(path)
        if data:
            return data[0]

    def dup_ui(self):
        self.console.adb(self.idx, "shell rm /sdcard/ui.xml -r -f ")
        self.console.adb(self.idx, "shell uiautomator dump /sdcard/ui.xml")
        ui_name = "temp/ui_%s.xml " % self.idx
        self.console.adb(self.idx, "pull /sdcard/ui.xml %s" % ui_name)
        a = etree.parse(ui_name)
        return a

    def get_task_type(self):
        try:
            self.console.adb(self.idx, "pull %s %s" % ("/sdcard/" + "task_info.txt", "temp/task_info.txt"))
            with open("temp/task_info.txt", encoding="utf-8", mode='r', newline="\n") as f:
                task_type = f.readlines()[-1]
                task_type = task_type.strip()
                return task_type
        except:
            return None

    def launch_(self):
        task = self.runner.get_task()
        if task == "zl":
            zl_account = self.runner.get_zl_account()
            self.start_zl(zl_account)
        else:
            self.start_game()
        self.runner.write_task(self.idx, task)
        self.start_date = dt.now()

    def is_zl_block(self):
        # 主要防止一直卡登录界面
        if not self.zl_login:
            if self.console.wait_picture(12, 1, RES_ZL_SS_DC):
                log.info("找到电池了，登录进去了")
                self.zl_login = True
            else:
                return False
        if self.get_runtime() < self.zl_block_cnt * 60:
            return False
        path = self.console.get_screencap(self.idx)
        crop = Utils.crop_picture(path, (103, 20, 207, 39))
        last_file = "temp/%d_last.png" % self.idx
        if not os.path.exists(last_file):
            os.rename(crop, last_file)
            return False

        result = Utils.is_similar_by_path(crop, last_file)
        if not result:
            os.rename(crop, last_file)
            self.zl_block_lasttime = dt.now()
        else:
            os.remove(crop)
        os.remove(path)
        self.zl_block_cnt += 1
        return result and (
                dt.now().timestamp() - self.zl_block_lasttime.timestamp()) > 10 * 60 and self.get_runtime() < 60 * 60

    def tap_checked(self, path):
        ele = self.ui_by_path(path)  # type:lxml.etree.Element
        if ele.attrib.get("checked", "false") != "true":
            area = self.ele_area(ele)
            self.console.touch(self.idx, int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2))

    def tap_path(self, path):
        ele = self.ui_by_path(path)
        area = self.ele_area(ele)
        if area:
            self.console.touch(self.idx, int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2))
            return True
        return False

    def launch(self):
        self.launch_()
        # thread = threading.Thread(target=launch_thread, args=(self,))
        # thread.start()
        # time.sleep(30)
        return True


RES_ZL_LAUNCH = "res/zl/zl_launch.png"
RES_ZL_SET = "res/zl/set.png"
RES_ZL_SET1 = "res/zl/set1.png"
RES_ZL_LOGOUT = "res/zl/logout.png"
RES_ZL_LOGIN = "res/zl/login.png"
RES_ZL_MAIN_TASK = "res/zl/main_task.png"
RES_ZL_SS_LOGIN = "res/zl/ss_login.png"
RES_ZL_SS_BIND = "res/zl/ss_bind.png"
RES_ZL_SS_DC = "res/zl/ss_dc.png"
KEY_DELETE = 67
KEY_HOME = 3
KEY_BACK = 4


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
    idx = 7
    mnq = MNQ(12, "temp/group1_mnq.config", console=console, )
    self = mnq
    path = "//node[@text='角色选择']"
    self.tap_path(path)
    time.sleep(2)
    path = "//node[@text='主线任务']"
    mnq.tap_checked(path)
    time.sleep(2)
    path = "//node[@text='通用版']"
    if self.tap_path(path):
        time.sleep(2)
        path = "//node[@text='上士']"
        self.tap_path(path)
        time.sleep(2)
    path = "//node[@text='功能设置']"
    self.tap_path(path)
    time.sleep(2)
    path = "//node[@text='刷完关闭游戏']"
    if self.tap_path(path):
        time.sleep(2)
        path = "//node[@text='等待重启']"
        self.tap_path(path)
    time.sleep(2)
    path = "//node[@text='启动脚本']"
    self.tap_path(path)
    time.sleep(5)
    path = "//node[@text='运行脚本']"
    self.tap_path(path)
    time.sleep(5)
    # self.dup_ui()
    # self.console.touch(mnq.idx,(area[0]+ret[2])/2,(ret[1]+ret[3])/2)
    # self = mnq
    # print(mnq.is_zl_block())
    idx = 7


if __name__ == '__main__':
    main()
