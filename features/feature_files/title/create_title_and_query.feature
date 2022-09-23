#language: zh-CN
@title
功能: create_title_and_query

  场景大纲: 创建title
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    那么请求成功断言data长度>5
    例子:
      | name      |
      | titleName |

  场景大纲:参数化用例
    假如获取title访问地址
#         当输入name为空,source_id不为空时
#         那么请求失败断言code=500
    当输入非必填参数source_id为空name不为空时
    那么请求成功断言data长度>5
    当请求movie接口获取source_id
    当输入重复的<name>时source_id不变
    那么断言message=<message>
    例子:
      | name       |message|
      | titleName  |The title already exists in the organization|

  场景大纲:创建title并在列表查询该title
    假如获取title访问地址
    当请求movie接口获取source_id
    当输入参数name:<name>和source时输入正确时获取title_uuid
    而且请求查询列表,并提取title_uuid_list
    那么断言create创建的title_uuid在查询title_uuid的列表里面
    例子:
      | name      |
      | titleName |