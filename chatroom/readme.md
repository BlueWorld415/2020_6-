# **聊天平台**

## 整体简介

使用MTV设计模式，Linux环境下开发，个人状态处于边学边用状态。

## 技术简介

前端：

​	bootstrap框架为基础，html+css为样式设计模式，Ajax为主要数据传输技术

后端：

​	Django为后端框架，未做上线处理，目前处于调试状态

​	Mysql 为数据存储数据库，主要存储用户信息、聊天室信息、聊天记录、文件记录等数据

​	Redis 为缓存数据库，为防止在聊天记录查询时，多次查询已有记录，使用redis记录已查询聊天记录id，使数据查询与存储高效。同时应用于聊天公告、文件列表、用户列表等模块

## 功能简介

普通用户登录后可选择聊天室进入，进入聊天室后可收发消息、上传下载文件、查看公告等

普通用户创建聊天室即可成为改聊天室管理员，聊天室管理员在普通用户功能基础上，增加发布公告、解散转让聊天室、踢出成员等功能

后台管理界面采用Django内建admin模块，使用超级管理员密码登录即可对数据库中各表进行操作

## 开发者言

​	此项目依旧具备各种问题及功能的缺陷，本人也在积极的改正，如果此项目功能或技术模块恰巧可以为你所用，那是我的荣幸。

​	也希望看到这个项目的大牛，可以对我指点一二，初入社会新人，请多关照。

​	email：Blue0415@126.com

​	期待同行交流，谢谢。


