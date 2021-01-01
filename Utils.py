# -*- coding: utf-8 -*-
import os

from PIL import Image
import time
import requests
import base64
from PIL import Image
import math


# color_str = "FFEECC-101010|F8ECB0-101010|FFFFFf-222222|F9E8A4-444444"
def get_text(fname):
    f = open(fname, 'rb')
    img = base64.b64encode(f.read())
    return get_ocr_data(img)


def get_ocr_data(img):
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    # f = open('[本地文件]', 'rb')
    # img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()
    return None


def get_ocr_num(img):
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    # 二进制方式打开图片文件
    # f = open('[本地文件]', 'rb')
    # img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()
    return None


token_info = {
    "access_token": None,
    "expires_in": 0,
    "last_time": 0
}


def get_token():
    # encoding:utf-8
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    if time.time() - token_info['last_time'] < token_info['expires_in'] - 3600:
        return token_info['access_token']
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=LIDqc8lxXgbDa8dtXHVm7FTX&client_secret=uFod2vGXK3HhWw3MYFkeXaNF82akB2TH'
    response = requests.get(host)
    if response:
        ret = response.json()
        if "error" in ret:
            print(ret)
        else:
            token_info['access_token'] = ret['access_token']
            token_info['expires_in'] = ret['expires_in']
            token_info['last_time'] = time.time()
    return token_info['access_token']


def rgb2int(hex):
    return int(hex, 16)


def get_rgb(color):
    return (rgb2int(color[0:2]), rgb2int(color[2:4]), rgb2int(color[4:6]))


def get_colors(colors):
    data = []
    for cs in colors.split("|"):
        c1, c2 = cs.split('-')
        data.append(get_rgb(c1) + get_rgb(c2))
    return data


# print(rgb2int('ff'))
# print(get_rgb('ffffff'))
# print(get_colors(color_str))
def get_gray(fb, color_str):
    im = Image.open(fb)
    return image2gray(im, color_str)


def image2gray(im, color_str):
    width = im.size[0]
    height = im.size[1]
    im = im.convert('RGB')
    target = Image.new("RGB", (width, height))
    rgb_list = get_colors(color_str)

    def check_rgb(r, g, b, rgb_list):
        for r1, b1, g1, r2, b2, g2 in rgb_list:
            if r1 - r <= r2 and g1 - g <= g2 and b1 - b <= b2:
                # print(r1,g1,b1)
                return True

        return False

    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            if (check_rgb(r, g, b, rgb_list)):
                target.putpixel((x, y), (255, 255, 255))

            else:
                target.putpixel((x, y), (0, 0, 0))

    return target


from functools import reduce

from PIL import Image


def hamming_distance(a, b):
    return bin(a ^ b).count('1')


def is_imgs_similar(img1, img2):
    return True if hamming_distance(phash(img1), phash(img2)) <= 5 else False


def phash(img):
    img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
    return reduce(
        lambda x, yz: x | (yz[1] << yz[0]),
        enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())),
        0
    )


def route_picture(path):
    file_path, file_name = os.path.split(path)
    im = Image.open(path)
    width, heigh = im.size
    if heigh > width:
        angle = 90
        im = im.rotate(angle, expand=True)
        im.save('temp/route' + file_name)
        os.remove(path)
        os.rename('temp/route' + file_name, path)


def crop_picture(path):
    file_path, file_name = os.path.split(path)
    im = Image.open(path)
    cropped = im.crop((0, 0, 200, 100))
    cropped.save(os.path.join(file_path, 'crop_' + file_name))
# im1=Image.open("temp.png")
# im2=Image.open("公告.png")
# print(is_imgs_similar(im1,im2))
