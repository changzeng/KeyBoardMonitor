# encoding: utf-8

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


def get_daily_usage():
    raw_data = get_raw_data()
    res = defaultdict(lambda : defaultdict(int))
    for item in raw_data:
        day, key = item[0], item[2]
        res[day][key] += 1
    return ujson.dumps(res)


if __name__ == "__main__":
    print(get_daily_usage())
