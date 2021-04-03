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
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib3
urllib3.disable_warnings()
#设置邮箱发送
import smtplib
from email.mime.text import MIMEText
mail_host = 'smtp.163.com'
mail_user = 'luckyhui2000'
mail_pass = 'JTPJVBDOKHEXRQEX'
sender = 'luckyhui2000@163.com'


def email(content, address):
    receivers = [address]
    message = MIMEText(content,'plain','utf-8')
    #邮件主题
    message['Subject'] = '今日有效阳光长跑'
    message['From'] = sender
    message['To'] = receivers[0]
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误

def ChoseEmail(name, content):
    if name == "王佳辉":
        email(content,'76946112@qq.com')
    elif name == "王岩":
        email(content,'1078588437@qq.com')
    elif name == "王奕翔":
        email(content,'1397445732@qq.com')
    elif name == "平玮":
        email(content,'3256298546@qq.com')
    elif name == "郑忠宇":
        email(content,'1951506459@qq.com')
    elif name == "禹宇帅":
        email(content,'1822403761@qq.com')
    elif name == "张宇霆":
        email(content,'479997378@qq.com')
    else:
        email("ChoseEmail Error",'76946112@qq.com')
        
    

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
    check_json = requests.get('https://aipao.liaoguoyin.com/check', verify=False,
                              params={'code': code, 'imei': 'Public-Gist'}).json()
    if check_json.get('code') == 200:
        global valid_name
        valid_name.append(check_json.get("data").get("name"))
        print(f'{code} 有效，姓名: {check_json.get("data").get("name")}')
        return True
    else:
        print(f'{code} 无效')
        return False


def run(code) -> bool:
    run_json = requests.get('https://aipao.liaoguoyin.com/run',verify=False, params={'code': code, 'imei': 'Public-Gist'}).json()
    print()
    check_json = requests.get('https://aipao.liaoguoyin.com/check', verify=False,
                              params={'code': code, 'imei': 'Public-Gist'}).json()
    #global s
    if run_json.get('code') == 200:
        ChoseEmail(check_json.get("data").get("name"),"wow!今日阳光长跑成功!")
        print(f'{code} 成功')
        return True
    else:
        if '今天已有有效跑步记录' in run_json.get("message"):
            #ChoseEmail(check_json.get("data").get("name"),"wow!今日已有跑步记录!")
            print(f'{code} {run_json.get("message")}', end='')
            return True
        else:
            ChoseEmail(check_json.get("data").get("name"),"oh!阳光长跑出错!")
            print(f'{code} 失败，{run_json.get("message")}', end='')
            return False


if __name__ == '__main__':
    code_list = load_local_imei_code()
    name_list = ["王佳辉","王岩","王奕翔","平玮","郑忠宇","禹宇帅","张宇霆"]
    print('*' * 50)
    s = ""
    code_count = len(code_list)
    valid_code_count = 0
    valid_code_list = []
    valid_name = []
    success_code_count = 0
    failure_code_count = 0
    for code in code_list:
        if check(code):
            valid_code_count += 1
            valid_code_list.append(code)
            
    for name in name_list:
        if name not in valid_name:
            print(name, "\tIMEICode已经失效")
            ChoseEmail(name, "haha!IMEICode已失效，速速发送!")
            
    print('*' * 50)
    print(f'共计 IMEICode {code_count} 个，有效 {valid_code_count} 个')
    #is_quit = input('按 Q 退出程序，输入其他任意字母开始跑步')
    #if is_quit.upper() == 'Q':
    #    exit(0)
    print('开始跑步..')
    print('*' * 50, end='')

    for code in valid_code_list:
        if run(code):
            success_code_count += 1
        else:
            failure_code_count += 1
    else:
        print(f'\n失败: {failure_code_count}\n今日已完成: {success_code_count}\n合计: {valid_code_count}')
        #input('完成，按任意键退出')
        exit(0)
