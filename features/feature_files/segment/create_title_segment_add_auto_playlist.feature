#language: zh-CN
@create_title_segment_add_auto_playlist
功能:create_title_segment_add_auto_playlist

  场景大纲: 添加满足场次的auto playlist并列表中查询
    假如获取playlist访问地址
    假如获取site访问地址
    假如获取producer_view访问地址
    假如获取title访问地址
    当默认"split_by_week"为false时创建title类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
#    创建时返回了segment_uuid
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当show页面接口查询有screen_show_attributes属性的pos同时提取show_title_name、pos_show_attributes属性和pos_uuid1
    那么成功获取参数pos_one_name_list和pos_one_name_str,pos_show_attributes
    当输入单个pos_one_name_list和title_uuid进行match_pos
#    创建auto_playlist
    当输入pos_show_attributes,创建变量为<playlist>的auto_playlist
#    查询auto_message
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且在library里查询segment
    而且把segment加到playlist里并保存草稿
    那么请求的content_list
#    publish
    当publish该playlist
    当等待90s
#    ---------------------
    当在show_detail页面查询上述执行情况，如果匹配完成，获取content_association_uuid和action_tag_uuid用于segment放在第二的位置
    当根据content_association_uuid和title_uuid查询segment的split_uuid
    当输入必填参数<content_title_text>创建cpl
    而且根据title查询创建的cpl的uuid
    当在library里查询content
    当把content加到title_segment里保存草稿
    当publish该title_segment
    当等待90s
    #    -----------------以下要修改，查看添加后的content的uuid
    当在show_detail页面查询上述执行情况
    那么segment添加的content_title在show_detail页面里面
    #    暂时存在bug重新发布后不显示show
#    当在segment_manage_shows页面查询上述执行情况
#    那么segment_manage_shows页面里显示刚匹配的pos_uuid
    当在process_queue页面查询segment发布状态
    那么process_queue页面显示该segment并且显示action为publish

    例子:
      | name      | type | title         | purpose        | playlist               | content_title_text |
      | titleName | 3    | title_segment | Advertisements | playlist_segment_title | content_title_text |
#    | name      | type          | title         | purpose        | playlist               | content_title_text |
#      | titleName | title_segment | title_segment | Advertisements | playlist_segment_title | content_title_text |
