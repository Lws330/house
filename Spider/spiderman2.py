import re  # 正则表达式，进行文字匹配
from bs4 import BeautifulSoup  # 网页解析，获取数据
import urllib.request, urllib.error  # 制定URL，获取网页数据
import pymysql


findplace1 = re.compile(
    r'<a href="/zufang/.*" target="_blank">(.*)</a>-<a href="/zufang/.* target="_blank">.*</a>-<a href="/zufang.*" target="_blank" title=".*">.*</a>')  # 创建正则表达式对象，表示规则（字符串的模式）
findplace2 = re.compile(
    r'<a href="/zufang/.*" target="_blank">.*</a>-<a href="/zufang/.* target="_blank">(.*)</a>-<a href="/zufang.*" target="_blank" title=".*">.*</a>')
findplace3 = re.compile(
    r'<a href="/zufang/.*" target="_blank">.*</a>-<a href="/zufang/.* target="_blank">.*</a>-<a href="/zufang.*" target="_blank" title=".*">(.*)</a>')
# 房子大小
finddaxiao = re.compile(r'<i>/</i>(.*)<i>/</i>.*<i>/</i>.*<span class="hide">', re.S)  # re.s让换行符包含在字符中
# 房子朝向
findfangxiang = re.compile(r'<i>/</i>.*<i>/</i>(.*)<i>/</i>.*<span class="hide">', re.S)
# 房子规格
findguige = re.compile(r'<i>/</i>.*<i>/</i>.*<i>/</i>(.*)<span class="hide">', re.S)
# 楼层类型
findleixing = re.compile(
    r'<p class="content__list--item--des">.*<i>/</i>(.*)</span>.*</p>.*<p class="content__list--item--bottom oneline">',
    re.S)
# 是否靠近地铁
findsubway = re.compile(r'<i class="content__item__tag--is_subway_house">(.*)</i>')
# 是否是精装
finddecoration = re.compile(r'<i class="content__item__tag--decoration">(.*)</i>')
# 是否可以随时看房
findkey = re.compile(r'<i class="content__item__tag--is_key">(.*)</i>')
# 是否是新上的
findnew = re.compile(r'<i class="content__item__tag--is_new">(.*)</i>')
# 维护时间
findtime = re.compile(r'<span class="content__list--item--time oneline">(.*)</span>')
# 平均租金
findmoney = re.compile(r'<span class="content__list--item-price"><em>(.*)</em>')


def getData():  # 调用获取页面信息的函数
    datalist = []  # 分配暂存的空间
    for i in range(0, 100):
        baseurl = "https://sh.lianjia.com/zufang/pg"
        url = baseurl + str(i) + "/#contentList"
        html = askURL(url)  # 保存获取到的网页源码

        # 逐一解析数据（边获取边解析）
        soup = BeautifulSoup(html, "html.parser")  # html.parser是html的解析器
        for item in soup.find_all('div', class_="content__list--item"):  # 查找符合要求的字符串，形成列表
            # print(item) #测试：查看链家item全部信息
            data = []
            item = str(item)  # 转换成字符串，否则无法识别
            # 链家详情链接

            place1 = re.findall(findplace1, item)[0]  # re库用来通过正则表达式查找指定的字符串
            place2 = re.findall(findplace2, item)[0]
            place3 = re.findall(findplace3, item)[0]
            place = place1 + '-' + place2
            data.append(place)  # 添加地址

            data.append(place3)  # 添加小区

            daxiao = re.findall(finddaxiao, item)[0]
            daxiao = daxiao.strip()
            data.append(daxiao.replace("㎡", ""))  # 添加房子大小(平米)并替换前后空格

            fangxiang = re.findall(findfangxiang, item)[0]
            data.append(fangxiang.replace(" ", ""))  # 添加房子朝向并替换空格

            guige = re.findall(findguige, item)[0]
            data.append(guige.replace(" ", ""))  # 添加房子户型并替换空格

            leixing1 = re.findall(findleixing, item)[0]
            leixing2 = leixing1.strip()  # 去掉前后空格
            leixing3 = leixing2.replace(" ", "")  # 将空格替换掉
            data.append(leixing3[0:3])  # 添加房子楼层类型并替换空格

            data.append(leixing3[4:8].replace("层）", ""))  # 添加房子层数并替换掉()

            subway = re.findall(findsubway, item)  # 可能写有靠近地铁
            if (len(subway)) != 0:
                subway = subway[0]
                data.append(subway)  # 添加近地铁
            else:
                data.append("不靠近地铁")  # 添加不靠近地铁

            decoration = re.findall(finddecoration, item)
            if len(decoration) != 0:
                decoration = decoration[0]
                data.append(decoration)  # 添加精装
            else:
                data.append("不是精装")  # 添加不是精装

            key = re.findall(findkey, item)
            if len(key) != 0:
                key = key[0]
                data.append(key)  # 添加随时看房
            else:
                data.append("不是随时看房")  # 添加不是随时看房

            new = re.findall(findnew, item)
            if len(new) != 0:
                new = new[0]
                data.append(new)  # 添加新上
            else:
                data.append("不是新上")  # 添加不是新上

            time = re.findall(findtime, item)[0]
            data.append(time)  # 添加维护时间

            money = re.findall(findmoney, item)[0]
            data.append(money)  # 添加平均租金（元/月）

            datalist.append(data)  # 将data中的数据放入datalist中
    return datalist


def askURL(url):
    head = {  # 模拟浏览器头部信息，向链家服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def saveData2DB(datalist):
    conn = pymysql.connect(
        user="root",
        port=3306,
        passwd="123456",
        db="house",
        host="127.0.0.1",
        charset='utf8'
    )
    cur = conn.cursor()
    id = 3001
    for i in datalist:
        id = id + 1
        x0 = str(i[0])
        x1 = str(i[1])
        x2 = str(i[2])
        x3 = str(i[3])
        x4 = str(i[4])
        x5 = str(i[5])
        x6 = str(i[6])
        x7 = str(i[7])
        x8 = str(i[8])
        x9 = str(i[9])
        x10 = str(i[10])
        x11 = str(i[11])
        x12 = str(i[12])
        insert_re = f'insert into erhouse(id,place,xiaoqu,house_size,chaoxiang,huxing,house_type,floor_num,subway,decoration,house_key,house_new,house_time,house_money)values (\'{id}\',\'{x0}\',\'{x1}\',\'{x2}\',\'{x3}\',\'{x4}\',\'{x5}\',\'{x6}\',\'{x7}\',\'{x8}\',\'{x9}\',\'{x10}\',\'{x11}\',\'{x12}\')'
        cur.execute(insert_re)  # 执行sql语句
        conn.commit()
        print(datalist)
        print("save....")
    conn.close()



if __name__ == '__main__':
    datalist = getData()
    # 保存数据
    saveData2DB(datalist)
print("爬取完毕")
