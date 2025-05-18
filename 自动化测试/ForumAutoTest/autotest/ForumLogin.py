from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from common.Utils import  ForumDriver

class FormLogin:
    url=""
    driver=""
    def __init__(self):
        self.url="http://127.0.0.1:58080/sign-in.html"
        self.driver=ForumDriver.driver
        self.driver.get(self.url)
    #正常登陆
    def LoginSuccess(self):
        #页面元素检查
        self.__check_element_exist()
        #显示密码功能测试
        self.__display_password()
        #输入正确的用户名和密码并点击
        self.RightName_RightPass()
        #如果当前页面不是登陆页面，就返回一下页面，复原
        if self.driver.current_url!=self.url:
            self.driver.back()
    #异常登陆
    def LoginFail(self):
        # 页面元素检查
        self.__check_element_exist()
        #测试
        self.WrongName_RightPass()
        self.RightName_WrongPass()
        self.WrongName_WrongPass()
        self.Having_Null()

    #登陆页面元素检查
    def __check_element_exist(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#password"))
        )
        self.driver.find_element(By.CSS_SELECTOR, "#username") #用户名
        self.driver.find_element(By.CSS_SELECTOR, "#password") #密码
        self.driver.find_element(By.CSS_SELECTOR, "#submit") #提交按钮
        self.driver.find_element(By.CSS_SELECTOR, "#signInForm > div.mb-2 > div > span")  #显示密码功能按钮
        self.driver.find_element(By.CSS_SELECTOR,"body > div > div > div > div:nth-child(1) > div > div.text-center.text-muted.mt-3 > a")  #注册入口
        # 截图
        ForumDriver.SavePicture()

    #显示密码功能测试：点击显示密码按钮
    def __display_password(self):
        elem_button=self.driver.find_element(By.CSS_SELECTOR, "#signInForm > div.mb-2 > div > span")  # 显示密码功能按钮

        elem_textbox=self.driver.find_element(By.CSS_SELECTOR, "#password")
        elem_textbox.clear()
        elem_textbox.send_keys("testdisplay")

        assert elem_textbox.get_attribute("type")=="password"
        elem_button.click()
        assert elem_textbox.get_attribute("type") == "text"
        elem_button.click()
        assert elem_textbox.get_attribute("type") == "password"
        # 截图
        ForumDriver.SavePicture()

    #用于作显式等待的参数，在规定的等待时间内反复点击显示密码按钮，一旦显示成功即停止等待
    def __wait_password_display(self,driver):
        driver.find_element(By.CSS_SELECTOR,"#signInForm > div.mb-2 > div > span").click()
        if driver.find_element(By.CSS_SELECTOR,"#password").get_attribute("type")=="text":
            return True
        else:
            return False

    #输入用户名和密码，点击显示密码(方便截图)，返回
    def InputNamePass(self,username,password):
        #首先清楚输入框
        self.driver.find_element(By.CSS_SELECTOR, "#username").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#password").clear()
        #输入
        if username!="":
            self.driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
        if password!="":
            self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        #显示密码，方便截图
        elembox=self.driver.find_element(By.CSS_SELECTOR, "#password")
        WebDriverWait(self.driver,10).until(
            lambda driver: elembox.get_attribute("type") in ["password", "text"]
        )
        if  elembox.get_attribute("type") =="password":
            # WebDriverWait(self.driver,10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR,"#signInForm > div.mb-2 > div > span"))
            # )
            #在20秒内反复点击密码显示按钮，一旦变为“text”就停止点击和等待，超时会报错
            WebDriverWait(self.driver, 20).until(
                self.__wait_password_display
            )
    #点击登陆页面的提交按钮
    def ClickLogin(self):
        elem_submit=WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit"))
        )
        elem_submit.click()

    #退出账号
    def ExitAccount(self):
        #点击头像
        elem_img=WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div.nav-item.dropdown > a"))
        )
        ActionChains(self.driver).move_to_element(elem_img).perform()
        elem_img.click()
        #点击退出
        elem_exit=WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"#index_user_logout") )
        )
        elem_exit.click()
        #检验是否回到登陆界面
        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#submit"))
        )

    #登陆成功后，检查用户昵称是否是“lyntester007”
    def CheckNickName(self,nickname):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_nav_avatar"))
        )
        elem.click()
        self.driver.find_element(By.CSS_SELECTOR, "#index_user_settings").click()
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#settings_nickname"))
        )
        assert elem.text == nickname

    #输入正确的用户名和正确的密码
    def RightName_RightPass(self):
        # "lyn"  "lyn12345"
        self.InputNamePass("lyn","lyn12345")
        self.ClickLogin()
        #点到个人中心，看看是不是正确的用户
        self.CheckNickName("lyntester007")
        #到此，是正确的用户，测试完要进行还原，返回登陆页面
        self.driver.back()

        #"LYN"  "lyn12345"
        self.InputNamePass("LYN","lyn12345")
        self.ClickLogin()
        self.CheckNickName("lyntester007")
        #到此，是正确的用户，测试完要进行还原，返回登陆页面
        self.driver.back()
        # 截图
        ForumDriver.SavePicture()
    #输入错误的用户名和正确的密码
    def WrongName_RightPass(self):

        self.InputNamePass("ly","lyn12345")
        self.ClickLogin()
        #测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()

        self.InputNamePass("lyb", "lyn12345")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()

        self.InputNamePass("lyn6", "lyn12345")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()
        # 截图
        ForumDriver.SavePicture()
    #输入正确的用户名和错误的密码
    def RightName_WrongPass(self):
        self.InputNamePass("lyn", "lyn1234")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()

        self.InputNamePass("lyn", "lyn12346")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()

        self.InputNamePass("lyn", "lyn123456")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()
        # 截图
        ForumDriver.SavePicture()
    #输入错误的用户名和错误的密码
    def WrongName_WrongPass(self):
        self.InputNamePass("ly", "lyn1234567")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()

        self.InputNamePass("lyc", "lyn123450")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()

        self.InputNamePass("LYN666", "lyn1234")
        self.ClickLogin()
        # 测试弹窗是否弹出且文本正确
        self.__LoginWarningTest()
        # 截图
        ForumDriver.SavePicture()
    #输入空项
    def Having_Null(self):
        self.InputNamePass("lyn", "")
        self.ClickLogin()
        # 等待提示信息出现
        self.__LoginTipNull("lyn","")

        self.InputNamePass("", "lyn12345")
        self.ClickLogin()
        # 等待提示信息出现
        self.__LoginTipNull("","lyn12345")

        self.InputNamePass("", "")
        self.ClickLogin()
        # 等待提示信息出现
        self.__LoginTipNull("","")
        # 截图
        ForumDriver.SavePicture()

    #登陆失败后的弹窗测试，包括弹窗是否出现，出现后文案是否是“用户名或密码错误”
    def __LoginWarningTest(self):
        elemlist = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "body > div.jq-toast-wrap.bottom-right > div"))
        )
        elem1_Text = elemlist[len(elemlist) - 1].text.split("\n")[2]
        assert elem1_Text == "用户名或密码错误"
    #有输入空项时的测试，输入框下会有提示“用户名不能为空”“密码不能为空”
    def __LoginTipNull(self,username,password):
        if username=="":
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#signInForm > div.mb-3 > div"))
            )
            assert elem.text == "用户名不能为空",f"实际：{elem.text}"
        if password=="":
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#signInForm > div.mb-2 > div > div"))
            )
            assert elem.text == "密码不能为空",f"实际：{elem.text}"

