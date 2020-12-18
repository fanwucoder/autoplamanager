#注意，请自行导入上面的类代码，否则无法使用
from Dnconsole import Dnconsole
import time
if __name__ == '__main__':
    Dnconsole.launch(0)#打开模拟器
    time.sleep(10)#等待启动
    #TODO: 其他的控制(touch)
    Dnconsole.quit(0)#退出模拟器