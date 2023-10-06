import os
import re_config

re_directory = "./re_data"
ml_directory = "./ml_wash_data"
output_directory = "./last_data"


def get_record(content):
    record = {}
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
            if now_string not in record:
                record.update({now_string: []})
            type_string = now_string
            now_string = ""
            type_begin = 0
            type_mark = 1
        if quotation_mark == 1:
            if ele == "," and pre_character == "\"":
                record[type_string].append(now_string)
                quotation_mark = 0
            if ele == "}" and pre_character == "\"":
                record[type_string].append(now_string)
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
    return record


for root, dirs, files in os.walk(ml_directory):
    for file_name in files:
        re_file_path = os.path.join(re_directory, file_name)
        ml_file_path = os.path.join(root, file_name)
        output_file_path = os.path.join(output_directory, file_name)
        re_file = open(re_file_path, "r", encoding='utf-8')
        ml_file = open(ml_file_path, "r", encoding='utf-8')
        output_file = open(output_file_path, "w", encoding='utf-8')
        re_file_content = re_file.read()
        ml_file_content = ml_file.read()
        re_record = get_record(re_file_content)
        ml_record = get_record(ml_file_content)
        re_record_induction = {}
        ml_record_induction = {}
        # print(re_record)
        # print(ml_record)
        for key, value in re_record.items():
            re_induction = ""
            for k in re_config.keyword:
                if k in key.lower():
                    re_induction = re_config.induction[k]
                    break
            if re_induction != "":
                if re_induction not in re_record_induction:
                    re_record_induction.update({re_induction: []})
            for v in value:
                re_record_induction[re_induction].append(v)

        for key, value in ml_record.items():
            ml_induction = ""
            for k in re_config.keyword:
                if k in key.lower():
                    ml_induction = re_config.induction[k]
                    break
            if ml_induction != "":
                if ml_induction not in ml_record_induction:
                    ml_record_induction.update({ml_induction: []})
            for v in value:
                ml_record_induction[ml_induction].append(v)

        # print(file_name)
        # print(re_record_induction)
        # print(ml_record_induction)
        record_induction = {}
        judge = set()
        for re_key, re_value in re_record_induction.items():
            value_set = set()
            for re_v in re_value:
                if re_v in judge:
                    continue
                judge.add(re_v)
                value_set.add(re_v)
            record_induction.update({re_key: value_set})
            if file_name == "shadow.txt" or file_name == "passwd.txt" or file_name == "sam.txt.txt":
                continue
            for ml_key, ml_value in ml_record_induction.items():
                if ml_key == re_key:
                    for v in ml_value:
                        if v in judge:
                            continue
                        judge.add(v)
                        record_induction[re_key].add(v)

        for ml_key, ml_value in ml_record_induction.items():
            if file_name == "shadow.txt" or file_name == "passwd.txt" or file_name == "sam.txt.txt" or file_name == "sam.hiv.txt.txt":
                continue
            if ml_key not in record_induction:
                record_induction.update({ml_key: ml_value})

        for key, value in record_induction.items():
            for v in value:
                if key == "port" and len(v) >= 7:
                    continue
                output_file.write("{" + "\"" + key + "\"" + ":" + v + "}\n")

for root, dirs, files in os.walk(re_directory):
    for file_name in files:
        if ".csv" in file_name:
            re_file_path = os.path.join(re_directory, file_name)
            output_file_path = os.path.join(output_directory, file_name)
            re_file = open(re_file_path, "r", encoding='utf-8')
            re_file_content = re_file.read()
            output_file = open(output_file_path, "w", encoding='utf-8')
            output_file.write(re_file_content)
