import os
import sys
sys.path.append(os.environ["AIRFLOW_HOME"] + '/../airflow/dags/airflow_dag/')

try:
    from mongodb import MongoManager
except ImportError:
    from stock_crawl.mongo.mongodb import MongoManager


import pandas as pd
import json

class CrawlCompanyInfor:
    mongoclient = None
    _companyinforrename_= {'회사명': 'company', '종목코드': 'code','업종':'business','주요제품':'main'
        ,'상장일':'startdate' ,'결산월':'statemonth','대표자명':'owner','홈페이지':'homepage','지역':'loc'}


    def __init__(self):
        if self.mongoclient == None:
            self.mongoclient = MongoManager.getInstance().stock_kor

    def __del__(self):
        MongoManager.getInstance().close()


    def getCompanyInfor(self):
        stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
        stock_code = stock_code.rename(columns= self._companyinforrename_)
        stock_code ['_id'] = stock_code['code']
        # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
        # stock_code.code = stock_code.code.map('{:06d}'.format)
        return stock_code

    def insertCompanyInfor(self):
        stock_code = self.getCompanyInfor()
        ids = json.loads(stock_code['_id'].T.to_json()).values()
        records = json.loads(stock_code.T.to_json()).values()
        for x in records:
            x['alive']=True

        idList = [x['_id'] for x in records]

        notInlist = list(self.mongoclient.companyinfor.find({"_id":{ "$nin":idList}}))
        print("not in id list",notInlist)

        from collections import defaultdict
        deListing = defaultdict(list)
        #todo : need to check when delisting happen
        for x in notInlist:
            tempValue=self.mongoclient.companyinfor.update({"_id":x["_id"]},{"alive":False},upsert=True)
            for k, v in tempValue.items():
                deListing[k].append(v)

        print("deListing",deListing)

        returnDic = defaultdict(list)
        for x in records:
            tempValue=self.mongoclient.companyinfor.update({"_id":x["_id"]},x,upsert=True)
            for k, v in tempValue.items():
                returnDic[k].append(v)

        print(returnDic)

        returnValue = {}
        from functools import reduce
        import numbers

        for x in returnDic.keys():
            if(isinstance(returnDic[x][0], numbers.Number)):
                returnValue[x]= reduce(lambda x,y: x + y,returnDic[x],0)
            elif type(x) == type(True) :
                returnValue[x] = len(returnDic[x])
            else:
                returnValue[x] = returnDic[x]

        return (returnValue)





    def getCompanySize(self):
        return self.mongoclient.companyinfor.count()

    def getCompanyCode(self):
        return [x['code'] for x in self.mongoclient.companyinfor.find({},{"_id": 0,"code":1})]

