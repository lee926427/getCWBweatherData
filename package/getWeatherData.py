import requests
import os
import datetime
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
class CwbOpenData():
    def __init__(self,auth):
        self.__url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization={}&downloadType=WEB&format=JSON".format(auth)
        self.__dbPath = os.getcwd()
        self.__year = datetime.date.today().year
        self.__month = datetime.date.today().month
        self.__date = datetime.date.today().day
        self.__savePath = "{}/db/{}".format(self.__dbPath,self.__year)
        self.saveFilePath = "{}/{}.xlsx".format(self.__savePath,self.__month)
        if self.__isExisting():
            self.__excel=pd.read_excel("{}/{}.xlsx".format(self.__savePath,self.__month),sheet_name="{}".format(self.__date))
            self.__fileTime = self.__excel["time.obsTime"][len(self.__excel)-1]
        
    def isConnectedCWB(self):
        self.__res = requests.get(self.__url)
        if self.__res.status_code == requests.codes.ok:
            print(self.__res.status_code)
            return True
        else:
            print("Error code:{}".formate(self.__res.status_code))
            return False
    def __isExisting(self):
        if os.path.isfile(self.saveFilePath):
            return True
        else:
            return False

    def build(self):
        print("Building the file!")
        payload = self.__res.json()
        df = DataFrame(json_normalize(payload["cwbopendata"]["location"]))
        del df["lat"]
        del df["lon"]
        excel=pd.ExcelWriter("{}/{}.xlsx".format(self.__savePath,self.__month),engine="xlsxwriter")
        df.to_excel(excel,sheet_name='{}'.format(self.__date),index=False,na_rep=True)
        excel.save()
        excel.close()
        print("Builded the file!")
    def __convertTime(self,time):
        #2019-09-25T16:30:00+08:00
        return datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S+08:00")
    def getCwbUpdateTime(self):
        res = requests.get(self.__url)
        payload = res.json()
        df = DataFrame(json_normalize(payload["cwbopendata"]["location"]))
        return self.__convertTime(df["time.obsTime"][len(df)-1])
    def getDBUpdateTime(self):
        excel=pd.read_excel("{}/{}.xlsx".format(self.__savePath,self.__month),sheet_name="{}".format(self.__date))
        fileTime = excel["time.obsTime"][len(excel)-1]

        return self.__convertTime(fileTime)
    def update(self):
        if self.__isExisting():
            self.__payload = self.__res.json()
            self.__df = DataFrame(json_normalize(self.__payload["cwbopendata"]["location"]))
            del self.__df["lat"]
            del self.__df["lon"]
            newData = self.__excel.append(self.__df)
            self.__newExcel=pd.ExcelWriter("{}/{}.xlsx".format(self.__savePath,self.__month),engine="xlsxwriter")
            newData.to_excel(self.__newExcel,sheet_name='{}'.format(self.__date),index=False,na_rep="True")
            self.__newExcel.save()
            self.__newExcel.close()
                    
        else:
            self.build()
            print("The file is not existing.")


