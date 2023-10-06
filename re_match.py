import csv
import os
import re

# 匹配包含省略和不含省略的ipv6地址
ipv6_pattern = r'(([\da-fA-F]{1,4}:){7}[\da-fA-F]{1,4}|:((:[\da−fA−F]1,4)1,6|:))'
# 匹配ipv4
ipv4_pattern = r'(([ ]?(1\d\d|2[0-4]\d|25[0-5]|[1-9]?\d)\.[ ]?){3}[ ]?(1[0-9][0-9]|2[0-4]\d|25[0-5]|[1-9]?\d|))'
# 匹配ipv4加端口
ipv4_with_port_pattern = r'((([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.){3}([1-9]?\d|1\d\d|2[0-4]\d|25[0-5]):\d{1,5})'
# 匹配mac地址
mac_pattern = r'(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})'
# 匹配email地址
email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
# 匹配电话号
phone_pattern = r'((\+86-)?1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8})'
# 匹配身份证号
id_card_pattern = r'(([1-8]\d{5}(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9Xx]))'
# 银行卡号
bank_account_pattern = r'(([1-9]{1})(\d{15,18}|\d{11}))'
# url
url_pattern = r'((socks5|https?|jdbc:mysql|file|ftp|mysql)://[^\'"\s（），。]+)'
# domain
domain_pattern = r'([^\s\n（）\u4E00-\u9FFF]+\.(com|cn|net|org|edu|info|gov))'
# jwt
jwt_pattern = r'([A-Za-z0-9_]{15,}\.[A-Za-z0-9_]{15,}\.[A-Za-z0-9_]{15,})'
# passwd
passwd_pattern = r'(([^:\n]+):([^:\n]+):([^:\n]+):([^:\n]+):([^:\n]*):([^:\n]+):([^:\n]+))'
# shadow
shadow_pattern = r'(([^:\s\n]+):([^:\n]*):([^:\n]*):([^:\n]*):([^:\n]*):([^:\n]*):([^:\n]?):([^:\n]?):([^:\n]?)|([^:\s\n]+):([^:\n]+):([^:\n]+):([^:\n]+):([^:\n]*):([^:\n]*):([^:\n]*))'
# rsa_pem_public_key ?号表示非贪婪匹配 注意[].被消解了意义
rsa_pem_public_key_pattern = r'(-----.*?PUBLIC KEY-----([\S\s\n]*?)-----.*?PUBLIC KEY-----)'
# rsa_pem_private_key
rsa_pem_private_key_pattern = r'(-----.*?PRIVATE KEY-----([\S\s\n]*?)-----.*?PRIVATE KEY-----)'
# rsa_ssh_public_key ?:表示不捕获
rsa_ssh_public_key_pattern = r'ssh-rsa\s+(\S+)(\s+[^\s]+)?'
# username
username_pattern = r'((username|user)\s*[=:]\s*([^\n\s]+))'
# username_level2
username_pattern2 = r'(\-u\s*([^\n\s]+))'
# password_level2
password_pattern2 = r'((\-p|passwd)\s*([^\n\s]+))'
# password
password_pattern = r'((password|passwd)\s*[=:]\s*([^\n\s]+))'
# access_key
access_key_pattern = r'((accesskey)\s*[=:]\s*([^\n\s]+))'
# secret_key
secret_key_pattern = r'((secretkey)\s*[=:]\s*([^\n\s]+))'
# password_cn
password_cn_pattern = r'((密码|口令)\s*[=:：是为\n\s]\s*([^\n\s)（），\u4E00-\u9FFF]+))'
# key
key_pattern = r'((密钥)\s*[=:：是为\n\s]\s*([^\n\s)（），\u4E00-\u9FFF]+))'
# username_cn
username_cn_pattern = r'((学号|身份证号||用户名|用户)\s*[=:：是为\n\s]?\s*([^。、”\n\s，（）\u4E00-\u9FFF]+))'
# phone_cn
phone_cn_pattern = r'(电话(号码)?\s*[是为=:：\n\s]\s*([0-9]+))'
# 公钥
public_key_cn_pattern = r'(公钥\s*[是为=:：\n\s]\s*([0-9]+))'
# 私钥
private_key_cn_pattern = r'(私钥\s*[是为=:：\n\s]\s*([0-9]+))'
# 匹配端口
port_cn_pattern = r'((tcp|udp|端口|端口号|端口\d*)\s*[是为=:：\n\s]\s*[0-9]{1,5})'
# pin
pin_pattern = r'((pin码|pin)\s*[=:：是为\n\s]\s*([^。、”\n\s，（）\u4E00-\u9FFF]+))'
# token
token_pattern = r'($_SESSION|$_Cookie|PHPSESSID|cookie|session|SessionID\s*[=:\s]\s*([^。、”\n\s，（）\u4E00-\u9FFF]+))'
# certificate
certificate_pattern = r'(-----.*?BEGIN CERTIFICATE-----([\S\s\n]*?)-----.*?END CERTIFICATE-----)'

