from RewriteSelenium.custom import *
import time
from datetime import datetime

# 弹出框异常
from selenium.common.exceptions import UnexpectedAlertPresentException

def initSeleniumWindowSetting():
    # 定义 基本变量
    webdriver_path = r'D:\ChromeDownloads\ChromeDriverEnv\chromedriver-win32\chromedriver-win32\chromedriver.exe'
    web_site = r'https://csustcj.edu-edu.com.cn/'
    # 初始化 webdriver
    web_driver = initWebDriver(webdriver_path)
    # 设置 最大的等待时间
    web_driver.implicitly_wait(6)
    # 打开指定网站
    openChromeWebSite(web_driver,web_site)
    time.sleep(3)
    # # 缩放 网页窗口至 0.8
    # setWindowZoomRatio(web_driver,0.8)
    # time.sleep(1)
    # # # 最大化 网页窗口
    web_driver.maximize_window()
    time.sleep(3)
    return web_driver

def loginPage(webdriver) -> bool:
    # 开始登陆
    # 获取 用户名 输入框元素
    username_input_id = r'txtUserName'
    username_input_element = getElementById(webdriver,username_input_id)
    # 获取 密码 输入框元素
    password_input_id = r'txtPwd'
    password_input_element = getElementById(webdriver,password_input_id)
    # 获取 登陆按钮 元素
    login_btn_id = r'btnSign'
    login_btn_element = getElementById(webdriver,login_btn_id)
    # 输入内容 到输入框
    # 输入用户名
    username = r'430423200009139053'
    sendKeysByElementObject(username_input_element,username,'clear')
    time.sleep(1)
    # 输入密码
    password = r'430423200009139053'
    sendKeysByElementObject(password_input_element,password,'clear')
    time.sleep(1)
    # 点击登陆
    clickElementByElementObject(login_btn_element)
    time.sleep(3)
    # 关闭对话框警告
    popupWindowAccept(webdriver)
    time.sleep(3)
    return True

# 进入 选课界面
def enterChooseCoursePage(webdriver,page_title,course_term,course_name):
    # 进入选课界面的主页
    # 开始判断是否在 选课界面
    # 根据 页面的标题栏来判断
    select_video_page_keyword = page_title
    # 如果 不在选课视频界面 则退出程序，并给出友好提示
    if(select_video_page_keyword not in webdriver.title):
        print('error')
        time.sleep(10)
        # 退出程序
        webdriver.quit()
    # 如果在选课界面，则 根据课程信息，来决定是否展开 第一学期课程内容
    # 弹出 弹出窗，提示课程信息
    alert_courseInfo = f"alert('第{course_term}学期 {course_name}')"
    excuteJavascript(webdriver,alert_courseInfo)
    time.sleep(1)
    popupWindowAccept(webdriver)
    time.sleep(3)
    webdriver.refresh()
    time.sleep(10)
    # 首先 切换到含有课程的 iframe 中
    switchToIframeHtmlByIframeIdOrName(webdriver,'iframUrl')
    # 切换到含有所有课程的列表视图
    switchToAllCurouses_selector = 'body > div.page.online > div.online-title > div.online-left > span:nth-child(2)'
    switchToAllCurouses_element = getElementByCssSelector(webdriver,switchToAllCurouses_selector)
    print(switchToAllCurouses_element)
    # 点击 切换到所有课程元素
    clickElementByElementObject(switchToAllCurouses_element)
    time.sleep(3)
    # 根据 课程所在学期，来决定是否 切换指定学期的课程视图
    # 如果 该课程是第二学期的，则不进行切换，如果是第一学期的，则进行切换
    if(course_term == 1):
        # 获取学期课程视图切换按钮
        switchToCourseTermView_xpath = r'/html/body/div[1]/div[1]/div[3]/ul/li[1]/div[1]/img'
        switchToCourseTermView_element = getElementByXpath(webdriver,switchToCourseTermView_xpath)
        # 点击 切换到指定课程学期视图元素
        clickElementByElementObject(switchToCourseTermView_element)
    # 获取 展示指定学期课程的ul每个学期课程的容器元素
    termCourse_ul_xpath = r'/html/body/div[1]/div[1]/div[3]/ul'
    termCourse_ul_element = getElementByXpath(webdriver,termCourse_ul_xpath)
    # 获取 展示给定学期课程的li课程容器元素
    termCourse_ul_li_element = getElementsByTagName(termCourse_ul_element,'li')[course_term - 1]
    # 指定学期中所有课程元素
    termCourse_ul_li_divs_element = getElementsByCssSelector(termCourse_ul_li_element,'div.single-xq-xl>div')
    # 根据课程名称 去找到指定的课程
    for termCourse_ul_li_div_element in termCourse_ul_li_divs_element:
        current_course_name = getElementByCssSelector(termCourse_ul_li_div_element,'div.list-content>div.list-content-right>h3').text
        # 根据 给到的课程名称，来获取指定的按钮元素，并点击进入 
        if(course_name in current_course_name):
            clickElementByElementObject(getElementByCssSelector(termCourse_ul_li_div_element,'div.list-content>div.list-content-right>div.learn-button>ul>li:nth-child(2)>span'))
            break
    
    time.sleep(3)
    # 从 iframe中切换到正常的默认视图
    switchToDefalutHtml(webdriver)
    time.sleep(3)


