# -*- coding: utf-8 -*-
import os
import shutil
import time
import cv2 as cv
import traceback
import numpy as np


class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])
        self.name = info[1]
        self.top_win_handler = int(info[2])
        self.bind_win_handler = int(info[3])
        self.is_in_android = True if int(info[4]) == 1 else False
        self.pid = int(info[5])
        self.vbox_pid = int(info[6])

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)


class UserInfo:
    def __init__(self, *args, **kwargs):
        self.info = None
        pass


class Dnconsole:
    # 请根据自己电脑配置
    basepath = "D:\\ChangZhi\\dnplayer2"
    # basepath="E:\\ChangZhi\\dnplayer2\\"
    console = basepath + '\\ldconsole.exe '
    ld = basepath + '\\ld.exe '

    # share_path = 'C:/Users/fan/Documents/雷电模拟器/Pictures'
    share_path = "D:/Backup/Documents/雷电模拟器/Pictures"

    @staticmethod
    def get_list():
        cmd = os.popen(Dnconsole.console + 'list2')
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(DnPlayer(dnplayer))
        return result

    @staticmethod
    def list_running() -> list:
        result = list()
        all = Dnconsole.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result

    @staticmethod
    def is_running(index: int) -> bool:
        all = Dnconsole.get_list()
        for a in all:
            if a.index == index:
                return a.is_running()
        return False

    @staticmethod
    def dnld(index: int, command: str, silence: bool = True):
        cmd = Dnconsole.ld + '-s %d "%s"' % (index, command)
        print(cmd)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def adb(index: int, command: str, silence: bool = False) -> str:
        cmd = Dnconsole.console + 'adb --index %d --command "%s"' % (index, command)
        print(cmd)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def install(index: int, path: str):
        shutil.copy(path, Dnconsole.share_path + str(index) + '/update.apk')
        time.sleep(1)
        Dnconsole.dnld(index, 'pm install /sdcard/Pictures/update.apk')

    @staticmethod
    def uninstall(index: int, package: str):
        cmd = Dnconsole.console + 'uninstallapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def invokeapp(index: int, package: str):
        cmd = Dnconsole.console + 'runapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        print(result)
        return result

    @staticmethod
    def stopapp(index: int, package: str):
        cmd = Dnconsole.console + 'killapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def input_text(index: int, text: str):
        cmd = Dnconsole.console + 'action --index %d --key call.input --value %s' % (index, text)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = Dnconsole.dnld(index, 'pm list packages')
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result

    @staticmethod
    def has_install(index: int, package: str):
        if Dnconsole.is_running(index) is False:
            return False
        return package in Dnconsole.get_package_list(index)

    @staticmethod
    def launch(index: int):
        cmd = Dnconsole.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def quit(index: int):
        cmd = Dnconsole.console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置屏幕分辨率为1080×1920
    @staticmethod
    def set_screen_size(index: int):
        cmd = Dnconsole.console + 'modify --index %d --resolution 1080,1920,480' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def touch(index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            Dnconsole.dnld(index, 'input tap %d %d' % (x, y))
        else:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d %d' % (x, y, x, y, delay))

    @staticmethod
    def press_key(index: int, key: int):
        Dnconsole.dnld(index, 'input keyevent %d' % key)

    @staticmethod
    def swipe(index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            Dnconsole.dnld(index, ' input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            Dnconsole.dnld(index, ' input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    @staticmethod
    def copy(name: str, index: int = 0):
        cmd = Dnconsole.console + 'copy --name %s --from %d' % (name, index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def add(name: str):
        cmd = Dnconsole.console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def auto_rate(index: int, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = Dnconsole.console + 'modify --index %d --autorotate %d' % (index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def change_device_data(index: int):
        # 改变设备信息
        cmd = Dnconsole.console + 'modify --index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def change_cpu_count(index: int, number: int):
        # 修改cpu数量
        cmd = Dnconsole.console + 'modify --index %d --cpu %d' % (index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def get_cur_activity_xml(index: int):
        # 获取activity的xml信息
        Dnconsole.dnld(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(1)
        f = open(Dnconsole.share_path + '%d/activity.xml' % index, 'r', encoding='utf-8')
        result = f.read()
        f.close()
        return result

    @staticmethod
    def get_user_info(index: int) -> UserInfo:
        xml = Dnconsole.get_cur_activity_xml(index)
        usr = UserInfo(xml)
        if 'id' not in usr.info:
            return UserInfo()
        return usr

    @staticmethod
    def get_activity_name(index: int):
        text = Dnconsole.dnld(index, 'dumpsys activity top | grep ACTIVITY', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    @staticmethod
    def wait_activity(index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if Dnconsole.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False

    @staticmethod
    def find_pic(screen: str, template: str, threshold: float):
        try:

            scr = Dnconsole.cv_imread(screen)
            tp = Dnconsole.cv_imread(template)
            # cv.namedWindow("aaa")
            # cv.imshow("aaa",scr)
            # cv.imshow("aaa", tp)
            result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
        except cv.error:
            traceback.print_exc()
            print('文件错误：', screen, template)
            time.sleep(1)
            try:
                scr = Dnconsole.cv_imread(screen)
                tp = Dnconsole.cv_imread(template)
                result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
            except cv.error:
                return False, None
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if min_val > threshold:
            print(template, min_val, max_val, min_loc, max_loc)
            return False, None
        print(template, min_val, min_loc)
        return True, min_loc

    ## 读取图像，解决imread不能读取中文路径的问题
    @staticmethod
    def cv_imread(filePath):
        cv_img = cv.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
        ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
        cv_img = cv.cvtColor(cv_img, cv.COLOR_RGB2BGR)
        return cv_img

    @staticmethod
    def wait_picture(index: int, timeout: int, template: str) -> bool:
        count = 0
        while count < timeout:
            Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr%d.png' % index)
            time.sleep(2)
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '/apk_scr%d.png' % index, template, 0.001)
            if ret is False:
                print(loc)
                time.sleep(2)
                count += 2
                continue
            print(loc)
            return True
        return False

    # 在当前屏幕查看模板列表是否存在,是返回存在的模板,如果多个存在,返回找到的第一个模板
    @staticmethod
    def check_picture(index: int, templates: list):
        Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr%d.png' % (index))
        time.sleep(1)
        for i, t in enumerate(templates):
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '/apk_scr%d.png' % index, t, 0.001)
            if ret is True:
                return i, loc

    def set_mnq_path(self, mnq_path):
        Dnconsole.basepath = mnq_path
        Dnconsole.console = Dnconsole.basepath + '\\ldconsole.exe '
        Dnconsole.ld = Dnconsole.basepath + '\\ld.exe '
