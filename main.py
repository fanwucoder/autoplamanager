# -*- coding: utf-8 -*-
from flask import Flask,Response,send_from_directory
from flask import request
from PIL import Image
import time
import base64
from io import BytesIO
import uuid
import json
from datetime import datetime as dt
import requests
from Utils import get_ocr_data, image2gray, is_imgs_similar, get_ocr_num
from GroupManager import GroupManager
manager=GroupManager()
manager.init()
mnq_op=manager.get_operate()
app = Flask(__name__)


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ
@app.route('/finish_result/<path:filename>')
def custom_static(filename):
    return send_from_directory("finish_result", filename)

@app.route('/')
def hello_world():
    return 'Hello, World!'
json_default=lambda obj: obj.__dict__
def get_last_image(idx):
    imgs=get_mnq_imgs(idx,"20201230")
    imgs=[x for x in imgs if x.endswith("start_run.png")]
    # print(imgs)
    sorted(imgs)
    if len(imgs)>0:
        return "http://localhost:5000/"+imgs[-1].replace("\\","/")
    return None
def get_mnq_imgs(idx,date=None):
    if date is None:
        date=dt.now().strftime("%Y%m%d")
    path="finish_result"
    pre="%d_%s"%(idx,date)
    names=[]
    for f in os.listdir(path):
        if f.startswith(pre):
            fpath=os.path.join(path,f)
            names.append(fpath.replace("\\","/"))
    return names
def get_crop_imgs(idx,date=None):
    imgs=["http://localhost:5000/"+x for x in get_crop_file(idx,date) if "game" in x]
    imgs=sorted(imgs)
    return imgs
def get_crop_file(idx,date=None):
    if date is None:
        date=dt.now().strftime("%Y%m%d")
    path="finish_result"
    pre="crop_%d_%s"%(idx,date)
    names=[]
    for f in os.listdir(path):
        if f.startswith(pre):
            fpath=os.path.join(path,f)
            names.append(fpath.replace("\\","/"))
    return names
@app.route("/list")
def list_mnq():
    import random
    from dnconsole import DnPlayer
    datas=[]
    for i in range(20):
        data=[i,"name"+str(i),0,0,random.randint(0,2),0,0]
        status=DnPlayer(data)
        status.last_img=get_last_image(status.index)
        status.img=get_crop_imgs(status.index,"20201230")
        datas.append(status)
    return  Response(json.dumps(datas,default=json_default), mimetype='application/json')
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['ocr_file']
        x1 = request.args.get('x1', type=int)
        y1 = request.args.get('y1', type=int)
        x2 = request.args.get('x2', type=int)
        y2 = request.args.get('y2', type=int)
        colors = request.args.get('colors', type=str)
        img = Image.open(f)
        print(x1, y1, x2, y2)
        img1 = image2gray(img.crop((x1, y1, x2, y2)), colors)
        buffered = BytesIO()
        img1.save(buffered, format="png")
        img1.save("res/temp.png", format="png")
        img_str = base64.b64encode(buffered.getvalue())
        data = get_ocr_data(img_str)
        print(data)
        if data and data['words_result_num'] > 0:
            ret = data["words_result"][0]['words']

            return ret
        # print("data:image/png;base64,"+str(img_str,encoding='utf-8'))
    return ""


@app.route('/upload1', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        f = request.files['ocr_file']
        colors = request.args.get('colors', type=str)
        img = Image.open(f)
        img.save("res/temp1.png")
        img1 = image2gray(img, colors)
        buffered = BytesIO()
        img1.save(buffered, format="png")
        img1.save("res/temp.png", format="png")
        img_str = base64.b64encode(buffered.getvalue())
        data = get_ocr_num(img_str)
        print(data)
        if data and data['words_result_num'] > 0:
            ret = data["words_result"][0]['words']

            return ret
        # print("data:image/png;base64,"+str(img_str,encoding='utf-8'))
    return ""


target_pic = {"1": "公告.png",
              "2": "自动游戏.png",
              "3": "精力为0.png",
              "4": "未通关.png",
              "5": "上士登录.png",
              "6": "排队等待.png",
              "7": "开始房间1.png",
              "8": "完成房间1.png",
              "9": "开始房间2.png",
              "10": "完成房间2.png",
              "11": "确认绑定.png"
              }


@app.route('/compare_img', methods=['GET', 'POST'])
def compare_img():
    if request.method == 'POST':
        f = request.files['ocr_file']
        x1 = request.args.get('x1', type=int)
        y1 = request.args.get('y1', type=int)
        x2 = request.args.get('x2', type=int)
        y2 = request.args.get('y2', type=int)
        target = request.args.get('target', type=str)
        img = Image.open(f)
        img1 = img.crop((x1, y1, x2, y2))
        img1.save("res/temp.png")
        target_fn = "res/" + target_pic[target]
        img2 = Image.open(target_fn)
        print(target_fn)
        ret = is_imgs_similar(img1, img2)
        print(str(ret))
        return str(ret)
        # print("data:image/png;base64,"+str(img_str,encoding='utf-8'))
    return str(False)


@app.route('/compare_img1', methods=['GET', 'POST'])
def compare_img1():
    if request.method == 'POST':
        f = request.files['ocr_file']
        target = "res/" + request.args.get('target', type=str)
        img1 = Image.open("res/" + f)
        img1.save("res/temp.png")
        img2 = Image.open(target)
        ret = is_imgs_similar(img1, img2)
        print(str(ret))
        return str(ret)
    return str(False)


@app.route('/save_img', methods=['GET', 'POST'])
def save_img():
    if request.method == 'POST':
        f = request.files['ocr_file']
        target = "res/" + request.args.get('target', type=str)
        img1 = Image.open(f)
        img1.save(target)
        return str(True)
    return str(False)


import os

print(os.path.abspath("."))
app.run(host='0.0.0.0')
