from custom_selenium import *
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
    # 开始登陆
    # 获取 用户名 输入框元素
    username_input_id = r'txtUserName'
    username_input_element = getElementById(web_driver,username_input_id)
    # 获取 密码 输入框元素
    password_input_id = r'txtPwd'
    password_input_element = getElementById(web_driver,password_input_id)
    # 获取 登陆按钮 元素
    login_btn_id = r'btnSign'
    login_btn_element = getElementById(web_driver,login_btn_id)
    # 输入内容 到输入框
    # 输入用户名
    username = r'430423200009139053'
    sendKeysByElementObject(username_input_element,username,'clear')
    time.sleep(1)
    # 输入密码
    password = r'430423200009139053'
    sendKeysByElementObject(password_input_element,password,'clear')
    time.sleep(3)
    # 点击登陆
    clickElementByElementObject(login_btn_element)
    time.sleep(30)

    # 开始 课程
    # 开始判断是否在 选课界面
    # 根据 页面的标题栏来判断
    select_video_page_keyword = r'长沙理工大学高等学历继续教育'
    # 如果 不在选课视频界面 则退出程序，并给出友好提示
    if(select_video_page_keyword not in web_driver.title):
        print('error')
        time.sleep(10)
        # 退出程序
        web_driver.quit()
    # 在选课界面，则 开始点击 课程
    # 设置听课顺序
    course_name = input("请输入需要进行 学习的课程名称：")
    print(course_name)
    # 选好课程之后，进入确认课程界面进行 确认是否需要 进入该课程听课
    # 课程时长
    # course_duration = el.innerText.split('应学时长：')[1].split(' 分钟')[0]
    # 课程已学时长
    # course_current_duration = el.innerText.split('已学时长：')[1].split(' 分钟')[0]

    # # 点击 页面导航，去到 页面2
    # pagination_navigate_linkTo_page2_selector = r'.pagination>li:nth-child(2)>a'
    # time.sleep(1)
    # # 获取该元素，并点击
    # clickElementByElementObject(getElementByCssSelector(web_driver,pagination_navigate_linkTo_page2_selector))
    # time.sleep(3)
    # # 获取 中国近代史纲要课程的 课程进入按钮并点击
    # chinesecourse_page_title_keyword = r'中国近代史纲要课程'
    # enter_chinesecourse_btn_xpath = r'/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[3]/ul/li[1]/span'
    # clickElementByElementObject(getElementByXpath(web_driver,enter_chinesecourse_btn_xpath))
    # time.sleep(20)
    # # 获取当前页面的 句柄
    # select_video_page_window_handle = getCurrentWindowHandle(web_driver)
    # # 切换 到点击之后的页面
    # chinesecourse_page_window_handle = switchToWindowByTitle(chinesecourse_page_title_keyword)
    # time.sleep(5)

    # # 开始播放了
    # # 这时，就需要时不时点击一下 是否连续播放的按钮
    # # 获取 切换是否连续播放按钮元素
    # switch_autoplay_btn_selector = r'#app > div > dl > div > span.ivu-switch.ivu-switch-default'
    # # 连续播放时，该按钮多出的类名
    # switch_autoplay_btn_enable_class = r'ivu-switch-checked'
    # # 让 程序在一定的条件之下，再关闭
    # script_status = True
    # while_count = 0
    # while(script_status):
    #     # 判断是否 正在播放
    #     time.sleep(10)
    #     # 视频控制按钮 选择器
    #     video_control_btn_xpath = r'/html/body/div[1]/div/div/div[1]/div[1]/div[1]'
    #     # 视频控制按钮 元素
    #     video_control_btn_element = getElementByXpath(web_driver,video_control_btn_xpath)
    #     # 获取 视频控制按钮元素的 类名
    #     video_control_btn_classlist = getAttributeByElementObject(video_control_btn_element,'class')
    #     # 暂停
    #     pause = r'pause'
    #     # 正在播放
    #     palying = r'playing'
    #     # 如果 处于 暂停状态，则点击按钮，让其处于 播放状态
    #     if(pause in video_control_btn_classlist):
    #         clickElementByElementObject(video_control_btn_element)

    #     time.sleep(60)

    #     # 连续播放 按钮是否打开
    #     # 通过 让按钮一直打开，来保证 视频一直播放下去
    #     # 判断该按钮的状态（通过该元素的 类名列表中是否有 ivu-switch-checked 类名即可）
    #     # 如果，该按钮 处于关闭状态，即如果 没有该类名时，自动点击该按钮
    #     switch_autoplay_btn_element = getElementById(web_driver,switch_autoplay_btn_selector)
    #     # 获取 该元素的类名列表
    #     switch_autoplay_btn_classList = getAttributeByElementObject(switch_autoplay_btn_element,'class')
    #     print(switch_autoplay_btn_classList)
    #     if(switch_autoplay_btn_enable_class not in switch_autoplay_btn_classList ):
    #         time.sleep(3)
    #         # 点击该 按钮
    #         clickElementByElementObject(switch_autoplay_btn_element)
    #     time.sleep(60)

    # 退出程序
    web_driver.quit()
