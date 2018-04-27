#导入数据
import pymysql
import pandas as pda
import matplotlib.pylab as pyl
conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="root",db="douban")
sql="select * from doubanmovie"
data=pda.read_sql(sql,conn)
data=data.T
print(data.shape)
x1=data.values[2]
y1=data.values[3]
print(x1.max(),y1.max())
# yS=(y1-y1.mean())/y1.std()  #标准差标准化
pyl.plot(x1,y1,"o")
pyl.title("show")
pyl.xlabel("rating")
pyl.ylabel("num")
pyl.show()