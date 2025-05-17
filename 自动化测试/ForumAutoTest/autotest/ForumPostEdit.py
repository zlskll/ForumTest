import datetime

from selenium.webdriver import ActionChains
from  selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.Utils import ForumDriver
from autotest import ForumLogin
class ForumPostEdit:
    url=""
    driver=""
    post_title=""
    post_content=""
    selector_of_entrance=""
    def __init__(self):
        self.url="http://127.0.0.1:58080/sign-in.html"
        self.driver=ForumDriver.driver
        self.driver.get(self.url)

    def EditSuccTest(self):
        #登陆后进入编辑页
        elem_login = ForumLogin.FormLogin()
        elem_login.RightName_RightPass()
        elem_login.ClickLogin()
        #得到第一个可以编辑的帖子的标题入口的选择器
        selector_entrance=self.__getEditElementSelector()
        if not selector_entrance:
            return
        else:
            # 把入口的选择器保存下来，方便子函数使用
            self.setEntrance(selector_entrance)
            #进入帖子详情页
            self.driver.find_element(By.CSS_SELECTOR,self.getEntrance()).click()
            #把帖子标题和帖子内容记录上,保存最新的标题和内容
            self.setPostTitle(
                WebDriverWait(self.driver,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,"#details_article_content_title"))
                )
                .text)
            self.setPostContent(
                WebDriverWait(self.driver,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,"#details_article_content > p"))
                )
                .text)
            #点击编辑按钮,进入编辑页
            self.driver.find_element(By.CSS_SELECTOR,"#details_artile_edit").click()
            #页面元素检查
            self.__check_elementExist()
            #编辑功能测试
            self.__edit_function_test()

    # 页面元素检查
    def __check_elementExist(self):
        #添加等待
        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#edit_article_submit"))
        )
        #检查原标题是否正确
        self.__check_oldTitle()
        #检查原内容是否正确
        self.__check_oldContent()
        # 检查提交按钮
        self.driver.find_element(By.CSS_SELECTOR, "#edit_article_submit")
        # 截图
        ForumDriver.SavePicture()

    # 检查原标题是否正确
    def __check_oldTitle(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#edit_article_submit"))
        )
        #得到显示的标题
        elem_input_title = self.driver.find_element(By.CSS_SELECTOR, "#edit_article_title")
        elem_title_text = elem_input_title.get_attribute("value")
        assert elem_title_text == self.getPostTitle()
    #检查原内容是否正确
    def __check_oldContent(self):
        #导入javascript代码
        java_script = "var elem=document.getElementById('edit_article_content');  return elem.value;"
        elem_input_content = self.driver.execute_script(java_script)
        assert elem_input_content == self.getPostContent()


    #编辑功能测试
    def __edit_function_test(self):
        #输入标题
        testtitle=self.__inputTitle()
        #输入编辑区
        testcontent=self.__inputContent()
        #截图
        ForumDriver.SavePicture()
        #点击提交按钮
        elem_sumit=self.driver.find_element(By.CSS_SELECTOR,"#edit_article_submit")
        ActionChains(self.driver).move_to_element(elem_sumit).perform()
        elem_sumit.click()
        #右下角弹窗测试
        self.__modifyAlertTest()

        #检验是否成功修改
        self.__check_modify_success(testtitle,testcontent)
        #成功修改后更新当前标题和内容
        self.setPostTitle(testtitle)
        self.setPostContent(testcontent)

    #输入标题
    def __inputTitle(self):
        testtitle = datetime.datetime.now().strftime("modify_Title:%Y%m%d-%H%M%S")
        #send_keys之前先清空
        elem_input_title=self.driver.find_element(By.CSS_SELECTOR, "#edit_article_title")
        elem_input_title.clear()
        elem_input_title.send_keys(f"{testtitle}")
        return testtitle

    #输入内容
    def __inputContent(self):
        testcontent = datetime.datetime.now().strftime("modify_Content:%Y%m%d-%H%M%S")
        java_script = f"var elem=document.getElementById('edit_article_content'); elem.value='{testcontent}'; "
        self.driver.execute_script(java_script)
        return testcontent
    #修改成功的弹窗测试
    def __modifyAlertTest(self):
        #等待包含“修改成功”的弹窗弹出
        elem_alert = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[contains(text(),'修改成功')]"))
        )
        alert_text = elem_alert.text
        assert alert_text.split("\n")[2] == "修改成功", f"实际:{alert_text}"


    #检验是否成功修改
    def __check_modify_success(self,testtitle,testcontent):
        # 首先保证现在页面处于 首页
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#artical-items-body"))
        )
        assert self.driver.find_element(By.CSS_SELECTOR,"#article_list_board_title").text=="首页"
        #直接用入口(修改的那个帖子的标题，点击即可进入帖子详情)
        entrance_selector=self.getEntrance()
        self.driver.find_element(By.CSS_SELECTOR,entrance_selector).click()
        elem_new_title=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#details_article_content_title"))
        )
        assert elem_new_title.text==testtitle,f"预期结果:{testtitle},实际结果：:{elem_new_title.text}"
        elem_new_content=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#details_article_content > p"))
        )
        assert elem_new_content.text==testcontent,f"预期结果:{testcontent},实际结果:{elem_new_content.text}"
        #返回首页
        self.driver.find_element(By.CSS_SELECTOR,"#nav_board_index > a").click()



    #得到首页可以编辑的第一个帖子元素的选择器selector
    def __getEditElementSelector(self):
        index = 1
        #选择器初始化
        selector_of_post = "#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a"
        #等待
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,selector_of_post))
        )
        #得到首页可以编辑的第一个帖子元素
        while self.driver.find_elements(By.CSS_SELECTOR,selector_of_post):
            elem_post_title=self.driver.find_element(By.CSS_SELECTOR,selector_of_post)
            ActionChains(self.driver).move_to_element(elem_post_title).perform()
            elem_post_title.click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,"#bit-forum-content > div.page-body > div > div > div:nth-child(1) > div.col-9.card.card-lg > div.card-footer.bg-transparent.mt-auto.justify-content-end > div > div:nth-child(1)"))
            )
            #判断编辑按钮是否存在
            elem_edit=self.driver.find_elements(By.CSS_SELECTOR,"#bit-forum-content > div.page-body > div > div > div:nth-child(1) > div.col-9.card.card-lg > div.card-footer.bg-transparent.mt-auto.justify-content-end > div > div:nth-child(2)")
            if not elem_edit or not elem_edit[0].is_displayed():
                index+=1
                selector_of_post=f"#artical-items-body > div:nth-child({index}) > div > div.col > div.text-truncate > a"
                self.__ReturnHomePage()
                continue
            elif elem_edit[0].is_displayed():
                self.__ReturnHomePage()
                return selector_of_post
        return None



    #返回到首页
    def __ReturnHomePage(self):
        # 进入首页
        elem_home = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#nav_board_index > a"))
        )
        ActionChains(self.driver).move_to_element(elem_home).perform()
        elem_home.click()
        #等待页面稳定
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#artical-items-body"))
        )



    def getPostTitle(self):
        return self.post_title
    def getPostContent(self):
        return self.post_content
    def setPostTitle(self,post_title):
        self.post_title=post_title
    def setPostContent(self,post_content):
        self.post_content=post_content
    def getEntrance(self):
        return self.selector_of_entrance
    def setEntrance(self,entrance_selector):
        self.selector_of_entrance=entrance_selector



