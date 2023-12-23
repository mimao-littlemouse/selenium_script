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

# 自定义类
from .selenium_element import Selenium_Element
# 导入 元素标识符
from . import element_uuid

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
def getElement(webdriver: WebDriver,selector: str = 'id',selector_value: str = '',is_list:bool = False) -> Union[WebElement,List[WebElement],None]:
    try:
        # id 选择器（通过id获取到的元素有且只有一个）
        if(selector == 'id'):
            return webdriver.find_element(By.ID, selector_value)
        elif(selector == 'classname'):
            # 类名选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.CLASS_NAME, selector_value)
            else:
                return webdriver.find_element(By.CLASS_NAME, selector_value)
        elif(selector == 'tagname'):
            # 标签选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.TAG_NAME, selector_value)
            else:
                return webdriver.find_element(By.TAG_NAME, selector_value)
        elif(selector == 'css'):
            # css选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.CSS_SELECTOR, selector_value)
            else:
                return webdriver.find_element(By.CSS_SELECTOR, selector_value)
        elif(selector == 'xpath'):
            # xpath选择器
            # 如果是获取多个元素，即 返回多个元素列表
            if(is_list):
                return webdriver.find_elements(By.XPATH, selector_value)
            else:
                return webdriver.find_element(By.XPATH, selector_value)
        else:
            # 不是以上 选项直接返回空
            return None
    except NoSuchElementException as exec:
        print(f'except: {exec} \n')
        excuteJavascript(webdriver,'debugger')
        print(f'没找到{selector}选择器对应{selector_value} 元素对象或集合\n输入exit 可退出程序')
        while(input()=='exit'):
            webdriver.quit()
        return None

# 通过指定的maskid来获取元素
def getElementByMaskid(webdriver: WebDriver,*,maskid: str) -> Union[WebElement,None]:
    try:
        return webdriver.find_element(By.CSS_SELECTOR, f'[{element_uuid.get_attr_name()}="{maskid}"]')
    except NoSuchElementException as exec:
        print(f'except: {exec} \n')
        excuteJavascript(webdriver,'debugger')
        print(f'输入exit 可退出程序')
        while(input()=='exit'):
            webdriver.quit()
        return None

# 获取元素内容
# 元素文本 element.text
# 输入框的值 element.get_attribute('value')
# outerHTML  整个元素对应的HTML文本内容
# innerHTML  元素 内部 的HTML文本内容
# innerText 显示元素可见文本内容
# textContent 显示所有内容（包括display属性为none的部分）
# 
# class  类名
# 等等
# element.get_attribute(attribute)

# 对元素内容 进行获取（采用 执行 javascript的方式实现）
# 比如：获取指定元素的属性等等  该方法默认 通过css selector的方式获取到元素
def getElementContent(webdriver: WebDriver,element: WebElement,get_type: str,get_key: str = None) -> None:
    # 提前声明 获取元素的脚本
    getelement_script = ''
    # 后面 根据所给参数实现相应获取元素 内容的功能
    if(get_type == 'attr'):
        getelement_script = getelement_script + f'''
return arguments[0].attribute('{get_key}')
'''
    elif(get_type == 'style'):
        getelement_script = getelement_script + f'''
return arguments[0].style.{get_key}
'''
    elif(get_type == 'id'):
        getelement_script = getelement_script + f'''
return arguments[0].id
'''
    elif(get_type == 'class'):
        getelement_script = getelement_script + f'''
return arguments[0].classList
'''
    elif(get_type == 'element'):
        if(get_key == 'text'):
            getelement_script = getelement_script + f'''
return arguments[0].innerText
'''
        elif(get_key == 'inner_html'):
            # 元素内部 html 
            getelement_script = getelement_script + f'''
return arguments[0].innerHTML
'''
        elif(get_key == 'outer_html'):
            # 元素内部 html 
            getelement_script = getelement_script + f'''
return arguments[0].outerHTML
'''
    # 执行 javascript 代码实现
    return webdriver.execute_script(getelement_script,element)

