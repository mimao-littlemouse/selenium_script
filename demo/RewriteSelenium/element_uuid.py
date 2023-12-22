# 便于生成uuid元素标识并进行加密和解密操作
import uuid
# 导入哈希加密（使用 md5加密方式）
import hashlib

# 获取属性名称
def get_attr_name():
    return 'selenium_element'

# 获取元素标识
def get_mask():
    # 生成最基本的UUID (UUID4)
    # 用于元素标识
    uuid_mark = uuid.uuid4()
    # 实例化加密对象
    md5=hashlib.md5()
    # 加密文本
    md5_text = str(uuid_mark).replace('-','_')
    # 进行加密操作
    md5.update(md5_text.encode('utf-8'))
    # 返回加密后的结果
    return f'{get_attr_name()}-{md5.hexdigest()}'