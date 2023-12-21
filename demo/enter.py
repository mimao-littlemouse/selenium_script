# 内置模块
import time
from datetime import datetime

# 第三方模块
# 导入 selenium 中的webdriver类型
from selenium.webdriver.chrome.webdriver import WebDriver
# 导入 selenium 中常见的异常类
# 弹出框异常类
# from selenium.common.exceptions import UnexpectedAlertPresentException

# 自定义模块
from RewriteSelenium.custom import *


def initSeleniumWindowSetting() -> WebDriver:
    # 定义 基本变量
    webdriver_path = r'D:\ChromeDownloads\ChromeDriverEnv\chromedriver-win32\chromedriver-win32\chromedriver.exe'
    web_site = r'https://csustcj.edu-edu.com.cn/'
    # 初始化 webdriver
    web_driver = initWebDriver(webdriver_path)
    # 设置 最大的等待时间
    web_driver.implicitly_wait(10)
    # 最大化 网页窗口
    web_driver.maximize_window()
    # 打开指定网站
    web_driver.get(web_site)
    return web_driver

def loginPage(webdriver: WebDriver) -> None:
    # 开始登陆
    # 获取 用户名 输入框元素
    username_id = r'txtUserName'
    usernameInput_element = getElement(webdriver,'id',username_id)
    # 获取 密码 输入框元素
    password_id = r'txtPwd'
    passwordInput_element = getElement(webdriver,'id',password_id)
    # 获取 登陆按钮 元素
    loginBtn_id = r'btnSign'
    loginBtn_element = getElement(webdriver,'id',loginBtn_id)
    # 输入内容 到输入框
    # 输入用户名
    username = r'430423200009139053'
    # 清除输入框中的内容
    usernameInput_element.clear()
    # 输入内容到 输入框 中
    usernameInput_element.send_keys(username)
    # 模拟用户输入 等待一段时间
    time.sleep(3)
    # 输入密码
    password = r'430423200009139053'
    # 清除输入框中的内容
    passwordInput_element.clear()
    # 输入内容到 输入框 中
    passwordInput_element.send_keys(password)
    # 模拟用户输入 等待一段时间
    time.sleep(1)
    # 点击登陆
    loginBtn_element.click()

# 查看通知
def handleNotice(webdriver: WebDriver) -> None:
    # 根据 css 选择器 获取 查看详情的按钮元素对象
    lookDetailBtn_element = getElement(webdriver,'css',r'#div_msg > a')
    # 点击按钮
    lookDetailBtn_element.click()
    # 保存当前窗口句柄
    currentWindow_handle = getCurrentWindowHandle(webdriver)
    # 切换到打开的页面
    newWindow_handle = switchToWindowByIndex(webdriver,1)
    # 关闭 新开的窗口
    newWindow_handle.close()
    # 切换到 之前的窗口
    switchToWindowByHandle(webdriver,currentWindow_handle)
    # 刷新页面
    webdriver.refresh()

# 在 选课界面进行课程的选择
def chooseCourse(webdriver,course_term,course_name):
    
    
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
            clickElementByElementObject(getElementByCssSelector(termCourse_ul_li_div_element,'div.list-content>div.list-content-right>div.learn-button>ul>li:nth-child(1) >span'))
            time.sleep(3)
            break
    
    time.sleep(3)
    # 从 iframe中切换到正常的默认视图
    switchToDefalutHtml(webdriver)
    time.sleep(3)


# 进入课程观看确认界面  返回 还需学习的时长
def enterCourseConfirmPage(webdriver) -> int:
    # 进入到 确认课程界面
    # 首先 切换到含有课程的 iframe 中
    switchToIframeHtmlByIframeIdOrName(webdriver,'iframUrl')
    # 选好课程之后，进入确认课程界面进行 确认是否需要 进入该课程听课
    course_duration_info = getElementByXpath(webdriver,'/html/body/div[2]/ul/li/div/div[1]/div/span').text
    # 课程时长
    course_duration = int(course_duration_info.split('应学时长：')[1].split(' 分钟')[0])
    # 课程已学时长
    course_current_duration = int(course_duration_info.split('已学时长：')[1].split(' 分钟')[0])
    # 还需学习时长
    needLearnCouse_duration = course_duration - course_current_duration
    # 如果时长相差小于60 或者 已学时长大于课程所需时长 就退出程序
    if(needLearnCouse_duration < 60):
        webdriver.close()
        time.sleep(3)
        webdriver.quit()
    time.sleep(3)
    # 点击 进入 课程观看界面
    clickElementByElementObject(getElementByXpath(webdriver,'/html/body/div[2]/ul/li/div/div[2]/div/a'))
    time.sleep(3)
    # 从 iframe中切换到正常的默认视图
    switchToDefalutHtml(webdriver)
    # 返回 需要学习的时长
    return needLearnCouse_duration

