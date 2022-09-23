#language: zh-CN
@create_title_segment_add_standard_playlist
功能:create_title_segment_add_standard_playlist

  场景大纲: 创建title_segment加入standard_playlist草稿并发布
    假如获取playlist访问地址
    假如获取site访问地址
    假如获取producer_view访问地址
    假如获取title访问地址
    当默认"split_by_week"为false时创建title类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
#    创建时返回了segment_uuid
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于create_title_segment_add_standard_playlist
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待5s
    当成功创建名字为变量<playlist>的playlist
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且在library里查询segment
    而且把segment加到playlist里并保存草稿
    那么请求的content_list
    当publish该playlist
    当用playlist_uuid和pos_uuid去assigned场次
    当等待90s
    #    ------------------
    当在show_detail页面查询上述执行情况，如果匹配完成，获取content_association_uuid和action_tag_uuid
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
#    当在segment_manage_shows页面查询上述执行情况
#    那么segment_manage_shows页面里显示刚匹配的pos_uuid
    当在process_queue页面查询segment发布状态
    那么process_queue页面显示该segment并且显示action为publish

    例子:
      | type | title         | purpose        | name      | playlist               | content_title_text |
      | 3    | title_segment | Advertisements | titleName | playlist_segment_title | content_title_text |
#    | type          | title         | purpose        | name      | playlist               |content_title_text|
#      | title_segment | title_segment | Advertisements | titleName | playlist_segment_title |content_title_text|
