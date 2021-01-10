# -*- coding: utf-8 -*-
import sys
import os


def main():
    xypath = '"%s"' % sys.argv[1]
    idx = sys.argv[2]
    for f in os.listdir("."):
        if f.endswith("lua"):
            command = "%s -i %s adb shell rm -r -f /sdcard/TouchSprite/lua/%s" % (xypath, idx, f)
            print(command)
            os.system(command)
            command = "%s -i %s adb push %s /sdcard/TouchSprite/lua/%s" % (xypath, idx, f, f)
            print(command)
            os.system(command)
        elif f.endswith(".py") or f.endswith(".bat") or f.endswith(".md"):
            continue
        else:
            command = "%s -i %s adb shell rm -r -f /sdcard/TouchSprite/res/%s" % (xypath, idx, f)
            print(command)
            os.system(command)
            command = "%s -i %s adb push %s /sdcard/TouchSprite/res/%s" % (xypath, idx, f, f)
            print(command)
            os.system(command)


if __name__ == '__main__':
    main()
