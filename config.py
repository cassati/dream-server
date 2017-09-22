import os
import time
from datetime import date

# 监听的ip和端口
host = '127.0.0.1'
port = 8078

# 计算任务的大小
task_size = 1000

# 开奖历史记录
history = []
simple_history = []

# 公式计算项目，包括: 6个落球序平码、特码的号码、号码头、波色位、生肖位
calc_item = ["L1|hm",  "L2|hm",  "L3|hm",  "L4|hm",  "L5|hm",  "L6|hm",  "tm|hm",
             # "L1|tou", "L2|tou", "L3|tou", "L4|tou", "L5|tou", "L6|tou", "tm|tou",
             # "L1|bo",  "L2|bo",  "L3|bo",  "L4|bo",  "L5|bo",  "L6|bo",  "tm|bo",
             "L1|sx",  "L2|sx",  "L3|sx",  "L4|sx",  "L5|sx",  "L6|sx",  "tm|sx"]
item_title = ["落球序1平",     "落球序2平",     "落球序3平",     "落球序4平",     "落球序5平",     "落球序6平",     "特",
              # "落球序1平头",   "落球序2平头",   "落球序3平头",   "落球序4平头",   "落球序5平头",   "落球序6平头",   "特头",
              # "落球序1平波",   "落球序2平波",   "落球序3平波",   "落球序4平波",   "落球序5平波",   "落球序6平波",   "特波",
              "落球序1平肖位", "落球序2平肖位", "落球序3平肖位", "落球序4平肖位", "落球序5平肖位", "落球序6平肖位", "特肖位"]

# 开始期数
start_qi_shu = 2002001

# 截止期数，-1代表全部计算
end_qi_shu = -1

# 项目路径
work_dir = os.getcwd()

# 历史记录文件绝对路径
_data_file = r"D:\data\lottery\six.txt"

# 生肖位
_sheng_xiao_wei = {
    "鼠": 1,
    "牛": 2,
    "虎": 3,
    "兔": 4,
    "龙": 5,
    "蛇": 6,
    "马": 7,
    "羊": 8,
    "猴": 9,
    "鸡": 10,
    "狗": 11,
    "猪": 12
}

# 波色位
_bo_se_wei = {
    "红": 0,
    "蓝": 1,
    "绿": 2
}

# 号码
_nums = [
    {"hm":  1, "bo_name": "红"},
    {"hm":  2, "bo_name": "红"},
    {"hm":  3, "bo_name": "蓝"},
    {"hm":  4, "bo_name": "蓝"},
    {"hm":  5, "bo_name": "绿"},
    {"hm":  6, "bo_name": "绿"},
    {"hm":  7, "bo_name": "红"},
    {"hm":  8, "bo_name": "红"},
    {"hm":  9, "bo_name": "蓝"},
    {"hm": 10, "bo_name": "蓝"},
    {"hm": 11, "bo_name": "绿"},
    {"hm": 12, "bo_name": "红"},
    {"hm": 13, "bo_name": "红"},
    {"hm": 14, "bo_name": "蓝"},
    {"hm": 15, "bo_name": "蓝"},
    {"hm": 16, "bo_name": "绿"},
    {"hm": 17, "bo_name": "绿"},
    {"hm": 18, "bo_name": "红"},
    {"hm": 19, "bo_name": "红"},
    {"hm": 20, "bo_name": "蓝"},
    {"hm": 21, "bo_name": "绿"},
    {"hm": 22, "bo_name": "绿"},
    {"hm": 23, "bo_name": "红"},
    {"hm": 24, "bo_name": "红"},
    {"hm": 25, "bo_name": "蓝"},
    {"hm": 26, "bo_name": "蓝"},
    {"hm": 27, "bo_name": "绿"},
    {"hm": 28, "bo_name": "绿"},
    {"hm": 29, "bo_name": "红"},
    {"hm": 30, "bo_name": "红"},
    {"hm": 31, "bo_name": "蓝"},
    {"hm": 32, "bo_name": "绿"},
    {"hm": 33, "bo_name": "绿"},
    {"hm": 34, "bo_name": "红"},
    {"hm": 35, "bo_name": "红"},
    {"hm": 36, "bo_name": "蓝"},
    {"hm": 37, "bo_name": "蓝"},
    {"hm": 38, "bo_name": "绿"},
    {"hm": 39, "bo_name": "绿"},
    {"hm": 40, "bo_name": "红"},
    {"hm": 41, "bo_name": "蓝"},
    {"hm": 42, "bo_name": "蓝"},
    {"hm": 43, "bo_name": "绿"},
    {"hm": 44, "bo_name": "绿"},
    {"hm": 45, "bo_name": "红"},
    {"hm": 46, "bo_name": "红"},
    {"hm": 47, "bo_name": "蓝"},
    {"hm": 48, "bo_name": "蓝"},
    {"hm": 49, "bo_name": "绿"}
]

