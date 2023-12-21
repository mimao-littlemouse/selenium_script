# 该文件 是对selenium的第二次封装，便于进行测试
import sys
import time
from typing import List,Dict
from typing import Optional
from typing import Union

# 初始化 web driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# 获取元素
from selenium.webdriver.common.by import By
# 鼠标
from selenium.webdriver.common.action_chains import ActionChains
# 等待
from selenium.webdriver.support.ui import WebDriverWait
# 等待条件方法
from selenium.webdriver.support import expected_conditions
# selenium中的类型
# webdriver类型
from selenium.webdriver.chrome.webdriver import WebDriver
# web元素
from selenium.webdriver.remote.webelement import WebElement
# 异常类型
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException

# 初始化 webdriver
def initWebDriver(driverPath: str,isMobile: bool = False,deviceName: str = "iPhone 6/7/8 5") -> WebDriver:
    # 默认初始化为 电脑模式，而非手机模式，如需初始化为手机模式 只需将isMobile选项设置为 True
    try:
        if(isMobile):
            mobile_emulation = { "deviceName":  deviceName}
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            web_driver = webdriver.Chrome(service = Service(driverPath),desired_capabilities = chrome_options.to_capabilities())
        else:
            web_driver = webdriver.Chrome(service = Service(driverPath))
        # 返回 webdriver对象
        return web_driver
    except WebDriverException as exce:
        print(exce('初始化失败，请检查 初始化参数是否正确'))
        time.sleep(3)
        web_driver.quit()

# 通过 id tagname selector xpath获取元素，斌返回该元素对象或元素集合
# css选择器（学习地址推荐：https://www.w3school.com.cn/cssref/css_selectors.asp）
# css 子代 后代 组合 选择器
# 子代：tag1>tag2  紧邻tag1下的所有tag2元素
# 后代：tag1 tag2  tag1后所有的tag2元素
# 组合：tag1,tag2  所有tag1和tag2标签
# 父元素子选择器
# tag:nth-child(1)  父元素下第一个元素 并且该元素为 tag标签
# tag:nth-last-child(1)  父元素下倒数第一个元素 并且该元素为 tag标签
# tag:nth-of-type(1)  父元素下第一个类型为tag标签的元素
# tag:nth-last-of-type(1)  父元素下倒数第一个类型为tag标签的元素
# tag:nth-child(even)  父元素下偶数节点元素 并且该元素为 tag标签
# tag:nth-child(odd)  父元素下奇数节点元素 并且该元素为 tag标签
# tag:nth-last-of-type(even)  父元素下偶数节点并类型为tag标签的元素
# tag:nth-last-of-type(odd)  父元素下奇数节点并类型为tag标签的元素
# 兄弟节点选择器
# 相邻兄弟元素：tag1+tag2 紧邻tag1标签的兄弟元素tag2元素
# 所有兄弟元素：tag1~tag2 tag1标签的所有兄弟元素tag2元素
# css属性选择器的写法
# tag[attribute*="keyword"] 表示：tag标签里面的属性包含了keyword关键字的所有tag标签元素
# tag[attribute^="keyword"] 表示：tag标签里面的属性值以keyword关键字开头的所有tag标签元素
# tag[attribute$="keyword"] 表示：tag标签里面的属性值以keyword关键字结尾的所有tag标签元素
# tag[attribute1="keyword"][attribute1="keyword"] 表示：tag标签里面的属性1为keyword关键字并且属性2为keyword关键字的tag标签元素
def getElement(webdriver: WebDriver,type: str = 'id',value: str = '',is_list:bool = False) -> Union[WebElement,List[WebElement]]:
    try:
        # id 选择器（通过id获取到的元素有且只有一个）
        if(type == 'id'):
            return webdriver.find_element(By.ID, value)
        elif(type == 'classname'):
            # 类名选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.CLASS_NAME, value)
            else:
                return webdriver.find_element(By.CLASS_NAME, value)
        elif(type == 'tagname'):
            # 标签选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.TAG_NAME, value)
            else:
                return webdriver.find_element(By.TAG_NAME, value)
        elif(type == 'css'):
            # css选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.CSS_SELECTOR, value)
            else:
                return webdriver.find_element(By.CSS_SELECTOR, value)
        elif(type == 'xpath'):
            # xpath选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.XPATH, value)
            else:
                return webdriver.find_element(By.XPATH, value)
        else:
            # 不是以上 选项直接返回空
            return None
    except NoSuchElementException as exec:
        print(f'except: {exec} \n')
        excuteJavascript(webdriver,'debugger')
        print(f'没找到{type}选择器对应{value} 元素对象或集合\n输入exit 可退出程序')
        while(input()=='exit'):
            webdriver.quit()
        return None

