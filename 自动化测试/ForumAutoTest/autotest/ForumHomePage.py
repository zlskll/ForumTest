from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from common.Utils import ForumDriver
from autotest import ForumLogin
class ForumHomePage:
    url=""
    driver = ""
    def __init__(self):
        self.url="http://127.0.0.1:58080/index.html"
        self.driver = ForumDriver.driver
        self.driver.get(self.url)

    #登陆情况下测试
    def HomePageTestByLogin(self):
        #成功登陆
        elem_login=ForumLogin.FormLogin()
        elem_login.RightName_RightPass()
        elem_login.ClickLogin()
        #页面元素检查
        self.__check_element_exist()
        #关键字搜索功能
        self.__KeySearchSuc()
        #切换背景颜色功能
        self.__SwitchBackSuc()
        #板块区
        for i in [0,9]:
            self.__SectionTest(i)
    #未登陆情况下测试
    def HomePageTestNoLogin(self):
        #登陆后退出
        elemlogin=ForumLogin.FormLogin()
        elemlogin.RightName_RightPass()
        elemlogin.ClickLogin()
        elemlogin.ExitAccount()
        #关键字搜索功能
        # 重新进入网页
        self.driver.get(self.url)
        self.__KeySearchFail()
        #切换背景颜色功能
        #重新进入网页
        self.driver.get(self.url)
        self.__SwichBackFail()
        #发布帖子按钮跳转测试
        #重新进入网页
        self.driver.get(self.url)
        self.__JumpTestFail()


    #板块区测试，
    # 0--首页，1--Java，2--C++，3--前端技术，4--MySQL，5--面试宝典，
    # 6--经验分享，7--招聘信息，8--福利待遇，9--灌水区
    def __SectionTest(self,section_id):
        #进入对应的板块区
        self.__EnterSectionbyid(section_id)
        #帖子数量测试,首页没有数量就不测试了，顺便加上标题测试
        if section_id!=0:
            self.__check_post_amount(section_id)
        post_amount = self.__get_post_amount(section_id)
        #帖子元素检查,有帖子的才查，没帖子的不查
        if post_amount > 0:
            self.__check_post_element()
        #跳转测试
        self.__JumpTest(section_id)

    #进入板块id为section_id的板块页
    def __EnterSectionbyid(self,section_id):
        # 找到对应的板块按钮
        sectionbut = self.driver.find_element(By.CSS_SELECTOR, f"#topBoardList > li:nth-child({section_id + 1}) > a")
        sectionbut.click()
        # 添加等待，等待帖子区加载
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#artical-items-body"))
        )

    #帖子跳转测试，包括帖子标题跳转和发布帖子跳转
    def __JumpTest(self,section_id):
        #点击帖子发布按钮
        elem_add_post=self.driver.find_element(By.CSS_SELECTOR,"#bit-forum-content > div.page-header.d-print-none > div > div > div.col-auto.ms-auto.d-print-none > div > a.btn.btn-primary.d-none.d-sm-inline-block.article_post")
        elem_add_post.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#article_post_title"))
        )
        #截图
        ForumDriver.SavePicture()
        #回到刚才的页面继续测试
        self.__EnterSectionbyid(section_id)
        #点击某一篇帖子的标题
        #有帖子才测试，没帖子不测试
        if self.__get_post_amount(section_id) > 0:
            elem_click_title=self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a")
            elem_click_title.click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,"#details_article_content_title"))
            )
        #截图
        ForumDriver.SavePicture()
        #回到刚才的页面
        self.__EnterSectionbyid(section_id)

    def __JumpTestFail(self):
        # 点击帖子发布按钮
        elem_add_post = WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#bit-forum-content > div.page-header.d-print-none > div > div > div.col-auto.ms-auto.d-print-none > div > a.btn.btn-primary.d-none.d-sm-inline-block.article_post") )
        )
        elem_add_post.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#submit"))
        )
        # 截图
        ForumDriver.SavePicture()

    #转换背景颜色测试
    def __SwitchBackSuc(self):
        elem_switch_to_dark=self.driver.find_element(By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div:nth-child(2) > a.nav-link.px-0.hide-theme-dark")
        elem_switch_to_dark.click()
        assert self.__get_backcolor() =="dark"
        #截图
        ForumDriver.SavePicture()
        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1)"))
        )
        elem_switch_to_light=self.driver.find_element(By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div:nth-child(2) > a.nav-link.px-0.hide-theme-light")
        elem_switch_to_light.click()
        assert self.__get_backcolor() =="light"

    def __SwichBackFail(self):
        elem_switch_to_dark = self.driver.find_element(By.CSS_SELECTOR,
                                                       "body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div:nth-child(2) > a.nav-link.px-0.hide-theme-dark")
        elem_switch_to_dark.click()
        #回到登陆页面
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#submit"))
        )
        #截图
        ForumDriver.SavePicture()

    #查看帖子各项信息是否正常展示
    def __check_post_element(self):
        self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-truncate > a")
        self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-muted.mt-2 > div > div.col > ul > li:nth-child(1)")
        self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-muted.mt-2 > div > div.col > ul > li:nth-child(2)")
        self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-muted.mt-2 > div > div.col-auto.d-none.d-md-inline > ul > li:nth-child(1)")
        self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-muted.mt-2 > div > div.col-auto.d-none.d-md-inline > ul > li:nth-child(2)")
        self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1) > div > div.col > div.text-muted.mt-2 > div > div.col-auto.d-none.d-md-inline > ul > li:nth-child(3)")


    #帖子数量和帖子标题测试,传入板块id
    def __check_post_amount(self,num):
        #帖子标题测试
        # 获取板块名字
        arr_section=["首页","Java","C++","前端技术","MySQL","面试宝典","经验分享","招聘信息","福利待遇","灌水区"]
        elem_title=self.driver.find_element(By.CSS_SELECTOR,"#article_list_board_title")
        assert elem_title.text == arr_section[num]
        #帖子数量测试
        actual_amount=self.__get_post_amount(num)
        #读取页面上显示的amount
        display_amount=self.driver.find_element(By.CSS_SELECTOR,"#article_list_count_board").text
        display_amount=int( display_amount.replace("帖子数量: ","") )
        assert actual_amount==display_amount,f"{elem_title.text}区实际数量={actual_amount}, 显示数量={display_amount}"

    #得到=section_id的板块的帖子真实数量
    def __get_post_amount(self,section_id):
        # 找到帖子列表区
        postarea = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#artical-items-body"))
        )
        # 找到所有class=“row"的元素，放到一个列表里
        postlist = postarea.find_elements(By.CSS_SELECTOR, "#artical-items-body > div > div.row")
        return len(postlist)

    #得到背景颜色，"dark" or "light"
    def __get_backcolor(self):
        current_url=self.driver.current_url
        back_color=current_url.replace("http://127.0.0.1:58080/?theme=","")
        return back_color
    #测试福利待遇
    def __KeySearchSuc(self):
        elem_search=self.driver.find_element(By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div.nav-item.d-none.d-md-flex.me-3 > div > form > div > input")
        keyword="test"
        elem_search.send_keys(keyword+Keys.RETURN)
        #检查搜索出的结果是否包含"福利待遇"
        self.__check_keysearch(keyword)
        #截图
        ForumDriver.SavePicture()

    def __KeySearchFail(self):
        elem_search = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div.nav-item.d-none.d-md-flex.me-3 > div > form > div > input")
        keyword = "test"
        elem_search.send_keys(keyword + Keys.RETURN)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#submit"))
        )
        # 截图
        ForumDriver.SavePicture()



    #页面元素检查
    def __check_element_exist(self):
        #添加等待，等待
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#artical-items-body > div:nth-child(1)"))
        )
        #发布帖子按钮
        self.driver.find_element(By.CSS_SELECTOR,"#bit-forum-content > div.page-header.d-print-none > div > div > div.col-auto.ms-auto.d-print-none > div > a.btn.btn-primary.d-none.d-sm-inline-block.article_post")
        #标头的板块切换
        self.driver.find_element(By.CSS_SELECTOR,"#topBoardList > li:nth-child(10) > a")
        #搜索
        self.driver.find_element(By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div.nav-item.d-none.d-md-flex.me-3 > div > form > div > input")
        #切换夜间按钮
        self.driver.find_element(By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div:nth-child(2) > a.nav-link.px-0.hide-theme-dark")
        #站内信按钮
        self.driver.find_element(By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div:nth-child(2) > div > a")
        #头像按钮
        self.driver.find_element(By.CSS_SELECTOR,"body > div.page > header.navbar.navbar-expand-md.navbar-light.d-print-none > div > div > div.nav-item.dropdown > a")
        #首页板块标题
        elem_title=self.driver.find_element(By.CSS_SELECTOR,"#article_list_board_title")
        assert elem_title.text=="首页"
        #帖子列表
        self.driver.find_element(By.CSS_SELECTOR,"#artical-items-body > div:nth-child(1)")
        #截图
        ForumDriver.SavePicture()

    #检查搜索出的结果是否包含keyword
    def __check_keysearch(self,keyword):
        #找到帖子区
        postarea=WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#artical-items-body"))
        )
        #找到所有class=“row"的元素，放到一个列表里
        postlist=postarea.find_elements(By.CSS_SELECTOR,"#artical-items-body > div > div.row")
        for post in postlist:
            post_title=post.find_element(By.CSS_SELECTOR,"div.row > div.col > div.text-truncate > a > strong").text
            post_author=post.find_element(By.CSS_SELECTOR,"div.row > div.col > div.text-muted.mt-2 > div > div.col > ul > li:nth-child(1)").text
            assert keyword in post_title or keyword in post_author