# 设置循环播放课程视频
def setCiclePlayCouseVideo(webdriver,playing = True):
    # 获取 切换是否连续播放按钮元素
    switch_autoplay_btn_selector = r'#app > div > dl > div > span.ivu-switch.ivu-switch-default'
    # 连续播放时，该按钮多出的类名
    switch_autoplay_btn_enable_class = r'ivu-switch-checked'
    
    # 连续播放 按钮是否打开
    # 通过 让按钮一直打开，来保证 视频一直播放下去
    # 判断该按钮的状态（通过该元素的 类名列表中是否有 ivu-switch-checked 类名即可）
    # 如果，该按钮 处于关闭状态，即如果 没有该类名时，自动点击该按钮
    switch_autoplay_btn_element = getElementByCssSelector(webdriver,switch_autoplay_btn_selector)
    # 获取 该元素的类名列表
    switch_autoplay_btn_classList = getAttributeByElementObject(switch_autoplay_btn_element,'class')
    # 只有当需要 设置为连续播放并且此时并未切换为连续播放  和 设置为不连续播放并且此时已经设置为连续播放时，才点击按钮进行切换
    if((playing and switch_autoplay_btn_enable_class not in switch_autoplay_btn_classList) and (not playing and switch_autoplay_btn_enable_class in switch_autoplay_btn_classList)):
        # 点击该 按钮
        clickElementByElementObject(switch_autoplay_btn_element)
        time.sleep(3)

# 设置视频播放状态
def setCourseVideoPlayingState(webdriver,playing = True):
    # 视频控制按钮 选择器
    video_control_btn_xpath = r'/html/body/div[1]/div/div/div[1]/div[1]/div[1]'
    # 视频控制按钮 元素
    video_control_btn_element = getElementByXpath(webdriver,video_control_btn_xpath)
    # 获取 视频控制按钮元素的 类名
    video_control_btn_classlist = getAttributeByElementObject(video_control_btn_element,'class')
    # 暂停
    pause = r'pause'
    # 如果 处于 暂停状态，则点击按钮，让其处于 播放状态
    if(pause in video_control_btn_classlist and playing):
        clickElementByElementObject(video_control_btn_element)
    else: 
        # 否则 当处于播放状态，而且 playing为False，则进行操作，否则不进行操作
        if(pause not in video_control_btn_classlist and not playing):
            # 将鼠标悬停在 视频上
            mouseoverElementByElementObject(webdriver,getElementByXpath(webdriver,'//*[@id="J_prismPlayer"]/video'))
            # 点击 暂停按钮
            clickElementByElementObject(getElementByXpath(webdriver,'/html/body/div[1]/div/div/div[1]/div[1]/div[9]/div[3]'))

def getCurrentCourseVideoDuration(webdriver) -> int:
    # 将鼠标悬停在 视频上
    mouseoverElementByElementObject(webdriver,getElementByXpath(webdriver,'//*[@id="J_prismPlayer"]/video'))
    time.sleep(3)
    # 获取 该视频的时长
    currentVideoDurationString = getElementByXpath(webdriver,'/html/body/div[1]/div/div/div[1]/div[1]/div[9]/div[4]/span[3]').text
    currentVideoDurationString_list = currentVideoDurationString.split(':')
    currentVideoDuration = 0
    if(currentVideoDurationString_list.__len__()==3):
        hour = int(currentVideoDurationString_list[0])
        mini = int(currentVideoDurationString_list[1])
        currentVideoDuration = hour * 60 + mini
    elif(currentVideoDurationString_list.__len__()==2):
        mini = int(currentVideoDurationString_list[0])
        currentVideoDuration = mini
    return currentVideoDuration


