1.1.3 / 2020-3-25
=================

* Readme中添加`Aliyun-Instance`链接
* 修复多次进行`user_id`转换导致`CTFd-Glowworm`插件重置容器失败的问题
* 修复`Aliyun-Instance`插件模版文件名重复导致的Bug

1.1.2 / 2020-3-17
=================

* fix vul & update single-nginx.yml
* aliyun-instance-first-commit

1.1.1 / 2020-1-26
=================

* Fix error when submit flags in Team mode when using `CTFd-Glowworm` (#15)
* Modify the sort method of `CTFd-Matrix-Scorebard`
* Add `.gitattributes` to prettify the repository
* Modify `H1ve-Theme` base.html to adapt more navs add in admin page
* Prettify the admin-containers page

1.1.0 / 2019-12-28
=================

* Offer random-ports option in `CTFd-Glowworm` (#7)
* Add more error tips when using `CTFd-Glowworm` plugin
* Fix Error when `docker_max_container_count` is None
* Fix error when `start_time` is not defined
* Support using existing image to start env for `CTFd-Glowworm` plugin
* Fix error when clicking `Expired this instance` button
* Modified messgage with different mode in owl-containers
* Fix bugs when `challenge_name` != `envname`
* Fix bugs when using `Teams` mode in `CTFd-Glowworm` plugins
* Update plugins README
* Add source codes of 3 challenges for CTFd-Glowworm plugin

1.0.9 / 2019-12-27
=================

* Seperate schedule-task into plugin-owned
* Uniform network name standard for `CTF_Owl` challenge templates
* Set regular alive time to 3600s for `CTFd_Owl` challenge containers

1.0.8 / 2019-12-26
=================

* Add error tips when using `CTFd-Owl` plugin

1.0.8 / 2019-12-25
=================

* Change `H1ve-theme` index content into admin page setting with route `index`

1.0.7 / 2019-12-24
=================

* Fix scheduled job repeat working
* Add targets and attack-logs message for view.html in `CTFd-Glowworm`
* Add README for `CTFd-Glowworm` plugin
* Uniform network name standard

1.0.6 / 2019-12-23
=================

* Change py-redis to 3.0 to adapt flask_apscheduler
* Fix bugs in `CTFd-Glowworm` plugin
* Add two icons and change some codes to adapt `CTFd-Glowworm` plugin
* Change Dockerfile to an exist base image
* Fix bugs when running with `CTFd-Glowworm` plugin
* Fix jsonify decimal type data error

1.0.5 / 2019-12-21
=================

* Adapt `single-nginx` mode
* Change `.yml` to v3.5 to set exact network name

1.0.3 / 2019-12-19
=================

* Add `CTFd-Glowworm` plugin basic functions

1.0.2 / 2019-12-17
=================

* Fix error msgs when frpc is not start
* Change log-file name to plugin name
* Change get_mode() to an ext-function to avoid loop-call errors
* fix test challenge: `file-upl0ad` build error
* Change index logo to white
* Fix `Max Renewal Times` was set to constant 3600

1.0.1 / 2019-12-16
=================

* Adapt different mode for ctfd-matrix-scoreboard plugin
* Fix some bugs (#3)

1.0.0 / 2019-12-1
=================

* Support CTFd v2.1.5
* Add a front site theme named `H1ve-theme`
* Add  dynamic hanging-out containers plugin supported `docker-compose` named  `CTFd-Owl`
* Add dynamic scoreboard plugin supported `CTFd>=2.0` named `CTFd-Matrix-Scoreboard`

