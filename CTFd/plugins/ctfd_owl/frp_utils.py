import requests

from .db_utils import DBUtils
from .models import DynamicCheckChallenge


class FrpUtils:
    @staticmethod
    def update_frp_redirect():
        configs = DBUtils.get_all_configs()

        containers = DBUtils.get_all_alive_container()
        # frps config
        output = configs.get("frpc_config_template")

        http_template = "\n\n[http_%s]\n" + \
                        "type = http\n" + \
                        "local_ip = %s\n" + \
                        "local_port = %s\n" + \
                        "subdomain = %s\n" + \
                        "use_compression = true"

        direct_template = "\n\n[direct_%s_tcp]\n" + \
                          "type = tcp\n" + \
                          "local_ip = %s\n" + \
                          "local_port = %s\n" + \
                          "remote_port = %s\n" + \
                          "use_compression = true" + \
                          "\n\n[direct_%s_udp]\n" + \
                          "type = udp\n" + \
                          "local_ip = %s\n" + \
                          "local_port = %s\n" + \
                          "remote_port = %s\n" + \
                          "use_compression = true"

        for c in containers:
            dynamic_docker_challenge = DynamicCheckChallenge.query \
                .filter(DynamicCheckChallenge.id == c.challenge_id) \
                .first_or_404()

            if dynamic_docker_challenge.redirect_type.upper() == 'HTTP':
                output += http_template % (
                    "user{}_{}_service_1".format(c.user_id, dynamic_docker_challenge.dirname.split("/")[1])
                    , "user{}_{}_service_1".format(c.user_id, dynamic_docker_challenge.dirname.split("/")[1])
                    , dynamic_docker_challenge.redirect_port
                    , c.docker_id)
            else:
                output += direct_template % (
                    "user{}_{}_service_1".format(c.user_id, dynamic_docker_challenge.dirname.split("/")[1])
                    , "user{}_{}_service_1".format(c.user_id, dynamic_docker_challenge.dirname.split("/")[1])
                    , dynamic_docker_challenge.redirect_port
                    , c.port
                    ,"user{}_{}_service_1".format(c.user_id, dynamic_docker_challenge.dirname.split("/")[1])
                    , "user{}_{}_service_1".format(c.user_id, dynamic_docker_challenge.dirname.split("/")[1])
                    , dynamic_docker_challenge.redirect_port
                    , c.port)
        frp_api_ip = "frpc"
        frp_api_port = "7400"
        # print(output)
        try:
            if configs.get("frpc_config_template") is not None:
                requests.put("http://" + frp_api_ip + ":" + frp_api_port + "/api/config", output,
                             timeout=5)
                requests.get("http://" + frp_api_ip + ":" + frp_api_port + "/api/reload", timeout=5)
            else:
                pass
        except Exception as e:
            pass