# 对元素内容 进行获取（采用 执行 javascript的方式实现）
# 比如：获取指定元素的属性等等  该方法默认 通过css selector的方式获取到元素
def getElementContentBySelector(webdriver: WebDriver,selector_value: str,get_type: str,get_key: str = None) -> None:
    # 提前声明 获取元素的脚本
    getelement_script = ''
    # 后面 根据所给参数实现相应获取元素 内容的功能
    getelement_script = f'''
let el = document.querySelector('{selector_value}')
'''
    if(get_type == 'attr'):
        getelement_script = getelement_script + f'''
return el.attribute('{get_key}')
'''
    elif(get_type == 'style'):
        getelement_script = getelement_script + f'''
return el.style.{get_key}
'''
    elif(get_type == 'id'):
        getelement_script = getelement_script + f'''
return el.id
'''
    elif(get_type == 'class'):
        getelement_script = getelement_script + f'''
return el.classList
'''
    elif(get_type == 'element'):
        if(get_key == 'text'):
            getelement_script = getelement_script + f'''
return el.innerText
'''
        elif(get_key == 'inner_html'):
            # 元素内部 html 
            getelement_script = getelement_script + f'''
return el.innerHTML
'''
        elif(get_key == 'outer_html'):
            # 元素内部 html 
            getelement_script = getelement_script + f'''
return el.outerHTML
'''
    # 执行 javascript 代码实现
    return webdriver.execute_script(getelement_script)


# 对元素内容 进行操作（采用 执行 javascript的方式实现）
# 比如：设置指定元素的属性  该方法默认 通过指定的元素 来设置元素信息
def setElement(webdriver: WebDriver,element: WebElement,modify_type: str,modify_key: str,modify_value: str) -> None:
    # 定义 设置元素的脚本
    setelement_script = ''
    # 根据所给的参数 来设置元素
    if(modify_type == 'attr'):
        setelement_script = setelement_script + f'''
arguments[0].setAttribute('{modify_key}','{modify_value}')
'''
    elif(modify_type == 'style'):
        setelement_script = setelement_script + f'''
arguments[0].style.{modify_key} = {modify_value}
'''
    elif(modify_type == 'id'):
        setelement_script = setelement_script + f'''
arguments[0].id = '{modify_key}'
'''
    elif(modify_type == 'class'):
        if(modify_key == 'remove'):
            setelement_script = setelement_script + f'''
arguments[0].classList.remove('{modify_value}')
'''
        elif(modify_key == 'add'):
            setelement_script = setelement_script + f'''
arguments[0].classList.add('{modify_value}')
'''
    elif(modify_type == 'element'):
        if(modify_key == 'text'):
            setelement_script = setelement_script + f'''
arguments[0].innerText = '{modify_value}'
'''
        elif(modify_key == 'inner_html'):
            # 元素内部 html 
            setelement_script = setelement_script + f'''
arguments[0].innerHTML = '{modify_value}'
'''
        elif(modify_key == 'outer_html'):
            # 元素内部 html 
            setelement_script = setelement_script + f'''
arguments[0].outerHTML = '{modify_value}'
'''
    # 执行 javascript 代码实现
    webdriver.execute_script(setelement_script,element)

