#language: zh-CN
@create_auto_playlist
功能:create_auto_playlist

  场景大纲: 创建动态播放列表
    假如获取playlist访问地址
    假如获取site访问地址
    当查询影院上传的场次属性show_attribute获取第一个参数
    而且输入pos_show_attributes,创建变量为<playlist>的auto_playlist
    那么请求成功断言playlist_uuid长度>5
    例子:
      |playlist|
      |playlist_title_text|

  场景大纲: 在playlist列表查看刚创建的动态playlist
    假如获取playlist访问地址
    假如获取site访问地址
    当查询影院上传的场次属性show_attribute获取第一个参数
    而且输入pos_show_attributes,创建变量为<playlist>的auto_playlist
    而且查看playlsit播放列表
    那么断言创建的playlist_uuid在播放列表里
    例子:
      |playlist|
      |playlist_title_text|

#   场景:已经存在场次的auto播放列表那么创建不成功