#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/6/21 17:53
#@Author :weige
#@File :user_behavior.py
# userid(19-38)
# articleid(33-102)
import MySQLdb
import random
# from pyExcelerator import *
# from pyExcelerator.Workbook import Workbook
# from Workbook import Workbook
db = MySQLdb.connect("localhost","root","wjl984296155@#$","laoqidjangobook",charset="utf8")
cursor = db.cursor()
# for i in range(19,39):
#     for a in range(1001):#每个用户有1000条随机记录，构造1000个在（33-102）之间的随机数
#         #
#         ran = random.randint(33,102)
#         sql =  "INSERT INTO articles_view_count(user_id,article_id) values (%d,%d)"%(i,ran)
#         cursor.execute(sql)
#         db.commit()
# sql = "DROP TABLE articles_view_count"
# cursor.execute(sql)
# db.commit()

#
# # 某个用户（随机，不是全部）浏览了某篇文章（随机，不是全部），产生3000条记录
# for i in range(30000):
#     user = random.randint(19,38)
#     article = random.randint(33,102)
#     sql = "INSERT INTO account_view_count(user_id,article_id) values (%d,%d)"%(user,article)
#     cursor.execute(sql)
#     db.commit()

# 取出结果，整理数据
sql = "SELECT * FROM account_view_count"
cursor.execute(sql)

result = cursor.fetchall()
user_count = []
user_counts = []
for i in result:
    user_counts.append(list(i))

# print(user_counts)
# file = open("user_counts.csv","w")
#
# for i in range(len(user_counts)):
#     for a in range(len(user_counts[i])):
#         file.write(str(user_counts[i][a])+',')
#     file.write("\n")
#


# 去除掉第一列id元素
for i in range(len(user_counts)):
    user_counts[i].remove(user_counts[i][0])
# print(user_counts)
# user_id aerticle_id count
# read_count = []
read_counts = []
count = 0
user_id_list = []
# 看看有多少个不同的user_id
for i in range(len(user_counts)):
    user_id_list.append(user_counts[i][0])

user_id_list = list(set(user_id_list))
user_id_list.sort()
# print(user_id_list)
# 一个一个遍历

for i in range(len(user_id_list)):
    user_read_record = []
    for a in range(len(user_counts)):
        if (user_id_list[i]==user_counts[a][0]):
            # print(user_counts[a])
            user_read_record.append(user_counts[a])
        if(a==len(user_counts)-1):
            # print(user_read_record)#每个用户的阅读行为在这里
#            每个用户读了多少篇不同的文章
            user_read_record_article = []
            for b in range(len(user_read_record)):
                user_read_record_article.append(user_read_record[b][1])
            # print(user_read_record_article)用户读过的文章在这里
            user_read_record_article = list(set(user_read_record_article))
            # 文章一篇一篇地遍历

            for c in range(len(user_read_record_article)):
                yueducishu = 0
                read_count = []
                article_localtion_in_matrix = 0
                for d in range(len(user_read_record)):
                    if(user_read_record_article[c]==user_read_record[d][1]):
                            yueducishu+=1
                read_count.append(user_id_list[i])
                read_count.append(user_read_record_article[c])
                read_count.append(yueducishu/10)
                read_count.append(i)
                read_count.append(c)
                read_counts.append(read_count)
                print("用户%d读文章%d读了%d次,此纪录在矩阵中的位置%d,%d"%(user_id_list[i],user_read_record_article[c],yueducishu,i,c))





# print(read_counts)
file = open("read_counts_divide10.csv","w")
digit = 0
for i in range(len(read_counts)):
    # file.write(str(digit) + ",")
    for a in range(len(read_counts[i])):
        file.write(str(read_counts[i][a])+",")
        # file.write("\n")
    file.write("\n")
    # digit+=1