## title_is(title: str)

title：期望的页面标题
判断当前页面标题是否是title

## title_contains(title: str)

title：期望的页面标题
判断当前页面标题是否包含title

## presence_of_element_located(locator: Tuple[str, str])

locator：元素的定位信息
元素是否存在于dom中，不一定需要显示在视图


locator：元素的定位信息
判断此定位的一组元素至少有一个在dom中，不一定需要显示在视图

## presence_of_all_elements_located(locator)

url: 符合正则表达式的网站，所以这里符合条件的都可通过

## url_matches(pattern: str)


url：期望的页面网址
判断页面网址是否为url

## url_contains(url: str)

url：期望的页面网址
判断页面网址是否为url

## url_to_be(url: str)

url：期望的页面网址
判断页面网址不是url

## url_changes(url: str)

url：期望的页面网址
判断此定位的元素是否可见

## visibility_of_element_located(locator: Tuple[str, str])

locator：元素的定位信息
判断此元素是否可见

## visibility_of(element)

element：所获得的元素
判断此定位的一组元素是否至少存在一个

## visibility_of_any_elements_located(locator)

locator：元素的定位信息
判断此定位的一组元素全部可见

## visibility_of_all_elements_located(locator)

locator：元素的定位信息
判断此定位中是否包含text_的内容

## text_to_be_present_in_element(locator, text_)

locator：元素的定位信息
text_：期望的文本信息
判断此定位中的value属性中是否包含text_的内容

## text_to_be_present_in_element_value(locator, text_)

locator：元素的定位信息
text_：期望的文本信息
判断定位的元素是否为frame，并直接切换到这个frame中

## text_to_be_present_in_element_attribute(locator: Tuple[str, str], attribute_: str, text_: str)

locator：元素的定位信息
attribute_: 属性名称
text_：期望的属性值

## frame_to_be_available_and_switch_to_it(locator)

locator：元素的定位信息
判断定位的元素是否不可见

## invisibility_of_element_located(locator)

locator：元素的定位信息
判断此元素是否不可见

## invisibility_of_element(element)

element：所获得的元素
判断所定位的元素是否不可见

## element_to_be_clickable(locator)

locator：元素的定位信息
判断此元素是否可点击

## staleness_of(element)

element：所获得的元素
判断该元素是否不再附加在dom中
直到元素不再附加在dom中

## element_to_be_selected(element)

element：所获得的元素
判断定位的元素是否被选中

## element_located_to_be_selected(locator)

locator：元素的定位信息
判断该元素被选中状态是否和期望状态相同

## element_selection_state_to_be(element,Boolean)

element：所获得的元素
Boolean：期望的状态（True/False）
判断定位的元素被选中状态是否和期望状态相同

## element_located_selection_state_to_be(locator,Boolean)

locator：元素的定位信息
Boolean：期望的状态（True/False）
判断当前浏览器页签数量是否为num

## number_of_windows_to_be(num)

num：期望的页签数量
判断是否有这么多窗口

## new_window_is_opened(handles)

handles：页签
是否打开了新窗口，句柄并且增加




## alert_is_present()
检查当前是否存在警报的期望，并切换到它

## element_attribute_to_include(locator: Tuple[str, str], attribute_: str)
该元素是否包括了 这个属性

## any_of(*expected_conditions: Callable[[D], T])

*expected_conditions: Callable[[D], T] 可变参数

多个预期条件中的任何一个都为真。

等同于逻辑“OR”。返回第一个匹配的结果条件，如果没有，则为 False

## all_of(*expected_conditions: Callable[[D], Union[T, Literal[False]])

*expected_conditions: Callable[[D], Union[T, Literal[False]]  可变参数

所有多个预期条件都为真的期望。

等同于逻辑上的“AND”。
返回值：
当不满足任何 ExpectedCondition 时：False
当满足所有 ExpectedConditions 时：包含每个 ExpectedCondition 返回值的列表

## none_of(*expected_conditions: Callable[[D], Any])

*expected_conditions: Callable[[D], Any]  可变参数

期望 1 个或多个预期条件都不成立。

等同于逻辑上的“NOT-OR”。返回一个 Boolean 值

    
