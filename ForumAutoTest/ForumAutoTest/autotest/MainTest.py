
from autotest import ForumLogin
from common.Utils import ForumDriver
from autotest import ForumLogon
from autotest import ForumHomePage
from autotest import ForumPostDetail
if __name__=='__main__':
    # ForumLogon.ForumLogon().LogonSuccess()
    # ForumLogon.ForumLogon().LogonFail()
    # ForumLogin.FormLogin().LoginFail()
    # ForumLogin.FormLogin().LoginSuccess()
    #首页
    #ForumHomePage.ForumHomePage().HomePageTestNoLogin()
    ForumPostDetail.ForumPostDetail().DetailTest()


    ForumDriver.driver.quit()
