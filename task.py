import uuid
import config

task_arr = []
task_id = uuid.uuid4().hex


def init():
    total = 2**(len(config.calc_item)) - 1
    tmp_total = 0
    task_size = config.task_size
    last_task_size = total % config.task_size
    task_index = 1
    while tmp_total < total:
        if tmp_total + last_task_size == total:
            task_size = last_task_size
        obj = {"task_id": task_id, "task_index": task_index, "task_start": tmp_total + 1, "task_size": task_size,
               "start_qi_shu": config.start_qi_shu, "end_qi_shu": config.end_qi_shu}
        task_arr.append(obj)
        tmp_total += task_size
        task_index += 1


def dispatch(path, data):
    return task_arr

