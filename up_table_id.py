#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
方便合服处理
将pinus玩家的所有关联的表的id都加一定的值
"""

import MySQLdb
import re

DB_HOST = "127.0.0.1"			# 数据库ip地址
DB_USER = "root"				# 数据库用户名
DB_PWD = ""						# 数据库用户密码
DB_NAME = "egame2"				# 数据库名称
ID_UP = 20000					# id要增加的值
TABLE_PLAYER = "player_db"		# 玩家数据库名称

# 无视处理的数据库名称映射
# key => 数据库名称
# val => 暂时没有
MAP_INGNORE_DB = {"user_db":1}

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
	
	
	arrList = range(len(arrDbId))
	
	# 移除外键约束
	for x in arrForeignKey:
		sqlStr = "ALTER TABLE %s DROP FOREIGN KEY %s" % (TABLE_PLAYER, x)
		print("invoke mysql sql:" + sqlStr)
		cur.execute(sqlStr)
		
	# 修改玩家id
	sqlStr = "UPDATE %s SET id=id+%d where id < %d;" % (TABLE_PLAYER, ID_UP, ID_UP)
	cur.execute(sqlStr)
	#exeInfo = cur.fetchall()
	print("invoke mysql sql:" + sqlStr + "  result:")

	# 修改所有关联的表id
	for x in arrList:
		tmpDbName = arrDbName[x]
		tmpProName = arrDbId[x]
		if(tmpDbName in MAP_INGNORE_DB):
			continue;
			
		sqlStr = "UPDATE %s SET %s=%s+%d where %s < %d;" % (tmpDbName, tmpProName, tmpProName, ID_UP, tmpProName, ID_UP)
		print("invoke mysql sql:" + sqlStr)
		cur.execute(sqlStr)
		
	# 修改玩家关联的id
	for x in arrList:
		tmpDbName = arrDbName[x]
		tmpProName = arrForeignId[x]
		if(tmpDbName in MAP_INGNORE_DB):
			continue;
			
		sqlStr = "UPDATE %s SET %s=%s+%d where %s < %d;" % (TABLE_PLAYER, tmpProName, tmpProName, ID_UP, tmpProName, ID_UP)
		print("invoke mysql sql:" + sqlStr)
		cur.execute(sqlStr)

	# 重新追加外键
	for x in arrList:
		sqlStr = "ALTER TABLE %s ADD CONSTRAINT %s FOREIGN KEY (%s) REFERENCES %s (%s);" % (TABLE_PLAYER, arrForeignKey[x], arrForeignId[x], arrDbName[x], arrDbId[x])
		print("invoke mysql sql:" + sqlStr)
		cur.execute(sqlStr)

	conn.commit();
	cur.close()
	conn.close()

	