# 进入平时作业选择界面
def enterChooseCourseHomeWorkPage(webdriver,course_name):
    # 进入到 平时作业选择界面
    # 首先 切换到含有课程的 iframe 中
    switchToIframeHtmlByIframeIdOrName(webdriver,'iframUrl')
    time.sleep(3)
    # 获取 展示作业的所有容器元素
    displayAllHomeworkElements = getElementsByCssSelector(webdriver,'body > div.task_list.main > ul > li')
    # 遍历所有作业，把所有作业都做完
    print(displayAllHomeworkElements)
    # 导入考试答案
    import homeWorkResult as examResult
    exam_result = []
    for examresult in examResult.exam_result_list:
        if(examresult["name"] == course_name):
            exam_result = examresult["result"]
    # 如果没有答案则直接结束程序
    if exam_result.__len__()==0: webdriver.quit()
    # 作业索引
    homeWorkBigIndex = 0
    for displayAllHomeworkElement in displayAllHomeworkElements:
        # 点击 进入 做作业界面
        clickElementByElementObject(getElementByCssSelector(displayAllHomeworkElement,'div:nth-of-type(2)>div>a:nth-child(1)'))
        time.sleep(3)
        # 关闭弹窗
        popupWindowAccept(webdriver)
        time.sleep(3)
        # 从 iframe中切换到正常的默认视图
        switchToDefalutHtml(webdriver)
        # 保存 当前视图
        currentDefaultHtml = getCurrentWindowHandle(webdriver)
        # 并 将视图切换到 考试界面
        time.sleep(3)
        switchToWindowByTitle(webdriver,'考试系统')
        time.sleep(6)
        # 点击 开始考试
        try:
            clickElementByElementObject(getElementByCssSelector(webdriver,'#ui-client-wrapper > table > tbody > tr:nth-last-child(1) >  td:nth-last-child(1) > a:nth-last-child(1)'))
        finally:
            # 进入考试页面
            time.sleep(3)
            # 之后，将 视图切换至 iframe中 以便获取 元素
            switchToIframeHtmlByIframeIdOrName(webdriver,getElementByTagName(webdriver,'iframe.ui-paper-iframe'))
            time.sleep(10)
            # 考试答案
            current_exam_result = exam_result[homeWorkBigIndex]
            # 开始考试
            # 获取展示题目的容器元素
            displayExamContentBigContainerElements = getElementsByXpath(webdriver,'/html/body/center/div[2]/div')
            for displayExamContentBigContainerElement in displayExamContentBigContainerElements:
                exam_group_index = 0
                exam_result_temp = current_exam_result[exam_group_index]
                displayExamContentLittleContainerElements = getElementsByCssSelector(displayExamContentBigContainerElement,'div')
                for displayExamContentLittleContainerElement in displayExamContentLittleContainerElements:
                    # 题目索引
                    exam_index = 0
                    # 选项索引
                    option_index = 0
                    for option_button_element in getElementsByCssSelector(displayExamContentLittleContainerElement,'ul.ui-question-options>li>span'):
                        if(str(option_index+1) in exam_result_temp[exam_index]):
                            clickElementByElementObject(option_button_element)
                            time.sleep(1)
                        option_index = option_index + 1
                    # 索引加1
                    exam_index = exam_index + 1
                    # 做完一题之后，做下一题
                    time.sleep(3)
                    clickElementByElementObject(getElementByCssSelector(webdriver,'#ui_wrapper > div.ui-main > div.ui-iframe-wrapper > div.ui-main-footer-toolbar.ui-component > button:nth-child(2)'))
                    time.sleep(1)
                # 对应 每组题目索引加1
                exam_group_index = exam_group_index + 1
            # 都做完之后，便交卷
            clickElementByElementObject(getElementByCssSelector(webdriver,'#ui_wrapper > div.ui-main > div.ui-iframe-wrapper > div.ui-main-footer-toolbar.ui-component > div > button'))
            time.sleep(3)
            # 点击 确认交卷
            clickElementByElementObject(getElementByCssSelector(webdriver,'#ui_wrapper > div.ui-popup-tip > div > div > button:nth-child(1)'))
            # 将 iframe 视图切换至 默认视图中
            switchToDefalutHtml(webdriver)
            # 关闭该页面，切换至其他窗口
            webdriver.close()
            switchToWindowByHandle(webdriver,currentDefaultHtml)
            time.sleep(3)
            homeWorkBigIndex = homeWorkBigIndex + 1
            continue

# 程序入口
if(__name__=='__main__'):
    # 初始化自动化窗口
    web_driver = initSeleniumWindowSetting()
    # 登陆网页
    loginPage(web_driver)
    time.sleep(3)
    # 关闭对话框警告
    popupWindowAccept(web_driver)
    time.sleep(1)
    # 课程学期
    course_term = 1
    # 课程名称
    course_name = f"马克思主义基本原理概论"
    course_all_chapter = 10
    course_big_chapter = 7
    # 选课页面标题
    chooseCoursePage_title = r'长沙理工大学高等学历继续教育'
    # 进入 选课页面
    enterChooseCoursePage(web_driver,chooseCoursePage_title,course_term,course_name)
    # 进入 考试页面 开始进行考试 
    enterChooseCourseHomeWorkPage(web_driver,course_name)
    # 退出程序
    web_driver.quit()
