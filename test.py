# from PIL import Image
# import math
# color_str = "FFEECC-101010|F8ECB0-101010|FFFFFf-222222|F9E8A4-444444"

# def rgb2int(hex):
#     return int(hex,16)
# def get_rgb(color):
#     return (rgb2int(color[0:2]),rgb2int(color[2:4]),rgb2int(color[4:6]))
# def get_colors(colors):
#     data=[]
#     for cs in color_str.split("|"):
#         c1, c2 = cs.split('-')
#         data.append(get_rgb(c1)+get_rgb(c2))
#     return data
# # print(rgb2int('ff'))
# # print(get_rgb('ffffff'))
# # print(get_colors(color_str))

# def get_gray(fb):
#     im = Image.open(fb)
#     width = im.size[0]
#     height = im.size[1]
#     im = im.convert('RGB')
#     target = Image.new("RGB", (width, height))
#     array = []
#     rgb_list=get_colors(color_str)
#     def check_rgb(r,g,b,rgb_list):
#         for r1,b1,g1,r2,b2,g2 in rgb_list:
#             if r1-r<=r2 and g1-g<=g2 and b1-b<=b2:
#                 # print(r1,g1,b1)
#                 return True
            
#         return False
#     for x in range(width):
#         for y in range(height):
#             r, g, b = im.getpixel((x, y))
#             if(check_rgb(r,g,b,rgb_list)):
#                 target.putpixel((x,y),(255,255,255))
                
#             else:
#                 target.putpixel((x,y),(0,0,0))
        
#     return target
# # target.save("new.png")
# # print(array)
# # print(int('ff'))


# data="""
# 一、描写人的品质：

# 平易近人　宽宏大度　冰清玉洁　　持之以恒　　锲而不舍　　废寝忘食　大义凛然　

# 临危不俱　光明磊落　不屈不挠　　鞠躬尽瘁　　死而后已

# 二、描写人的智慧：

# 料事如神　　足智多谋　　融会贯通　　学贯中西　　博古通今　才华横溢　出类拔萃　　博大精深　　

# 集思广益　　举一反三

# 三、描写人物仪态、风貌：

# 憨态可掬　　文质彬彬　　风度翩翩　　相貌堂堂　　落落大方  斗志昂扬　意气风发　　威风凛凛　　

# 容光焕发　　神采奕奕

# 四、描写人物神情、情绪：

# 悠然自得　　眉飞色舞　喜笑颜开　神采奕奕　欣喜若狂　呆若木鸡　喜出望外　　

# 垂头丧气　　无动于衷　　勃然大怒

# 五、描写人的口才：

# 能说会道　　巧舌如簧　　能言善辩　　滔滔不绝　　伶牙俐齿　出口成章　　语惊四座　　娓娓而谈　　

# 妙语连珠　　口若悬河

# 六、来自历史故事的成语：

# 三顾茅庐　　铁杵成针　　望梅止渴　　完璧归赵　　四面楚歌  　负荆请罪　精忠报国　　手不释卷　　

# 悬梁刺股　　凿壁偷光
# """
# a=[]
# for d in data.split("\n"):
#     if "：" in d:
#         continue
#     a=a+d.split("\u3000")
# a=[x for x in a if x]
# import json
# print(json.dumps(a).encode('utf-8').decode('unicode_escape'))

# accounts={"dayigui","dalaoban","zhuandaqian","zhiduanda","haojixing","fwqkwhui","dayibkrj","rshvgt"}
# import random
# a=random.randint(123,888)
# for x in accounts:
#     for i in range(10):
#         account="%s%s"%(x,a+i)
#         print("%s=%s"%(account,account))
passwords="""dayigui20=dayigui20
dayigui21=dayigui21
dayigui22=dayigui22
dayigui22=dayigui22
dayigui23=dayigui23
dayigui24=dayigui24
dalaoban20=dalaoban20
dalaoban21=dalaoban21
dalaoban22=dalaoban22
dalaoban23=dalaoban23
zhiduanda3544=zhiduanda3544
dayigui20=dayigui20
dayigui21=dayigui21
dayigui22=dayigui22
dayigui22=dayigui22
dayigui23=dayigui23
dayigui24=dayigui24
dalaoban20=dalaoban20
dalaoban21=dalaoban21
dalaoban22=dalaoban22
dalaoban23=dalaoban23
dalaoban4871=dalaoban4871
zhuandaqian8007=zhuandaqian8007
dayibkrj7639=dayibkrj7639
dayigui838=dayigui838
haojixing223=haojixing223
dayigui20=dayigui20
dayigui21=dayigui21
dayigui22=dayigui22
dayigui22=dayigui22
dayigui23=dayigui23
dayigui24=dayigui24
dalaoban20=dalaoban20
dalaoban21=dalaoban21
dalaoban22=dalaoban22
dalaoban23=dalaoban23
dalaoban3837=dalaoban3837
haojixing2779=haojixing2779
zhuandaqian8405=zhuandaqian8405
dayigui9031=dayigui9031
dayigui20=dayigui20
dayigui21=dayigui21
dayigui22=dayigui22
dayigui22=dayigui22
dayigui23=dayigui23
dayigui24=dayigui24
dalaoban20=dalaoban20
dalaoban21=dalaoban21
dalaoban22=dalaoban22
dalaoban23=dalaoban23
zhuandaqian3233=zhuandaqian3233
haojixing2798=haojixing2798
dayigui2280=dayigui2280
haojixing1876=haojixing1876
haojixing6475=haojixing6475
haojixing5486=haojixing5486
zhiduanda1996=zhiduanda1996
dayigui2761=dayigui2761
fwqkwhui7913=fwqkwhui7913
zhiduanda3606=zhiduanda3606
fwqkwhui6715=fwqkwhui6715
zhiduanda9408=zhiduanda9408"""
print("\n".join(set(passwords.split("\n"))))