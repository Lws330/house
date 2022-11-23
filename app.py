from flask import Flask, render_template, request
import pymysql
import jieba
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index', methods=['POST','GET'])
def home():
    return index()


@app.route('/house', methods=['POST','GET'])
def house():
    datalist = []
    con = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='house',
        charset='utf8'
    )
    cur = con.cursor()
    sql = "select * from erhouse"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        datalist.append(item)
    cur.close()

    # print(datalist)
    return render_template("house.html", houses=datalist)


@app.route('/country', methods=['POST','GET'])
def country():
    country = []  # 小区
    num = []  # 数量
    s = []
    conn = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='house',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from housenum2"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        s.append(item)
        country.append(str(item[1]))
        num.append(int(item[2]))

    cur.close()

    return render_template("country.html", country=country, num=num)


@app.route('/team', methods=['POST','GET'])
def team():
    return render_template("team.html")


# @app.route('/show', methods=['POST', 'GET'])
# def show():
#     search_result = []
#     # 取出待搜索keyword
#     keyword = request.form.get('keyword')
#     # 对keyword分词
#     cut_keywords = jieba.cut_for_search(keyword)
#     # 遍历所有切分出来的词，搜索数据库
#     for cut_keyword in cut_keywords:
#         search_result.append(sql_query(cut_keyword))  # sql_query()写在最后
#     # 记录搜到了多少数据
#     search_result = set(search_result)
#     return render_template('show.html', search_result=search_result, keyword=keyword)
#
#
# def sql_query(keyword):
#     conn = pymysql.Connect(
#         host='127.0.0.1',
#         port=3306,
#         user='root',
#         passwd='123456',
#         db='house',
#         charset='utf8'
#     )
#     cur = conn.cursor()
#     sql = "select id,place,xiaoqu,house_size,chaoxiang,huxing,house_type,floor_num,subway,decoration,house_key,house_new,house_time,house_money from erhouse where place like '%{keyword}%'".format(
#         keyword=keyword)
#     cur.execute(sql)
#     result = cur.fetchall()
#     return result
@app.route('/show', methods=['GET', 'POST'])
def show():
    resultform = []
    a = request.args
    keyword = a.get("keyword")
    conn = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='house',
            charset='utf8'
        )
    cur = conn.cursor()
    sql = "select id,place,xiaoqu,house_size,chaoxiang,huxing,house_type,floor_num,subway,decoration,house_key,house_new,house_time,house_money from erhouse where place like '%{keyword}%' or xiaoqu like '%{keyword}%' or house_size like '%{keyword}%' or chaoxiang like '%{keyword}' or huxing like '%{keyword}' or house_type like '%{keyword}' or floor_num like '%{keyword}' or subway like '%{keyword}' or decoration like '%{keyword}' or house_key like '%{keyword}' or house_new like '%{keyword}' or house_time like '%{keyword}' or house_money like '%{keyword}'".format(
        keyword=keyword)
    cur.execute(sql)
    result = cur.fetchall()
    for i in result:
        resultform.append(i)
    return render_template('show.html', result=result, keyword=keyword)


if __name__ == '__main__':
    app.run(debug=True)
