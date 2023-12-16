from custom_selenium import *
import time

if(__name__=='__main__'):
    # 定义 基本变量
    webdriver_path = r'D:\ChromeDownloads\ChromeDriverEnv\chromedriver-win32\chromedriver-win32\chromedriver.exe'
    web_site = r'https://cws.edu-edu.com/page/client#/courseware-player?uid=147369'
    # 初始化 webdriver
    web_driver = initWebDriver(webdriver_path)
    # 设置 最大的等待时间
    web_driver.implicitly_wait(10)
    # 打开指定网站
    openChromeWebSite(web_driver,web_site)
    

    # 退出程序
    web_driver.quit()
