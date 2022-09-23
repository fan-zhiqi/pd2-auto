#language: zh-CN
@create_match_shows_auto_playlist
功能:create_match_shows_auto_playlist

  场景大纲: 添加满足场次的auto playlist并列表中查询
    假如获取playlist访问地址
    假如获取site访问地址
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当show页面接口查询有screen_show_attributes属性的pos同时提取show_title_name、pos_show_attributes属性和pos_uuid
    那么成功获取参数pos_one_name_list和pos_one_name_str,pos_show_attributes
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当输入pos_show_attributes,创建变量为<playlist>的auto_playlist
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且publish该playlist
    当等待90s
    当在show_detail页面查询上述执行情况
    那么创建的playlist_uuid在show_detail页面里面
    当在auto_playlist_manage_shows页面查询上述执行情况
    那么playlist_manage_shows页面里显示刚匹配的pos_uuid
    当在process_queue页面查询上述执行情况
    那么process_queue页面显示该playlist_uuid
    例子:
      | name      | playlist            |
      | titleName | playlist_title_text |