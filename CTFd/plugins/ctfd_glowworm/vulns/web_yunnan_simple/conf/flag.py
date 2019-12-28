#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import uuid, time, sys, requests, re, json

def genFlag(uuid_key, name, timestamp, key):
    flag = uuid.uuid3(uuid.UUID(uuid_key), name + timestamp + key)
    flag = 'flag{' + str(flag) + '}'
    return flag

# Flag放到Linux根目录
def main(key, teamId, interval):
    # 正则替换下面两个字段
    uuid_key = str(uuid.uuid1())
    name = teamId
    timestamp = str(time.time())
    flag = genFlag(uuid_key, name, timestamp, key)
    # 根据权限情况调整
    filePath = "/flag"
    write_to_file(filePath, flag)
    write_to_api(uuid_key, name, timestamp, key)
    print "Update Finished. " + name + " " + flag


# 将flag覆盖写入指定文件
def write_to_file(filename, flag):
    file = open(filename, "w")
    file.write(str(flag))
    file.close()


# 将flag提交至API
def write_to_api(uuid_key, name, timestamp, key):
    request = requests.Session()
    gateway = "10.2.0.10"
    get = "http://{}:4000".format(gateway)
    rq = request.get(get)
    token = "".join(re.findall("var csrf_nonce = \"(.*)\"", rq.text))

    url = "http://{}:4000/plugins/ctfd-glowworm/flag".format(gateway)
    data = {
        'key': key,
        'uuid': uuid_key,
        'name': name,
        'time': timestamp
    }
    headers = {"CSRF-Token": token, "Content-Type": "application/json"}
    print request.post(url, data=json.dumps(data), headers=headers).text

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])