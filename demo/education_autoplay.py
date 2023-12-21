from RewriteSelenium.custom import *
import time

if(__name__=='__main__'):
    # 定义 基本变量
    webdriver_path = r'D:\ChromeDownloads\ChromeDriverEnv\chromedriver-win32\chromedriver-win32\chromedriver.exe'
    web_site = r'https://csustcj.edu-edu.com.cn/'
    # 初始化 webdriver
    web_driver = initWebDriver(webdriver_path)
    # 设置 最大的等待时间
    web_driver.implicitly_wait(10)
    # 打开指定网站
    openChromeWebSite(web_driver,web_site)
    time.sleep(3)
    web_driver.maximize_window()
    time.sleep(2)
    string = r'/html/body/div[2]/div/div/div[3]/div[3]/font[1]'
    el = getElementByXpath(web_driver,string)
    print(el.text)

    # # 课程名称
    # course_name = "马克思主义基本原理概论"
    # # 弹出 弹出窗，提示课程信息
    # alert_courseInfo = f"alert('第1学期名称：{course_name}')"
    # excuteJavascript(web_driver,alert_courseInfo)
    # time.sleep(3)
    # popupWindowAccept(web_driver)
    # time.sleep(3)
    # if(screenshotSaveAsCustomPath(web_driver,'/1.png')):
    #     excuteJavascript(web_driver,"alert('截图成功')")
    #     time.sleep(2)
    #     popupWindowAccept(web_driver)
    # else:
    #     excuteJavascript(web_driver,"alert('截图成功')")
    #     time.sleep(2)
    #     popupWindowAccept(web_driver)

    time.sleep(3)
    # 退出程序
    web_driver.quit()
