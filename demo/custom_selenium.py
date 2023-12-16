from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def initWebDriver(driverPath,isMobile = False,deviceName = "iPhone 6/7/8 5"):
    # 默认初始化为 电脑模式，而非手机模式，如需初始化为手机模式 只需将isMobile选项设置为 True
    if(isMobile):
        mobile_emulation = { "deviceName":  deviceName}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        web_driver = webdriver.Chrome(service = Service(driverPath),desired_capabilities = chrome_options.to_capabilities())
        return web_driver
    else:
        web_driver = webdriver.Chrome(service = Service(driverPath))
        return web_driver

def openChromeWebSite(webdriver,webSite):
    webdriver.get(webSite)

# 获取元素
# 根据id获取元素
def getElementById(webdriver,id):
    return webdriver.find_element(By.ID, id)

# 根据类名获取元素
def getElementByClassName(webdriver,className):
    return webdriver.find_element(By.CLASS_NAME, className)
# 根据类名获取多个元素
def getElementsByClassName(webdriver,className):
    return webdriver.find_elements(By.CLASS_NAME, className)

# 根据元素标签获取元素
def getElementByTagName(webdriver,tagName):
    return webdriver.find_element(By.TAG_NAME, tagName)
# 根据元素标签获取多个元素
def getElementsByTagName(webdriver,tagName):
    return webdriver.find_elements(By.TAG_NAME, tagName)

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
# 根据Css选择器获取元素（比如：button[type=submit] ）
def getElementByCssSelector(webdriver,cssSelector):
    return webdriver.find_element(By.CSS_SELECTOR,cssSelector)
# 根据Css选择器获取多个元素（比如：button[type=submit] ）
def getElementsByCssSelector(webdriver,cssSelector):
    return webdriver.find_elements(By.CSS_SELECTOR,cssSelector)

# 根据 xpath来获取 元素
def getElementByXpath(webdriver,xPath):
    return webdriver.find_element(By.XPATH, xPath)
    # 根据 xpath来获取 多个元素
def getElementsByXpath(webdriver,xPath):
    return webdriver.find_elements(By.XPATH, xPath)

# 向元素输入值
def sendKeysByElementObject(element,keys,mode = 'append'):
    if(mode != 'append'):
        element.clear()
    return element.send_keys(keys)
# 点击元素
def clickElementByElementObject(element):
    element.click()

# 鼠标悬浮 在元素上
def mouseoverElementByElementObject(webdriver,element):
    action_chains = ActionChains(webdriver)
    # 鼠标移动到 元素上
    action_chains.move_to_element(element).perform()

# 获取元素内容
# attribute可选值：
# text  元素文本
# input_text  输入框的值
# outerHTML  整个元素对应的HTML文本内容
# innerHTML  元素 内部 的HTML文本内容
# innerText 显示元素可见文本内容
# textContent 显示所有内容（包括display属性为none的部分）
# 
# class  类名
# 等等
def getAttributeByElementObject(element,attribute):
    if(attribute == 'text'):
        return element.text()
    if(attribute == 'input_text'):
        return element.get_attribute('value')
    return element.get_attribute(attribute)



# 切换至 外部主html文件中(即：切换到原来的html文件中)
def switchToDefalutHtml(webdriver):
    webdriver.switch_to.default_content()
    
# 切换至 iframe框架中引入的html文件中(即：切换到iframe中)
def switchToIframeHtmlByIframeIdOrName(webdriver,idOrName):
    webdriver.switch_to.frame(idOrName)


# 窗口
# 得到当前窗口大小
def getCurrentWindowSize(webdriver):
    return webdriver.get_window_size()
# 设置当前窗口大小
def setCurrentWindowSize(webdriver,size = {"x":0,"y":0}):
    return webdriver.set_window_size(size.x, size.y)
# 获取当前窗口信息
def getCurrentInfo(webdriver,title = True,url = False):
    if(url):
        return webdriver.current_url
    else:
        return webdriver.title
# 保存当前 窗口句柄
def getCurrentWindowHandle(webdriver):
    return webdriver.current_window_handle
# 切换窗口 并返回 窗口句柄
def switchToWindowByHandle(webdriver,handle):
    return webdriver.switch_to.window(handle)
# 通过 窗口标题 来切换至对应的窗口，并返回对应窗口的窗口句柄
def switchToWindowByTitle(webdriver,title):
    # 赋初值
    current_window = getCurrentWindowHandle(webdriver)
    for handle in webdriver.window_handles:
        # 先切换窗口，然后通过 窗口标题来判断 当前窗口是否是对应的窗口
        current_window = switchToWindowByHandle(webdriver,handle)
        # 根据窗口的标题栏，判断是不是要操作的那个窗口
        if title in webdriver.title:
            # 是该窗口 则跳出循环 并返回 该窗口句柄
            break
    return current_window

# 冻结窗口
def freezeWindow():
    excuteJavascript('debugger')

# 截屏 并保存至自定义路径中
def screenshotSaveAsCustomPath(webdriver,customPath):
    webdriver.get_screenshot_as_file(customPath)

# 执行 javascript 并返回其结果
def excuteJavascript(webdriver,javaScript,arg = None):
    if(arg):
        webdriver.execute_script(javaScript.replace(r'${0}',r'arguments[0]'), arg)
    else:
        webdriver.execute_script(javaScript)



# 弹出窗口(pop up 弹出) 的确认与取消（可以是 alert的确认和获取内容  confirm的确认和取消和获取内容）
# 弹窗确认
def popupWindowAccept(webdriver):
    webdriver.switch_to.alert.accept()
# 弹窗取消
def popupWindowCancel(webdriver):
    webdriver.switch_to.alert.dismiss()
# 弹窗内容
def popupWindowContent(webdriver):
    return webdriver.switch_to.alert.text
# 向弹窗输入内容
def inputPopupWindowContent(webdriver,content):
    webdriver.switch_to.alert.send_keys(content)



