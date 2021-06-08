#bilibili github
from pandasql import sqldf
import pandas as pd
import tushare as ts
import requests
import time,datetime

## 替换2.1: 数据直接插入到MySQL
## from sqlalchemy import create_engine
## yconnect = create_engine('mysql+pymysql://root:password@ip:3306/database?charset=utf8mb4')
## 替换2.1: 

## 替换1: 这是从tushare下载A股代码，可以替换成自己的跟踪代码
pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data=sqldf('select distinct (lower(substr(ts_code,8,2)) || substr(ts_code,1,6))  api_tick from data')['api_tick']
## data=['sz399001','sz399006','sh000001']
## 替换1: 

sina_api='http://hq.sinajs.cn/?format=json&list={0}'
update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("start:",datetime.datetime.now())
for tick in data:
    current={   'name':[],'tick':[],'trade_date':[],'Open':[],'High':[],'Low':[],'pre_close':[],'Volume':[],'Amt':[], 'date':[] ,'upd':[]   }    
#            content=requests.get('http://hq.sinajs.cn/?format=json&list=sh688005').text
    content=requests.get(sina_api.format(tick)).text

    list = content.split(',')
    if float(list[3]) !=0:
        current['name']=list[0][list[0].find("=")+1:30]
        current['tick']=tick
        current['Open']=list[1]
        current['pre_close']=list[2] #上一日收盘价
        current['Close'] =list[3]
        current['High']=list[4]
        current['Low']=list[5]
        current['trade_date']=list[30].replace("-","")
        current['Volume']=float(list[8])/100
        current['Amt']=float(list[9])/10000
        current['date']=list[30]+" "+list[31]
        current['pct_chg']=round(((float(list[3])-float(list[2]))/float(list[2]))*100,2)
        current['upd']=update

## 替换2.2 数据直接插入到MySQL,如直接插入MySQL 以下这段替换 ##   
    
        if tick == data[0]:  
            p_update=pd.DataFrame(current,index=[0])
        else:
            p_update=p_update.append(pd.DataFrame(current,index=[0]))
print("finish:",datetime.datetime.now(),"   len:",len(p_update))
## pd.io.sql.to_sql(p_update.reset_index(drop=True), "In_Day", yconnect, if_exists='append', chunksize=10000)
## 替换2.2 数据直接插入到MySQL,如直接插入MySQL 以上这段替换 ##        
## MySQL的设定请参考评论区 
