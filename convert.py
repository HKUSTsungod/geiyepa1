"""
将image同名转为pdf
"""
import sys
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image

import os

# root_dir为要读取文件的根目录
root_dir = "./pic"
# 读取批量文件后要写入的文件


def imgtopdf(input_paths, outputpath):
    (maxw, maxh) = Image.open(input_paths).size
    c = canvas.Canvas(outputpath, pagesize=portrait((maxw, maxh)))
    c.drawImage(input_paths, 0, 0, maxw, )
    c.showPage()
    c.save()


# 依次读取根目录下的每一个文件
for file in os.listdir(root_dir):
    base = file[:-4]
    if not os.path.exists("./pdf/" + base + ".pdf"):
        imgtopdf(root_dir+"/"+file, "./pdf/" + base + ".pdf")
    print(base + "完成")

# 调用demo:
# imgtopdf("D:\XY1700054820171104.png", "cc.pdf")
