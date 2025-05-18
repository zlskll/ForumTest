import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autotest import ForumLogin
from common.Utils import ForumDriver

class ForumPostDetail:
    url=""
    driver=""
    def __init__(self):
        self.url="http://127.0.0.1:58080/index.html"
        self.driver=ForumDriver.driver
        self.driver.get(self.url)

    #帖子详情页测试
    def DetailTest(self):
        #首先登陆系统，选定首页第一个帖子标题，点击进入
        elem_login=ForumLogin.FormLogin()
        elem_login.RightName_RightPass()
        elem_login.ClickLogin()
        elem_title=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a"))
        )
        elem_title.click()
        #页面元素检查
        self.__check_element_exist()
        #点赞功能测试
        self.__LikePostTest()
        #跳转功能测试
        self.__JumpTest()
        #回复功能测试
        self.__replyTest()

    #页面元素检查
    def __check_element_exist(self):
        #添加等待
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#details_article_content"))
        )
        #帖子信息:帖子标题、帖子内容、发布时间、浏览量、点赞量、回复量
        self.driver.find_element(By.CSS_SELECTOR,"#details_article_title")
        self.driver.find_element(By.CSS_SELECTOR,"#details_article_content")
        self.driver.find_element(By.CSS_SELECTOR,"#details_article_createTime")
        self.driver.find_element(By.CSS_SELECTOR,"#details_article_visitCount")
        self.driver.find_element(By.CSS_SELECTOR,"#details_article_likeCount")
        self.driver.find_element(By.CSS_SELECTOR,"#details_article_replyCount")
        #作者信息:作者头像、作者名称、帖子标题、帖子内容
        self.driver.find_element(By.CSS_SELECTOR,"#article_details_author_avatar")
        elem_author_name=self.driver.find_element(By.CSS_SELECTOR,"#article_details_author_name")
        #回复区:回复者头像、名称、回复内容、回复时间
        # details_reply_area
        #先找到回复区，有回复再判断
        reply_area=self.driver.find_element(By.CSS_SELECTOR,"#details_reply_area")
        replylist=reply_area.find_elements(By.CSS_SELECTOR,"#details_reply_area > div.row")
        for reply in replylist:
            reply.find_element(By.CSS_SELECTOR, "div.row > div.col-3.card > div > span") #头像
            reply.find_element(By.CSS_SELECTOR, "div.row > div.col-3.card > div > h3 > a")#名称
            reply.find_element(By.CSS_SELECTOR, "div.row > div.col-9.card.card-lg > div.card-body > [class='markdown-body editormd-html-preview']")#回复内容
            reply.find_element(By.CSS_SELECTOR,"div.row > div.col-9.card.card-lg > div.card-footer.bg-transparent.mt-auto > div > div > ul > li") #回复时间
        #回复编辑区
        self.driver.find_element(By.CSS_SELECTOR,"#article_details_reply")
        self.driver.find_element(By.CSS_SELECTOR, "#details_btn_article_reply")
        #显示点赞按钮,如果作者是当前用户的话再显示编辑、删除按钮
        self.driver.find_element(By.CSS_SELECTOR,"#details_btn_like_count")
        if elem_author_name.text == self.__getLoginName():
            #编辑按钮
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,"#details_artile_edit"))
            )
            #删除按钮
            self.driver.find_element(By.CSS_SELECTOR,"#bit-forum-content > div.page-body > div > div > div:nth-child(1) > div.col-9.card.card-lg > div.card-footer.bg-transparent.mt-auto.justify-content-end > div > div:nth-child(3) > div > a")
        # 截图
        ForumDriver.SavePicture()

    # 点赞功能测试
    def __LikePostTest(self):
        # 保存点赞前的点赞数
        clickbefor_amount = self.driver.find_element(By.CSS_SELECTOR, "#details_article_likeCount").text
        clickbefor_amount = int(clickbefor_amount)
        # 点赞
        self.driver.find_element(By.CSS_SELECTOR, "#details_btn_like_count").click()
        # 右下角弹窗
        elem_alert = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.jq-toast-wrap.bottom-right > div"))
        )
        assert elem_alert.text.split("\n")[2] == "点赞成功"
        # 记录点赞后的点赞数
        clickafter_amount = self.driver.find_element(By.CSS_SELECTOR, "#details_article_likeCount").text
        clickafter_amount = int(clickafter_amount)
        assert clickafter_amount == (clickbefor_amount + 1)
        # 截图
        ForumDriver.SavePicture()

    #帖子详情页的回复功能测试
    def __replyTest(self):
        #进入首页第一个帖子详情页
        elem_entrance=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a"))
        )
        elem_entrance.click()
        #等待编辑区加载
        elem_edit_area=WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#article_details_reply"))
        )
        # 滑动到编辑区
        ActionChains(self.driver).move_to_element(elem_edit_area).perform()
        #输入回复
        now_time=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        reply_text="reply"+now_time
        java_script=("var sum=document.getElementById('details_article_reply_content'); "
                     f"sum.value='{reply_text}'; ")
        self.driver.execute_script(java_script)
        # 滑动到回复按钮处，不然无法点击
        elem_reply_but=self.driver.find_element(By.CSS_SELECTOR, "#details_btn_article_reply")
        ActionChains(self.driver).move_to_element(elem_reply_but).perform()
        #点击回复
        elem_reply_but.click()
        #右下角弹窗回复成功
        elem_alert=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[contains(text(),'回复成功')]"))
        )
        reply_alert_text=elem_alert.text
        assert reply_alert_text.split("\n")[2] == "回复成功",f"实际:{reply_alert_text.split('\n')[2]}"
        #截图
        ForumDriver.SavePicture()

    #跳转功能测试，包括作者名字跳转、编辑按钮跳转，删除按钮测试
    def __JumpTest(self):
        #作者名字跳转测试
        self.__nameJumpTest()
        #编辑按钮测试
        self.__editbutTest()
        #删除按钮测试
        self.__deletebutTest()
        #截图
        ForumDriver.SavePicture()

    #作者名字跳转
    def __nameJumpTest(self):
        elem_authorname = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#article_details_author_name"))
        )
        authorname = elem_authorname.text
        elem_authorname.click()
        elem_pro_nickname = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#profile_nickname"))
        )
        profile_name=elem_pro_nickname.text
        assert authorname == profile_name, f"详情页显示: {authorname},主页显示: {profile_name}"
        #回到详情页
        self.__ReturnDetailPage()
    #编辑按钮功能测试
    def __editbutTest(self):
        elements=self.driver.find_elements(By.CSS_SELECTOR, "#bit-forum-content > div.page-body > div > div > div:nth-child(1) > div.col-9.card.card-lg > div.card-footer.bg-transparent.mt-auto.justify-content-end > div > div:nth-child(2)")
        if not elements or not elements[0].is_displayed():
            return None
        else:
            elem_edit=self.driver.find_element(By.CSS_SELECTOR,"#details_artile_edit")
            elem_edit.click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#edit_article_title"))
            )
            #回退到首页第一个帖子详情页
            self.__ReturnDetailPage()
    #删除按钮功能测试
    def __deletebutTest(self):
        #先判断是否有删除按钮
        elements = self.driver.find_elements(By.CSS_SELECTOR,
                                             "#bit-forum-content > div.page-body > div > div > div:nth-child(1) > div.col-9.card.card-lg > div.card-footer.bg-transparent.mt-auto.justify-content-end > div > div:nth-child(3)")
        if not elements or not elements[0].is_displayed():
            return None
        else:
            elem_deletebut=WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#bit-forum-content > div.page-body > div > div > div:nth-child(1) > div.col-9.card.card-lg > div.card-footer.bg-transparent.mt-auto.justify-content-end > div > div:nth-child(3) > div > a"))
            )
            elem_deletebut.click()
            #确认删除
            elem_right_delete=WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#details_artile_delete"))
            )
            #等待其他弹窗消失了再点击删除
            # WebDriverWait(self.driver, 10).until(
            #     EC.invisibility_of_element_located((By.CSS_SELECTOR, "body > div.jq-toast-wrap.bottom-right > div"))
            # )
            elem_right_delete.click()
            #检查右下角弹窗
            elem_alert=WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[contains(text(),'删除成功')]"))
            )
            assert elem_alert.text.split("\n")[2] == "删除成功",f"实际: {elem_alert.text.split('\n')[2]}"

    #返回到主页第一个帖子的详情页
    def __ReturnDetailPage(self):
        #进入首页
        self.driver.find_element(By.CSS_SELECTOR, "#nav_board_index > a").click()
        #进入首页第一个帖子的详情页
        elem_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a"))
        )
        elem_title.click()

    #返回当前用户的昵称
    def __getLoginName(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_nav_avatar"))
        )
        elem.click()
        self.driver.find_element(By.CSS_SELECTOR, "#index_user_settings").click()
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#settings_nickname"))
        )
        loginname=elem.text
        self.__ReturnDetailPage()
        return loginname





