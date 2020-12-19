import os

from Log import log
from dnconsole import Dnconsole
import time


class MNQ:
    script_path = "scripts"
    device_path = "/sdcard/TouchSprite"

    def __init__(self, console: Dnconsole = None, *args, **kwargs):
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

    @staticmethod
    def start_game(index: int):
        if not MNQ.lanch_mnq(index):
            return False
        MNQ.start_touch(index)

    @staticmethod
    def lanch_mnq(index):
        log.info("启动模拟器,index:%d", index)
        if not Dnconsole.is_running(index):
            Dnconsole.launch(index)
        cnt = 0
        while cnt < 120:
            time.sleep(3)
            if Dnconsole.is_running(index):
                log.info("启动模拟器成功,index:%d", index)
                return True

        return False

    @classmethod
    def start_touch(cls, index: int):
        # Dnconsole.adb(index, "kill-server",silence=False)
        # Dnconsole.adb(index, "wait-for-device",silence=False)
        MNQ.copyScripts(index)
        Dnconsole.adb(index, "shell echo >/sdcard/touch_status.txt ")
        Dnconsole.invokeapp(index, "com.touchsprite.android")
        Dnconsole.wait_activity(index, "com.touchsprite.android/.activity.MainActivity", 120)
        Dnconsole.swipe(index, (100, 300), (100, 700))
        time.sleep(5)
        ret = Dnconsole.check_picture(index, [os.path.join(os.path.abspath("."), "res\main.png")])
        log.info("main 脚本位置%s", str(ret))
        if ret:
            log.info("开始启动main脚本")
            i, xy = ret
            Dnconsole.touch(index, xy[0], xy[1] + 20)
            time.sleep(2)
            Dnconsole.touch(index, 672, xy[1] + 80)
            time.sleep(2)
            Dnconsole.touch(index, 672, xy[1] + 160)

    @classmethod
    def copyScripts(cls, index):
        script_path = os.path.abspath(cls.script_path)
        for f in os.listdir(script_path):
            path = os.path.join(script_path, f)
            if f.endswith("lua"):
                Dnconsole.adb(index, "push %s %s" % (path, cls.device_path + "/lua/" + f))
            else:
                Dnconsole.adb(index, "push %s %s" % (path, cls.device_path + "/res/" + f))

    @classmethod
    def get_status(cls, index):
        Dnconsole.adb(index, "pull %s %s" % ("/sdcard/touch_status.txt", "temp/touch_status.txt"))
        with open("temp/touch_status.txt", mode='r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                return None
            return lines[-1]


def main():
    pass
    mnq = MNQ()

    # print(mnq.get_status(4) == "start\n")
    # mnq.start_game(4)
    # Dnconsole.
    # Dnconsole.find_pic()
    # MNQ.copyScripts(4)

    # ret = Dnconsole.wait_picture(4, 120, "res/main.png")

    # ret=Dnconsole.adb(5,"input swipe 360, 100 361, 700")
    # Dnconsole.touch(5,30,60)

    # ret = Dnconsole.adb(5, "ls /sdcard/")
    # print(ret)
    index = 5
    ret = Dnconsole.check_picture(index, [os.path.join(os.path.abspath("."), "res\main.png")])
    log.info("main 脚本位置%s", str(ret))
    if ret:
        log.info("开始启动main脚本")
        i, xy = ret
        Dnconsole.touch(index, xy[0], xy[1] + 20)
        time.sleep(2)
        Dnconsole.touch(index, 672, xy[1] + 80)
        # todo 通过找图实现
        time.sleep(2)
        Dnconsole.touch(index, 672, xy[1] + 160)


if __name__ == '__main__':
    main()
