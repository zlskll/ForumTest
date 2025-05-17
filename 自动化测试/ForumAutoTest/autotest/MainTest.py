
from autotest import ForumLogin
from autotest import ForumPostAdd
from common.Utils import ForumDriver
from autotest import ForumLogon
from autotest import ForumHomePage
from autotest import ForumPostDetail
from autotest import ForumPostEdit
from autotest import ForumSendMessage
if __name__=='__main__':
    #登陆注册页面
    ForumLogon.ForumLogon().LogonSuccess()
    ForumLogon.ForumLogon().LogonFail()
    ForumLogin.FormLogin().LoginFail()
    ForumLogin.FormLogin().LoginSuccess()
    #首页测试
    ForumHomePage.ForumHomePage().HomePageTestNoLogin()
    #帖子详情页测试，选定首页第一个帖子标题进入，进行测试
    ForumPostDetail.ForumPostDetail().DetailTest()
    #帖子编辑页测试，选定首页第一个可以编辑的帖子的标题进入，进行编辑测试
    ForumPostEdit.ForumPostEdit().EditSuccTest()
    #帖子发布页测试，每一个板块区都发一个帖子测试
    ForumPostAdd.ForumPostAdd().AddSuccTest()
    #站内私信测试
    ForumSendMessage.ForumSendMessage().PostMessageTest()
    #退出浏览器
    ForumDriver.driver.quit()
