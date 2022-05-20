# coding=utf-8
# @Time : 2022/4/24 9:35
# @Author : jnk
# @FileName: createtable.py
# @Software: PyCharm
import sqlite3
sql = '''
        create table movie250 
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric ,
        rated numeric ,
        instroduction text,
        info text
        )

    '''  # 创建数据表
conn = sqlite3.connect("doubanTOP250.db")
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
conn.close()