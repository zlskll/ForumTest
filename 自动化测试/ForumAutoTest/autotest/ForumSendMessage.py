import datetime

from selenium.webdriver import ActionChains
from  selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.Utils import ForumDriver
from autotest import ForumLogin

class ForumSendMessage:
    url = ""
    driver = ""
    current_nickname=""
    receive_massage=""
    reply_massage=""
    def __init__(self):
        self.url = "http://127.0.0.1:58080/sign-in.html"
        self.driver = ForumDriver.driver
        self.driver.get(self.url)

    def PostMessageTest(self):
        #登陆后进入首页
        elem_login = ForumLogin.FormLogin()
        elem_login.RightName_RightPass()
        elem_login.ClickLogin()
        self.setNickName(self.__getLoginNameOnHome())
        #私信入口测试
        #self.__sendMessageEnterTest()
        #发送私信测试
        self.__sendFunctionTest()
        #查看私信测试，停留在详情框
        self.__lookMessageTest()
        #回复私信测试,停留在首页
        self.__replyMessageTest()
        #查看回复测试
        self.__lookReplyTest()






    # 私信入口测试,结果停留在详情页
    def __sendMessageEnterTest(self):
        # 点击首页,进入首页帖子区,
        self.__ReturnHomePage()
        #保存入口选择器
        index=1
        post_entrance_selector=f"#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a"
        while self.driver.find_elements(By.CSS_SELECTOR, post_entrance_selector):
            # 每次循环都重新定位帖子
            post_entrance=self.driver.find_element(By.CSS_SELECTOR, post_entrance_selector)
            ActionChains(self.driver).move_to_element(post_entrance).perform()
            post_entrance.click()
            #进入详情页
            elem_author_nickname=WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,"#article_details_author_name"))
            )
            #作者名字和当前用户名字作比较,不等的话再看有没有私信按钮
            if elem_author_nickname.text != self.getNickName():
                WebDriverWait(self.driver,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,"#btn_details_send_message"))
                )
            #返回首页，以便能进行下一次循环的测试
            self.__ReturnHomePage()
            #更新选择器
            index=index+1
            post_entrance_selector = f"#artical-items-body > div:nth-child({index}) > div > div.col > div.text-truncate > a"

    # 发送私信测试，为了方便接下来的测试只有"lyn222"的用户会收到"lyn"的私信
    def __sendFunctionTest(self):
        # 得到首页第一个有私信按钮的帖子入口的选择器,然后点击进入详情页
        having_send_entrance_selector = self.__getElementHavingSend_selector()
        if not having_send_entrance_selector:
            return
        elem_entrance=self.driver.find_element(By.CSS_SELECTOR,having_send_entrance_selector)
        ActionChains(self.driver).move_to_element(elem_entrance).click().perform()
        #点击私信按钮
        elem_send_but=WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn_details_send_message"))
        )
        ActionChains(self.driver).move_to_element(elem_send_but).click().perform()
        # 出现模态框，进行输入测试,保存发送的内容
        send_message_content=self.__inputMessageTest()
        # 发送后的弹窗测试
        self.__alertSendTest()
        #保存私信内容，方便查看私信时核对
        self.setMessageContent(send_message_content)
        # 截图
        ForumDriver.SavePicture()

    #查看私信测试
    def __lookMessageTest(self):
        #登陆"lyn222"的账号
        elem_login=ForumLogin.FormLogin()
        elem_login.InputNamePass("lyn222","lyn222")
        elem_login.ClickLogin()
        #等待页面稳定
        elem_message_entrance=WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div:nth-child(2) > div > a"))
        )
        elem_message_entrance.click()
        #等待私信窗口出现
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#index_div_message_list"))
        )
        #检查显示未读已读功能
        self.__checkIfNoRead()
        #私信详情内容测试，停留在详情框
        self.__lookReceiveMessageDetailTest()
    #查看回复测试
    def __lookReplyTest(self):
        # 登陆"lyn"的账号
        elem_login = ForumLogin.FormLogin()
        elem_login.InputNamePass("lyn", "lyn12345")
        elem_login.ClickLogin()
        # 等待页面稳定,点击右上角站内私信按钮
        elem_message_entrance = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div:nth-child(2) > div > a"))
        )
        elem_message_entrance.click()
        # 等待私信窗口出现
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_div_message_list"))
        )
        # 检查显示未读已读功能
        self.__checkIfNoRead()
        # 查看回复详情内容测试，停留在详情框
        self.__lookReplyMessageDetailTest()


    # 回复私信功能测试
    def __replyMessageTest(self):
        # 点击回复按钮
        elem_reply_entrance = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn_index_message_reply"))
        )
        elem_reply_entrance.click()
        # 等待输入框出现
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_message_reply_div"))
        )
        # 输入内容
        reply_massage_content=self.__inputReplyMessage()
        # 回复成功弹窗提醒测试
        self.__alertReplyTest()
        #回复成功后，第一个私信状态变成[已回复]
        self.__checkIfHadReply()
        # 保存私信内容，方便查看私信时核对
        self.setReplyMassage(reply_massage_content)
        #截图
        ForumDriver.SavePicture()
        #回到首页，把私信区关闭
        self.driver.find_element(By.CSS_SELECTOR,"#index_message_offcanvasEnd > div.offcanvas-header > button").click()
        #等待页面稳定
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div.nav-item.dropdown > a"))
        )




    # 出现模态框，进行输入测试
    def __inputMessageTest(self):
        #等待弹窗出现
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_message_modal > div > div > div.modal-body > div > div"))
        )
        #输入内容,使用JavaSrcipt输入
        test_text=datetime.datetime.now().strftime("SendMessageTest:%Y%m%d-%H%M%S")
        java_script=("var elem=document.getElementById('index_message_receive_content'); "
                     f"elem.value='{test_text}';")
        self.driver.execute_script(java_script)
        #点击发送
        self.driver.find_element(By.CSS_SELECTOR, "#btn_index_send_message").click()
        return test_text

    #输入回复的私信
    def __inputReplyMessage(self):
        #使用javascript
        test_text = datetime.datetime.now().strftime("ReplyMessageTest:%Y%m%d-%H%M%S")
        java_script = ("var elem=document.getElementById('index_message_reply_receive_content'); "
                       f"elem.value='{test_text}';")
        self.driver.execute_script(java_script)
        # 点击发送
        self.driver.find_element(By.CSS_SELECTOR, "#btn_index_send_message_reply").click()
        return test_text

    # 发送私信后的弹窗测试
    def __alertSendTest(self):
        #等待弹窗
        alert_send=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.jq-toast-wrap.bottom-right > div"))
        )
        assert alert_send.text.split("\n")[2] == "发送成功"
    #回复私信的弹窗测试
    def __alertReplyTest(self):
        # 等待弹窗
        alert_send = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.jq-toast-wrap.bottom-right > div"))
        )
        assert alert_send.text.split("\n")[2] == "操作成功"

    #得到首页第一个有私信按钮的帖子的标题入口，为了方便接下来的测试只有"lyn222"的用户会收到"lyn"的私信
    def __getElementHavingSend_selector(self):
        special_author_name="lyn222"
        index = 1
        #如果不能找到帖子了，就停止循环
        while self.driver.find_elements(By.CSS_SELECTOR, f"#artical-items-body > div:nth-child({index}) > div > div.col > div.text-truncate > a"):
            #还有帖子没查看,点击帖子标题
            elem_entrance=self.driver.find_element(By.CSS_SELECTOR, f"#artical-items-body > div:nth-child({index}) > div > div.col > div.text-truncate > a")
            ActionChains(self.driver).move_to_element(elem_entrance).click().perform()
            #进入详情页面，等待页面稳定
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#details_article_content > p"))
            )
            #检查是否有私信按钮,获取作者名字,为了方便接下来的测试只有"lyn222"的用户会收到"lyn"的私信
            page_author_name=self.driver.find_element(By.CSS_SELECTOR, "#article_details_author_name").text
            if self.driver.find_elements(By.CSS_SELECTOR, "#btn_details_send_message") and page_author_name==special_author_name:
                # 有私信按钮且是"lyn222"，直接返回主页
                self.__ReturnHomePage()
                #等待页面稳定
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a"))
                )
                #返回选择器
                elem_entrance_selector=f"#artical-items-body > div:nth-child({index}) > div > div.col > div.text-truncate > a"
                return elem_entrance_selector
            else :
                # 没有私信按钮，直接返回主页，进行下一个循环
                self.__ReturnHomePage()
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,  f"#artical-items-body > div:nth-child({index}) > div > div.col > div.text-truncate > a"))
                )
                index=index+1
        #循环结束都没有返回入口的话，就说明没有  有私信按钮 的元素
        return None

    # 检查是否是“[未读]”,点击以后是否变为[已读]
    def __checkIfNoRead(self):
        elem_noread=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_div_message_list > div:nth-child(1) > div > div.col.text-truncate > a > span.index_message_item_statue"))
        )
        assert elem_noread.text=="[未读]"
        self.__clickLookDetailByTitle()
        self.__clickConcelDetail()
        elem_readed=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_div_message_list > div:nth-child(1) > div > div.col.text-truncate > a > span.index_message_item_statue"))
        )
        assert elem_readed.text=="[已读]"

    #检查回复以后是否变成[已回复]
    def __checkIfHadReply(self):
        elem_hadreply = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "#index_div_message_list > div:nth-child(1) > div > div.col.text-truncate > a > span.index_message_item_statue"))
        )
        assert elem_hadreply.text=="[已回复]"

    #收到的私信详情内容测试,最终停留在私信详情框
    def __lookReceiveMessageDetailTest(self):
        #点击标题进入详情页
        self.__clickLookDetailByTitle()
        #检查内容是否一样
        elem_detail=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#index_message_detail_content"))
        )
        assert elem_detail.text==self.getMessageContent(),f"实际:{elem_detail.text}"

    # 查看回复详情内容测试,最终停留在私信详情框
    def __lookReplyMessageDetailTest(self):
        # 点击标题进入详情页
        self.__clickLookDetailByTitle()
        # 检查内容是否一样
        elem_detail = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_message_detail_content"))
        )
        assert elem_detail.text == self.getReplyMassage(),f"实际:{elem_detail.text}"


    #通过标题，打开第一篇消息的详细内容
    def __clickLookDetailByTitle(self):
        elem_look_detail=WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"#index_div_message_list > div:nth-child(1) > div > div.col.text-truncate > a"))
        )
        elem_look_detail.click()
    #点击取消按钮
    def __clickConcelDetail(self):
        elem_concel_detail=WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"#index_message_reply_cancel"))
        )
        elem_concel_detail.click()

    # 前提：当前页面是首页,返回当前用户的昵称,结果：回到首页
    def __getLoginNameOnHome(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#index_nav_avatar"))
        )#头像
        elem.click()
        self.driver.find_element(By.CSS_SELECTOR, "#index_user_settings").click()
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#settings_nickname"))
        )
        loginname = elem.text
        self.__ReturnHomePage()
        return loginname



    #返回到主页,然后通过入口进入该帖子的详情页
    def __ReturnDetailPage(self,entrance):
        self.__ReturnHomePage()
        #进入帖子entrance的详情页
        entrance=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(entrance)
        )
        ActionChains(self.driver).move_to_element(entrance).perform()
        entrance.click()

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

    # #退出当前账号
    # def __exitAccount(self):
    #     elem_img=self.driver.find_element(By.CSS_SELECTOR, "body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div.nav-item.dropdown > a")
    #     ActionChains(self.driver).move_to_element(elem_img).perform()
    #     elem_img.click()
    #     elem_exit=WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR,"#index_user_logout"))
    #     )
    #     elem_exit.click()
    #     #等待页面稳定
    #     WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((By.CSS_SELECTOR,"#submit"))
    #     )


    def setNickName(self,nickname):
        self.current_nickname=nickname
    def getNickName(self):
        return self.current_nickname
    def setMessageContent(self,receive_massage):
        self.receive_massage=receive_massage
    def getMessageContent(self):
        return self.receive_massage
    def setReplyMassage(self,reply_massage):
        self.reply_massage=reply_massage
    def getReplyMassage(self):
        return self.reply_massage
