import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from  selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.Utils import ForumDriver
from autotest import ForumLogin
class ForumPostAdd:
    url=""
    driver=""
    post_title=""
    post_content=""
    arr_section = \
        ["首页", "Java", "C++", "前端技术", "MySQL", "面试宝典", "经验分享", "招聘信息", "福利待遇","灌水区"]
    def __init__(self):
        self.url="http://127.0.0.1:58080/sign-in.html"
        self.driver=ForumDriver.driver
        self.driver.get(self.url)

    # 0--首页，1--Java，2--C++，3--前端技术，4--MySQL，5--面试宝典，
    # 6--经验分享，7--招聘信息，8--福利待遇，9--灌水区
    #成功发布测试
    def AddSuccTest(self):
        #登陆后进入发布帖子页
        elem_login = ForumLogin.FormLogin()
        elem_login.RightName_RightPass()
        elem_login.ClickLogin()
        #输入测试
        for section_id in range(1,10):
            self.__addFunctionTest(section_id)
    #发布失败测试
    def AddFailTest(self):
        # 登陆后进入发布帖子页
        elem_login = ForumLogin.FormLogin()
        elem_login.RightName_RightPass()
        elem_login.ClickLogin()
        #输入测试
        self.__addPostFailTest()

    #点击"发布帖子"按钮入口，进入发布页，前提处于首页或者某个板块页下
    def __clickAddPost(self):
        elem_but=WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#bit-forum-content > div.page-header.d-print-none > div > div > div.col-auto.ms-auto.d-print-none > div > a.btn.btn-primary.d-none.d-sm-inline-block.article_post"))
        )
        elem_but.click()
    #点击提交按钮，进行帖子提交
    def __clickSubmit(self):
        #滑动到提交的区域
        elem_submit_but=self.driver.find_element(By.CSS_SELECTOR, "#article_post_submit")
        ActionChains(self.driver).move_to_element(elem_submit_but).perform()
        #等待到当前页面没有弹窗出现
        WebDriverWait(self.driver,10).until(
            lambda driver: all(
                not elem.is_displayed()
                for elem in driver.find_elements(By.CSS_SELECTOR, "body > div.jq-toast-wrap.bottom-right > div")
            )
        )
        elem_submit_but.click()

    # 0--首页，1--Java，2--C++，3--前端技术，4--MySQL，5--面试宝典，
    # 6--经验分享，7--招聘信息，8--福利待遇，9--灌水区
    #成功发布功能测试
    def __addFunctionTest(self,section_id):
        # 点击发布帖子按钮
        self.__clickAddPost()
        #选择板块
        self.__selectSection(section_id)
        #输入标题
        testtitle=self.__inputTitle(section_id)
        #输入编辑区
        testcontent=self.__inputContent(section_id)
        #截图
        ForumDriver.SavePicture()
        #点击提交按钮
        self.__clickSubmit()
        #右下角弹窗测试
        self.__alertEqualText("发帖成功")
        #检验是否成功发布
        self.__check_add_success(testtitle,testcontent,section_id)
        #成功修改后更新当前标题和内容
        self.setPostTitle(testtitle)
        self.setPostContent(testcontent)
    #发帖区选择板块
    def __selectSection(self,section_id=1):
        #添加等待,先定位到所有板块
        elm_section=WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#article_post_borad"))
        )
        ActionChains(self.driver).move_to_element(elm_section).perform()
        # 创建Select对象,from selenium.webdriver.support.ui import Select
        select_obj = Select(elm_section)
        # 通过value属性直接选择 value=section_id  (string) 的元素
        section_id=str(section_id)
        select_obj.select_by_value(section_id)
    #输入标题
    def __inputTitle(self,section_id=1):
        testtitle = datetime.datetime.now().strftime(f"{self.arr_section[section_id]}:addpost_Title:%Y%m%d-%H%M%S")
        elem_title=self.driver.find_element(By.CSS_SELECTOR, "#article_post_title")
        ActionChains(self.driver).move_to_element(elem_title).perform()
        elem_title.send_keys(f"{testtitle}")
        return testtitle
    #输入内容
    def __inputContent(self,section_id=1):
        testcontent = datetime.datetime.now().strftime(f"{self.arr_section[section_id]}:addpost_Content:%Y%m%d-%H%M%S")
        java_script = f"var elem=document.getElementById('article_post_content'); elem.value='{testcontent}'; "
        self.driver.execute_script(java_script)
        return testcontent

    #发帖失败的输入测试
    def __addPostFailTest(self):
        # 点击发布帖子按钮
        self.__clickAddPost()
        #不输入标题测试
        self.__noInputTileTest()
        #不输入内容测试
        self.__noInputContentTest()
    #不输入标题
    def __noInputTileTest(self):
        #等待页面稳定
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#article_post_title"))
        )
        #清空标题
        self.__clearTitle()
        # 输入内容
        self.__inputContent()
        # 点击提交按钮
        self.__clickSubmit()
        #弹窗测试
        self.__alertEqualText(alert_text="请输入帖子标题")
        #截图
        ForumDriver.SavePicture()
    #不输入内容
    def __noInputContentTest(self):
        # 等待页面稳定
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#article_post_title"))
        )
        # 输入标题
        self.__inputTitle()
        #清空内容
        self.__clearContent()
        # 点击提交按钮
        self.__clickSubmit()
        # 弹窗测试
        self.__alertEqualText(alert_text="请输入帖子内容")
        # 截图
        ForumDriver.SavePicture()
    #清空标题
    def __clearTitle(self):
        elem_title=WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#article_post_title"))
        )
        elem_title.clear()
    #清空内容
    def __clearContent(self):
        java_script = f"var elem=document.getElementById('article_post_content'); elem.value=''; "
        self.driver.execute_script(java_script)

    #检验出现的弹窗文本是否是alert_text
    def __alertEqualText(self,alert_text):
        #等待弹窗出现
        elem_alert = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.jq-toast-wrap.bottom-right > div"))
        )
        elem1_Text = elem_alert.text.split("\n")[2]
        assert elem1_Text == alert_text, f"实际:{elem1_Text}"
    #检验是否成功发布
    def __check_add_success(self,testtitle,testcontent,section_id):
        #进入选择的板块区
        self.__enterSection(section_id)
        #等待帖子加载,获得帖子列表
        post_list=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#artical-items-body > div > div.row"))
        )
        flag=False
        for post in post_list:
            if self.__postAddCheck(post, testtitle, testcontent):
                flag=True
                break
            # 返回当前板块
            self.__enterSection(section_id)
        assert flag #找到了
        # 返回当前板块
        self.__enterSection(section_id)
    #进入板块区，目的是检验是否成功发布
    def __enterSection(self,section_id):
        elem_section = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"#topBoardList > li:nth-child({section_id + 1}) > a"))
        )
        elem_section.click()
    #检查发布的帖子标题和内容是否对应
    def __postAddCheck(self,post,testtitle,testcontent):
        entrance=post.find_element(By.CSS_SELECTOR,"div.row > div.col > div.text-truncate > a")
        ActionChains(self.driver).move_to_element(entrance).perform()
        entrance.click()
        elem_title=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#details_article_content_title"))
        )
        elem_content=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#details_article_content > p"))
        )
        if elem_title.text!=testtitle or elem_content.text!=testcontent:
            return False
        else:
            return True


    #get和set函数
    def getPostTitle(self):
        return self.post_title
    def getPostContent(self):
        return self.post_content
    def setPostTitle(self,post_title):
        self.post_title=post_title
    def setPostContent(self,post_content):
        self.post_content=post_content