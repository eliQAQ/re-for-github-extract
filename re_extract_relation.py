import ast
import json
import os
import re

directory_path = "../result/output/output"
last_directory = "./last_data"
relation_directory = "./ml_wash_relation_data"


def merge_relation(getrecord):
    ret_record = []
    for i in getrecord:
        vis_1 = 0
        now_item = i
        del_list = []
        for num in range(len(ret_record)):
            vis_0 = 0
            for y_key, y_value in ret_record[num].items():
                for x_key, x_value in i.items():
                    if y_value in x_value or x_value in y_value:
                        del_list.append(num)
                        vis_0 = 1
                        break
                    if vis_0 == 1:
                        break
                if vis_0 == 1:
                    break
            if vis_0 == 1:
                for y_key, y_value in ret_record[num].items():
                    vis_1 = 1
                    for x_key, x_value in i.items():
                        if y_value in x_value or x_value in y_value:
                            vis_1 = 0
                    if vis_1 == 1:
                        now_item.update({y_key: y_value})

        new_list = []
        for j in range(len(ret_record)):
            vis_2 = 0
            for z in del_list:
                if z == j:
                    vis_2 = 1
                    break
            if vis_2 == 0:
                new_list.append(ret_record[j])
        ret_record = new_list
        ret_record.append(now_item)
    return ret_record


def get_record(content):
    getrecord = {}
    now_string = ""
    pre_character = ""
    type_begin = 0
    quotation_mark = 0
    type_mark = 0
    type_string = ""
    for i, ele in enumerate(content):
        if i == 0:
            continue
        if ele == ":" and pre_character == "\"" and type_begin == 1:
            if now_string not in getrecord:
                getrecord.update({now_string: []})
            type_string = now_string
            now_string = ""
            type_begin = 0
            type_mark = 1
        if quotation_mark == 1:
            if ele == "," and pre_character == "\"":
                getrecord[type_string].append(now_string)
                quotation_mark = 0
            if ele == "}" and pre_character == "\"":
                getrecord[type_string].append(now_string)
                quotation_mark = 0
        if type_mark == 1:
            if ele == "\"":
                quotation_mark = 1
                type_mark = 0
                now_string = ""
        if type_begin == 0 and ele == "\"" and quotation_mark == 0:
            # print(now_string)
            type_begin = 1
            now_string = ""
        pre_character = ele
        now_string += ele
    return getrecord


def get_record2(content):
    getrecord_list = []
    now_string = ""
    pre_character = ""
    type_begin = 0
    quotation_mark = 0
    type_mark = 0
    type_string = ""
    getrecord = {}
    for i, ele in enumerate(content):
        if i == 0:
            continue

        if ele == ":" and pre_character == "\"" and type_begin == 1:
            now_string = now_string[1:]
            now_string = now_string[:-1]
            type_string = now_string
            now_string = ""
            type_begin = 0
            type_mark = 1
        if quotation_mark == 1:
            if ele == "," and pre_character == "\"":
                if not (type_string == "port" and len(now_string) >= 7):
                    now_string = now_string[1:]
                    now_string = now_string[:-1]
                    getrecord.update({type_string: now_string})
                quotation_mark = 0
            if ele == "}" and pre_character == "\"":
                if not (type_string == "port" and len(now_string) >= 7):
                    now_string = now_string[1:]
                    now_string = now_string[:-1]
                    getrecord.update({type_string: now_string})
                if len(getrecord) >= 1:
                    getrecord_list.append(getrecord)
                getrecord = {}
                quotation_mark = 0
        if type_mark == 1:
            if ele == "\"":
                quotation_mark = 1
                type_mark = 0
                now_string = ""
        if type_begin == 0 and ele == "\"" and quotation_mark == 0:
            # print(now_string)
            type_begin = 1
            now_string = ""
        pre_character = ele
        now_string += ele
    return getrecord_list


