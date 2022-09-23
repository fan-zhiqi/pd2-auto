#language: zh-CN
@create_stanard_playlist
功能:create_stanard_playlist

  场景大纲: 创建静态播放列表
    假如获取playlist访问地址
    当成功创建名字为变量<playlist>的playlist
    那么请求成功断言playlist_uuid长度>5
    例子:
      |playlist|
      |playlist_title_text|

    场景大纲:在playlist列表查看刚创建的静态playlist
      假如获取playlist访问地址
      当成功创建名字为变量<playlist>的playlist
      而且查看playlsit播放列表
      那么断言创建的playlist_uuid在播放列表里
      例子:
      |playlist|
      |playlist_title_text|