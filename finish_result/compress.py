import cv2
import os
from math import *
import numpy as np
from PIL import Image
class Compress_img:

    def __init__(self, img_path):
        self.img_path = img_path
        self.img_name = img_path.split('/')[-1]

    def compress_img_CV(self, compress_rate=0.8, show=False):
        
        im = Image.open(self.img_path)
        width,heigh=im.size
        if heigh>width:
            angle = 90
            im = im.rotate(angle, expand=True)
            # name=self.img_path.replace(".png","t.png")
            # out.save(name)
            # os.remove(self.img_path)
            # os.rename(name,self.img_path)
        cropped = im.crop((0, 0, 200, 100))
        cropped.save('crop_' + self.img_name)
        # img = cv2.imread(self.img_path)
        # width,heigh = img.shape[:2]
        # center=(heigh/2,width/2)

        # # 双三次插值
        # img = cv2.resize(img, (int(heigh*compress_rate), int(width*compress_rate)),
        #                         interpolation=cv2.INTER_AREA)
        # cv2.imwrite('crop_' + self.img_name, img)
        # print("%s 已压缩，" % (self.img_name), "压缩率：", compress_rate)
        # if show:
        #     cv2.imshow(self.img_name, img)
        #     cv2.waitKey(0)
        
    def remane(self):
        os.remove(self.img_path)
        os.rename('result_cv_' + self.img_name,self.img_path)
if __name__ == '__main__':
    img_path = './'
    for f in os.listdir(img_path):
        if f.endswith(".png"):
            name=os.path.join(img_path,f)
            compress = Compress_img(name)

            # 使用opencv压缩图片
            compress.compress_img_CV()
            # compress.remane()
            # break