# 对元素内容 进行操作
# element.send_keys() 以追加的方式向元素 添加内容
# element.clear() 清除元素中的内容

# 鼠标悬浮 在元素上
def mouseoverElement(webdriver: WebDriver,element: WebElement) -> None:
    action_chains = ActionChains(webdriver)
    # 鼠标移动到 元素上
    action_chains.move_to_element(element).perform()

# 获取元素内容
# 元素文本 element.text()
# 输入框的值 element.get_attribute('value')
# outerHTML  整个元素对应的HTML文本内容
# innerHTML  元素 内部 的HTML文本内容
# innerText 显示元素可见文本内容
# textContent 显示所有内容（包括display属性为none的部分）
# 
# class  类名
# 等等
# element.get_attribute(attribute)

# 切换至 外部主html文件中(即：切换到原来的html文件中)
def switchToDefalutHtml(webdriver: WebDriver) -> None:
    webdriver.switch_to.default_content()
    
# 切换至 iframe框架中引入的html文件中(即：切换到iframe中)
# 使用 css selector 来获取iframe元素 来实现切换
def switchToIframeHtml(webdriver: WebDriver,css_selector: str) -> None:
    webdriver.switch_to.frame(webdriver.find_elements(By.CSS_SELECTOR, css_selector))



# 窗口

# 窗口大小
# 得到当前窗口大小
def getCurrentWindowSize(webdriver: WebDriver) -> Dict:
    return webdriver.get_window_size()
# 设置当前窗口大小
def setCurrentWindowSize(webdriver: WebDriver,size: Dict = {"x":0,"y":0}) -> None:
    webdriver.set_window_size(size.x, size.y)

# 获取当前窗口信息
# 获取窗口标题
# webdriver.title
# 获取窗口当前url地址
# webdriver.current_url

# 获取当前 窗口句柄
def getCurrentWindowHandle(webdriver: WebDriver) -> int:
    return webdriver.current_window_handle
# 切换窗口
def switchToWindowByHandle(webdriver: WebDriver,handle: int) -> None:
    webdriver.switch_to.window(handle)
# 通过 窗口标题 来切换至对应的窗口，并返回对应窗口的窗口句柄
def switchToWindowByTitle(webdriver: WebDriver,title: str) -> int:
    # 赋初值
    current_window_handle = getCurrentWindowHandle(webdriver)
    for handle in webdriver.window_handles:
        # 先切换窗口，然后通过 窗口标题来判断 当前窗口是否是对应的窗口
        current_window_handle = switchToWindowByHandle(webdriver,handle)
        # 根据窗口的标题栏，判断是不是要操作的那个窗口
        if title in webdriver.title:
            # 是该窗口 则跳出循环 并返回 该窗口句柄
            break
    return current_window_handle

# 通过 窗口索引 来切换至对应的窗口，并返回对应窗口的窗口句柄
def switchToWindowByIndex(webdriver: WebDriver,index: int) -> int:
    # 初始化 当前窗口句柄
    current_window_handle = getCurrentWindowHandle(webdriver)
    # 获取 当前所有窗口的句柄列表
    all_window_handles = webdriver.window_handles
    # 判断 传入的参数index是否会超过索引 超过索引，则返回当前窗口 并提示开发者当前 出现索引错误
    try:
        if(index<0 or index >=all_window_handles.__len__()):
            raise IndexError
        else:
            current_window_handle = all_window_handles[index]
    except IndexError as error:
        # 当前文件名
        print(f"传入参数的索引无效 \n{error}")
    finally:
        return current_window_handle


