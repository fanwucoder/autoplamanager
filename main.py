# -*- coding: utf-8 -*-
from concurrent.futures.thread import ThreadPoolExecutor

from flask import Flask, Response, send_from_directory, redirect
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
import time
import threading
from Log import log

from leidianManager import AutoRunner

app = Flask(__name__, static_folder='static', static_url_path='/static')


def start_groups():
    manager.run()


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route('/finish_result/<path:filename>')
def custom_static(filename):
    return send_from_directory("finish_result", filename)


@app.route('/')
def hello_world():
    return send_from_directory(".", "index.html")


json_default = lambda obj: obj.__dict__


def get_last_image(idx):
    imgs = get_mnq_imgs(idx)
    imgs = [x for x in imgs if x.endswith("start_run.png")]
    # print(imgs)
    sorted(imgs, reverse=True)
    if len(imgs) > 0:
        return imgs[0].replace("\\", "/")
    return None


def get_mnq_imgs(idx, date=None):
    if date is None:
        date = ''
    path = "finish_result"
    pre = "%d_%s" % (idx, date)
    names = []
    for f in os.listdir(path):
        if f.startswith(pre) and f.endswith(".jpeg"):
            fpath = os.path.join(path, f)
            names.append(fpath.replace("\\", "/"))
    return sorted(names, reverse=True)


def get_crop_imgs(idx, date=None):
    imgs = [x for x in get_crop_file(idx, date) if "game" in x]
    imgs = sorted(imgs, reverse=True)
    imgs = imgs[:4]
    return imgs


def get_crop_file(idx, date=None):
    if date is None:
        date = dt.now().strftime("%Y%m%d")
    path = "finish_result"
    pre = "crop_%d_%s" % (idx, date)
    names = []
    for f in os.listdir(path):
        if f.startswith(pre) and f.endswith(".jpeg"):
            fpath = os.path.join(path, f)
            names.append(fpath.replace("\\", "/"))
    return names


@app.route("/api/list")
def list_mnq():
    datas = []
    for status in group_runner.get_DnPlayers():
        status.last_img = get_last_image(status.index)
        status.img = get_crop_imgs(status.index)
        datas.append(status)
    return Response(json.dumps(datas, default=json_default), mimetype='application/json')


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


@app.route('/api/stop_mnq', methods=['GET', 'POST'])
def stop_mnq():
    idx = request.form.get("idx", type=int)
    result = group_runner.stop_mnq_by_idx(idx)
    return Response(get_msg(result, None), mimetype='application/json')


def _start_mnq(idx):
    try:
        group_runner.start_mnq_by_idx(idx)
    except:
        log.exception("一部任务启动失败")


@app.route('/api/start_mnq', methods=['GET', 'POST'])
def start_mnq():
    idx = request.form.get("idx", type=int)
    executor.submit(_start_mnq, idx)

    return Response(get_msg(True, "启动成功"), mimetype='application/json')


@app.route('/api/last_img', methods=['GET', 'POST'])
def get_last_img():
    idx = request.form.get("idx", type=int)
    group_runner.mark_img(idx)
    last_img = get_last_image(idx)
    return Response(get_msg(True, last_img), mimetype='application/json')


@app.route('/api/history_pic', methods=['GET', 'POST'])
def history_pic():
    idx = request.form.get("idx", type=int)
    his_img = get_mnq_imgs(idx)[:30]
    return Response(get_msg(True, his_img), mimetype='application/json')


def get_msg(success, data):
    return json.dumps({"success": success, "data": data})


import os

if __name__ == '__main__':
    import sys

    port = 5000
    only_web = False
    if len(sys.argv) > 1:
        only_web = sys.argv[1] == 'True'
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    if not only_web:
        server_base = "http://192.168.0.103:5000/"
        manager = GroupManager()
        manager.init()
        executor = ThreadPoolExecutor(2)
        manager_thread = threading.Thread(target=start_groups)
        manager_thread.start()
        time.sleep(1)
        group_runner = manager.get_single_group()  # type:AutoRunner

    print(os.path.abspath("."))
    app.run(host='0.0.0.0', port=port)
