#language: zh-CN
@create_macro
功能:create_macro

  场景大纲: 创建不同类型macro
    假如获取playlist访问地址
    当输入变量为<title>和type=<type>时获取macro_uuid
    那么请求成功断言macro_uuid长度>5
    例子:
      | title                       | type                |
      | screenwriter_standard_macro | screenwriter_standard_macro |
      | group_macro                 | group_macro                 |
      | dynamic_macro               | dynamic_macro               |
      | standard_macro              | standard_macro              |

  场景大纲: 创建不同类型macro并在列表中查询
    假如获取playlist访问地址
    当输入变量为<title>和type=<type>时获取macro_uuid
    而且根据title列表中查询出的macro_uuid列表
    那么创建的uuid在列表中查询的macro_uuid列表中
    例子:
      | title                       | type               |
      | screenwriter_standard_macro | screenwriter_standard_macro |
      | group_macro                 | group_macro                 |
      | dynamic_macro               | dynamic_macro               |
      | standard_macro              | standard_macro              |