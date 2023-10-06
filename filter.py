import os
import re
import shutil

# 匹配包含省略和不含省略的ipv6地址
ipv6_pattern = r'(?i)(([\da-fA-F]{1,4}:){7}[\da-fA-F]{1,4}|:((:[\da−fA−F]1,4)1,6|:))'
# 匹配ipv4
ipv4_pattern = r'(?i)((([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.){3}([1-9]?\d|1\d\d|2[0-4]\d|25[0-5]))'
# 匹配ipv4加端口
ipv4_with_port_pattern = r'(?i)((([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.){3}([1-9]?\d|1\d\d|2[0-4]\d|25[0-5]):\d{1,5})'
# 匹配mac地址
mac_pattern = r'(?i)(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})'
# 匹配email地址
email_pattern = r'(\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)'
# 匹配电话号
phone_pattern = r'(?i)((\+86-)?1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8})'
# 匹配身份证号
id_card_pattern = r'(?i)(([1-8]\d{5}(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9Xx]))'
# 银行卡号
bank_account_pattern = r'(?i)(([1-9]{1})(\d{15,18}|\d{11}))'
# url
url_pattern = r'(?i)((https?|jdbc:mysql|file|ftp|mysql)://[^\'"\s]+)'
# domain
domain_pattern = r'(?i)([^\s\n（）\u4E00-\u9FFF]+\.(com|cn|net|org|edu|info|gov))'
# jwt
jwt_pattern = r'(?i)([A-Za-z0-9_]{15,}\.[A-Za-z0-9_]{15,}\.[A-Za-z0-9_]{15,})'
# passwd
passwd_pattern = r'(?i)(([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]+):([^:\s\n]+))'
# shadow
shadow_pattern = r'(?i)(([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]?):([^:\s]?):([^:\s\n]?))'
# rsa_pem_public_key ?号表示非贪婪匹配 注意[].被消解了意义
rsa_pem_public_key_pattern = r'(?i)(-----.*?PUBLIC KEY-----([\S\s\n]*?)-----.*?PUBLIC KEY-----)'
# rsa_pem_private_key
rsa_pem_private_key_pattern = r'(?i)(-----.*?PRIVATE KEY-----([\S\s\n]*?)-----.*?PRIVATE KEY-----)'
# rsa_ssh_public_key ?:表示不捕获
rsa_ssh_public_key_pattern = r'(?i)ssh-rsa\s+(\S+)(\s+[^\s]+)?'
# username
username_pattern = r'(?i)((username|user)\s*[=:]\s*([^\n\s]+))'
# password
password_pattern = r'(?i)((password|passwd)\s*[=:]\s*([^\n\s]+))'
# password_cn
password_cn_pattern = r'(?i)((密码|密钥)\s*[=:：是为\n\s]\s*([^\n\s)（），\u4E00-\u9FFF]+))'
# username_cn
username_cn_pattern = r'(?i)((学号|身份证号|银行卡号|卡号|用户名|用户)\s*[=:：是为\n\s]\s*([^\n\s，（）\u4E00-\u9FFF]+))'
# phone_cn
phone_cn_pattern = r'(?i)(电话(号码)?\s*[是为=:：\n\s]?\s*([0-9]+))'
# 匹配端口
port_cn_pattern = r'(?i)((Tcp|TCP|tcp|Udp|UDP|udp|端口|端口号|端口\d*)\s*[是为=:：\n\s]?\s*[0-9]{1,5})'
# define_name
define_pattern = r"define\(\'\'\)"

patterns = {'ipv6': ipv6_pattern, 'ipv4': ipv4_pattern, 'ipv4_with_port': ipv4_with_port_pattern, 'mac': mac_pattern,
            'phone': phone_pattern, 'id_card': id_card_pattern, 'bank_account': bank_account_pattern, 'url': url_pattern,
            'jwt': jwt_pattern, 'passwd': passwd_pattern, 'shadow': shadow_pattern, 'rsa_pem_public_key': rsa_pem_public_key_pattern,
            'rsa_pem_private_key': rsa_pem_private_key_pattern, 'rsa_ssh_public_key': rsa_ssh_public_key_pattern, 'username': username_pattern,
            'password': password_pattern, 'cn_password': password_cn_pattern, 'cn_phone': phone_cn_pattern, 'domain': domain_pattern,
            'username_cn': username_cn_pattern, 'port':port_cn_pattern, 'mail': email_pattern}


def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append([os.path.join(root, file), file])
    return file_list


target_directory = "data"

get_files = list_files(target_directory)
destination_folder = "filter_data"
for x in get_files:
    f = open(x[0], encoding="utf-8")
    match_str = f.read()
    f.close()
    for key, value in patterns.items():
        matches = re.findall(value, match_str)
        if matches is not None and len(matches) != 0:
            write_path = os.path.join(destination_folder, x[1])
            with open(write_path + ".match", "a", encoding="utf-8") as w:
                w.write(key + ":\n")
                for match in matches:
                    w.write(match[0])
                    w.write("\n")
                w.write("\n\n")
            shutil.copy(x[0], destination_folder)