# CTFd-Owl

**Dynamic Check Challenges with docker-compose for CTFd**



## Installation

**REQUIRES: CTFd >= v2.x**

1. Clone this repository to `CTFd/plugins`. It is important that the folder is
named `ctfd-owl`.

## How to Use

### Configuration

**Docker Flag Prefix** Flag前缀

**Docker APIs URL** API名字（默认为`unix://var/run/docker.sock`）

**Max Container Count** 最大容器数量（默认无限制）

**Max Renewal Time** 最大容器延长时间（超过将无法延长，达到时间后会自动摧毁）

![docker-setting-demo-w150](./assets/demo_img/owl-docker_shrink.png)



**FRP Http Domain Suffix** FRP域名前缀（如开启动态域名转发必填）

**FRP Direct Ip Address FRP** frp服务器IP

**FRP Direct Minimum Port** 最小端口

**FRP Direct Maximum Port** 最大端口

**FRP Config Template** Frpc热重载配置头模版(如不会自定义，尽量按照默认配置)

```
[common]
token = random_this
server_addr = frps
server_port = 80
admin_addr = 0.0.0.0
admin_port = 7400
```

![frp-setting-demo-w150](./assets/demo_img/owl-frp_shrink.png)

### Add Challenge

**Challenge Type** 题目类型(选`dynamic_check_docker`)

**Deployment Type** 部署方式(选`SINGLE-DOCKER-COMPOSE`)

**Dirname** 题目所在文件夹（相对于`source`的相对路径）

**FRP Type** frp类型(`DIRECT`为ip直接访问，`HTTP`为域名访问)

**FRP Port** 题目内网端口(例子中为`80`)

![owl-challenges-demo-w150](./assets/demo_img/owl-challenges_shrink.png)



### Demo

![instance-demo-w150](./assets/demo_img/owl-instance_shrink.png)

![containers-demo-w150](./assets/demo_img/owl-containers_shrink.png)

## Twins

* [CTFd-Whale](https://github.com/glzjin/CTFd-Whale) (Support docker-swarm)