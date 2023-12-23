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
    usernameInput_element = waitUtilElement(webdriver,'id',username_id,'in_dom')
    # 获取 密码 输入框元素
    password_id = r'txtPwd'
    passwordInput_element = waitUtilElement(webdriver,'id',password_id,'in_dom')
    # 获取 登陆按钮 元素
    loginBtn_id = r'btnSign'
    loginBtn_element = waitUtilElement(webdriver,'id',loginBtn_id,'in_dom')
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

# 创建 selenium html 界面 返回创建元素的重要信息元素的选择器字典信息
def createSeleniumHtmlElementMount(webdriver: WebDriver) -> Dict[str,str]:
    # 创建 自动化界面 元素对象
    container_styles = {
        # 设置 定位于屏幕上
        "position":"fixed",
        "top":"60px",
        "right":"60px",
        # 宽高
        "width":"300px",
        "height":"200px",
        # 字体颜色
        "color":"white",
        # 字体大小
        "fontSize":"12px",
        # 背景颜色
        "background":"#8383f1",
        # 透明度
        "opcity":"0.9",
        # 圆角
        "borderRadius":"5px 10px 10px",
        # 使用 flex 布局
        "display":"flex",
        "flexDirection":"column",
        "justifyContent": "flex-start",
        "alignItems":"flex-start"
    }
    container_attrs = {
        # 设置元素可拖动
        "draggable":"true"
    }
    container_event = {
        "ondragstart startDrag(event)":'''
function startDrag(e){
    e.target.style.cursor = "move";
    e.target.dataset.startPositionX = e.offsetX;
    e.target.dataset.startPositionY = e.offsetY;
    e.target.style.opcity = 0.8;
}
'''     ,"ondragover dragover(event)":'''
function dragover(e){
    e.preventDefault();
}
'''     ,"ondragend dragend(event)":'''
function dragend(e){
    startX = e.target.dataset.startPositionX;
    startY = e.target.dataset.startPositionY;
    endX = e.offsetX;
    endY = e.offsetY;
    offsetX = endX - startX;
    offsetY = endY - startY;
    e.target.style.right = (Number((e.target.style.right).split("px")[0]) - offsetX) + "px";
    e.target.style.top = (Number((e.target.style.top).split("px")[0]) + offsetY) + "px";

    e.target.style.cursor = "default";
    e.target.style.opcity = 0.9;
}
'''
    }
    
    # 创建 自动化界面 容器
    selenium_html_element_maskid = createElementMount(webdriver,'div',styles=container_styles,attrs=container_attrs,event_list=container_event)
    # 定义 界面 信息
    # 定义 界面  行列数量
    selenium_html_element_row = 4
    selenium_html_element_column = 4
    # 标题（位于第一行）
    title_name_maskid = None
    # 课程名称 需要学习的时长 已学时长(位于第二行)
    course_name_maskid = None
    need_learn_duration_maskid = None
    now_learn_duration_maskid = None
    # 行通用样式
    row_styles = {
        # 宽高 高度设置为 每行等高
        "width":"100%",
        "height":f"{(1/selenium_html_element_row) * 100}%",
        # 采用 flex 布局
        "display":"flex",
        "justifyContent": "space-around",
        "alignItems":"center"
    }
    # 遍历 生成元素
    for row in range(1, (selenium_html_element_row + 1) ):
        # 创建 div 元素
        row_element_maskid = createElementMount(web_driver,'div',mount_container_maskid=selenium_html_element_maskid,styles=row_styles)
        column_element_maskid = None
        
        # 遍历 每一列
        for column in range(1,(selenium_html_element_column + 1) ):
            # 每列样式
            col_styles = {
                # 宽高 宽度设置为等宽
                "width":f"{(1/selenium_html_element_column) * 100 }%",
                "height": "100%",
                # 采用 flex 布局
                "display":"flex",
                "justifyContent": "center",
                "alignItems":"center"
            }
            # 根据 每一个重要信息所在位置 在每列进行处理时或不需要进行处理的时候 才进行添加选择器
            # 第一行，只需遍历一次就行 并且 只创建让第一行中 只有一列的标题（居中）
            if(row == 1 and column == 1):
                # 该列为 标题列 创建标题列元素
                # 重置 该列的宽度为 100%
                col_styles["width"] = "100%"
                # 并设置 鼠标图标 为可拖动
                col_styles["cursor"] = "move"
                # 设置标题大小
                col_styles["fontSize"] = "14px"
                title_name_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                column_element_maskid = setElementByMaskid(webdriver,title_name_maskid,'element','text','Selenium 自动化界面')
                break

            elif(row == 2 and column == 1):
                # 第二行 第一列 为课程名称标题
                # 创建列元素
                column_element_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                column_element_maskid = setElementByMaskid(webdriver,column_element_maskid,'element','text','课程标题')
                
            elif(row == 2 and column == 2):
                # 第二行 第二列 为总学习的时长标题
                # 创建列元素
                column_element_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                column_element_maskid = setElementByMaskid(webdriver,column_element_maskid,'element','text','总时长')
                
            elif(row == 2 and column == 3):
                # 第二行 第三列 为已学学习的时长标题
                # 创建列元素
                column_element_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                column_element_maskid = setElementByMaskid(webdriver,column_element_maskid,'element','text','已学时长')
            
            elif(row == 2 and column == 4):
                # 第二行 第四列 为还需学习的时长标题
                # 创建列元素
                column_element_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                column_element_maskid = setElementByMaskid(webdriver,column_element_maskid,'element','text','还需学习')
               
            elif(row == 3 and column == 1):
                # 第三行 第一列 为课程名称
                # 该列为 课程标题内容列 创建课程标题内容列元素
                course_name_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                course_name_maskid = setElementByMaskid(webdriver,course_name_maskid,'element','text','初始化中')
                
            elif(row == 3 and column == 2):
                # 第三行 第二列 为总学习时长
                # 该列为 总学习时长内容列 创建总学习时长内容列元素
                need_learn_duration_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                need_learn_duration_maskid = setElementByMaskid(webdriver,need_learn_duration_maskid,'element','text','0')
                
            elif(row == 3 and column == 3):
                # 第三行 第三列 已学学习的时长标题
                # 该列为 已学学习时长内容列 创建已学学习时长内容列元素
                now_learn_duration_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                now_learn_duration_maskid = setElementByMaskid(webdriver,now_learn_duration_maskid,'element','text','0')
            
            elif(row == 3 and column == 4):
                # 第三行 第四列 为还需要学习的时长标题
                # 该列为 还需要学习时长内容列 创建还需要学习时长内容列元素
                contiune_learn_duration_element_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                contiune_learn_duration_element_maskid = setElementByMaskid(webdriver,contiune_learn_duration_element_maskid,'element','text','0')

            elif(row == 4 and column == 1):
                # 第四行 第三列 为状态栏
                # 该列为 主要显示通知和进程
                col_styles["width"] = "100%"
                col_styles["padding"] = "2px 2px 15px 5px"
                col_styles["color"] = "black"
                col_styles["fontSize"] = "13px"
                col_styles["display"] = "flex"
                col_styles["justifyContent"] = "flex-start"
                col_styles["alignItems"] = "center"
                status_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                # 设置元素内容
                status_maskid = setElementByMaskid(webdriver,status_maskid,'element','text','状态良好')
                break

            else:
                # 创建普通元素
                column_element_maskid = createElementMount(webdriver,'div',mount_container_maskid=row_element_maskid,styles=col_styles)
                
            
    return {
        "container": selenium_html_element_maskid,
        "title": title_name_maskid,
        "course_name": course_name_maskid,
        "all_duration": need_learn_duration_maskid,
        "now_duration": now_learn_duration_maskid,
        "continue_duration": contiune_learn_duration_element_maskid,
        "status": status_maskid
    }

