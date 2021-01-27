# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import multiprocessing
import os
import sys
import json
import random
import time
from multiprocessing.context import Process
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
import subprocess
import traceback
from Log import log

all_proxy = {}


def _load_proxy():
    global all_proxy
    with open("all_proxy.json", encoding="utf-8") as f:
        data = f.read()
        all_proxy = json.loads(data)


test_url_str = "http://www.baidu.com"

test_url_str1 = "http://ifconfig.me/ip"
myip = "112.13.169.243"


def test_url():
    import socket
    import socks
    import requests
    session = requests.Session()
    session.trust_env = False
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10800)
    socket.socket = socks.socksocket
    resp = session.get(test_url_str, timeout=1)
    delay = resp.elapsed.total_seconds()
    resp.close()
    print(delay)  # 获取实际的响应时间
    return delay


def get_used():
    with open("ss_used.txt", mode="r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def vpn_remove(ss):
    vpn_use = get_used()
    if ss in vpn_use["used"]:
        vpn_use["used"].remove(ss)
    if ss in vpn_use["ss_info"]:
        del vpn_use["ss_info"][ss]
    save_vpn_used(vpn_use)


def save_vpn_used(vpn_use):
    with open("ss_used.txt", mode="w+", encoding="utf-8") as f:
        f.write(json.dumps(vpn_use, indent=4, ensure_ascii=False))


def save_vnp_use(account, ss):
    vpn_use = get_used()
    vpn_use["used"].append(ss)
    vpn_use["account_info"][account] = ss
    vpn_use["ss_info"][ss] = account
    save_vpn_used(vpn_use)


def clear_port(port):
    try:
        result = execute_cmd("netstat -ano |findstr %d|findstr LISTENING" % port)
        if result:
            pid = [x for x in result.split(" ") if x][4]
            pid = pid[:-1]
            ret = execute_cmd("taskkill /f /pid %s" % pid)
            print(ret)
    except:
        log.exception("清理端口失败")


def execute_cmd(cmd):
    process = os.popen(cmd)
    result = process.read()
    process.close()
    return result


def _get_proxy(account: str, q: multiprocessing.Queue):
    _load_proxy()
    chose_proxy = all_proxy.copy()
    vpn_use = get_used()
    ret = False
    check_used = False
    while True:
        if account in vpn_use["account_info"] and not check_used:
            proxy_name = vpn_use["account_info"][account]
            vpn_remove(proxy_name)
        else:
            rest = list(set(list(chose_proxy.keys())) - set(vpn_use.get("used", [])))
            if not rest:
                log.info("没有代理连接了")
                break
            proxy_name = random.choice(rest)
        proxy = chose_proxy[proxy_name]
        s = proxy["clash"]
        command = proxy['command']
        print(command)
        clear_port(10800)
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        print(proxy_name)
        proxy["time"] = time.time()
        try:
            check_used = True
            vpn_remove(proxy_name)
            delay_time = test_url()
            proxy["delay"] = delay_time
            if delay_time < 2:
                with open("temp/test.yaml", "w+", encoding="utf-8") as f:
                    f.write(s)
                save_vnp_use(account, proxy_name)
                ret = True
                del chose_proxy[proxy_name]
                break
            else:
                proxy["bad"] = True
        except:
            proxy["bad"] = True
            traceback.print_exc()

            del chose_proxy[proxy_name]
        finally:
            log.debug("执行finally")
            p.terminate()
        time.sleep(3)
        print("end")
    q.put(ret)


def get_proxy(name):
    q = multiprocessing.Queue()
    p1 = Process(target=_get_proxy, args=(name, q))  # 必须加,号
    p1.start()
    p1.join()
    if not q.empty():
        return q.get()
    return False


def main1():
    get_proxy("dayigui21")
    # "[SS] 🇨🇳 中国-台湾 IEPL HiNet固接 E02 Netflix 动画疯"
    "[SS] 🇭🇰 中国-香港 IEPL Equinix HK2 E 20"
    # clear_port(10800)

def main():
    pass
if __name__ == '__main__':
    main()

# test_url()
