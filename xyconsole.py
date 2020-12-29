# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback

from dnconsole import DnPlayer
import cv2 as cv
import numpy as np
from Log import log
from datetime import datetime


class XYConsole:
    path = ""
    memuc = ""
    share_path = ""

    @classmethod
    def init(cls, path):
        cls.path = path
        cls.memuc = "\"%s\" " % (cls.path + "/memuc.exe")
        cls.share_path = os.path.join(os.path.abspath("."), "temp")

    @classmethod
    def launch(cls, index: int):
        """
        """
        cmd = cls.memuc + ' start -i ' + str(index)
        return cls.execute_cmd(cmd)

    @classmethod
    def get_list(cls):
        cmd = cls.memuc + 'listvms'
        log.debug("execute command:%s", cmd)
        cmd = os.popen(cmd)
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                dnplayer.insert(3, 0)
                dnplayer.append(0)
                result.append(DnPlayer(dnplayer))
        return result

    @classmethod
    def list_running(cls) -> list:
        result = list()
        all = cls.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result

    @classmethod
    def execute_cmd(cls, cmd: str):
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    ## 读取图像，解决imread不能读取中文路径的问题
    @classmethod
    def cv_imread(cls, file_path: str):
        cv_img = cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
        cv_img = cv.cvtColor(cv_img, cv.COLOR_RGB2BGR)
        return cv_img

    @classmethod
    def stopapp(cls, index: int, package: str):
        cmd = cls.memuc + '  -i %d  stopapp  "%s"' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @classmethod
    def find_pic(cls, screen: str, template: str, threshold: float):
        try:

            scr = cls.cv_imread(screen)
            tp = cls.cv_imread(template)
            # cv.namedWindow("aaa")
            # cv.imshow("aaa",scr)
            # cv.imshow("aaa", tp)
            result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
        except cv.error:
            traceback.print_exc()
            print('文件错误：', screen, template)
            time.sleep(1)
            try:
                scr = cls.cv_imread(screen)
                tp = cls.cv_imread(template)
                result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
            except cv.error:
                return False, None
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if min_val > threshold:
            print(template, min_val, max_val, min_loc, max_loc)
            return False, None
        print(template, min_val, min_loc)
        return True, min_loc

    @classmethod
    def adb(cls, index: int, command: str, silence: bool = False) -> str:
        cmd = cls.memuc + '  -i %d  adb  "%s"' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @classmethod
    def wait_picture(cls, index: int, timeout: int, template: str) -> bool:
        count = 0
        while count < timeout:

            path = cls.get_screencap(index)
            time.sleep(2)
            ret, loc = cls.find_pic(path, template, 0.01)
            if ret is False:
                print(loc)
                time.sleep(2)
                count += 2
                continue
            print(loc)
            return True
        return False

    @classmethod
    def get_screencap(cls, index):
        path = cls.share_path + "/%s.png" % index
        device_path = '/sdcard/1.png'
        cls.make_screencap(index, device_path)
        cls.dowload_file(index, device_path, path)
        return path

    @classmethod
    def dowload_file(cls, index, device_path, path):
        cls.adb(index, 'pull %s %s' % (device_path, path))

    @classmethod
    def make_screencap(cls, index, device_path):
        cls.adb(index, ' shell screencap %s' % device_path)

    @classmethod
    def is_running(cls, index: int) -> bool:
        vm_list = cls.get_list()
        for x in vm_list:
            if x.index == index:
                return x.is_running()
        return False

    @classmethod
    def touch(cls, index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            cls.adb(index, 'shell input tap %d %d' % (x, y))
        else:
            cls.adb(index, 'shell input swipe %d %d %d %d %d' % (x, y, x, y, delay))

    @classmethod
    def quit(cls, index: int):
        cmd = "{} stop  -i {}".format(cls.memuc, index)
        # cmd="taskkill /f /pid %d".format(21324)
        result = cls.execute_cmd(cmd)
        return result

    @classmethod
    def invokeapp(cls, index: int, package: str):
        cmd = cls.memuc + '-i %d startapp %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        print(result)
        return result

    @classmethod
    def wait_activity(cls, index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if cls.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False

    @classmethod
    def get_activity_name(cls, index: int):
        text = cls.adb(index, 'shell dumpsys activity top | grep ACTIVITY', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    @classmethod
    def check_picture(cls, index: int, templates: list):
        path = cls.get_screencap(index)
        time.sleep(1)
        for i, t in enumerate(templates):
            ret, loc = cls.find_pic(path, t, 0.01)
            if ret is True:
                return i, loc
        return None, None

    @classmethod
    def swipe(cls, index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            cls.adb(index, ' shell input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            cls.adb(index, ' shell input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    @classmethod
    def set_mnq_path(cls, mnq_path):
        cls.init(mnq_path)

    @classmethod
    def pressKey(cls, idx, key):
        cls.adb(idx, " shell input keyevent %s" % key)

    @classmethod
    def inputText(cls, idx, txt):
        cls.adb(idx, "shell input text %s" % txt)

    @classmethod
    def get_result(cls, index):
        ret = cls.adb(index, "shell ls /sdcard/* |grep .png")
        pictures = [x.strip() for x in ret.split("\n") if x and x.endswith(".png")]
        if not os.path.exists("finish_result"):
            os.makedirs("finish_result")
        for p in pictures:
            name = p.split("/")[-1]
            local_path = "%s_%s_%s" % (index, datetime.now().strftime("%Y%m%d%H%M%S"), name)
            if name.startswith("start") or name.startswith("finish"):
                cls.dowload_file(index, p, os.path.join("finish_result", local_path))
                cls.adb(index, "shell rm %s" % p)


def _test():
    XYConsole.init("D:/Program Files/Microvirt/MEmu")
    # XYConsole.invokeapp(1, "com.touchsprite.android")
    XYConsole.wait_activity(1, "com.touchsprite.android/.activity.MainActivity", 10)
    # print(XYConsole.launch(1))
    # vm_list = XYConsole.get_list()
    # for x in vm_list:
    #     print(x)
    # # time.sleep(5)
    # result = XYConsole.wait_picture(1, 120, "res/逍遥测试.png")
    # # result = XYConsole.quit(1)
    # print("--->" + str(result))
    # XYConsole.touch(1, 190, 352)
    # print(XYConsole.is_running(1))


if __name__ == '__main__':
    _test()
