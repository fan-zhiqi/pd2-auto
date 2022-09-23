## language: zh-CN
#功能: 删除一个在影厅是unused的CPL
#    场景: 删除在某一个影厅中，这个CPL的状态是unused的
#        假如获取cpl访问地址
##        当先从接口中获取到unuse的cpl_uuid
#        当先从接口中获取到含有device的unuse的cpl_uuid
#        而且根据cpl_uuid获取到complex_uuid和device_uuid
#        而且获取到所需数据之后,根据cpl_uuid和complex_uuid和device_uuid来进行删除操作
#        当等待90s之后
#        而且检查数据库并打印对应字段