def updateSeleniumHtmlElementContent(webdriver: WebDriver,maskid:str,update_content: str) -> None:
    # 根据 maskid 设置元素的文本
    setElementByMaskid(webdriver,maskid,'element','text',update_content)

# 在 选课界面进行课程的选择
def chooseCourse(webdriver,all_term,current_term,course_name):
    # 首先 切换到含有课程的 iframe 中
    iframUrl_element = waitUtilElement(webdriver,'id','iframUrl','iframe_available')
    switchToIframeHtmlByElement(webdriver,iframUrl_element)
    # 点击全部学期按钮 默认显示最新学期的所有课程列表
    allTermBtn_selector = 'body > div.page.online > div.online-title > div.online-left > span:nth-child(2)'
    allTermBtn_element = getElement(webdriver,'css',allTermBtn_selector)
    # 等待元素出现在视图
    waitUtilElement(webdriver,'css',allTermBtn_selector,'one-visible')
    # 等待元素可点击
    waitUtilElement(webdriver,'css',allTermBtn_selector,'clickable')
    # 点击元素
    allTermBtn_element.click()
    # 现在 对于不同学期，做出指定的课程页面展开
    # 如果 该学期为最新学期，则无需展开直接进行课程选择  否则需要进行点击学期展开按钮
    if(all_term != current_term):
        # 每学期的展开按钮选择器
        term_button_selector = f'body > div.page.online > div.online-title > div.xq-content.all-xq > ul > li:nth-child({current_term})>div.single-xq > img' 
        term_button_element = getElement(webdriver,'css',term_button_selector)
        # 等待元素可见，并且可点击时，进行点击
        # 等待元素出现在视图
        waitUtilElement(webdriver,'css',term_button_selector,'one-visible')
        # 等待元素可点击
        waitUtilElement(webdriver,'css',term_button_selector,'clickable')
        # 点击元素
        term_button_element.click()
    
    # 该学期所有课程列表的容器选择器
    term_all_courselist_container_selector = f'body > div.page.online > div.online-title > div.xq-content.all-xq > ul > li:nth-child({current_term}) > div.single-xq-xl > div.single-lists'
    # 该学期所有课程列表的容器选择器元素对象
    term_all_courselist_container_elements = getElement(webdriver,'css',term_all_courselist_container_selector,is_list=True)
    # 根据课程名称 去找到指定的课程 并点击进入
    # 该元素的索引，用于方便 获取对应元素的选择器
    term_all_courselist_container_index = 1
    for term_all_courselist_container_element in term_all_courselist_container_elements:
        container_course_name = getElement(term_all_courselist_container_element,'css','div.list-content>div.list-content-right>h3').text
        # 根据得到的课程名称和给到的课程名称对比，如果一致则 点击对应按钮进行该课程的确认界面 
        if(course_name in container_course_name):
            # 让元素滚动到视图上
            excuteJavscriptByElement(webdriver,'arguments[0].scrollIntoView()',term_all_courselist_container_element)
            # 该元素选择器 
            course_element_selector = f'body > div.page.online > div.online-title > div.xq-content.all-xq > ul > li:nth-child({current_term}) > div.single-xq-xl > div.single-lists:nth-child({term_all_courselist_container_index})'
            # 等元素滚到了 视图上
            waitUtilElement(webdriver,'css',course_element_selector,'one_visible')
            # 缩小页面 比例
            setWindowZoomRatio(webdriver,0.8)
            # 等待该元素可点击
            waitUtilElement(webdriver,'css',course_element_selector,'clickable')
            # 获取元素
            course_element_element = getElement(term_all_courselist_container_element,'css','div.list-content>div.list-content-right>div.learn-button>ul>li:nth-child(1) >span')
            # 之后点击 进入 课程确认界面 并使用 js 执行的方式进行点击（此处有东西遮挡）
            excuteJavscriptByElement(webdriver,'arguments[0].click()',course_element_element)
            
            
            break
        term_all_courselist_container_index = term_all_courselist_container_index + 1
    # 切换到默认页面
    switchToDefalutHtml(webdriver)

