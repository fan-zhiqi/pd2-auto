#language: zh-CN
@match_title
功能:unmatch_title_and_match_and_query

  场景大纲:单个show_title进行unmatch_title
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当查询全部shows获取pos_name_list，pos_one_name_list
    那么查询的pos_name_list，pos_one_name_list的值
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待10s
    当输入单个pos_name_list和title_uuid进行unmatch_pos
    那么断言返回的message=<message>
    例子:
      | name      | message |
      | titleName | success |

  场景大纲:多个show_title进行unmatch_title
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当查询全部shows获取pos_name_list，pos_one_name_list
    那么查询的pos_name_list，pos_one_name_list的值
    当输入多个pos_name_list和title_uuid进行match_pos
    当等待10s
    当输入多个pos_name_list和title_uuid进行unmatch_pos
    那么断言返回的message=<message>
    例子:
      | name      | message |
      | titleName | success |


  场景大纲:单个show_title匹配title
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当查询全部shows获取pos_name_list，pos_one_name_list
    那么查询的pos_name_list，pos_one_name_list的值
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待10s
    当输入单个pos_name_list和title_uuid进行unmatch_pos
    当输入单个pos_one_name_list和title_uuid进行match_pos
    那么断言返回的message=<message>
    例子:
      | name      | message |
      | titleName | success |

  场景大纲:多个show_title匹配title
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当查询全部shows获取pos_name_list，pos_one_name_list
    那么查询的pos_name_list，pos_one_name_list的值
    当输入多个pos_name_list和title_uuid进行match_pos
    当等待10s
    当输入多个pos_name_list和title_uuid进行unmatch_pos
    当输入多个pos_name_list和title_uuid进行match_pos
    那么断言返回的message=<message>
    例子:
      | name      | message |
      | titleName | success |

  场景大纲:单个匹配show_title后重新匹配title
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当查询全部shows获取pos_name_list，pos_one_name_list
    那么查询的pos_name_list，pos_one_name_list的值
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待10s
    当输入单个pos_name_list和title_uuid进行unmatch_pos
    当输入单个pos_one_name_list和title_uuid进行match_pos
    那么断言返回的message=<message>
    例子:
      | name      | message |
      | titleName | success |

  场景大纲:多个匹配show_title后重新匹配title
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当查询全部shows获取pos_name_list，pos_one_name_list
    那么查询的pos_name_list，pos_one_name_list的值
    当输入多个pos_name_list和title_uuid进行match_pos
    当等待10s
    当输入多个pos_name_list和title_uuid进行unmatch_pos
    当输入多个pos_name_list和title_uuid进行match_pos
    那么断言返回的message=<message>
    例子:
      | name      | message |
      | titleName | success |

  场景大纲:列表查询match_title后的结果
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当查询全部shows获取pos_name_list，pos_one_name_list用于match—title
    那么查询的pos_name_list，pos_one_name_list的值
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待10s
    当输入单个pos_name_list和title_uuid进行unmatch_pos
    当等待5s
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待10s
    当关键字show_title_name查询列表，获取title_uuid_list
    那么创建的title_uuid在列表查询的title_uuid_list，match成功
    例子:
      | name      |
      | titleName |

  场景大纲:列表查询unmatch_title后的结果
    假如获取producer_view访问地址
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    当请求列表获取未锁定而且有match_title获取show_title_name
    当输入单个pos_one_name_list和title_uuid进行match_pos
    当等待10s
    当输入单个pos_name_list和title_uuid进行unmatch_pos
    当等待10s
    当关键字show_title_name查询列表，获取title_uuid_list
    那么创建的title_uuid不在列表查询的title_uuid_list，unmatch成功
    例子:
      | name      |
      | titleName |