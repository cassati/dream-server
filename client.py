import os
import sys
import json
import time
import uuid
import http.client

host = '127.0.0.1'
port = 8078
client_id = uuid.uuid4().hex
calc_item = None
history = None


# 加载配置
def _load_config(file_name):
    for line in open(file_name, encoding="utf8"):
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        arr = line.split('=')
        if arr[0] == 'host':
            global host
            host = arr[1]
        elif arr[0] == 'port':
            global port
            port = int(arr[1])
    return


def do_post(url, body):
    jsonstr = json.dumps(body)
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request('POST', url, jsonstr.encode('utf-8'))
    response = conn.getresponse()
    bytedata = response.read()
    message = bytedata.decode('utf-8')
    conn.close()
    return message


def init():
    request = {'client_id': client_id}
    response = do_post('/base_data', request)
    obj = json.loads(response)
    if obj['status'] == 'success':
        global calc_item, history
        calc_item = obj['message']['calc_item']
        history = obj['message']['history']
        return
    raise Exception('加载初始化数据失败，请重试')


def request_task():
    request = {'client_id': client_id}
    try:
        response = do_post('/request_task', request)
    except Exception as e:
        raise Exception('获取任务失败: ')
    obj = json.loads(response)
    if obj['status'] == 'success':
        return obj['message']
    raise Exception('获取任务失败')


def process(task):
    task.update({'client_id': client_id, 'client_start_time': time.time(), 'details': []})
    for h in history:
        pass
    return task


def submit_task(request):
    try:
        response = do_post('/submit_task', request)
    except Exception as e:
        raise Exception('提交任务失败: ')
    obj = json.loads(response)
    if obj['status'] == 'success':
        return obj['message']
    raise Exception('提交任务失败')


def do_work():
    while True:
        task = request_task()
        result = process(task)
        submit_task(result)


if __name__ == "__main__":
    config_file_name = "base.config"
    if len(sys.argv) <= 1:
        work_dir = os.getcwd()
    else:
        work_dir = sys.argv[1]

    try:
        print()
        print("-" * 60)
        _load_config(os.path.join(work_dir, config_file_name))
        init()
        do_work()
    except Exception as e:
        print(e)
