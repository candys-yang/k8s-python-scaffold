## k8s-python-Scaffold

一个基于 Kubernetes Deployment 的 python 应用开发脚手架。

脚手架的代码版本更新较为活跃，版本之间的脚手架编码结构可能有较大的变化。

版本策略，标准修改将增加子版本号，结构上的更改增加主版本号

__Code Version: 2.0__

Readme文档的 >version 为 deploy.sh 打包的版本标记，用于版本发布。

>version: 0


### 结构

标准的脚手架结构主要由三个应用组成：

Agent 用于连接 ETCD 注册中心，监听和拉取最新的应用配置信息。

Flask 用于为外部提供应用的 api 接口。

Redis  用于 pod 内的应用间数据交互。



### Agent

部署 Agent 主要依赖 Deployment 的 ConfigMap 绑定。

etcd 应使用集群中的3个节点或更多

config 字段: itsm 为默认的配置键值，etcdmap 为配置中心映射的字段。 item 和 etcdmap 之间存在关联。

Agent 源码： https://github.com/candys-yang/k8s-ConfigAgent-Sidecar



