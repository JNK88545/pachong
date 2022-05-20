# coding=utf-8https://github.com/JNK88545/pachong/blob/main/top_250.py
# @Time : 2022/4/22 14:40
# @Author : jnk
# @FileName: top_250.py
# @Software: PyCharm
import pymysql
from bs4 import BeautifulSoup #网页解析获取数据
import re #正则表达式文字匹配
import urllib.request,urllib.error #制定url,获取网页
import urllib3
import xlwt #进行Excel操作
import sqlite3 #进行SQLite数据库操作

def main():
    baseurl="https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist=getdata(baseurl)
    # savepath="豆瓣TOP250.xls"
    # savedata(datalist,savepath)
    # dbpath="doubanTOP250.db"
    dbpath='douban250'
    sqlsave(datalist,dbpath)
#影片连接
findLink=re.compile(r'<a href="(.*?)">') #创建正则表达式对象，创建规则
#影片图片链接
findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S)
#影片名
findname=re.compile(r'<span class="title">(.*?)</span>') #创建正则表达式对象，创建规则
#影片英文名
findfrename=re.compile(r'<span class="title">\xa0/\xa0(.*?)</span>') #创建正则表达式对象，创建规则
#影片港台名
findotname=re.compile(r'<span class="other">(.*?)</span>') #创建正则表达式对象，创建规则
#影片评分
findscore=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
#影片评价人数
findnum=re.compile(r'<span>(\d*)人评价</span>')
#概况
findInq=re.compile(r'<span class="inq">(.*?)</span>')
#影片导演主演
finddert=re.compile(r'<p class="">(.*?)</p>',re.S)
#影片评价人数
#1.爬取网页
def getdata(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        html = askurl(url)  # 保存获取到的网页源码

        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)   #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)  # 添加链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片

            titles = re.findall(findname, item)  # 片名可能只有一个中文名，没有外国名
            if (len(titles) == 2):
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号
                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名字留空

            rating = re.findall(findscore, item)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findnum, item)[0]
            data.append(judgeNum)  # 提加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")  # 留空

            bd = re.findall(finddert, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)  # 把处理好的一部电影信息放入datalist

    return datalist


#得到一个指定url的数据
def askurl(url):
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36"
    } #高数服务器是我们是什么信息
    req=urllib.request.Request(url,headers=headers)
    html=""
    try:
        response=urllib.request.urlopen(req,timeout=10)
        html=response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
#3.保存数据
def savedata(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)  # 保存
#保存到sqllite数据库
# def sqlsave(datalist,dbpath):
#     #连接数据库
#     conn=sqlite3.connect(dbpath)
#     cur = conn.cursor()
#     for data in datalist:
#         for index in range(len(data)):
#             if index == 4 or index == 5:
#                 continue
#             data[index]='"'+data[index].replace(u'\xa0', u'')+'"'
#             sql = '''
#                 insert into  movie250 values(null,%s)'''%",".join(data)
#         print(sql)
#         cur.execute(sql)
#         conn.commit()
#     cur.close()
#     conn.close()
#保存到MySQL
def sqlsave(datalist,dbpath):
    #连接数据库
    conn=pymysql.connect(host='localhost',
                         port=3309,
                         user='root',
                         password='*****',
                         database=dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index]='"'+data[index].replace(u'\xa0', u'')+'"'
            sql = '''
                insert into  movie250 values(null,%s)'''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
if __name__ == '__main__':
    main()
