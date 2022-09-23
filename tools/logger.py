import logging.handlers
## 单例模式的思想：通过逻辑控制，只生成一个对象
import time
from setting import DIR_NAME
import logging
import sys

import allure


class GetLogger():
    '''
    当已经创建了logger对象的时候，那么之后就不在创建了，也就是只创建一次对象
    '''
    # 把logger对象的初始值设置为None
    logger = None

    # 创建logger，并且返回这个logger
    @classmethod
    def get_logger(cls):
        now = time.strftime('%Y-%m-%d-%H-%M-%S')

        if cls.logger is None:
            ########创建日志器，控制他的创建次数
            cls.logger = logging.getLogger()  # 不是None
            # 设置总的级别
            cls.logger.setLevel(logging.INFO)
            # 2获取格式器
            # 2.1 要给格式器设置要输出的样式
            fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            with allure.step("%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"):

                # 2.2创建格式器，并且给他设置样式
                fm = logging.Formatter(fmt)
                # 3.创建处理器 按照时间进行切割文件
                tf = logging.handlers.TimedRotatingFileHandler(filename=DIR_NAME + '/logger/{}.log'.format(now),  # 原日志文件
                                                               when='H',  # 间隔多长时间把日志存放到新的文件中
                                                               interval=1,
                                                               backupCount=2,  # 除了原日志文件，还有3个备份
                                                               encoding='utf-8'
                                                               )

                # 在处理器中添加格式器
                tf.setFormatter(fm)
                # 在日志器中添加处理器
                cls.logger.addHandler(tf)

        return cls.logger






# class GetLogger(logging.Logger):
#     formatter = None
#
#     def __init__(self, name):
#         super().__init__(name)
#         self.formatter = logging.Formatter(fmt='%(asctime)s-%(levelname)s:\t %(message)s',
#                                            datefmt='%H:%M:%S')
#
#     def get_logger(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
#         """
#                 Low-level logging routine which creates a LogRecord and then calls
#                 all the handlers of this logger to handle the record.
#                 """
#         sinfo = None
#         if logging._srcfile:
#             # IronPython doesn't track Python frames, so findCaller raises an
#             # exception on some versions of IronPython. We trap it here so that
#             # IronPython can use logging.
#             try:
#                 fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
#             except ValueError:  # pragma: no cover
#                 fn, lno, func = "(unknown file)", 0, "(unknown function)"
#         else:  # pragma: no cover
#             fn, lno, func = "(unknown file)", 0, "(unknown function)"
#         record = self.makeRecord(self.name, level, fn, lno, msg, args,
#                                  None, func, None, None)
#         title = self.formatter.format(record)
#         with allure.step(title):#输出step
#
#             if exc_info:
#                 if isinstance(exc_info, BaseException):
#                     exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
#                 elif not isinstance(exc_info, tuple):
#                     exc_info = sys.exc_info()
#             record = self.makeRecord(self.name, level, fn, lno, msg, args,
#                                      exc_info, func, extra, sinfo)
#             if exc_info:#如果执行异常，把堆栈信息写入allure attach文件
#                 allure.attach(self.formatter.format(record), "堆栈", allure.attachment_type.TEXT)
#                 pass
#             self.handle(record)
#             pass
#         pass
#
#     pass
#
#



# if __name__ == '__main__':
#     logger = GetLogger().get_logger()
#     print(logger.info('aa'))
#     logger1 = GetLogger().get_logger()
#     print(id(logger1))
#     logger.debug('调试')  # 相当print小括号中的信息
#     logger.info('信息')
#     logger.warning('警告')
#     name = 'yaoyao'
#     logger.error('这个变量是{}'.format(name))
#     logger.critical('致命的')
#
#