# patterns = {'ipv6': ipv6_pattern, 'ipv4': ipv4_pattern, 'ipv4_with_port': ipv4_with_port_pattern, 'mac': mac_pattern,
#             'phone': phone_pattern, 'id_card': id_card_pattern, 'bank_account': bank_account_pattern, 'url': url_pattern,
#             'jwt': jwt_pattern, 'passwd': passwd_pattern, 'shadow': shadow_pattern, 'rsa_pem_public_key': rsa_pem_public_key_pattern,
#             'rsa_pem_private_key': rsa_pem_private_key_pattern, 'rsa_ssh_public_key': rsa_ssh_public_key_pattern, 'username': username_pattern,
#             'password': password_pattern, 'cn_password': password_cn_pattern, 'cn_phone': phone_cn_pattern, 'domain': domain_pattern,
#             'username_cn': username_cn_pattern, 'port':port_cn_pattern, 'mail': email_pattern}

keyword = (
    "ip", "username", "user", "password", "pass", "passwd", "port", "端口", "用户名", "密码", "用户", "口令", "密钥",
    "key", "公钥", "私钥",
    "path", "操作系统", "system", "cookie", "session", "rsa", "ssh", "地址")

patterns = {'ip': ipv4_pattern, 'ipv4_with_port': ipv4_with_port_pattern, 'mac': mac_pattern,
            'phone': phone_pattern, 'id_card': id_card_pattern,  # 'bank_account': bank_account_pattern,
            'url': url_pattern,
            'jwt': jwt_pattern, 'passwd': passwd_pattern, 'shadow': shadow_pattern,
            'rsa_pem_public_key': rsa_pem_public_key_pattern,
            'rsa_pem_private_key': rsa_pem_private_key_pattern, 'rsa_ssh_public_key': rsa_ssh_public_key_pattern,
            'username': username_pattern, 'key': key_pattern,
            'password': password_pattern, 'cn_password': password_cn_pattern, 'cn_phone': phone_cn_pattern,
            'domain': domain_pattern, "public_key_cn": public_key_cn_pattern, "private_key_cn": private_key_cn_pattern,
            'username_cn': username_cn_pattern, 'port': port_cn_pattern, 'mail': email_pattern,
            'access_key': access_key_pattern, 'secret_key': secret_key_pattern,
            'pin': pin_pattern, 'certificate': certificate_pattern, 'token': token_pattern}

# patterns_level2 = {'username_level2': username_pattern2, 'password_level2': password_pattern2}
#
# patterns.update(patterns_level2)