# 对元素内容 进行操作（采用 执行 javascript的方式实现）
# 比如：设置指定元素的属性  该方法默认 通过css selector的方式获取到元素并进行设置元素信息
def setElementBySelector(webdriver: WebDriver,selector_value: str,modify_type: str,modify_key: str,modify_value: str) -> None:
    setelement_script = f'''
let el = document.querySelector('{selector_value}')
'''
    if(modify_type == 'attr'):
        setelement_script = setelement_script + f'''
el.setAttribute('{modify_key}','{modify_value}')
'''
    elif(modify_type == 'style'):
        setelement_script = setelement_script + f'''
el.style.{modify_key} = {modify_value}
'''
    elif(modify_type == 'id'):
        setelement_script = setelement_script + f'''
el.id = '{modify_key}'
'''
    elif(modify_type == 'class'):
        if(modify_key == 'remove'):
            setelement_script = setelement_script + f'''
el.classList.remove('{modify_value}')
'''
        elif(modify_key == 'add'):
            setelement_script = setelement_script + f'''
el.classList.add('{modify_value}')
'''
    elif(modify_type == 'element'):
        if(modify_key == 'text'):
            setelement_script = setelement_script + f'''
el.innerText = '{modify_value}'

'''
        elif(modify_key == 'inner_html'):
            # 元素内部 html 
            setelement_script = setelement_script + f'''
el.innerHTML = '{modify_value}'
'''
        elif(modify_key == 'outer_html'):
            # 元素内部 html 
            setelement_script = setelement_script + f'''
el.outerHTML = '{modify_value}'
'''
    # 执行 javascript 代码实现
    webdriver.execute_script(setelement_script)

# 对元素内容 进行操作（采用 执行 javascript的方式实现）
# 比如：设置指定元素的属性  该方法默认 通过指定元素的maskid 来获取元素并设置元素信息
def setElementByMaskid(webdriver: WebDriver,maskid: str,modify_type: str,modify_key: str,modify_value: str) -> Union[Selenium_Element,None]:
    setelement_script = f'''
let el = document.querySelector('[{element_uuid.get_attr_name()}="{maskid}"]')
'''
    if(modify_type == 'attr'):
        setelement_script = setelement_script + f'''
el.setAttribute('{modify_key}','{modify_value}')
'''
    elif(modify_type == 'style'):
        setelement_script = setelement_script + f'''
el.style.{modify_key} = {modify_value}
'''
    elif(modify_type == 'id'):
        setelement_script = setelement_script + f'''
el.id = '{modify_key}'
'''
    elif(modify_type == 'class'):
        if(modify_key == 'remove'):
            setelement_script = setelement_script + f'''
el.classList.remove('{modify_value}')
'''
        elif(modify_key == 'add'):
            setelement_script = setelement_script + f'''
el.classList.add('{modify_value}')
'''
    elif(modify_type == 'element'):
        if(modify_key == 'text'):
            setelement_script = setelement_script + f'''
el.innerText = '{modify_value}'
'''
        elif(modify_key == 'inner_html'):
            # 元素内部 html 
            setelement_script = setelement_script + f'''
el.innerHTML = '{modify_value}'
'''
        elif(modify_key == 'outer_html'):
            # 元素内部 html 
            setelement_script = setelement_script + f'''
el.outerHTML = '{modify_value}'
'''
    # 执行 javascript 代码实现
    webdriver.execute_script(setelement_script)
    # 返回之前的 maskid
    return maskid