# 与农历年相关的属性
_cn_attr = {
    "1976": [
        {"hm":  1, "sx_name": "龙"},
        {"hm":  2, "sx_name": "兔"},
        {"hm":  3, "sx_name": "虎"},
        {"hm":  4, "sx_name": "牛"},
        {"hm":  5, "sx_name": "鼠"},
        {"hm":  6, "sx_name": "猪"},
        {"hm":  7, "sx_name": "狗"},
        {"hm":  8, "sx_name": "鸡"},
        {"hm":  9, "sx_name": "猴"},
        {"hm": 10, "sx_name": "羊"},
        {"hm": 11, "sx_name": "马"},
        {"hm": 12, "sx_name": "蛇"}
    ]
}


# 加载配置
def _load_config(config_file_name):
    for line in open(config_file_name, encoding="utf8"):
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        arr = line.split('=')
        if arr[0] == 'data_file':
            global _data_file
            _data_file = arr[1]
        elif arr[0] == 'start_qi_shu':
            global start_qi_shu
            start_qi_shu = int(arr[1])
        elif arr[0] == 'end_qi_shu':
            global end_qi_shu
            end_qi_shu = int(arr[1])
        elif arr[0] == 'host':
            global host
            host = arr[1]
        elif arr[0] == 'port':
            global port
            port = int(arr[1])
        elif arr[0] == 'task_size':
            global task_size
            task_size = int(arr[1])
    return


# 初始化基本属性
def _init_num():
    # 处理号码的头尾和波色位
    for num in _nums:
        num["bo"] = _bo_se_wei[num["bo_name"]]
        num["tou"] = num["hm"] // 10
        num["wei"] = num["hm"] % 10

    # 处理1976的13-49的生肖
    for n in range(13, 50):
        _cn_attr["1976"].append({"hm": n, "sx_name": _cn_attr["1976"][n - 13]["sx_name"]})

    # 处理1977至今的生肖
    for y in range(1977, date.today().year + 1):
        arr = []
        _cn_attr[str(y)] = arr
        for n in range(0, 49):
            arr.append({"hm": n + 1})
        for n in range(49, 1, -1):
            arr[n - 1]["sx_name"] = _cn_attr[str(y - 1)][n - 2]["sx_name"]
        arr[0]["sx_name"] = arr[48]["sx_name"]

    # 处理1976至今的其他属性
    for y in range(1976, date.today().year + 1):
        for obj in _cn_attr[str(y)]:
            obj["cn_year"] = y
            obj["sx"] = _sheng_xiao_wei[obj["sx_name"]]
            obj.update(_nums[obj["hm"] - 1])
    return


