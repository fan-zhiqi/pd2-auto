#language: zh-CN
#@fixture.kafkaproducer
#@fixture.kafkaconsumer
#功能: pos数据同步到producer2,kafka数据流向
#  """
#  流程包括以下内容
#  发送pos-week.fetch消息队列
#  验证pos-week.raw消息队列接收到pos-week.fetch消息队列
#  发送pos-hash.fetch消息队列
#  验证pos-hash.raw消息队列消费pos-hash.fetch消息队列
#  发送pos.fetch消息队列
#  验证pos.raw消息队列消费pos.fetch消息队列
#  发送pos.mapping.request消息队列
#  验证pos.mapping.response消息队列消费pos.mapping.request消息队列
#  """
#  场景: pos-week.fetch发送消息队列,验证pos-week.raw接收到消息队列
#      当 发送pos-week.fetch消息队列topic为"pos-week.fetch"
#      那么 检查pos-week.raw消息队列接收到pos-week.fetch消息队列的topic为"pos-week.raw"
#
#  场景: pos-hash.fetch发送消息队列,验证pos-hash.raw接收到消息队列
#      当 发送pos-hash.fetch消息队列topic为"pos-hash.fetch"
#      那么 检查pos-hash.raw消息队列接收到pos-hash.fetch消息队列的topic为"pos-hash.raw"
#
#  场景: pos.fetch发送消息队列,验证pos-hash.raw接收到消息队列
#      当 发送pos.fetch消息队列topic为"pos.fetch"
#      那么 检查pos.raw消息队列接收到pos.fetch消息队列的topic为"pos.raw"
#
#
#  场景: pos.mapping.request发送消息队列,验证pos-week.raw接收到消息队列
#      当 发送pos.mapping.request消息队列topic为"pos.mapping.request"
#      那么 检查pos.mapping.response消息队列接收到pos.mapping.request消息队列的topic为"pos.mapping.response"
#
