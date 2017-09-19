import os
import sys
import json
import time
import uuid
import http.client

host = '127.0.0.1'
port = 8078
client_id = uuid.uuid4().hex
calc_item = []
history = []
history_calc = []
calc_formula_format = "{:0>28}"


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


# 当前时间 yyyy-mm-dd hh:MM:ss
def curr_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


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
        global calc_item, history, calc_formula_format
        history = obj['message']['history']
        calc_item = obj['message']['calc_item']
        calc_formula_format = "{:0>" + str(len(calc_item)) + "}"
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
    print("{} process task start, {}".format(curr_time(), task))
    global history_calc
    if task['end_qi_shu'] == -1:
        history_calc = history
    else:
        history_calc = [h for h in history if task['start_qi_shu'] <= h['qi_shu'] <= task['end_qi_shu']]
    task.update({'client_id': client_id, 'client_start_time': curr_time(), 'details': {}})
    results = []
    for x in range(task['task_size']):
        results.append(do_calc(task, x + task['task_start'] + 1))
    coolest = {'total_yes': 0, 'total_no': 0,
               'max_multi_yes': 0, 'max_multi_no': 0,
               'current_multi_yes': 0, 'current_multi_no': 0}
    for r in results:
        if not str(r['current_multi_yes']) in task['details']:
            task['details'][str(r['current_multi_yes'])] = {'times': r['current_multi_yes'], 'odd': 0, 'even': 0}
        if r['result'] == 1:
            task['details'][str(r['current_multi_yes'])]['odd'] += 1
        else:
            task['details'][str(r['current_multi_yes'])]['even'] += 1
        coolest['total_yes'] += r['total_yes']
        coolest['total_no'] += r['total_no']
        if coolest['max_multi_yes'] < r['max_multi_yes']:
            coolest['max_multi_yes'] = r['max_multi_yes']
        if coolest['max_multi_no'] < r['max_multi_no']:
            coolest['max_multi_no'] = r['max_multi_no']
        if coolest['current_multi_yes'] < r['current_multi_yes']:
            coolest['current_multi_yes'] = r['current_multi_yes']
        if coolest['current_multi_no'] < r['current_multi_no']:
            coolest['current_multi_no'] = r['current_multi_no']
    task['coolest'] = coolest
    task['client_end_time'] = curr_time()
    print("{} process task end,   {}".format(curr_time(), task))
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


def do_calc(task, formula_id):
    formula_content = calc_formula_format.format(str(bin(formula_id))[2:])
    formula = {'formula_id': formula_id, 'formula_content': formula_content,
               'start_qi_shu': task['task_start'], 'end_qi_shu': task['end_qi_shu'],
               'total_yes': 0, 'total_no': 0,
               'max_multi_yes': 0, 'max_multi_no': 0,
               'current_multi_yes': 0, 'current_multi_no': 0,
               'calc_result': 0, 'result': 0}
    hid = 0
    for h in history_calc:
        tmp = 0
        for flag, key in zip(formula_content, calc_item):
            if flag == '1':
                tmp += h[key]
        r = tmp % 49
        formula['calc_result'] = r
        formula['result'] = r % 2
        if hid + 1 < len(history_calc):
            if history_calc[hid + 1]['tm|hm'] % 49 % 2 == formula['result']:
                formula['total_yes'] += 1
                formula['current_multi_yes'] += 1
                formula['current_multi_no'] = 0
                if formula['current_multi_yes'] > formula['max_multi_yes']:
                    formula['max_multi_yes'] = formula['current_multi_yes']
            else:
                formula['total_no'] += 1
                formula['current_multi_no'] += 1
                formula['current_multi_yes'] = 0
                if formula['current_multi_no'] > formula['max_multi_no']:
                    formula['max_multi_no'] = formula['current_multi_no']
        hid += 1
    return formula


def start():
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
        start()
    except Exception as e:
        print(e)
