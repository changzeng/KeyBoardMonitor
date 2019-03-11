# encoding: utf-8

import os
import time
import ujson
from collections import defaultdict

file_name = "output.log"
KEY_MAP = {
    "\x05": "ins"
}


def get_raw_data():
    res = []
    with open(file_name) as fd:
        for line in fd:
            line = line.strip().split(" ")
            key = line[2]
            if len(key) > 1 and key[0] in {"'", "\""}:
                key = key[1:-1]
                if key == "\\\\":
                    key = "\\"
            elif key.startswith("Key."):
                key = key.replace("Key.", "")
            if len(key) == 1 and 65 <= ord(key) <= 90:
                key = key.lower()
            line[2] = key
            res.append(line)
    return res


def cache(file_name, cache_time=300):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if (not os.path.exists(file_name)) or os.stat(file_name).st_mtime-time.time()>=cache_time:
                res = func(*args, **kwargs)
                with open(file_name, "w") as fd:
                    ujson.dump(res, fd)
                return res
            else:
                with open(file_name) as fd:
                    return ujson.load(fd)
        return wrapper
    return decorator


# @cache("data/daily_log_time.json")
def get_daily_log_time(raw_data):
    res = defaultdict(lambda : defaultdict(int))
    for item in raw_data:
        day, key = item[0], item[2]
        res[day][key] += 1
    return res


# @cache("data/daily_total_press_time.json")
def get_daily_total_press_time(raw_data):
    press_dict = {}
    res = defaultdict(lambda :defaultdict(float))
    for item in raw_data:
        day = item[0]
        second, millsec = item[1].split(",")
        timestr = "{0} {1}".format(day, second)
        timestamp = time.mktime(time.strptime(timestr, "%Y-%m-%d %H:%M:%S"))
        timestamp = timestamp + float(millsec)/1000

        key = item[2]
        op = item[3]
        if op == "p":
            if press_dict.get(key, None) in {None, -1}:
                press_dict[key] = timestamp
        elif op == "r":
            if press_dict.get(key, None) not in {None, -1}:
                timesep = timestamp - press_dict[key]
                if timesep <= 10:
                    res[day][key] += timesep
                    res[day][key] = round(res[day][key], 2)
                press_dict[key] = -1
    return res


if __name__ == "__main__":
    raw_data = get_raw_data()
    total_press_time = get_daily_total_press_time(raw_data)
    # for day, day_usage in total_press_time.items():
    #     for key, total_time in sorted(day_usage.items(), key=lambda x:x[1], reverse=True):
    #         print(day, key, total_time)
