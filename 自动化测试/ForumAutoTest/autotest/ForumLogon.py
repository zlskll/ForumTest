from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.Utils import ForumDriver
from autotest import ForumLogin
#尝试登陆，用"lyn333","lyn345678"登陆，验证昵称是不是lyn333
def Trylogin():
    elemlogin=ForumLogin.FormLogin()
    elemlogin.InputNamePass("lyn333", "lyn345678")
    elemlogin.ClickLogin()
    elemlogin.CheckNickName("lyn333")
class ForumLogon:
    url=""
    driver=""
    def __init__(self):
        self.url="http://127.0.0.1:58080/sign-up.html"
        self.driver=ForumDriver.driver
        self.driver.get(self.url)
    #正常注册
    def LogonSuccess(self):
        #页面元素检查
        self.__check_element_exist()
        # 显示密码功能测试
        self.__display_passwordTest()
        #输入一串正确的
        self.__AllRightTest()
        # 返回原先页面，复原
        self.driver.back()
    #异常注册
    def LogonFail(self):
        # 页面元素检查
        self.__check_element_exist()
        # 显示密码功能测试
        self.__display_passwordTest()
        #输入错误登录的测试用例1
        self.__WrongTest_1()
        self.__WrongTest_2()
        self.__WrongTest_3()
        self.__WrongTest_4()
        self.__WrongTest_5()
        self.__WrongTest_6()
        self.__WrongTest_7()

    #页面元素检查
    def __check_element_exist(self):
        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#passwordRepeat"))
        )
        self.driver.find_element(By.CSS_SELECTOR,"#username")#用户名
        self.driver.find_element(By.CSS_SELECTOR, "#nickname")#昵称
        self.driver.find_element(By.CSS_SELECTOR, "#password")#密码
        self.driver.find_element(By.CSS_SELECTOR, "#passwordRepeat")#确认密码
        self.driver.find_element(By.CSS_SELECTOR, "#policy")#同意条款打勾框
        self.driver.find_element(By.CSS_SELECTOR, "#submit")#提交
        self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/a")  #登陆入口
        # 截图
        ForumDriver.SavePicture()
    #显示密码测试
    def __display_passwordTest(self):
        elem_button=self.driver.find_element(By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(4) > div > span")  # 显示密码功能按钮
        elem_button_repeat=self.driver.find_element(By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > span")  # 显示密码功能按钮
        elem_textbox=self.driver.find_element(By.CSS_SELECTOR, "#password")
        elem_textbox_repeat = self.driver.find_element(By.CSS_SELECTOR, "#passwordRepeat")
        elem_textbox.clear()
        elem_textbox_repeat.clear()
        #输入测试密码
        elem_textbox.send_keys("testdisplay")
        elem_textbox_repeat.send_keys("test_repeat")
        assert elem_textbox.get_attribute("type")=="password"
        assert elem_textbox_repeat.get_attribute("type") == "password"
        WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable(elem_button)
        )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(elem_button_repeat)
        )
        #点击显示密码按钮
        while elem_textbox.get_attribute("type") == "password":
            elem_button.click()
        while elem_textbox_repeat.get_attribute("type") == "password":
            elem_button_repeat.click()
        assert elem_textbox.get_attribute("type") == "text",f"实际: {elem_textbox.get_attribute('type')}"
        assert elem_textbox_repeat.get_attribute("type") == "text"
        #点击隐藏密码
        while elem_textbox.get_attribute("type") == "text":
            elem_button.click()
        while elem_textbox_repeat.get_attribute("type") == "text":
            elem_button_repeat.click()
        assert elem_textbox.get_attribute("type") == "password"
        assert elem_textbox_repeat.get_attribute("type") == "password"
        # 截图
        ForumDriver.SavePicture()

    #输入注册的各项信息,返回注册的昵称
    def __InputLogon(self,username,nickname,password,passrepeat,agreebutt):
        # 首先清除输入框
        self.driver.find_element(By.CSS_SELECTOR, "#username").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#nickname").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#password").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#passwordRepeat").clear()
        #同意条款框清空
        elem_check=self.driver.find_element(By.CSS_SELECTOR, "#policy")
        if elem_check.is_selected():
            elem_check.click()

        #输入
        if username!="":
            self.driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
        if nickname!="":
            self.driver.find_element(By.CSS_SELECTOR, "#nickname").send_keys(nickname)
        if password!="":
            self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        if passrepeat!="":
            self.driver.find_element(By.CSS_SELECTOR, "#passwordRepeat").send_keys(passrepeat)
        if agreebutt != 0:  #需要勾选
            checkbox=self.driver.find_element(By.ID,"policy")
            while not checkbox.is_selected():
                checkbox.click()
        # 显示密码，方便截图
        self.__DisplayPassword()
        self.__DisplayRepeatPass()
        return nickname

    # 所有信息都正确，注册后去尝试登陆
    def __AllRightTest(self):
        self.__InputLogon("lyn333", "lyn333", "lyn345678", "lyn345678", 1)
        self.__Submit()
        # 尝试登陆
        Trylogin()
        self.driver.back()  # 尝试登陆后返回登陆页面
        # 到此，是正确的用户，测试完要进行还原，返回注册页面
        self.driver.back()
        # 截图
        ForumDriver.SavePicture()

    #输入用户名、昵称、密码、确认密码，勾选同意条款，确认密码和密码不同
    def __WrongTest_1(self):
        self.__InputLogon("lyn444", "lyn444", "lyn45678", "lyn56789", 1)
        self.__Submit()
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > div"))
        )
        assert elem.text == "请检查确认密码"
        # 截图
        ForumDriver.SavePicture()
    #输入用户名，不输入昵称、密码、确认密码，不勾选同意条款
    def __WrongTest_2(self):
        self.__InputLogon("lyn444", "", "", "", 0)
        self.__Submit()
        elem_1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > div"))
        )
        assert elem_1.text == "请检查确认密码",f"实际: {elem_1.text}"
        elem_2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(3) > div"))
        )
        assert elem_2.text == "昵称不能为空",f"实际: {elem_2.text}"
        elem_3 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(4) > div > div"))
        )
        assert elem_3.text == "密码不能为空",f"实际: {elem_3.text}"
        # 截图
        ForumDriver.SavePicture()
    # 输入昵称、确认密码，不输入用户名、密码，不勾选同意条款
    def __WrongTest_3(self):
        self.__InputLogon("", "lyn444", "", "lyn45678", 0)
        self.__Submit()
        elem_1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > div"))
        )
        assert elem_1.text == "请检查确认密码", f"实际: {elem_1.text}"
        elem_2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(2) > div"))
        )
        assert elem_2.text == "用户名不能为空", f"实际: {elem_2.text}"
        elem_3 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(4) > div > div"))
        )
        assert elem_3.text == "密码不能为空", f"实际: {elem_3.text}"
        # 截图
        ForumDriver.SavePicture()
    #输入密码，不输入用户名、昵称、确认密码，勾选同意条款
    def __WrongTest_4(self):
        self.__InputLogon("", "", "lyn45678", "", 1)
        self.__Submit()
        elem_1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > div"))
        )
        assert elem_1.text == "请检查确认密码", f"实际: {elem_1.text}"
        elem_2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(2) > div"))
        )
        assert elem_2.text == "用户名不能为空", f"实际: {elem_2.text}"
        elem_3 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(3) > div"))
        )
        assert elem_3.text == "昵称不能为空", f"实际: {elem_3.text}"
        # 截图
        ForumDriver.SavePicture()
    #输入用户名、昵称、密码，不输入确认密码，不勾选同意条款
    def __WrongTest_5(self):
        self.__InputLogon("lyn444", "lyn444", "lyn45678", "", 0)
        self.__Submit()
        elem_1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > div"))
        )
        assert elem_1.text == "请检查确认密码", f"实际: {elem_1.text}"
        # 截图
        ForumDriver.SavePicture()
    #输入确认密码，不输入用户名、昵称、密码，勾选同意条款
    def __WrongTest_6(self):
        self.__InputLogon("", "", "", "lyn45678", 1)
        self.__Submit()
        elem_1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > div"))
        )
        assert elem_1.text == "请检查确认密码", f"实际: {elem_1.text}"
        elem_2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(2) > div"))
        )
        assert elem_2.text == "用户名不能为空", f"实际: {elem_2.text}"
        elem_3 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(3) > div"))
        )
        assert elem_3.text == "昵称不能为空", f"实际: {elem_3.text}"
        elem_4 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(4) > div > div"))
        )
        assert elem_4.text == "密码不能为空", f"实际: {elem_4.text}"
        # 截图
        ForumDriver.SavePicture()
    #输入已注册过的用户名
    def __WrongTest_7(self):
        self.__InputLogon("lyn", "lyn444", "lyn45678", "lyn45678", 1)
        self.__Submit()
        elemalert=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div.jq-toast-wrap.bottom-right > div") )
        )
        alert_text=elemalert.text.split("\n")[2]
        assert  alert_text=="用户已存在"
        #截图
        ForumDriver.SavePicture()

    #点击显示密码按钮使密码显示出来，方便截图查看
    def __DisplayPassword(self):
        elembox = self.driver.find_element(By.CSS_SELECTOR, "#password")
        WebDriverWait(self.driver, 10).until(
            lambda driver: elembox.get_attribute("type") in ["password", "text"]
        )
        if elembox.get_attribute("type") == "password":
            # 在20秒内反复点击密码显示按钮，一旦变为“text”就停止点击和等待，超时会报错
            WebDriverWait(self.driver, 20).until(
                self.__wait_password_display
            )
    ##点击显示确认密码按钮使确认密码显示出来，方便截图查看
    def __DisplayRepeatPass(self):
        elembox = self.driver.find_element(By.CSS_SELECTOR, "#passwordRepeat")
        WebDriverWait(self.driver, 10).until(
            lambda driver: elembox.get_attribute("type") in ["password", "text"]
        )
        if elembox.get_attribute("type") == "password":
            # 在20秒内反复点击密码显示按钮，一旦变为“text”就停止点击和等待，超时会报错
            WebDriverWait(self.driver, 20).until(
                self.__wait_repeatpass_display
            )

    #用于作显式等待的参数，在规定的等待时间内反复点击显示密码按钮，一旦显示成功即停止等待
    def __wait_password_display(self,driver):
        driver.find_element(By.CSS_SELECTOR,"#signUpForm > div > div:nth-child(4) > div > span").click()
        if driver.find_element(By.CSS_SELECTOR,"#password").get_attribute("type")=="text":
            return True
        else:
            return False
    #用于作显式等待的参数，在规定的等待时间内反复点击显示确认密码按钮，一旦显示成功即停止等待
    def __wait_repeatpass_display(self,driver):
        driver.find_element(By.CSS_SELECTOR, "#signUpForm > div > div:nth-child(5) > div > span").click()
        if driver.find_element(By.CSS_SELECTOR, "#passwordRepeat").get_attribute("type") == "text":
            return True
        else:
            return False
    #点击提交注册按钮
    def __Submit(self):
        elem_submit=WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"#submit"))
        )
        elem_submit.click()