# 进入课程观看确认界面  返回 还需学习的时长
def confirmCourse(webdriver) -> Dict[str,int]:
    # 首先 切换到含有课程的 iframe 中
    iframUrl_element = waitUtilElement(webdriver,'id','iframUrl','iframe_available')
    switchToIframeHtmlByElement(webdriver,iframUrl_element)
    # 获取课程信息
    # 该信息标签选择器
    info_selector = 'body > div.task_list.main > ul > li > div > div.titer-main-left > div > span'
    # 等待元素出现
    waitUtilElement(webdriver,'css',info_selector,'in_dom')
    # 获取元素
    info_element = getElement(webdriver,'css',info_selector)
    # 让元素滚动到 视图
    scrollIntoViewByElement(webdriver,info_element)
    # 等待元素出现在视图
    waitUtilElement(webdriver,'css',info_selector,'one_visible')
    course_duration_info = info_element.text
    # 课程总时长
    all_duration = int(course_duration_info.split('应学时长：')[1].split(' 分钟')[0])
    # 课程已学时长
    now_duration = int(course_duration_info.split('已学时长：')[1].split(' 分钟')[0])
    # 还需学习时长
    continue_duration = all_duration - now_duration
    
    # 点击 进入 课程观看界面
    enter_play_button_selector = 'body > div.task_list.main > ul > li > div > div.titer-main-right > div > a'
    waitUtilElement(webdriver,'css',enter_play_button_selector,'one_visible')
    waitUtilElement(webdriver,'css',enter_play_button_selector,'clickable')
    clickByJavascriptByCSSselector(webdriver,enter_play_button_selector)
    # 切换到默认页面
    switchToDefalutHtml(webdriver)
    # 返回 需要学习的时长
    return {
        "all_duration":all_duration,
        "now_duration":now_duration,
        "continue_duration":continue_duration
    }

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
    switch_autoplay_btn_element = getElement(webdriver,'css',switch_autoplay_btn_selector)
    # 获取 该元素的类名列表
    switch_autoplay_btn_classList = getElementContent(webdriver,switch_autoplay_btn_element,'class')
    # 只有当需要 设置为连续播放并且此时并未切换为连续播放  和 设置为不连续播放并且此时已经设置为连续播放时，才点击按钮进行切换
    if((playing and switch_autoplay_btn_enable_class not in switch_autoplay_btn_classList) and (not playing and switch_autoplay_btn_enable_class in switch_autoplay_btn_classList)):
        # 点击该 按钮
        clickByJavascriptByElement(webdriver,switch_autoplay_btn_element)
        time.sleep(3)

