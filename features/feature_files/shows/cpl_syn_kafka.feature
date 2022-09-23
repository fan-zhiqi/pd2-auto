#language: zh-CN
#@fixture.kafkaproducer
#@fixture.kafkaconsumer
#功能: cpl数据同步到producer2,kafka数据流向
#  """
#  流程包括以下内容
#  发送cpl.locations.request消息队列
#  验证cpl.locations.response消息队列接收到cpl.location.request消息队列
#  发送cpl.xml.request消息队列
#  验证cpl.xml.response消息队列消费cpl.xml.request消息队列
#  """
#  场景: cpl.locations.request发送消息队列,验证cpl.locations.response接收到消息队列
#      当 发送cpl.locations.request消息队列topic为"cpl.locations.request"
#      那么 检查cpl.locations.response消息队列接收到cpl.locations.request消息队列的topic为"cpl.locations.response"
#
#  场景: cpl.xml.request发送消息队列,验证cpl.xml.response接收到消息队列
#      当 发送cpl.xml.request消息队列topic为"cpl.xml.request"
#      那么 检查cpl.xml.response消息队列接收到cpl.xml.request消息队列的topic为"cpl.xml.response"