# 创建元素（采用 执行 javascript的方式实现）
# 默认采用 生成具有对应属性 并值为 maskid的元素的方式来产生 独立标识码的元素
# /表示 前方参数不能以关键字参数进行传参 *后面参数 必须以关键字传参 
# attrs styles class_list event_list maskid 可传可不传
# 返回 该创建元素的 唯一独立标识码 uuid 通过 md5 加密得来
def createElementMount(webdriver: WebDriver,tagname: str,/,*,attrs: Dict[str,str] = None,styles: Dict[str,str] = None,id: str = None,class_list: List[str] = None,event_list: Dict[str,str] = None,mount_container_maskid: str = None) -> Selenium_Element:
    create_element_script = f'''
let el = document.createElement('{tagname}')
'''
    # 添加属性
    if(attrs):
        for attr_name,attr_value in attrs.items():
            create_element_script = create_element_script + f'''
el.setAttribute('{ attr_name.strip() }','{ attr_value.strip() }')
'''
    # 添加id属性
    if(id):
        create_element_script = create_element_script + f'''
el.id = '{id.strip()}'
'''  
    # 添加类名
    if(class_list):
        for class_name in class_list:
            create_element_script = create_element_script + f'''
el.classList.add('{class_name.strip()}')
'''
    # 添加样式
    if(styles):
        for style_name,style_value in styles.items():
            create_element_script = create_element_script + f'''
el.style.{ style_name.strip() } = '{ style_value.strip() }'
'''

    # 为元素添加事件(直接将其方法的实现 写入body下 为body创建新的 script标签)
    if(event_list):
        # 创建 body 元素对象，以免多次创建
        create_element_script = create_element_script + r'''
let bodyelement_tomountelement = document.querySelector('body')
let script_element = null
'''
        for event,event_func in event_list.items():
            # event "事件名称 方法名称"
            event_name = event.strip().split(' ')[0]
            event_func_name = event.strip().split(' ')[1]
            # 对 方法进行 压缩（将多余空格都去掉）
            event_func = "".join(map(lambda x: x.strip(),event_func.split('\n')))
            # 添加换行符，以便区分其他方法
            # 将事件添加到创建脚本中
            create_element_script = create_element_script + f'''
// 创建该标签 并挂载到 body中
script_element = document.createElement('script')
bodyelement_tomountelement.append(script_element)
script_element.type="text/javascript"
// 将方法内容写入 script中
script_element.innerText = script_element.innerText + '{event_func}'
// 将 事件名称属性设置到元素上
el.setAttribute('{ event_name }', '{ event_func_name }')
'''

    # 返回 构建的元素对象的标识符
    # 获取 uuid加密标识符 并将该标识符放入元素中
    uuid_attr_name = element_uuid.get_attr_name()
    uuid_mask = element_uuid.get_mask()
    create_element_script = create_element_script + f'''
el.setAttribute('{ uuid_attr_name }','{ uuid_mask }')
'''
    # 将元素添加到 指定元素中
    # 如果 元素识别id 为None，则表示 直接挂载至 body中
    if(not mount_container_maskid):
        create_element_script = create_element_script + f'''
let body_element = document.querySelector('body')
body_element.append(el)
'''  
    else:
        create_element_script = create_element_script + f'''
let container_element = document.querySelector('[{uuid_attr_name}="{mount_container_maskid}"]')
container_element.append(el)
'''  
    # print(f'359 create_element_script：{create_element_script}')
    # 执行 javascripit 代码 实现创建元素的功能
    webdriver.execute_script(create_element_script)
    # 返回该元素的识别id
    return uuid_mask

# 挂载元素（将 元素挂载到 元素容器里）
def mountElement(webdriver,mount_container_element: WebElement = None,mount_element: WebElement = None) -> None:
    if(mount_element and mount_container_element):
        mount_script = '''
arguments[0].append(arguments[1])
'''
        # 执行 javscript 代码实现
        webdriver.execute_script(mount_script,mount_container_element,mount_element)


# 对输入框进行操作
# element.send_keys() 以追加的方式向元素 添加内容
# element.clear() 清除元素中的内容

# 鼠标悬浮 在元素上
def mouseoverElement(webdriver: WebDriver,element: WebElement) -> None:
    action_chains = ActionChains(webdriver)
    # 鼠标移动到 元素上
    action_chains.move_to_element(element).perform()


# 切换至 外部主html文件中(即：切换到原来的html文件中)
def switchToDefalutHtml(webdriver: WebDriver) -> None:
    webdriver.switch_to.default_content()
    
# 切换至 iframe框架中引入的html文件中(即：切换到iframe中)
# 使用 css selector 来获取iframe元素 来实现切换
def switchToIframeHtmlBySelector(webdriver: WebDriver,css_selector: str) -> None:
    webdriver.switch_to.frame(webdriver.find_elements(By.CSS_SELECTOR, css_selector))