# 加载开奖历史记录
def _load_history(datafile):
    for row in open(datafile):
        obj = {}
        history.append(obj)
        arr = row.split()
        obj["qi_shu"] = int(arr[0])
        obj["year"] = int(arr[1])
        obj["month"] = int(arr[2])
        obj["day"] = int(arr[3])
        obj["L1"] = int(arr[4])
        obj["L2"] = int(arr[5])
        obj["L3"] = int(arr[6])
        obj["L4"] = int(arr[7])
        obj["L5"] = int(arr[8])
        obj["L6"] = int(arr[9])
        obj["tm"] = int(arr[10])
        obj["d1"] = int(arr[11])
        obj["d2"] = int(arr[12])
        obj["d3"] = int(arr[13])
        obj["d4"] = int(arr[14])
        obj["d5"] = int(arr[15])
        obj["d6"] = int(arr[16])
        obj["cn_year"] = int(arr[17])
        obj["next_qi_shu"] = int(arr[18])
        obj["tm_sx_name"] = arr[19]
        obj["tm_wei"] = int(arr[20])
        obj["tm_he"] = int(arr[21])
        obj["tm_duan"] = int(arr[22])
        obj["tm_tou"] = int(arr[23])
        obj["tm_ds"] = arr[24]
        obj["tm_dx"] = arr[25]
        obj["tm_bo_name"] = arr[26]
        obj["tm_he_ds"] = arr[27]
        obj["tm_he_dx"] = arr[28]
        obj["tm_wei_dx"] = arr[29]


# 处理历史记录的计算元素值
def _deal_history_calc_item():
    global simple_history
    for h in history:
        cnyear = str(h["cn_year"])
        for item in calc_item:
            numkey, attrkey = item.split("|")
            num = h[numkey]
            h[item] = get_num(cnyear, num)[attrkey]
    # simple history
    less_keys = ["qi_shu", "year", "next_qi_shu"]
    less_keys[-1:] = calc_item[:]
    for h in history:
        if h["qi_shu"] < start_qi_shu:
            continue
        obj = {}
        simple_history.append(obj)
        for k in less_keys:
            obj[k] = h[k]
    simple_history = sorted(simple_history, key=lambda h: h['qi_shu'], reverse=False)
    return


# 执行初始化
def init(workdir, configfilename):
    global work_dir
    work_dir = workdir
    _load_config(os.path.join(work_dir, configfilename))
    _init_num()
    _load_history(_data_file)
    _deal_history_calc_item()


# 按原格式打印开奖历史记录
def save_history(dstfile, extendfield=False):
    f = open(dstfile, 'w')
    try:
        for h in history:
            arr = ["{:0>7}".format(h["qi_shu"]),
                   "{:0>4}".format(h["year"]), "{:0>2}".format(h["month"]),  "{:0>2}".format(h["day"]),
                   "{:0>2}".format(h["L1"]), "{:0>2}".format(h["L2"]), "{:0>2}".format(h["L3"]),
                   "{:0>2}".format(h["L4"]), "{:0>2}".format(h["L5"]), "{:0>2}".format(h["L6"]),
                   "{:0>2}".format(h["tm"]),
                   "{:0>2}".format(h["d1"]), "{:0>2}".format(h["d2"]), "{:0>2}".format(h["d3"]),
                   "{:0>2}".format(h["d4"]), "{:0>2}".format(h["d5"]), "{:0>2}".format(h["d6"]),
                   "{:0>4}".format(h["cn_year"]), "{:0>7}".format(h["next_qi_shu"]), h["tm_sx_name"],
                   "{:0>2}".format(h["tm_wei"]), "{:0>2}".format(h["tm_he"]), "{:0>2}".format(h["tm_duan"]),
                   "{:0>2}".format(h["tm_tou"]),
                   h["tm_ds"], h["tm_dx"], h["tm_bo_name"],
                   h["tm_he_ds"], h["tm_he_dx"],  h["tm_wei_dx"]]
            if extendfield:
                for item in calc_item:
                    arr.append("{:0>2}".format(h[item]))
            f.write("  ".join(arr) + "  \n")
    finally:
        f.close()


# 根据农历年获取号码属性
def get_num(cnyear, x):
    return _cn_attr[str(cnyear)][x - 1]


# 当前时间 yyyy-mm-dd hh:MM:ss
def curr_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

if __name__ == "__main__":
    print()
    print("-" * 60)
    init(os.getcwd(), "base.config")
    print("total history records are {}".format(len(history)))
    # save_history(r"D:\data\lottery\six2.txt")