directory_path = "../result/output/output"
output_path = "./re_data"
for root, dirs, files in os.walk(directory_path):
    for file_name in files:
        print("\n文件" + file_name + "敏感信息有:")
        file_path = os.path.join(root, file_name)
        output_file_path = os.path.join(output_path, file_name + ".txt")
        output_file_path_relation = os.path.join(output_path, file_name + "_relation.txt")
        w = open(output_file_path, "w", encoding='utf-8')
        w_relation = open(output_file_path_relation, "w", encoding='utf-8')
        if file_name.endswith(".csv"):
            f = open(file_path, "r", encoding="utf-8")
            csv_reader = csv.reader(f)
            mark = {}
            minn = -1
            for i, row in enumerate(csv_reader):
                if i == 0:
                    for j, ele in enumerate(row):
                        for name in keyword:
                            if name in ele.lower():
                                mark.update({j: name})
                                if minn == -1:
                                    minn = j
                else:
                    if minn != -1:
                        w_relation.write("{")
                        for j, ele in enumerate(row):
                            if j in mark.keys():
                                w.write("{" + f'\"{mark[j]}\":\"{ele}\"' + "}\n")
                                if j == minn:
                                    w_relation.write(f'\"{mark[j]}\":\"{ele}\"')
                                else:
                                    w_relation.write(f',\"{mark[j]}\":\"{ele}\"')
                                # print(f'{mark[j]} : {ele}')
                        w_relation.write("}\n")
        else:
            f = open(file_path, encoding='utf-8')
            match_str = f.read()
            f.close()
            judge = set()
            username = []
            password = []
            port = []
            ip = []
            ip_with_port = []
            mac = []
            public_key = []
            private_key = []
            access_key = []
            secret_key = []
            token = []
            url = []
            for key, value in patterns.items():
                matches = re.findall(value, match_str, re.IGNORECASE)
                matches2 = re.finditer(value, match_str, re.IGNORECASE)
                for match in matches2:
                    if key == 'username' or key == 'username_cn' or key == 'mail' or key == 'cn_phone':
                        username.append(match)
                    if key == 'password' or key == 'cn_password':
                        password.append(match)
                    if key == 'ip':
                        ip.append(match)
                    if key == 'ipv4_with_port':
                        ip_with_port.append(match)
                    if key == 'mac':
                        mac.append(match)
                    if key == 'rsa_pem_public_key_pattern':
                        public_key.append(match)
                    if key == 'rsa_pem_private_key_pattern':
                        private_key.append(match)
                    if key == 'access_key':
                        access_key.append(match)
                    if key == 'secret_key':
                        secret_key.append(match)
                    if key == 'token':
                        token.append(match)
                    if key == 'url' or key == 'domain':
                        url.append(match)
                if matches is not None:
                    for index in matches:
                        if isinstance(index, tuple):
                            if index[0] in judge:
                                continue
                            else:
                                judge.add(index[0])
                            x1 = index[0].replace("\n", "")
                            if key == "ipv4_with_port":
                                x2 = re.split(":", x1)
                                w.write("{" + f'\"ip\":\"{x2[0]}\"' + "}\n")
                                w.write("{" + f'\"port\":\"{x2[1]}\"' + "}\n")
                            else:
                                w.write("{" + f'\"{key}\":\"{x1}\"' + "}\n")
                            # print(f'{key} : {index[0]}')
                        else:
                            if index in judge:
                                continue
                            else:
                                judge.add(index)
                            x2 = index.replace("\n", "")
                            w.write("{" + f'\"{key}\":\"{x2}\"' + "}\n")
                            # print(f'{key} : {index}')
            #  策略1取最近值
            distance = 10000
            for p in password:
                mark = None
                for u in username:
                    if u.start() <= p.start():
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    else:
                        if distance < abs(u.start() - p.start()):
                            break
                        else:
                            distance = abs(u.start() - p.start())
                            mark = u
                if mark is not None:
                    w_relation.write("{")
                    x1 = mark.group().replace("\n", "")
                    x2 = p.group().replace("\n", "")
                    w_relation.write(f'\"uesrname\":\"{x1}\"')
                    w_relation.write(f',\"password\":\"{x2}\"')
                    w_relation.write("}\n")

            for p in port:
                mark = None
                for u in ip:
                    if u.start() <= p.start():
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    else:
                        if distance < abs(u.start() - p.start()):
                            break
                        else:
                            distance = abs(u.start() - p.start())
                            mark = u
                if mark is not None:
                    w_relation.write("{")
                    x1 = mark.group().replace("\n", "")
                    x2 = p.group().replace("\n", "")
                    w_relation.write(f'\"ip\":\"{x1}\"')
                    w_relation.write(f',\"port\":\"{x2}\"')
                    w_relation.write("}\n")

            for p in private_key:
                mark = None
                for u in public_key:
                    if u.start() <= p.start():
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    else:
                        if distance < abs(u.start() - p.start()):
                            break
                        else:
                            distance = abs(u.start() - p.start())
                            mark = u
                if mark is not None:
                    w_relation.write("{")
                    x1 = mark.group().replace("\n", "")
                    x2 = p.group().replace("\n", "")
                    w_relation.write(f'\"private_key\":\"{x1}\"')
                    w_relation.write(f',\"public_key\":\"{x2}\"')
                    w_relation.write("}\n")

            for p in mac:
                mark = None
                for u in ip:
                    if u.start() <= p.start():
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    else:
                        if distance < abs(u.start() - p.start()):
                            break
                        else:
                            distance = abs(u.start() - p.start())
                            mark = u
                if mark is not None:
                    w_relation.write("{")
                    x1 = mark.group().replace("\n", "")
                    x2 = p.group().replace("\n", "")
                    w_relation.write(f'\"ip\":\"{x1}\"')
                    w_relation.write(f',\"mac\":\"{x2}\"')
                    w_relation.write("}\n")

            for p in token:
                mark = None
                for u in url:
                    if u.start() <= p.start():
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    else:
                        if distance < abs(u.start() - p.start()):
                            break
                        else:
                            distance = abs(u.start() - p.start())
                            mark = u
                if mark is not None:
                    w_relation.write("{")
                    x1 = mark.group().replace("\n", "")
                    x2 = p.group().replace("\n", "")
                    w_relation.write(f'\"url\":\"{x1}\"')
                    w_relation.write(f',\"token\":\"{x2}\"')
                    w_relation.write("}\n")

            vis = set()
            for i in ip_with_port:
                if i.group() in vis:
                    continue
                vis.add(i.group())
                result = re.split(r':', i.group(), flags=re.IGNORECASE)
                w_relation.write("{")
                x1 = result[0].replace(" ", "")
                x2 = result[1].replace(" ", "")
                w_relation.write(f'\"ip\":\"{x1}\"')
                w_relation.write(f',\"port\":\"{x2}\"')
                w_relation.write("}\n")

            for p in secret_key:
                mark = None
                for u in access_key:
                    if u.start() <= p.start():
                        if distance > abs(u.start() - p.start()):
                            distance = abs(u.start() - p.start())
                            mark = u
                    else:
                        if distance < abs(u.start() - p.start()):
                            break
                        else:
                            distance = abs(u.start() - p.start())
                            mark = u
                if mark is not None:
                    w_relation.write("{")
                    x1 = mark.group().replace("\n", "")
                    x2 = p.group().replace("\n", "")
                    w_relation.write(f'\"url\":\"{x1}\"')
                    w_relation.write(f',\"token\":\"{x2}\"')
                    w_relation.write("}\n")
