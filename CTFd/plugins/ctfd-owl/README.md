# CTFd-Owl

**Dynamic Check Challenges with docker-compose for CTFd**



## Installation

**REQUIRES: CTFd >= v2.x**

1. Clone this repository to `CTFd/plugins`. It is important that the folder is
named `ctfd-owl`.

## How to Use

### Configuration

**Docker Flag Prefix ** Flag前缀

**Docker APIs URL** API名字（默认为`unix://var/run/docker.sock`）

**Max Container Count** 最大容器数量（默认无限制）

**Max Renewal Time** 最大容器失效时间（超过会自动关闭容器）



![docker-setting-demo-w150](./assets/demo_img/owl-docker_shrink.png)

**FRP Http Domain Suffix** FRP域名前缀（如开启动态域名转发必填）

**FRP Direct Ip Address FRP** frp服务器IP

**FRP Direct Minimum Port** 最小端口

**FRP Direct Maximum Port** 最大端口

**FRP Config Template** Frpc热重载配置头模版

![frp-setting-demo-w150](./assets/demo_img/owl-frp_shrink.png)

### Demo

![instance-demo-w150](./assets/demo_img/owl-instance_shrink.png)

![containers-demo-w150](./assets/demo_img/owl-containers_shrink.png)

## Twins

* [CTFd-Whale](https://github.com/glzjin/CTFd-Whale) (Support docker-swarm)