# 切换至 iframe框架中引入的html文件中(即：切换到iframe中)
# 使用 iframe元素 来实现切换
def switchToIframeHtmlByElement(webdriver: WebDriver,element: WebElement) -> None:
    webdriver.switch_to.frame(element)


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
def excuteJavascript(webdriver: WebDriver,javaScript: str) -> Union[int,str,bool,None]:
    return webdriver.execute_script(javaScript)

# 指定特定元素 执行特定的javascript代码( 书写javascript代码时 arguments[0] 可代替 传入的元素进行书写 )
def excuteJavscriptByElement(webdriver: WebDriver,javaScript: str,element: WebElement) -> Union[int,str,bool,None]:
    return webdriver.execute_script(javaScript,element)

# 指定多个特定元素 执行特定的javascript代码( 书写javascript代码时 arguments[i] 可代替 传入的元素进行书写 其中i为传入的元素个数的索引 以0开头)
def excuteJavscriptByElements(webdriver: WebDriver,javaScript: str,*element: WebElement) -> Union[int,str,bool,None]:
    return webdriver.execute_script(javaScript,*element)


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

# 通过执行 javascript 来点击元素（根据 已有的 元素）
def clickByJavascriptByElement(webdriver: WebDriver,element: WebElement) -> None:
    webdriver.execute_script('arguments[0].click()',element)

# 通过执行 javascript 来点击元素（根据 css selector）
def clickByJavascriptByCSSselector(webdriver: WebDriver,css_selector: str) -> None:
    webdriver.execute_script('arguments[0].click()',webdriver.find_element(By.CSS_SELECTOR, css_selector))

# 通过执行 javascript 来让元素滚动到视图可见区域（根据 已有的 元素）
def scrollIntoViewByElement(webdriver: WebDriver,element: WebElement) -> None:
    webdriver.execute_script('arguments[0].scrollIntoView()',element)

# 通过执行 javascript 来让元素滚动到视图可见区域（根据 css selector）
def scrollIntoViewByCSSselector(webdriver: WebDriver,css_selector: str) -> None:
    webdriver.execute_script('arguments[0].scrollIntoView()',webdriver.find_elements(By.CSS_SELECTOR, css_selector))

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
# 等待 window alert 、窗口 title url
def waitUtilWebdriver(webdriver: WebDriver,condition:str,condition_value:str='',max_wait_time:int=10) -> WebDriver:
    # 创建WebDriverWait实例
    webdriver_wait = WebDriverWait(webdriver, max_wait_time)
    # 后面 根据 condition 来决定后面的功能
    if(condition == 'windownum'):
        return webdriver_wait.until(expected_conditions.number_of_windows_to_be(condition_value))
    elif(condition == 'newwindow'):
        return webdriver_wait.until(expected_conditions.new_window_is_opened(condition_value))
    elif(condition == 'alert'):
        return webdriver_wait.until(expected_conditions.alert_is_present())

    if(condition == 'equal_title'):
        return webdriver_wait.until(expected_conditions.title_is(condition_value))
    elif(condition == 'contain_title'):
        # contain
        return webdriver_wait.until(expected_conditions.title_contains(condition_value))
    elif(condition == 'notequal_title'):
        # notequal
        return webdriver_wait.until(expected_conditions.none_of(expected_conditions.title_is(condition_value)))
    elif(condition == 'notcontain_title'):
        # notcontain
        return webdriver_wait.until(expected_conditions.none_of(expected_conditions.title_contains(condition_value)))
    
    if(condition == 'equal_url'):
        return webdriver_wait.until(expected_conditions.url_to_be(condition_value))
    elif(condition == 'contain_url'):
        # contain
        return webdriver_wait.until(expected_conditions.url_contains(condition_value))
    elif(condition == 'notequal_url'):
        # notequal
        return webdriver_wait.until(expected_conditions.url_changes(condition_value))
    elif(condition == 'notcontain_url'):
        # notcontain
        return webdriver_wait.until(expected_conditions.none_of(expected_conditions.url_contains(condition_value)))
    
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
    print('wait',selector_value)
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
