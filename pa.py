"""
根据target和pic 路径爬取图片吉他谱，存为storagePath下的图片
"""
import requests
from bs4 import BeautifulSoup
import os

target = "https://www.jitashe.org"
# pic = "/guide/hottab/t2/"  # 热门图片谱
pic = "/guide/newtab/t2/"  # 最新图片谱

storagePath = './pic/'

piclinks = {}
imgInfo = {}

if not os.path.exists(storagePath):
    os.mkdir(storagePath)

while True:
    r = requests.get(target + pic)
    soup = BeautifulSoup(r.text, 'html.parser')
    picTAGa = soup.find_all(name='a', attrs={"class": "title"})
    for a in picTAGa:
        title = a.text
        href = a['href']
        piclinks[title] = target + href

    nextpage = soup.find(name="a", attrs={"class": "nxt"})
    if nextpage:
        pic = nextpage['href']
        print("next")
    else:
        break


for name in piclinks:
    imgInfo[name] = []
    picIndex = 1
    nr = requests.get(piclinks[name])
    soup = BeautifulSoup(nr.text, 'html.parser')
    divAll = soup.find(name="div", attrs={"class": "imgtab maintabview"})
    if divAll:
        divAll = divAll.children
    else:
        print(name + " 格式不对 ")
        continue
    for div in divAll:
        if div.name == "ignore_js_op":
            subDivs = div.children
            for subdiv in subDivs:
                if subdiv.name == "picture":
                    subSubDivs = subdiv.children
                    for subsubdiv in subSubDivs:
                        if subsubdiv.name == "img":
                            imgInfo[name].append(subsubdiv["src"])
    for src in imgInfo[name]:
        filePath = storagePath + name + str(picIndex) + ".jpg"
        # noinspection PyBroadException
        try:
            if not os.path.exists(filePath):
                r = requests.get(src)
                r.raise_for_status()
                with open(filePath, "wb") as f:
                    f.write(r.content)
                print("写入" + name + " " + str(picIndex))

            else:
                print(name + " " + str(picIndex) + " 已存在")
            picIndex += 1
        except Exception as e:
            print("写入" + name + " " + str(picIndex) + " 失败！！")
            print(e)

print(imgInfo)