# 设置视频播放状态
def setCourseVideoPlayingState(webdriver,playing = True):
    # 视频控制按钮 选择器
    video_control_btn_xpath = r'/html/body/div[1]/div/div/div[1]/div[1]/div[1]'
    # 视频控制按钮 元素
    video_control_btn_element = getElement(webdriver,'xpath',video_control_btn_xpath)
    # 获取 视频控制按钮元素的 类名
    video_control_btn_classlist = getElementContent(webdriver,video_control_btn_element,'class')
    # 暂停
    pause = r'pause'
    # 如果 处于 暂停状态，则点击按钮，让其处于 播放状态
    if(pause in video_control_btn_classlist and playing):
        clickByJavascriptByElement(webdriver,video_control_btn_element)
    else: 
        # 否则 当处于播放状态，而且 playing为False，则进行操作，否则不进行操作
        if(pause not in video_control_btn_classlist and not playing):
            # 将鼠标悬停在 视频上
            mouseoverElement(webdriver,getElement(webdriver,'xpath','//*[@id="J_prismPlayer"]/video'))
            time.sleep(3)
            # 点击 暂停按钮
            clickByJavascriptByElement(getElement(webdriver,'xpath','/html/body/div[1]/div/div/div[1]/div[1]/div[9]/div[3]'))

