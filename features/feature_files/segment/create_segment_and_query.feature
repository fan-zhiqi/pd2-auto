#language: zh-CN
@create_segment
功能:create_segment

  场景大纲: 创建third_parth类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建third_parth类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    那么请求成功断言segment_uuid长度>5
    例子:
      | type | title       | purpose |
      | 4    | third_parth | None    |

#      | api_segment | third_parth | None    |


  场景大纲: 创建playlist类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建playlist类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    那么请求成功断言segment_uuid长度>5
    例子:
      | type | title                  | purpose        |
      | 2    | playlist_segment_title | Advertisements |
      | 2    | playlist_segment_title | Trailers       |
      | 2    | playlist_segment_title | Idents         |
      | 2    | playlist_segment_title | Other          |
#    | playlist_segment | playlist_segment_title | Advertisements |
#      | playlist_segment | playlist_segment_title | Trailers       |
#      | playlist_segment | playlist_segment_title | Idents         |
#      | playlist_segment | playlist_segment_title | Other          |

  场景大纲: 创建playlist类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建title类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    那么请求成功断言segment_uuid长度>5
    例子:
#      | type          | title         | purpose        |
#      | title_segment | title_segment | Advertisements |
#      | title_segment | title_segment | Trailers       |
#      | title_segment | title_segment | Idents         |
#      | title_segment | title_segment | Other          |
      | type | title         | purpose        |
      | 3    | title_segment | Advertisements |
      | 3    | title_segment | Trailers       |
      | 3    | title_segment | Idents         |
      | 3    | title_segment | Other          |

  场景大纲: 创建org-segment类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建org-segment类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    那么请求成功断言segment_uuid长度>5
    例子:
      | type | title         | purpose |
      | 6    | segment_title | None    |
#       | type         | title         | purpose |
#      | base_segment | segment_title | None    |


  场景大纲: 查看third_parth类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建third_parth类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    而且根据title列表中查询出的uuid列表
    那么创建的uuid在列表中查询的uuid列表中
    例子:
      | type | title       | purpose |
      | 4    | third_parth | None    |
#     | type        | title       | purpose |
#      | api_segment | third_parth | None    |

  场景大纲: 查看playlist类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建playlist类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    而且根据title列表中查询出的uuid列表
    那么创建的uuid在列表中查询的uuid列表中
    例子:
#      | type             | title                  | purpose        |
#      | playlist_segment | playlist_segment_title | Advertisements |
#      | playlist_segment | playlist_segment_title | Trailers       |
#      | playlist_segment | playlist_segment_title | Idents         |
#      | playlist_segment | playlist_segment_title | Other          |
      | type | title                  | purpose        |
      | 2    | playlist_segment_title | Advertisements |
      | 2    | playlist_segment_title | Trailers       |
      | 2    | playlist_segment_title | Idents         |
      | 2    | playlist_segment_title | Other          |

  场景大纲: 查看title类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建title类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    而且根据title列表中查询出的uuid列表
    那么创建的uuid在列表中查询的uuid列表中
    例子:
#      | type          | title         | purpose        |
#      | title_segment | title_segment | Advertisements |
#      | title_segment | title_segment | Trailers       |
#      | title_segment | title_segment | Idents         |
#      | title_segment | title_segment | Other          |
      | type | title         | purpose        |
      | 3    | title_segment | Advertisements |
      | 3    | title_segment | Trailers       |
      | 3    | title_segment | Idents         |
      | 3    | title_segment | Other          |

  场景大纲: 查看org-segment类型的segment
    假如获取playlist访问地址
    当默认"split_by_week"为false时创建org-segment类型的segment时type=<type>和purpose=<purpose>和输入变量title为<title>时
    而且根据title列表中查询出的uuid列表
    那么创建的uuid在列表中查询的uuid列表中
    例子:
#      | type         | title         | purpose |
#      | base_segment | segment_title | None    |
      | type | title         | purpose |
      | 6    | segment_title | None    |