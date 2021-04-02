# -*- coding: UTF-8 -*-
# 如果你觉得它帮助到你了，可以移步: https://liaoguoyin.com/donation
#
# 需求：
# 1. 创建并读取本地 code.txt
# 2. 检查 IMEICode 状态，问询是否开始
# 3. 跑步账号个数
# 4. 跑步结果
import os
import requests


def load_local_imei_code(file_name='code.txt') -> list:
    imei_code_list = []
    if not os.path.exists(file_name):
        open(file_name, 'w+', encoding='UTF-8')
        print(f'{file_name} 不存在，已自动创建')
    else:
        print(f'{file_name} 存在，开始处理')
    with open(file_name, encoding='UTF-8') as fp:
        [imei_code_list.append(line[:32]) for line in fp.readlines()]
    return imei_code_list


def check(code) -> bool:
    check_json = requests.get('https://aipao.liaoguoyin.com/check',
                              params={'code': code, 'imei': 'Public-Gist'}).json()
    if check_json.get('code') == 200:
        print(f'{code} 有效，姓名: {check_json.get("data").get("name")}')
        return True
    else:
        print(f'{code} 无效')
        return False


def run(code) -> bool:
    run_json = requests.get('https://aipao.liaoguoyin.com/run', params={'code': code, 'imei': 'Public-Gist'}).json()
    print()
    if run_json.get('code') == 200:
        print(f'{code} 成功')
        return True
    else:
        if '今天已有有效跑步记录' in run_json.get("message"):
            print(f'{code} {run_json.get("message")}', end='')
            return True
        else:
            print(f'{code} 失败，{run_json.get("message")}', end='')
            return False


if __name__ == '__main__':
    code_list = load_local_imei_code()
    print('*' * 50)

    code_count = len(code_list)
    valid_code_count = 0
    valid_code_list = []
    success_code_count = 0
    failure_code_count = 0
    for code in code_list:
        if check(code):
            valid_code_count += 1
            valid_code_list.append(code)

    print('*' * 50)
    print(f'共计 IMEICode {code_count} 个，有效 {valid_code_count} 个')
    is_quit = input('按 Q 退出程序，输入其他任意字母开始跑步')
    if is_quit.upper() == 'Q':
        exit(0)
    print('开始跑步..')
    print('*' * 50, end='')

    for code in valid_code_list:
        if run(code):
            success_code_count += 1
        else:
            failure_code_count += 1
    else:
        print(f'\n失败: {failure_code_count}\n今日已完成: {success_code_count}\n合计: {valid_code_count}')
        input('完成，按任意键退出')
