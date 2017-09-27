import os
import copy
import json
import uuid
import config

# 本次任务的版本
task_version = uuid.uuid4().hex

# 本次任务开始结束时间
task_start_time = None
task_end_time = None

# 任务列表
task_arr = []
# 未开始的任务
task_unstart = []
# 执行中的任务
task_working = []
# 已完成的任务
task_finished = []


def init():
    global task_start_time
    task_start_time = config.curr_time()
    total = 2**(len(config.calc_item)) - 1
    tmp_total = 0
    task_size = config.task_size
    last_task_size = total % config.task_size
    task_id = 1
    while tmp_total < total:
        if tmp_total + last_task_size == total:
            task_size = last_task_size
        obj = {"task_version": task_version, "task_id": task_id, "task_start": tmp_total + 1,
               "task_size": task_size, "start_qi_shu": config.start_qi_shu, "end_qi_shu": config.end_qi_shu}
        task_arr.append(obj)
        tmp_total += task_size
        task_id += 1
    global task_unstart
    task_unstart = [copy.deepcopy(t) for t in task_arr]


def dispatch(path, data, request):
    obj = json.loads(data)
    if path == '/base_data':
        result = handle_base_data(obj, request)
    elif path == '/request_task':
        result = handle_request_task(obj, request)
    elif path == '/submit_task':
        result = handle_submit_task(obj, request)
    else:
        result = '请求错误'
    return result


def handle_base_data(obj, request):
    log('base_data', obj, request)
    return {'calc_item': config.calc_item, 'history': config.simple_history}


def handle_request_task(obj, request):
    log('request_task', obj, request)
    if len(task_finished) == len(task_arr):
        raise Exception('all tasks are finished')
    client = get_client(obj, request)
    client['client_start_time'] = config.curr_time()
    t = None
    if task_unstart:
        t = task_unstart.pop()
        task_working.append(t)
        t['worker'] = [client]
    elif task_working:
        t = task_working[0]
        t['worker'].append(client)
    return t


def handle_submit_task(obj, request):
    log('submit_task', obj, request)
    if len(task_finished) == len(task_arr):
        return 'ok'
    client = get_client(obj, request)
    for t in task_working:
        if t['task_id'] != obj['task_id']:
            continue
        for w in t['worker']:
            if w['client_id'] == obj['client_id']:
                t['client_id'] = obj['client_id']
                t['ip'] = client['ip']
                t['port'] = client['port']
                t['client_start_time'] = obj['client_start_time']
                t['client_end_time'] = obj['client_end_time']
                t['details'] = obj['details']
        del t['worker']
        task_finished.append(t)
        task_working.remove(t)
        break
    if len(task_finished) == len(task_arr):
        do_finished()
    return 'ok'


def log(oper, obj, request):
    msg = "{} {: <15} called by {} from {}:{}"
    print(msg.format(config.curr_time(), oper, obj['client_id'], *request.client_address))


def get_client(obj, request):
    return {'client_id': obj['client_id'], 'ip': request.client_address[0], 'port': request.client_address[1]}


def do_finished():
    print('{} tasks finished.', config.curr_time())
    global task_end_time
    task_end_time = config.curr_time()
    global task_finished
    task_finished = sorted(task_finished, key=lambda task: task['task_id'], reverse=False)
    details = {}
    for t in task_finished:
        for k in t['details']:
            if k in details:
                details[k]['odd'] += t['details'][k]['odd']
                details[k]['even'] += t['details'][k]['even']
            else:
                details[k] = {'times': t['details'][k]['times'],
                              'odd': t['details'][k]['odd'],
                              'even': t['details'][k]['even']}

    f = open(os.path.join(config.work_dir, str(config.start_qi_shu) + '-' + str(config.end_qi_shu) + '.txt'), 'w')
    for t in task_finished:
        f.write(str(t) + '\n')
    f.write(str(details) + '\n')
    f.flush()
    f.close()
    print(str(details))
    return
