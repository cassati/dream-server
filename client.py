import json
import time
import uuid
import http.client

host = '127.0.0.1'
port = 8078
client_id = uuid.uuid4().hex
calc_item = None
history = None


def post_data(url, body):
    jsonstr = json.dumps(body)
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request('POST', url, jsonstr.encode('utf-8'))
    response = conn.getresponse()
    bytedata = response.read()
    message = bytedata.decode('utf-8')
    return message


def init():
    param = {'client_id': client_id}
    data = post_data('/base_data', param)
    jsonobj = json.loads(data)
    if jsonobj['status'] == 'success':
        global calc_item, history
        calc_item = jsonobj['message']['calc_item']
        history = jsonobj['message']['history']
        return
    raise Exception('加载初始化数据失败，请重试')


def request_task():
    param = {'client_id': client_id}
    try:
        data = post_data('/request_task', param)
    except Exception as e:
        raise Exception('获取任务失败: ')
    jsonobj = json.loads(data)
    if jsonobj['status'] == 'success':
        return jsonobj
    raise Exception('获取任务失败')


def process(task):
    task.update({'client_id': client_id, 'client_start_time': time.time(), 'details': []})
    for h in history:
        pass
    return task


def submit_task(param):
    try:
        data = post_data('/submit_task', param)
    except Exception as e:
        raise Exception('提交任务失败: ')
    jsonobj = json.loads(data)
    if jsonobj['status'] == 'success':
        return jsonobj
    raise Exception('提交任务失败')


def do_work():
    while True:
        task = request_task()
        result = process(task)
        submit_task(result)


if __name__ == "__main__":
    init()
    do_work()
