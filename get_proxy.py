import sys
import json
import random
import time
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
import subprocess
import traceback
all_proxy = None


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


def get_proxy():
    if all_proxy is None:
        _load_proxy()
    chose_proxy = all_proxy.copy()
    while True:

        proxy_name = random.choice(list(chose_proxy.keys()))
        proxy = chose_proxy[proxy_name]
        s = proxy["clash"]
        command = proxy['command']
        print(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        print(proxy_name)
        proxy["time"]=time.time()
        try:
            delay_time = test_url()
            proxy["delay"]=delay_time
            if delay_time < 2:
                break
            del chose_proxy[proxy_name]
        except:
            proxy["bad"]=True
            # traceback.print_exc()
            del chose_proxy[proxy_name]
        finally:
            p.terminate()
        time.sleep(3)
        print("end")
        with open("test.yaml", "w+", encoding="utf-8") as f:
            f.write(s)
    print(proxy_name)


get_proxy()
# test_url()
