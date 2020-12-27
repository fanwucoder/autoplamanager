# -*- coding: utf-8 -*-

from GroupManager import GroupManager
import signal

gm = None


def quit(signum, frame):
    print('You choose to stop me.')
    gm.quit()


def main():
    global gm
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    gm = GroupManager()
    gm.init()
    gm.run()


if __name__ == '__main__':
    main()