for root, dirs, files in os.walk(directory_path):
    for file_name in files:
        if ".csv" in file_name:
            continue
        else:
            raw_file_path = os.path.join(directory_path, file_name)
            raw_file = open(raw_file_path, "r", encoding='utf-8')
            raw_file_content = raw_file.read()
            detect_file_path = os.path.join(last_directory, file_name)
            output_file_path_relation = os.path.join(last_directory, file_name + "_relation.txt")
            w_relation = open(output_file_path_relation, "w", encoding='utf-8')
            detect_file = open(detect_file_path + ".txt", "r", encoding='utf-8')
            relation_file_path = os.path.join(relation_directory, file_name + "_relation.txt")
            relation_file = open(relation_file_path, "r", encoding='utf-8')
            detect_file_content = detect_file.read()
            relation_file_content = relation_file.read()
            information_record = get_record(detect_file_content)
            relation_record_list = get_record2(relation_file_content)
            #print(relation_record_list)
            username = []
            password = []
            port = []
            ip = []
            mac = []
            public_key = []
            private_key = []
            access_key = []
            secret_key = []
            token = []
            url = []
            salt = []
            record = []
            for key, value in information_record.items():
                key = key[1:]
                key = key[:-1]
                key = key.lower()
                for v in value:
                    v1 = v[1:]
                    v1 = v1[:-1]
                    matches = re.finditer(re.escape(v1), raw_file_content, re.IGNORECASE)
                    for match in matches:
                        if key == 'username':
                            username.append(match)
                        if key == 'password':
                            password.append(match)
                        if key == 'ip':
                            ip.append(match)
                        if key == 'port':
                            port.append(match)
                        if key == 'mac':
                            mac.append(match)
                        if key == 'public_key':
                            public_key.append(match)
                        if key == 'private_key':
                            private_key.append(match)
                        if key == 'access_key':
                            access_key.append(match)
                        if key == 'secret_key':
                            secret_key.append(match)
                        if key == 'token':
                            token.append(match)
                        if key == 'url' or key == 'domain':
                            url.append(match)
                        if key == 'salt':
                            salt.append(match)

                #  策略1取最近值
                for p in password:
                    mark = None
                    distance = 10000
                    for u in username:
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    if mark is not None:
                        # w_relation.write("{")
                        x1 = mark.group().replace("\n", "")
                        x2 = p.group().replace("\n", "")
                        now_record = {"username": x1, "password": x2}
                        record.append(now_record)
                        # w_relation.write(f'\"uesrname\":\"{x1}\"')
                        # w_relation.write(f',\"password\":\"{x2}\"')
                        # w_relation.write("}\n")

                for p in port:
                    mark = None
                    distance = 10000
                    for u in ip:
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    if mark is not None:
                        # w_relation.write("{")
                        x1 = mark.group().replace("\n", "")
                        x2 = p.group().replace("\n", "")
                        # w_relation.write(f'\"ip\":\"{x1}\"')
                        # w_relation.write(f',\"port\":\"{x2}\"')
                        # w_relation.write("}\n")
                        now_record = {"ip": x1, "port": x2}
                        record.append(now_record)

                for p in private_key:
                    mark = None
                    distance = 10000
                    for u in public_key:
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    if mark is not None:
                        # w_relation.write("{")
                        x1 = mark.group().replace("\n", "")
                        x2 = p.group().replace("\n", "")
                        # w_relation.write(f'\"private_key\":\"{x1}\"')
                        # w_relation.write(f',\"public_key\":\"{x2}\"')
                        # w_relation.write("}\n")
                        now_record = {"public_key": x1, "private_key": x2}
                        record.append(now_record)

                for p in mac:
                    mark = None
                    distance = 10000
                    for u in ip:
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    if mark is not None:
                        # w_relation.write("{")
                        x1 = mark.group().replace("\n", "")
                        x2 = p.group().replace("\n", "")
                        # w_relation.write(f'\"ip\":\"{x1}\"')
                        # w_relation.write(f',\"mac\":\"{x2}\"')
                        # w_relation.write("}\n")
                        now_record = {"ip": x1, "mac": x2}
                        record.append(now_record)

                for p in token:
                    mark = None
                    distance = 10000
                    for u in url:
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    if mark is not None:
                        # w_relation.write("{")
                        x1 = mark.group().replace("\n", "")
                        x2 = p.group().replace("\n", "")
                        # w_relation.write(f'\"url\":\"{x1}\"')
                        # w_relation.write(f',\"token\":\"{x2}\"')
                        # w_relation.write("}\n")
                        now_record = {"url": x1, "token": x2}
                        record.append(now_record)

                for p in secret_key:
                    mark = None
                    distance = 10000
                    for u in access_key:
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    if mark is not None:
                        # w_relation.write("{")
                        x1 = mark.group().replace("\n", "")
                        x2 = p.group().replace("\n", "")
                        # w_relation.write(f'\"url\":\"{x1}\"')
                        # w_relation.write(f',\"token\":\"{x2}\"')
                        # w_relation.write("}\n")
                        now_record = {"secret_key": x1, "access_key": x2}
                        record.append(now_record)

                for p in salt:
                    distance = 10000
                    mark = None
                    for u in password:
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    if mark is not None:
                        # w_relation.write("{")
                        x1 = mark.group().replace("\n", "")
                        x2 = p.group().replace("\n", "")
                        now_record = {"password": x1, "salt": x2}
                        record.append(now_record)
                        # w_relation.write(f'\"url\":\"{x1}\"')
                        # w_relation.write(f',\"token\":\"{x2}\"')
                        # w_relation.write("}\n")
            record = record + relation_record_list
            output_record = merge_relation(record)
            for i in output_record:
                w_relation.write("{")
                x = 0
                for key, value in i.items():
                    if x == 0:
                        w_relation.write(f'\"{key}\":\"{value}\"')
                        x = 1
                    else:
                        w_relation.write(f',\"{key}\":\"{value}\"')
                w_relation.write("}\n")
