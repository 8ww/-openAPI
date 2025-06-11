"""
蜜雪冰城签到

打开微信小程序抓token填到变量mxbcck里面即可

支持多用户运行

多用户用&或者@隔开
例如账号1：10086 账号2： 1008611
则变量为10086&1008611
export mxbcck=""

cron: 0 7 * * *
const $ = new Env("蜜雪冰城签到");
"""
import requests
import re
import os
import time
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

all_print_list = []  # 用于记录所有 print 输出的字符串

# 用于记录所有 print 输出的字符串，暂时实现 print 函数的 sep 和 end
def myprint(*args, sep=' ', end='\n', **kwargs):
    global all_print_list
    output = ""
    # 构建输出字符串
    for index, arg in enumerate(args):
        if index == len(args) - 1:
            output += str(arg)
            continue
        output += str(arg) + sep
    output = output + end
    all_print_list.append(output)
    # 调用内置的 print 函数打印字符串
    print(*args, sep=sep, end=end, **kwargs)


#分割变量
if 'mxbcck' in os.environ:
    mxbcck = re.split("@|&",os.environ.get("mxbcck"))
    print(f'查找到{len(mxbcck)}个账号')
else:
    mxbcck = ['']
    myprint('无mxbcck变量')



# 发送通知消息
def send_notification_message(title):
    try:
        from notify import send

        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')


base_url = "https://mxsa.mxbc.net"
headers = {
    "app": "mxbc",
    "appchannel": "xiaomi",
    "appversion": "3.0.3",
    "Access-Token": "",
    "Host": "mxsa.mxbc.net",
    "User-Agent": "okhttp/4.4.1"
}

private_key_string = """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCtypUdHZJKlQ9L
L6lIJSphnhqjke7HclgWuWDRWvzov30du235cCm13mqJ3zziqLCwstdQkuXo9sOP
Ih94t6nzBHTuqYA1whrUnQrKfv9X4/h3QVkzwT+xWflE+KubJZoe+daLKkDeZjVW
nUku8ov0E5vwADACfntEhAwiSZUALX9UgNDTPbj5ESeII+VztZ/KOFsRHMTfDb1G
IR/dAc1mL5uYbh0h2Fa/fxRPgf7eJOeWGiygesl3CWj0Ue13qwX9PcG7klJXfToI
576MY+A7027a0aZ49QhKnysMGhTdtFCksYG0lwPz3bIR16NvlxNLKanc2h+ILTFQ
bMW/Y3DRAgMBAAECggEBAJGTfX6rE6zX2bzASsu9HhgxKN1VU6/L70/xrtEPp4SL
SpHKO9/S/Y1zpsigr86pQYBx/nxm4KFZewx9p+El7/06AX0djOD7HCB2/+AJq3iC
5NF4cvEwclrsJCqLJqxKPiSuYPGnzji9YvaPwArMb0Ff36KVdaHRMw58kfFys5Y2
HvDqh4x+sgMUS7kSEQT4YDzCDPlAoEFgF9rlXnh0UVS6pZtvq3cR7pR4A9hvDgX9
wU6zn1dGdy4MEXIpckuZkhwbqDLmfoHHeJc5RIjRP7WIRh2CodjetgPFE+SV7Sdj
ECmvYJbet4YLg+Qil0OKR9s9S1BbObgcbC9WxUcrTgECgYEA/Yj8BDfxcsPK5ebE
9N2teBFUJuDcHEuM1xp4/tFisoFH90JZJMkVbO19rddAMmdYLTGivWTyPVsM1+9s
tq/NwsFJWHRUiMK7dttGiXuZry+xvq/SAZoitgI8tXdDXMw7368vatr0g6m7ucBK
jZWxSHjK9/KVquVr7BoXFm+YxaECgYEAr3sgVNbr5ovx17YriTqe1FLTLMD5gPrz
ugJj7nypDYY59hLlkrA/TtWbfzE+vfrN3oRIz5OMi9iFk3KXFVJMjGg+M5eO9Y8m
14e791/q1jUuuUH4mc6HttNRNh7TdLg/OGKivE+56LEyFPir45zw/dqwQM3jiwIz
yPz/+bzmfTECgYATxrOhwJtc0FjrReznDMOTMgbWYYPJ0TrTLIVzmvGP6vWqG8rI
S8cYEA5VmQyw4c7G97AyBcW/c3K1BT/9oAj0wA7wj2JoqIfm5YPDBZkfSSEcNqqy
5Ur/13zUytC+VE/3SrrwItQf0QWLn6wxDxQdCw8J+CokgnDAoehbH6lTAQKBgQCE
67T/zpR9279i8CBmIDszBVHkcoALzQtU+H6NpWvATM4WsRWoWUx7AJ56Z+joqtPK
G1WztkYdn/L+TyxWADLvn/6Nwd2N79MyKyScKtGNVFeCCJCwoJp4R/UaE5uErBNn
OH+gOJvPwHj5HavGC5kYENC1Jb+YCiEDu3CB0S6d4QKBgQDGYGEFMZYWqO6+LrfQ
ZNDBLCI2G4+UFP+8ZEuBKy5NkDVqXQhHRbqr9S/OkFu+kEjHLuYSpQsclh6XSDks
5x/hQJNQszLPJoxvGECvz5TN2lJhuyCupS50aGKGqTxKYtiPHpWa8jZyjmanMKnE
dOGyw/X4SFyodv8AEloqd81yGg==
-----END PRIVATE KEY-----"""


