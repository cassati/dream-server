import os
import sys
import config
import time
from functools import reduce


reviews = []
formula_format = "{:0>" + str(len(config.calc_item)) + "}"
formulas = [{'fid': fid, 'formula': formula_format.format(str(bin(fid))[2:]),
             'total_yes': 0, 'total_no': 0,
             'max_multi_yes': 0, 'max_multi_no': 0,
             'current_multi_yes': 0, 'current_multi_no': 0} for fid in range(1, 2 ** (len(config.calc_item)))]


def start():
    start_time = time.time()
    print('starting at ', config.curr_time())
    hid = 0
    for h in [h for h in config.simple_history]:
        review = {'hid': hid, 'qi_shu': h['qi_shu'], 'next': h['next_qi_shu'],
                  'max_multi_yes': 0, 'max_multi_no': 0,
                  'current_multi_yes': 0, 'current_multi_no': 0,
                  'details': {}}
        for f in formulas:
            if hid > 0:
                stat(f, hid - 1)
        for f in formulas:
            calc(f, hid)
            if not str(f['current_multi_yes']) in review['details']:
                review['details'][str(f['current_multi_yes'])] = set()
            review['details'][str(f['current_multi_yes'])].add(f['result'])
            if review['max_multi_yes'] < f['max_multi_yes']:
                review['max_multi_yes'] = f['max_multi_yes']
            if review['max_multi_no'] < f['max_multi_no']:
                review['max_multi_no'] = f['max_multi_no']
            if review['current_multi_yes'] < f['current_multi_yes']:
                review['current_multi_yes'] = f['current_multi_yes']
            if review['current_multi_no'] < f['current_multi_no']:
                review['current_multi_no'] = f['current_multi_no']
        reviews.append(review)
        hid += 1
    file = open(os.path.join(config.work_dir, 'review_tm.txt'), 'w')
    for review in reviews:
        file.write(str(review) + '\n')
    file.close()
    for f in formulas:
        if f['current_multi_yes'] >= 2:
            print('fid = {}, current_multi_yes = {}'.format(f['fid'], f['current_multi_yes']))
    end_time = time.time()
    print('finished at ', config.curr_time(), ', time elapsed ', end_time - start_time)


def calc(f, hid):
    flag_key = list(zip(f['formula'], config.calc_item))
    tmp = 0
    for flag, key in flag_key:
        if flag == '1':
            tmp += config.simple_history[hid][key]
    f['calc_result'] = tmp % 49
    f['result'] = f['calc_result']
    return f


def stat(f, hid):
    if config.simple_history[hid + 1]['tm|hm'] == f['result']:
        f['total_yes'] += 1
        f['current_multi_yes'] += 1
        f['current_multi_no'] = 0
        if f['current_multi_yes'] > f['max_multi_yes']:
            f['max_multi_yes'] = f['current_multi_yes']
    else:
        f['total_no'] += 1
        f['current_multi_no'] += 1
        f['current_multi_yes'] = 0
        if f['current_multi_no'] > f['max_multi_no']:
            f['max_multi_no'] = f['current_multi_no']
    return f


if __name__ == "__main__":
    config_file_name = "base.config"
    if len(sys.argv) <= 1:
        work_dir = os.getcwd()
    else:
        work_dir = sys.argv[1]

    try:
        print()
        print("-" * 60)
        config.init(work_dir, config_file_name)
        print("total history records are {}, {}-{}".format(
            len(config.history), config.history[-1]["qi_shu"], config.history[0]["qi_shu"]))
        start()
    except Exception as e:
        print(e)
