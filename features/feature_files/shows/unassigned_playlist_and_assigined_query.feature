#language: zh-CN
@assigned_playlist_and_unassigined_query
功能:assigned_playlist_and_unassigined_query

  场景大纲:单个show_title进行assigined
    假如获取producer_view访问地址
    假如获取title访问地址
    假如获取playlist访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于assigned
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待5s
    当成功创建名字为变量<playlist>的playlist
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且publish该playlist
    当用playlist_uuid和pos_uuid去assigned场次
    那么断言code=<code>
    例子:
      | name      | playlist               | code |
      | titleName | assigned_show_playlist | 200  |

  场景大纲:单个show_title进行unassigined
    假如获取producer_view访问地址
    假如获取title访问地址
    假如获取playlist访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于unassigned
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待5s
    当成功创建名字为变量<playlist>的playlist
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且publish该playlist
    当用playlist_uuid和pos_uuid去assigned场次
    当等待90s
    当对该pos_uuid进行unassigned
    那么断言code=<code>
    例子:
      | name      | playlist               | code |
      | titleName | assigned_show_playlist | 200  |

  场景大纲:单个show_title进行assigined后在show_detail、playlist_manage_shows、process_queues页面查询
    假如获取producer_view访问地址
    假如获取title访问地址
    假如获取playlist访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于query_assigned
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待5s
    当成功创建名字为变量<playlist>的playlist
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且publish该playlist
    当用playlist_uuid和pos_uuid去assigned场次
    当等待90s
    当在show_detail页面查询上述执行情况
    那么创建的playlist_uuid在show_detail页面里面
    当在standard_playlist_manage_shows页面查询上述执行情况
    那么playlist_manage_shows页面里显示刚匹配的pos_uuid
    当在process_queue页面查询上述执行情况
    那么process_queue页面显示该playlist_uuid
    例子:
      | name      | playlist               |
      | titleName | assigned_show_playlist |

    场景大纲:单个show_title进行unassigined后在show_detail查询
    假如获取producer_view访问地址
    假如获取title访问地址
    假如获取playlist访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于unassigned
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待5s
    当成功创建名字为变量<playlist>的playlist
    当根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息
    而且publish该playlist
    当用playlist_uuid和pos_uuid去assigned场次
    当等待90s
    当对该pos_uuid进行unassigned
    当等待90s
     当在show_detail页面查询上述执行情况
    那么show_detail里的ppl为空
    例子:
      | name      | playlist               |
      | titleName | assigned_show_playlist |