def getCurrentCourseVideoDuration(webdriver) -> int:
    # 将鼠标悬停在 视频上
    mouseoverElement(webdriver,getElement(webdriver,'xpath','//*[@id="J_prismPlayer"]/video'))
    time.sleep(3)
    # 获取 该视频的时长
    currentVideoDurationString = getElementContent(webdriver,getElement(webdriver,'xpath','/html/body/div[1]/div/div/div[1]/div[1]/div[9]/div[4]/span[3]'),'element','text')
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
    littleChapter_index = ''
    currentLittleChapter_index = ''

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
            # 大章节元素的 选择器
            bigChapter_selector = '#navBox > div.typeBox1 > div > div > ul'
            bigChapter_elements = getElement(webdriver,'css',bigChapter_selector,is_list=True)
            bigChapter_cicleCount = 0
            for bigChapter_element in bigChapter_elements:
                bigChapter_cicleCount = bigChapter_cicleCount + 1
                # 有时候课程会有导言，所以这里需要进行判断 来进行不同于正常章节的操作
                if(bigChapter_cicleCount<=(course_all_chapter - course_big_chapter)):
                    # 相对于 导言这种，直接对应的就是 一大章就是一个视频，所以 直接获取到的就是一个小标题
                    littleChapter_element = getElement(bigChapter_element,'css','li>span:nth-child(2)')
                    if('activeVideo' in getElementContent(webdriver,littleChapter_element,'class')):
                        littleChapter_title = getElementContent(webdriver,littleChapter_element,'attr','title')
                        littleChapter_index = littleChapter_title.split(' ')[0]
                    pass
                else:
                    # 小章节
                    littleChapter_container_elements = getElement(bigChapter_element,'css','li>ul',is_list=True)
                    for littleChapter_container_element in littleChapter_container_elements:
                        littleChapter_element = getElement(littleChapter_container_element,'css','li>span:nth-child(2)')
                        if('activeVideo' in getElementContent(webdriver,littleChapter_element,'class')):
                            courseChapter_littleTitle = getElementContent(webdriver,littleChapter_element,'attr','title')
                            littleChapter_index = courseChapter_littleTitle.split(' ')[0]
            
            # 根据获取到的章节索引，算出当前所学时长
            if(littleChapter_index != currentLittleChapter_index):
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
            longtimeConfirmAlertStyleString_list = getElementContent(webdriver,getElement(webdriver,'xpath','/html/body/div[8]/div[2]/div'),'style').split(';')
            for longtimeConfirmAlertStyleString in longtimeConfirmAlertStyleString_list:
                if('display' in longtimeConfirmAlertStyleString):
                    if(longtimeConfirmAlertStyleString.split(':')[1] == 'block'):
                        # 当 页面播放时间太长时，会出现 弹出框来确认是否坐在电脑旁
                        # 点击 确认
                        clickByJavascriptByElement(webdriver,getElement(webdriver,'xpath','/html/body/div[8]/div[2]/div/div/div[2]/div[2]/button'))
                        time.sleep(5)
                        webdriver.refresh()

        cicle_count = cicle_count + 1


# 程序入口
if(__name__=='__main__'):
    try:
        # 初始化自动化窗口
        web_driver = initSeleniumWindowSetting()
        # 登陆网页
        loginPage(web_driver)
        # 等待弹出框出现
        waitUtilWebdriver(web_driver,'alert')
        # 对 弹出框 进行确认
        popupWindowAccept(web_driver)
        # 等待通知出现，并点击 查看通知详情
        # handleNotice(web_driver)
        # 等待弹出框出现
        waitUtilWebdriver(web_driver,'alert')
        # 再次对 弹出框 进行确认
        popupWindowAccept(web_driver)
        # 创建 selenium 展示界面
        selenium_elements_maskid = createSeleniumHtmlElementMount(web_driver)
        # 填写必要字段 去进行自动化观看视频
        # 当前所有学期
        all_term = 3
        # 课程学期
        current_term = 1
        # 课程名称
        course_name = "线性代数"
        # 设置课程标题提示
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["title"],course_name)
        # 正准备进入 选课界面
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["status"],'准备进入 选课界面')
        # 进入 选课页面
        chooseCourse(web_driver,all_term,current_term,course_name)
        # 正准备进入 确认界面
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["status"],'准备进入 确认界面')
        # 确认课程 进入播放页面(返回 总时长 已学时长)
        course_duration_info = confirmCourse(web_driver)
        # 正准备进入 确认界面
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["status"],'准备进入 播放界面')
        # 设置 总时长提示
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["all_duration"],course_duration_info["all_duration"])
        # 设置已学时长提示
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["now_duration"],course_duration_info["now_duration"])
        # 设置还需学习时长提示
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["continue_duration"],course_duration_info["continue_duration"])
        # 设置 已经进入播放界面 提示
        updateSeleniumHtmlElementContent(web_driver,selenium_elements_maskid["status"],'正在播放')
        # 将当前窗口句柄保存，并将窗口切换至新打开的窗口界面 
        currentWindow_handle = getCurrentWindowHandle(web_driver)
        # 将窗口切换至新打开的窗口界面 
        switchToWindowByTitle(web_driver,course_name)
        # 开始播放视频(并 随时监听视频播放时长 )
        addListenVideoPlay(web_driver,course_duration_info["continue_duration"],10,7)
    
    except Exception as error:
        print(error)
        # # 退出程序
        web_driver.quit()
