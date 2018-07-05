# -*- coding: utf-8 -*- 
 
import os
import re
import hashlib
from tkinter import filedialog


# 获取路径下所有的文件及路径，返回数据字典
def getfile(file_dir): 
	# 新建空字典
	file_dict = {} 
	for root, dirs, files in os.walk(file_dir):
		for file in files:
			# 如果文件的扩展名为'.png'，将文件及其路径加入字典
			# if os.path.splitext(file)[1] == '.png':
			file_dict[file] = os.path.join(root, file)
	return file_dict

# 获取一个文件的MD5
def getmd5(file_name):
	f = open(file_name, 'rb')
	m = hashlib.md5()
	m.update(f.read())
	fmd5 = m.hexdigest()
	print('文件：%s\nMD5：%s' % (file_name, fmd5))
	return fmd5

# 新建CSV文件，将列表数据写入
def csv_writer(data_list):
	# 在脚本所在的目录生成对比结果的CSV文档
	with open('对比结果.csv', 'w', encoding='utf-8') as f:
		f.write(u'\ufeff')# 使用utf-8-bom编码，解决Excel打开csv中文乱码问题
		f.write('filename,dir1,dir2\n')
		for i in data_list:
			f.write(i+'\n')

# 比较两个路径中相同文件的MD5并统计
def compare(dir1, dir2):
	fd1 = getfile(dir1)
	fd2 = getfile(dir2)
	# 字典的key列表转集合取交集，再转为列表
	same = list(set(fd1.keys())&set(fd2.keys()))
	total_count = 0
	same_count = 0
	# 遍历列表中的key(文件名)，比较MD5
	row_list = []
	for i in same:
		f1_md5 = getmd5(fd1[i])
		f2_md5 = getmd5(fd2[i])
		total_count += 1
		if f1_md5 == f2_md5:
			same_count += 1
			row = '%s,%s,%s' % (i, fd1[i], fd2[i])
			row_list.append(row)
	csv_writer(row_list)
	same_percent = same_count/total_count
	print('共比对%s个文件，MD5相同文件%s个，占比%s%%' % (total_count, same_count, round(same_percent*100, 2)))

# 主函数
def main():
	# 选择文件夹的初始路径
	# initialdir = ''
	# askdirectory()中可以传入initialdir设置文件夹选择器的初始路径
	dir1 = filedialog.askdirectory()# 选择路径1
	dir2 = filedialog.askdirectory()# 选择路径2
	compare(dir1, dir2)# 调用compare()比对所有同名文件的MD5


# 脚本被直接打开而非import时，运行main()
if __name__ == '__main__':
	main()