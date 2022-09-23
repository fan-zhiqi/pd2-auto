import  os
'''
producer为请求路径，对应requests_session修改
'''

ABS_PATH = os.path.abspath(__file__)
DIR_NAME = os.path.dirname(ABS_PATH)


root_path = str(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
__all__ = [
    "root_path",
]
