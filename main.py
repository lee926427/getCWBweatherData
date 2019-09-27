import pandas as pd
import numpy as np
import datetime
import os,time,sched
from package.getWeatherData import CwbOpenData as cwb

class buildDB():
    def __init__(self):
        self.curPath = os.getcwd()
        self.nowTime = datetime.date.today()
        #print("curPath:",self.curPath)

    def checkDbPath(self):
        self.curPath += "/db"
        #print("curPath:",self.curPath)
        if not os.path.isdir(self.curPath):
            os.mkdir("db")
            os.chdir(self.curPath)
        print("db checked!")
        self.curPath += "/{}".format(str(self.nowTime.year))
        #print("curPath:",self.curPath)
        if not os.path.isdir(self.curPath):
            os.mkdir(str(self.nowTime.year))
        else:
            print("DataBase checked!")
            return True

    def getDBPath(self):
        print(self.curPath)
class getWeather():
    def __init__(self,auth):
        self.isBuilded = buildDB().checkDbPath()
        self.__auth = auth
        self.cwdData = cwb(self.__auth)
    def run(self):
        #while(True):
        if self.cwdData.isConnectedCWB():
            if os.path.isfile(self.cwdData.saveFilePath) == False:
                self.cwdData.build()
            if self.cwdData.getCwbUpdateTime() != self.cwdData.getDBUpdateTime():
                self.cwdData.update()
                print("Update the file!\nTime:{}".format(self.cwdData.getCwbUpdateTime()))
            else:
                print("The file last Updated Time:{}".format(self.cwdData.getDBUpdateTime()))
        else:
            print("please check internet for CWB with api.")
            #time.sleep(60*60)

if __name__ == "__main__":
    auth = "CWB-8EE6A92A-B903-4AC3-ADF5-465DFF5987F2"
    main = getWeather(auth)
    if main.isBuilded:
        main.run()
            