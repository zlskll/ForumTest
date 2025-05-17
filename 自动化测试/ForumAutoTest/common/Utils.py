import datetime
import os
import sys

from selenium import webdriver  #webdriver
from selenium.webdriver.chrome.service import Service  #service
from webdriver_manager.chrome import ChromeDriverManager   #ChoremeDriverManager

#创建浏览器驱动driver
class Driver:
    driver=""
    def __init__(self):
        options=webdriver.ChromeOptions()
        self.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()) ,options=options)

    def SavePicture(self):
        #文件夹路径
        filedir="../images/"+datetime.datetime.now().strftime("%Y-%m-%d")
        #不存在则创建文件夹路径
        if not os.path.exists(filedir):
             os.mkdir(filedir)
        # 当前调用者的名字
        callername = sys._getframe(1).f_code.co_name
        callername_last = sys._getframe(2).f_code.co_name
        # 文件本体名字
        filename = callername_last+"-"+callername+"-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
        self.driver.save_screenshot(filedir+"/"+filename)


#创建唯一实例
ForumDriver=Driver()