# 监听 课程视频的播放
def addListenVideoPlay(webdriver,duration,course_all_chapter,course_big_chapter):
    cancelListen = False
    currentLearnDuration = 0
    courseChapterIndex = ''
    currentCourseChapterIndex = ''

    # 循环次数
    cicle_count = 1
    while(not cancelListen):
        # 当时间 在 3点到5点，则进行程序睡眠
        now_time = datetime.now()
        now_time_hour = now_time.hour
        now_time_minute = now_time.minute
        if(now_time_hour >= 3 and now_time_hour <= 4):
            need_wait_time = (5-now_time_hour)*60*60 - now_time_minute*60
            print(need_wait_time)
            time.sleep(need_wait_time)
            # 睡眠之后，进行刷新
            webdriver.refresh()
        
        if(cicle_count==1):
            setCourseVideoPlayingState(webdriver,True)
            time.sleep(3)
            setCiclePlayCouseVideo(webdriver)
            time.sleep(3)
        
        # 过30分钟 就将点击 暂停和播放
        if(cicle_count == 1000*60*30):
            # 先暂停
            setCourseVideoPlayingState(webdriver,False)
            time.sleep(3)
            setCourseVideoPlayingState(webdriver,True)
            time.sleep(3)

        # 过60分钟 就刷新一次页面
        if(cicle_count == 1000*60*60):
            cicle_count = 1
            webdriver.refresh()
            time.sleep(5)

        # 5分钟 获取一次当前 所在章节索引
        if(cicle_count == 1000*60*5):
            # 大章节
            courseChapter_bigTitle_elements = getElementsByXpath(webdriver,'/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/ul')
            courseChapter_bigTitle_element_cicleCount = 0
            for courseChapter_bigTitle_element in courseChapter_bigTitle_elements:
                courseChapter_bigTitle_element_cicleCount = courseChapter_bigTitle_element_cicleCount + 1
                # 有时候课程会有导言，所以这里需要进行判断 来进行不同于正常章节的操作
                if(courseChapter_bigTitle_element_cicleCount<=(course_all_chapter - course_big_chapter)):
                    # 相对于 导言这种，直接对应的就是 一大章就是一个视频，所以 直接获取到的就是一个小标题
                    courseChapter_littleTitle_elements = getElementByCssSelector(courseChapter_bigTitle_element,'li>span:nth-child(2)')
                    if('activeVideo' in getAttributeByElementObject(courseChapter_littleTitle_elements,'class')):
                        courseChapter_littleTitle = getAttributeByElementObject(courseChapter_littleTitle_elements,'title')
                        currentCourseChapterIndex = courseChapter_littleTitle.split(' ')[0]
                    pass
                else:
                    # 小章节
                    courseChapter_littleTitle_container_elements = getElementsByCssSelector(courseChapter_bigTitle_element,'li>ul')
                    for courseChapter_littleTitle_container_element in courseChapter_littleTitle_container_elements:
                        courseChapter_littleTitle_elements = getElementByCssSelector(courseChapter_littleTitle_container_element,'li>span:nth-child(2)')
                        if('activeVideo' in getAttributeByElementObject(courseChapter_littleTitle_elements,'class')):
                            courseChapter_littleTitle = getAttributeByElementObject(courseChapter_littleTitle_elements,'title')
                            currentCourseChapterIndex = courseChapter_littleTitle.split(' ')[0]
            
            # 根据获取到的章节索引，算出当前所学时长
            if(courseChapterIndex != currentCourseChapterIndex):
                # 获取当前视频的时长
                currentCourseVideoDuration = getCurrentCourseVideoDuration(webdriver)
                currentLearnDuration = currentLearnDuration + currentCourseVideoDuration

            # 根据目前所学时长和课程要求时长 决定是否还需要继续 观看视频（即 是否还需要进行监听）
            if(currentLearnDuration - 30 > duration):
                # 取消监听
                cancelListen = True
        
        # 10分钟检查一次 是否有长时间不在电脑前的警告
        if(cicle_count == 1000*60*10):
            # 检查 是否有长时间 确认框检查 有则添加对应事件
            longtimeConfirmAlertStyleString_list = getAttributeByElementObject(getElementByXpath(webdriver,'/html/body/div[8]/div[2]/div'),'style').split(';')
            for longtimeConfirmAlertStyleString in longtimeConfirmAlertStyleString_list:
                if('display' in longtimeConfirmAlertStyleString):
                    if(longtimeConfirmAlertStyleString.split(':')[1] == 'block'):
                        # 当 页面播放时间太长时，会出现 弹出框来确认是否坐在电脑旁
                        # 点击 确认
                        clickElementByElementObject(getElementByXpath(webdriver,'/html/body/div[8]/div[2]/div/div/div[2]/div[2]/button'))
                        time.sleep(5)
                        webdriver.refresh()

        cicle_count = cicle_count + 1


# 程序入口
if(__name__=='__main__'):
    # 初始化自动化窗口
    web_driver = initSeleniumWindowSetting()
    # 登陆网页
    loginPage(web_driver)
    # 等待 弹出框的出现
    time.sleep(3)
    # 对 弹出框 进行确认
    popupWindowAccept(web_driver)
    # 等待通知出现，并点击 查看通知详情
    # handleNotice(web_driver)
    # 等待第二次 弹出框的出现
    time.sleep(3)
    # 再次对 弹出框 进行确认
    popupWindowAccept(web_driver)
    while(input()=='exit'):
        web_driver.quit()
    # # 关闭对话框警告
    # popupWindowAccept(web_driver)
    # time.sleep(1)
    # # 课程学期
    # course_term = 1
    # # 课程名称
    # course_name = f"线性代数"
    # course_all_chapter = 33
    # course_big_chapter = 0
    # # 选课页面标题
    # chooseCoursePage_title = r'长沙理工大学高等学历继续教育'
    # # 进入 选课页面
    # try:
    #     enterChooseCoursePage(web_driver,chooseCoursePage_title,course_term,course_name)
    # except:
    #     excuteJavascript(web_driver,'debugger')
    # # 进入 指定课程页面的确认页面 返回 还需学习的时长
    # needLearnDuration = enterCourseConfirmPage(web_driver)
    # # 将当前窗口句柄保存，并将窗口切换至新打开的窗口界面 
    # currentWindow_handle = getCurrentWindowHandle(web_driver)
    # # 将窗口切换至新打开的窗口界面 
    # switchToWindowByTitle(web_driver,course_name)
    # time.sleep(3)
    # # 开始播放视频(并 随时监听视频播放时长 )
    # addListenVideoPlay(web_driver,needLearnDuration,course_all_chapter,course_big_chapter)
    
    # # 退出程序
    web_driver.quit()
