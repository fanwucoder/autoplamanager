accounts1 = """1,dalaoban22,2231360,1,204
2,dayigui21,0,0,0
3,dayigui24,0,0,0
4,haojixing2798,592440,1,8360
5,haojixing223,0,0,0
6,flybird125,0,0,0
7,flybird123,0,0,0
8,flybird124,0,0,0
9,dayibkrj7639,0,0,0
10,dayigui838,722898,1,6280
11,dayigui23,3018500,1,6576
12,dayigui22,3932650,1,14524
13,dayigui20,1510902,1,8124
14,haojixing6475,19073242,1,15788
15,zhiduanda9408,2883672,1,14352
16,zhuandaqian8405,6686920,1,14652
18,fwqkwhui6715,2885344,1,14348
20,dalaoban4871,2494664,1,17032
21,dalaoban23,0,0,0
22,+zhiduanda3606,0,0,0
23,+zhiduanda1996,0,0,0
26,zhuandaqian8007,0,0,0
27,dayigui21,0,0,0"""

accounts2 = """





flybird125=123456
flybird123=123456
flybird124=123456


zhuandaqian8007=zhuandaqian8007
haojixing223=haojixing223
haojixing1876=haojixing1876
dayigui21=dayigui21
dayigui24=dayigui24


dalaoban22=dalaoban22
dayigui2280=dayigui2280

dayibkrj7639=dayibkrj7639
haojixing2798=haojixing2798
haojixing5486=haojixing5486
dayigui838=dayigui838
dayigui2761=dayigui2761
dayigui23=dayigui23
dayigui22=dayigui22
dayigui20=dayigui20
haojixing6475=haojixing6475
zhiduanda9408=zhiduanda9408
zhuandaqian8405=zhuandaqian8405
fwqkwhui6715=fwqkwhui6715
zhiduanda3544=zhiduanda3544
dalaoban4871=dalaoban4871
dalaoban23=dalaoban23
zhiduanda3606=zhiduanda3606
zhiduanda1996=zhiduanda1996


zhuandaqian3233=zhuandaqian3233
dalaoban20=dalaoban20
fwqkwhui7913=fwqkwhui7913
dayigui9031=dayigui9031
haojixing2779=haojixing2779
dalaoban3837=dalaoban3837
"""
a1 = []
for a in accounts1.split("\n"):
    if a:
        a = a.split(",")[1]
        if "+" in a:
            a = a[1:]
        a1.append(a)
a2 = []
for x in accounts2.split("\n"):
    if x:
        a2.append(x.split("=")[0])
print(set(a2) - set(a1))
rest = {'dayigui9031', 'haojixing5486', 'dalaoban20', 'dalaoban3837',
        'zhuandaqian3233', 'dayigui2761', 'fwqkwhui7913',
        'zhiduanda3544', 'haojixing2779', 'dayigui2280', 'haojixing1876'}
