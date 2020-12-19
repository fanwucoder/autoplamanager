import sys
import json
import random
import time
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
    print(delay)  # 获取实际的响应时间
    return delay


def get_used():
    with open("ss_used.txt", mode="r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def get_proxy(account):
    if not all_proxy:
        _load_proxy()
    chose_proxy = all_proxy.copy()
    vpn_use = get_used()
    while True:
        rest = list(set(list(chose_proxy.keys())) - set(vpn_use.get("used", [])))
        if not rest:
            log.info("没有代理连接了")
            return False
        proxy_name = random.choice(rest)
        proxy = chose_proxy[proxy_name]
        s = proxy["clash"]
        command = proxy['command']
        print(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        print(proxy_name)
        proxy["time"] = time.time()
        try:
            delay_time = test_url()
            proxy["delay"] = delay_time
            if delay_time < 2:
                with open("temp/test.yaml", "w+", encoding="utf-8") as f:
                    f.write(s)
                return True
            del chose_proxy[proxy_name]
        except:
            proxy["bad"] = True
            # traceback.print_exc()
            del chose_proxy[proxy_name]
        finally:
            log.debug("执行finally")
            p.terminate()
        time.sleep(3)
        print("end")


get_proxy("test_account")
# test_url()
