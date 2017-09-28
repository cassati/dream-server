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
                review['details'][str(f['current_multi_yes'])] = {'times': f['current_multi_yes'], 'odd': 0, 'even': 0}
            if f['result'] == 1:
                review['details'][str(f['current_multi_yes'])]['odd'] += 1
            else:
                review['details'][str(f['current_multi_yes'])]['even'] += 1
            if review['max_multi_yes'] < f['max_multi_yes']:
                review['max_multi_yes'] = f['max_multi_yes']
            if review['max_multi_no'] < f['max_multi_no']:
                review['max_multi_no'] = f['max_multi_no']
            if review['current_multi_yes'] < f['current_multi_yes']:
                review['current_multi_yes'] = f['current_multi_yes']
            if review['current_multi_no'] < f['current_multi_no']:
                review['current_multi_no'] = f['current_multi_no']
        schema(review)
        reviews.append(review)
        hid += 1
    file = open(os.path.join(config.work_dir, 'review.txt'), 'w')
    for review in reviews:
        file.write(str(review) + '\n')
    file.close()
    line = "{: <7} " + " {: >9}" * len(list(betting.keys()))
    f2 = open(os.path.join(config.work_dir, 'stat.txt'), 'w')
    f2.write(line.format('qi_shu', *list(sorted(betting.keys()))) + '\n')
    for review in reviews:
        f2.write(line.format(review['qi_shu'], *[review['bet'][k]['result'] for k in sorted(betting.keys())]) + '\n')
    for k in sorted(betting.keys()):
        f2.write('{} agg: {}\n'.format(k, reduce(lambda x, y: x + y, [r['bet'][k]['result'] for r in reviews])))
    f2.close()
    end_time = time.time()
    print('finished at ', config.curr_time(), ', time elapsed ', end_time - start_time)


def calc(f, hid):
    flag_key = list(zip(f['formula'], config.calc_item))
    tmp = 0
    for flag, key in flag_key:
        if flag == '1':
            tmp += config.simple_history[hid][key]
    f['calc_result'] = tmp % 49
    f['result'] = f['calc_result'] % 2
    return f


def stat(f, hid):
    if config.simple_history[hid + 1]['tm|hm'] % 2 == f['result']:
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


def schema(review):
    review['bet'] = {k: schema_calc(review, betting[k]) for k in sorted(betting.keys())}


def schema_calc(review, bets):
    bet = {'odd': 0, 'even': 0}
    details = review['details']
    for k in details:
        times, odd, even = int(details[k]['times']), details[k]['odd'], details[k]['even']
        bet['odd'] += odd * bets[times]
        bet['even'] += even * bets[times]
    if review['hid'] == len(config.simple_history):
        bet['next_tm'] = 0
        bet['result'] = 0
    else:
        bet['next_tm'] = config.simple_history[review['hid']]['tm|hm']
        bet['result'] = (bet['even'] - bet['odd']) if bet['next_tm'] % 2 == 0 else (bet['odd'] - bet['even'])
    return bet


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


betting = {
    'normal': list(range(1, 30)),
    'doub': [2**n for n in range(30)],
    'doub_2': [2**n if n < 2 else 2**2 for n in range(30)],
    'doub_3': [2**n if n < 3 else 2**3 for n in range(30)],
    'doub_4': [2**n if n < 4 else 2**4 for n in range(30)],
    'doub_5': [2**n if n < 5 else 2**5 for n in range(30)],
    'doub_6': [2**n if n < 6 else 2**6 for n in range(30)],
    'doub_7': [2**n if n < 7 else 2**7 for n in range(30)],
    'doub_8': [2**n if n < 8 else 2**8 for n in range(30)],
    'doub_9': [2**n if n < 9 else 2**9 for n in range(30)],
    'doub_10': [2**n if n < 10 else 2**10 for n in range(30)],
    'doub_11': [2**n if n < 11 else 2**11 for n in range(30)],
    'doub_12': [2**n if n < 12 else 2**12 for n in range(30)],
    'doub_13': [2**n if n < 13 else 2**13 for n in range(30)],
    'doub_14': [2**n if n < 14 else 2**14 for n in range(30)],
    'doub_15': [2**n if n < 15 else 2**15 for n in range(30)],
    'doub_16': [2**n if n < 16 else 2**16 for n in range(30)],
    'doub_17': [2**n if n < 17 else 2**17 for n in range(30)],
    'doub_18': [2**n if n < 18 else 2**18 for n in range(30)],
    'doub_19': [2**n if n < 19 else 2**19 for n in range(30)],
    'doub_20': [2**n if n < 20 else 2**20 for n in range(30)],
    'doub_21': [2**n if n < 21 else 2**21 for n in range(30)],
    'doub_22': [2**n if n < 22 else 2**22 for n in range(30)],
    'doub_23': [2**n if n < 23 else 2**23 for n in range(30)],
    'doub_24': [2**n if n < 24 else 2**24 for n in range(30)],
    'doub_25': [2**n if n < 25 else 2**25 for n in range(30)],
    'fibs': [2 ** n for n in range(30)],
    'fibs_2': [2 ** n if n < 2 else 2 ** 2 for n in range(30)],
    'fibs_3': [2 ** n if n < 3 else 2 ** 3 for n in range(30)],
    'fibs_4': [2 ** n if n < 4 else 2 ** 4 for n in range(30)],
    'fibs_5': [2 ** n if n < 5 else 2 ** 5 for n in range(30)],
    'fibs_6': [2 ** n if n < 6 else 2 ** 6 for n in range(30)],
    'fibs_7': [2 ** n if n < 7 else 2 ** 7 for n in range(30)],
    'fibs_8': [2 ** n if n < 8 else 2 ** 8 for n in range(30)],
    'fibs_9': [2 ** n if n < 9 else 2 ** 9 for n in range(30)],
    'fibs_10': [2 ** n if n < 10 else 2 ** 10 for n in range(30)],
    'fibs_11': [2 ** n if n < 11 else 2 ** 11 for n in range(30)],
    'fibs_12': [2 ** n if n < 12 else 2 ** 12 for n in range(30)],
    'fibs_13': [2 ** n if n < 13 else 2 ** 13 for n in range(30)],
    'fibs_14': [2 ** n if n < 14 else 2 ** 14 for n in range(30)],
    'fibs_15': [2 ** n if n < 15 else 2 ** 15 for n in range(30)],
    'fibs_16': [2 ** n if n < 16 else 2 ** 16 for n in range(30)],
    'fibs_17': [2 ** n if n < 17 else 2 ** 17 for n in range(30)],
    'fibs_18': [2 ** n if n < 18 else 2 ** 18 for n in range(30)],
    'fibs_19': [2 ** n if n < 19 else 2 ** 19 for n in range(30)],
    'fibs_20': [2 ** n if n < 20 else 2 ** 20 for n in range(30)],
    'fibs_21': [2 ** n if n < 21 else 2 ** 21 for n in range(30)],
    'fibs_22': [2 ** n if n < 22 else 2 ** 22 for n in range(30)],
    'fibs_23': [2 ** n if n < 23 else 2 ** 23 for n in range(30)],
    'fibs_24': [2 ** n if n < 24 else 2 ** 24 for n in range(30)],
    'fibs_25': [2 ** n if n < 25 else 2 ** 25 for n in range(30)],
}


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
