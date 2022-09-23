#language: zh-CN
@create_dynamic_macro_add_auto_playlist
功能:create_dynamic_macro_add_auto_playlist

  场景大纲: 添加满足场次的auto playlist并列表中查询
    假如获取playlist访问地址
    假如获取site访问地址
    假如获取producer_view访问地址
    假如获取title访问地址
    当输入变量为<title>和type=<type>时获取macro_uuid
#    创建时返回了segment_uuid
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当show页面接口查询有screen_show_attributes属性的pos同时提取show_title_name、pos_show_attributes属性和pos_uuid2
    那么成功获取参数pos_one_name_list和pos_one_name_str,pos_show_attributes
    当输入单个pos_one_name_list和title_uuid进行match_pos
#    创建auto_playlist
    当输入pos_show_attributes,创建变量为<playlist>的auto_playlist
#    查询auto_message
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且在library里查询macro
    而且把macro加到playlist里并保存草稿
    那么请求的content_list
#    publish
    当publish该playlist
    当等待90s
#    ---------------------
    当在show_detail页面查询上述执行情况，如果匹配完成，获取content_association_uuid和action_tag_uuid用于segment放在第二的位置
    那么获取的content_association_uuid和action_tag_uuid
    当根据content_association_uuid获取第一组macro的split_uuid
    当在library里查询automation
    当把automation加到Dynamic_macro里保存草稿
    当publish该Dynamic_macro
    当等待90s
    #    -----------------以下要修改，查看添加后的content的uuid
    当在show_detail页面查询上述执行情况
    那么macro添加的automation在show_detail页面里面
    当在process_queue页面查询macro发布状态
    那么process_queue页面显示该macro并且显示action为publish

    例子:
      | name        | type          | title         | playlist               |
      | movie_title | dynamic_macro | dynamic_macro | playlist_segment_title |