# 截屏 并保存至自定义路径中
def screenshotSaveAsCustomPath(webdriver: WebDriver,customPath: str) -> bool:
    return webdriver.get_screenshot_as_file(customPath)

# 执行 javascript 并返回其结果
def excuteJavascript(webdriver: WebDriver,javaScript: str,arg: Union[WebElement,str] = None) -> Union[int,str,bool]:
    if(arg):
        return webdriver.execute_script(javaScript.replace(r'${0}',r'arguments[0]'), arg)
    else:
        return webdriver.execute_script(javaScript)

# 通过 执行 javascript代码实现
# 获取 窗口缩放比例
def getWindowZoomRatio(webdriver: WebDriver) -> float:
    return webdriver.execute_script('return window.devicePixelRatio')
# 设置窗口缩放至指定比例（默认设置为：100%）
def setWindowZoomRatio(webdriver: WebDriver,ratio: float = 1) -> None:
    # 缩放之前的值
    zoomBeforeValue = getWindowZoomRatio(webdriver)
    # 将缩放之前的值与传过来的参数比较
    # 如果，它们不相等，才进行缩放操作
    if(zoomBeforeValue != ratio):
        zoomScript = f'document.body.style.zoom = {ratio}'
        webdriver.execute_script(zoomScript)

# 弹出窗口(pop up 弹出) 的确认与取消（可以是 alert的确认和获取内容  confirm的确认和取消和获取内容）
# 弹窗确认
def popupWindowAccept(webdriver: WebDriver) -> None:
    webdriver.switch_to.alert.accept()
# 弹窗取消
def popupWindowCancel(webdriver: WebDriver) -> None:
    webdriver.switch_to.alert.dismiss()
# 弹窗内容
def popupWindowContent(webdriver: WebDriver) -> str:
    return webdriver.switch_to.alert.text
# 向弹窗输入内容
def inputPopupWindowContent(webdriver: WebDriver,content: str) -> None:
    webdriver.switch_to.alert.send_keys(content)


# 等待 webdriver 的某个条件符合时
# 等待 window alert 
def waitUtilWebdriver(webdriver: WebDriver,key:str,value:str,max_wait_time:int=10) -> WebDriver:
    # 创建WebDriverWait实例
    webdriver_wait = WebDriverWait(webdriver, max_wait_time)
    # key 可选值  windownum窗口数量    newwindow是否有新窗口打开    alert是否有警告框打开
    # 对应可选值：窗口可能的数量        当前窗口的句柄列表            无参数
    if(key == 'windownum'):
        return webdriver_wait.until(expected_conditions.number_of_windows_to_be(value))
    elif(key == 'newwindow'):
        return webdriver_wait.until(expected_conditions.new_window_is_opened(value))
    elif(key == 'alert'):
        return webdriver_wait.until(expected_conditions.alert_is_present())
    else:
        raise "传入参数有问题"

# 等待 窗口 title url
def waitUtilWebdriver(webdriver: WebDriver,key:str,value:str,condition:str,max_wait_time:int=10) -> WebDriver:
    # 创建WebDriverWait实例
    webdriver_wait = WebDriverWait(webdriver, max_wait_time)
    # key 可选值： title url
    # condition 可选值： equal相等 contain包含 notequal不相等 nocontain不包含
    if(key == 'title'):
        # equal
        if(condition == 'equal'):
            return webdriver_wait.until(expected_conditions.title_is(value))
        elif(condition == 'contain'):
            # contain
            return webdriver_wait.until(expected_conditions.title_contains(value))
        elif(condition == 'noequal'):
            # notequal
            return webdriver_wait.until(expected_conditions.none_of(expected_conditions.title_is(value)))
        else:
            # nocontain
            return webdriver_wait.until(expected_conditions.none_of(expected_conditions.title_contains(value)))
    elif(key == 'url'):
        # equal
        if(condition == 'equal'):
            return webdriver_wait.until(expected_conditions.url_to_be(value))
        elif(condition == 'contain'):
            # contain
            return webdriver_wait.until(expected_conditions.url_contains(value))
        elif(condition == 'noequal'):
            # notequal
            return webdriver_wait.until(expected_conditions.url_changes(value))
        else:
            # nocontain
            return webdriver_wait.until(expected_conditions.none_of(expected_conditions.url_contains(value)))
    else:
        # 如果传入参数不符合上述，即 抛出错误
        raise "传入参数有问题"
    
