# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from PIL import Image
import time
import base64
from io import BytesIO
import uuid
import requests
from Utils import get_ocr_data, image2gray, is_imgs_similar, get_ocr_num

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


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
