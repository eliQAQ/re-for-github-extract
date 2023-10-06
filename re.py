import argparse
import os
from time import sleep

import requests
import base64

# 设置 GitHub Token
github_token = ''

# 构建请求头，包含 Authorization 头部
headers = {
    'Authorization': f'token {github_token}'
}


def query_content(repo, keyword2):
    base_url = "https://api.github.com/search/code"
    params = {
        'q': f"{keyword2} in:file repo:{repo}"
    }
    res = requests.get(base_url, headers=headers, params=params)
    if res.status_code == 200:
        data = res.json()
        items = data['items']
        for item in items:
            url = item['url']
            res2 = requests.get(url, headers=headers)
            data2 = res2.json()
            decoded_bytes = base64.b64decode(data2['content'])
            decoded_string = decoded_bytes.decode("utf-8")
            path = str(item['path'])
            path = path.replace("/", ".")
            path = path.replace('\\', ".")
            print(path)

            path2 = f"data/{keyword2}/"
            if not os.path.isdir(path2):
                os.makedirs(path2)
            with open(path2 + path + ".txt", "w", encoding='utf-8') as f:
                f.write(decoded_string)
    elif res.status_code == 403:
        sleep(60)

    else:
        dt = res.json()
        print(dt)
        print(f"Request failed with status code: {res.status_code}")


def query_repo(keyword, keyword2):
    # 构建查询参数
    params = {
        'q': keyword
    }
    # 发起搜索请求
    response = requests.get('https://api.github.com/search/repositories', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        items = data['items']
        projects_list = []

        for item in items:
            repository = item['full_name']
            projects_list.append(repository)
            query_content(repository, keyword2)
            print(f'Repository: {repository}')
            print('-' * 50)
    else:
        print(f"Request failed with status code: {response.status_code}")



parser = argparse.ArgumentParser(description="一个简单的命令行参数示例")

# 添加一个位置参数
parser.add_argument("-k1", default="password", help="库关键字")
parser.add_argument("-k2", default="password", help="内容关键字")

args = parser.parse_args()

data_path = 'data'
if not os.path.isdir(data_path):
    os.makedirs(data_path)

query_repo(args.k1, args.k2)