# 等待元素
def waitUtilElement(webdriver,selector:str,selector_value,condition:str,condition_value:str = '',max_wait_time:int=10) -> Union[WebElement,List[WebElement]]:
    # 创建WebDriverWait实例
    webdriver_wait = WebDriverWait(webdriver, max_wait_time)
    locator = None
    # 根据传入的selector类型，来决定locator的值
    if(selector == 'id'):
        locator = (By.ID,selector_value)
    elif(selector == 'classname'):
        locator = (By.CLASS_NAME,selector_value)
    elif(selector == 'tagname'):
        locator = (By.TAG_NAME,selector_value)
    elif(selector == 'css'):
        locator = (By.CSS_SELECTOR,selector_value)
    elif(selector == 'xpath'):
        locator = (By.XPATH,selector_value)
    # 然后，根据condition来确定方法的功能

    # 元素是否在dom
    if(condition == 'in_dom'):
        # 元素在dom中  in_dom
        return webdriver_wait.until(expected_conditions.presence_of_element_located(locator))
    elif(condition == 'least_one_in_dom'):
        # 至少有一个 在dom中 least_one_in_dom
        return webdriver_wait.until(expected_conditions.presence_of_all_elements_located(locator))

    # 元素是否可见
    if(condition == 'one_visible'):
        # 一个元素可见 one_visible
        return webdriver_wait.until(expected_conditions.visibility_of_element_located(locator))
    elif(condition == 'all_visible'):
        # 所有元素可见 all_visible
         return webdriver_wait.until(expected_conditions.visibility_of_all_elements_located(locator))
    elif(condition == 'least_one_visible'):
        # 至少一个元素可见 
        return webdriver_wait.until(expected_conditions.visibility_of_any_elements_located(locator))
    elif(condition == 'not_visible' or condition == 'not_in_dom'):
        # 一个元素 要么不可见 要么不在dom上  not_visible  或   not_in_dom
        return webdriver_wait.until(expected_conditions.invisibility_of_element_located(locator))
    
    # 文本 在 元素
    if(condition == 'text_in_element'):
        # 文本在元素中 text_in_element
        return webdriver_wait.until(expected_conditions.text_to_be_present_in_element(locator,condition_value))
    elif(condition == 'text_in_elementvalue'):
        # 文本在元素的value中 text_in_elementvalue
        return webdriver_wait.until(expected_conditions.text_to_be_present_in_element_value(locator,condition_value))
    elif(condition == 'text_in_elementattr'):
        # 文本在元素的指定的属性中  text_in_elementattr
        return webdriver_wait.until(expected_conditions.text_to_be_present_in_element_attribute(locator,condition_value))
    elif(condition == 'attr_in_element'):
        # 在元素中包含指定的属性  attr_in_element
        return webdriver_wait.until(expected_conditions.element_attribute_to_include(locator,condition_value))
    
    # 元素是否可点击
    if(condition == 'clickable'):
        # 元素可点击
        return webdriver_wait.until(expected_conditions.element_to_be_clickable(locator))
    
    # 指定的iframe是否可用，如果可用直接切换至 iframe中 iframe_available
    if(condition == 'iframe_available'):
        return webdriver_wait.until(expected_conditions.element_to_be_clickable(locator))
