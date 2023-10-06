import json
import os
import re
import re_config

directory_path = "../ml/data_output/data_result"
detect_path = "../result/output/output"
output_path = "./ml_wash_data"
output_relation_path = "./ml_wash_relation_data"

for root, dirs, files in os.walk(directory_path):
    for file_name in files:
        if "csv" in file_name:
            continue
        else:
            route_output = os.path.join(output_path, file_name)
            route_information = os.path.join(root, file_name)
            route_detect = os.path.join(detect_path, file_name[:-4])
            output_file = open(route_output, "w", encoding='utf-8')
            detect_file = open(route_detect, "r", encoding='utf-8')
            relation = os.path.join(output_relation_path, file_name[:-4] + "_relation.txt")
            relation_file = open(relation, "w", encoding='utf-8')
            information_file = open(route_information, "r", encoding='utf-8')
            information_file_content = information_file.read()
            information_file.close()
            detect_file_content = detect_file.read()
            now_string = ""
            pre_character = ""
            quotation_mark = 0
            type_mark = 0
            type_string = ""
            bracket_mark = 0
            type_begin = 0

            information_dictionary = {}
            for i, ele in enumerate(information_file_content):
                if i == 0:
                    continue
                if ele == ":" and pre_character == "\"" and type_begin == 1:
                    if now_string not in information_dictionary:
                        information_dictionary.update({now_string: []})
                    type_string = now_string
                    now_string = ""
                    type_begin = 0
                    type_mark = 1  # 寻找类型
                if bracket_mark == 1:
                    if ele == "]":
                        quotation_mark = 0
                        bracket_mark = 0
                        information_dictionary[type_string].append(now_string)
                        now_string = ""
                    if ele == "\"":
                        if quotation_mark == 0:
                            quotation_mark = 1
                            now_string = ""
                    if ele == "," and pre_character == "\"":
                        information_dictionary[type_string].append(now_string)
                        quotation_mark = 0
                elif quotation_mark == 1:
                    if ele == "," and pre_character == "\"":
                        information_dictionary[type_string].append(now_string)
                        quotation_mark = 0
                    if ele == "}" and pre_character == "\"":
                        information_dictionary[type_string].append(now_string)
                        quotation_mark = 0
                if type_mark == 1:
                    if ele == "[":
                        bracket_mark = 1
                        type_mark = 0
                        now_string = ""
                    if ele == "\"":
                        quotation_mark = 1
                        type_mark = 0
                        now_string = ""
                if type_begin == 0 and ele == "\"" and bracket_mark == 0 and quotation_mark == 0:
                    type_begin = 1
                    now_string = ""
                pre_character = ele
                now_string += ele

            information_dictionary_2 = {}
            for key, value in information_dictionary.items():
                mark = 0
                for k in re_config.keyword:
                    if k in key.lower():
                        mark = 1
                if mark == 0:
                    continue
                for v in value:
                    begin = 0
                    end = -1
                    while v[begin] != "\"":
                        begin += 1
                    while v[end] != "\"":
                        end -= 1
                    if end + 1 == 0:
                        value_detect = v[:]
                    else:
                        value_detect = v[: end + 1]
                    value_detect = value_detect[begin:]
                    if value_detect[1:-1] not in detect_file_content:
                        continue
                    information_dictionary_2.update({key: value_detect})
                    output_file.write("{" + key + ":" + value_detect + "}\n")

            if file_name == "shadow.txt" or file_name == "passwd.txt" or file_name == "sam.txt.txt" or file_name == "sam.hiv.txt.txt":
                continue
            information_file = open(route_information, "r", encoding='utf-8')
            information_file_content = information_file.read()
            information_file_content = information_file_content.replace("\n", "")
            line = ""
            pre_character = ""

            for num, i in enumerate(information_file_content):
                line += i
                if num == len(information_file_content) - 1 and i == "}" or i == "}" and information_file_content[num + 1] == "{":
                    relation_dictionary = {}
                    for key, value in information_dictionary_2.items():
                        if value in line:
                            relation_dictionary.update({key: value})
                    if len(relation_dictionary) == 0:
                        continue
                    relation_dictionary_2 = {}
                    for key, value in relation_dictionary.items():
                        re_induction = ""
                        for k in re_config.keyword:
                            if k in key.lower():
                                re_induction = re_config.induction[k]
                                break
                        if re_induction != "":
                            if re_induction not in relation_dictionary_2:
                                relation_dictionary_2.update({re_induction: [value]})
                            else:
                                relation_dictionary_2[re_induction].append(value)
                    x = 0
                    if len(relation_dictionary_2) == 0:
                        continue
                    relation_file.write("{")
                    for key, value in relation_dictionary_2.items():
                        for num, v in enumerate(value):
                            if x == 0:
                                if num == 0:
                                    relation_file.write("\"" + key + "\"" + ":" + v)
                                else:
                                    relation_file.write("\"" + key + str(num) + "\"" + ":" + v)
                                x = 1
                            else:
                                if num == 0:
                                    relation_file.write("," + "\"" + key + "\"" + ":" + v)
                                else:
                                    relation_file.write("," + "\"" + key + str(num) + "\"" + ":" + v)
                    line = ""
                    relation_file.write("}\n")
                pre_character = i
