# -*- coding: utf-8 -*-
template=u"""
proxies:
  - {content}
proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - {name}
rules:
  - 'MATCH,Proxy'
"""
import json
command_tp="""sslocal.exe  -s {server} -p {port} -l {local_port} -m "{method}" -k "{password}\""""
all_proxy=dict()
with open("nodeinfo.txt",encoding="utf-8") as f:
    data=f.read()
for line in data.split("\n"):
    name= line[line.find(":")+2:line.find(", server")]
    server=line[line.find("r:")+3:line.find(", port:")]
    port=line[line.find("t:")+3:line.find(", type")]
    method=line[line.find("her:")+5:line.find(", pas")]
    password=line[line.find("d:")+3:line.find(", udp")]
    command=command_tp.format(server=server,port=port,local_port=10800,method=method,password=password)
    print(command)
    ret={"name":name,"content":line}
    s=template.format(**ret)
    all_proxy[name]={
      "clash":s,
      "command":command
    }
with open("all_proxy.json",mode="w+") as f:
  f.write(json.dumps(all_proxy,indent=4))