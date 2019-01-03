#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
方便合服处理
设置pinus创建的关联的数据库的自增值
"""

import MySQLdb
import re

DB_HOST = "127.0.0.1"			# 数据库ip地址
DB_USER = "root"				# 数据库用户名
DB_PWD = ""						# 数据库用户密码
DB_NAME = "egame2"				# 数据库名称
ID_START = 1000					# id起始值
TABLE_PLAYER = "player_db"		# 玩家数据库名称

if __name__ == '__main__':
	
	conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PWD, db=DB_NAME);
	cur = conn.cursor()
	
	# 获取玩家表的创建信息
	cur.execute("show create table player_db");
	createInfo = cur.fetchone()[1]
	# 正则查找所有的外键语句
	pattern = re.compile(r'CONSTRAINT.*')
	arrSql = pattern.findall(createInfo)
	#createInfo = createInfo.replace("\\n", "\n") 

	# 处理外键创建语句
	arrForeignKey = []
	arrForeignId = []
	arrDbName = []
	arrDbId = []
	
	for k in arrSql:
		#print(k)
		pattern = re.compile(r'`.*`')
		arrVal = k.split("`")
		#print(arrVal)
		arrForeignKey.append(arrVal[1]);
		arrForeignId.append(arrVal[3]);
		arrDbName.append(arrVal[5]);
		arrDbId.append(arrVal[7]);
		
	#print(arrForeignKey);
	#print(arrForeignId);
	#print(arrDbName);
	#print(arrDbId);
	
	# 移除外键约束
	for x in arrForeignKey:
		sqlStr = "ALTER TABLE %s DROP FOREIGN KEY %s" % (TABLE_PLAYER, x)
		print("invoke mysql sql:" + sqlStr)
		cur.execute(sqlStr)
		
	# 设置主键递增的值
	for x in arrDbName:
		sqlStr = "ALTER TABLE %s AUTO_INCREMENT=%s;" % (x, ID_START)
		print("invoke mysql sql:" + sqlStr)
		cur.execute(sqlStr)
	
	# 重新追加外键
	arrList = range(len(arrDbId))
	for x in arrList:
		sqlStr = "ALTER TABLE %s ADD CONSTRAINT %s FOREIGN KEY (%s) REFERENCES %s (%s);" % (TABLE_PLAYER, arrForeignKey[x], arrForeignId[x], arrDbName[x], arrDbId[x])
		print("invoke mysql sql:" + sqlStr)
		cur.execute(sqlStr)
	
	"""	
	# 设置主键默认值
	#for x in arrDbName:
	#	sqlStr = "ALTER TABLE %s modify id INT(11) DEFAULT %d, AUTO_INCREMENT;" % (x, ID_START)
	#	print("invoke mysql sql:" + sqlStr)
	#	cur.execute(sqlStr)
	
	# 追加默认值属性
	#for x in arrDbName:
	#	sqlStr = "ALTER TABLE %s ADD id INT(11) DEFAULT %d;" % (x, ID_START)
	#	print("invoke mysql sql:" + sqlStr)
	#	cur.execute(sqlStr)
		
	# 追加自增属性
	#for x in arrDbName:
	#	sqlStr = "ALTER TABLE %s modify id INT(11) AUTO_INCREMENT;" % (x)
	##	print("invoke mysql sql:" + sqlStr)
	#	cur.execute(sqlStr)
	"""
	
	"""
	# 测试
	conn = MySQLdb.connect(host='127.0.0.1', user='root',passwd='', db='egame');
	cur = conn.cursor()
	cur.execute("ALTER TABLE player_db modify petPackageId INT(11) DEFAULT 1000;")
	cur.close()
	conn.close()
	"""

	
	cur.close()
	conn.close()

	