def get_sha256_with_rsa(content):
    private_key = load_pem_private_key(private_key_string.encode(), password=None, backend=default_backend())
    signature = private_key.sign(
        content.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return urlsafe_b64encode(signature).decode()


def fetch(url, params=None):
    try:
        if url.startswith("/") or url.startswith(":"):
            url = base_url + url
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print(f"⛔️ 请求发起失败: {e}")
        return None


def get_user_info():
    try:
        timestamp = str(int(time.time() * 1000))
        params = {
            "appId": "d82be6bbc1da11eb9dd000163e122ecb",
            "t": timestamp,
            "sign": get_sha256_with_rsa(f'appId=d82be6bbc1da11eb9dd000163e122ecb&t={timestamp}')
        }
        res = fetch("/api/v1/customer/info", params)
        if res and (res.get('code') == 0 or res.get('code') == 5020):
            return {
                'userName': res['data']['mobilePhone'],
                'level': res['data']['customerLevel'],
                'levelName': res['data']['customerLevelVo']['levelName'],
                'point': res['data']['customerPoint']
            }
        else:
            raise ValueError("Failed to get user info")
    except Exception as e:
        myprintprint(f"❌ 获取用户信息失败: {e}")
        return None


def signin():
    try:
        timestamp = str(int(time.time() * 1000))
        params = {
            "appId": "d82be6bbc1da11eb9dd000163e122ecb",
            "t": timestamp,
            "sign": get_sha256_with_rsa(f'appId=d82be6bbc1da11eb9dd000163e122ecb&t={timestamp}')
        }
        res = fetch("/api/v1/customer/signin", params)
        if res and (res.get('code') == 0 or res.get('code') == 5020):
            myprint(f"签到成功: 获得 {res['data'].get('ruleValuePoint', 0)} 币")
        else:
            raise ValueError("签到失败")
    except Exception as e:
        myprint(f"⛔️ 签到失败: {e}")



# 主函数
def main():
    z = 1
    for ck in mxbcck:
        try:
            print(f'登录第{z}个账号')
            print('----------------------')
            headers["Access-Token"] = ck
            user_info = get_user_info()
            if user_info:
                signin()
                myprint(f"用户 {user_info['userName']} 当前余额: {user_info['point']} 雪王币")
            else:
                myprint(f"用户 {user['userName']} 信息获取失败")
            print('----------------------')
            z = z + 1
        except Exception as e:
            myprint('未知错误')



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        myprint('未知错误')
    try:
        send_notification_message(title='蜜雪冰城')  # 发送通知
    except Exception as e:
        myprint('推送失败')