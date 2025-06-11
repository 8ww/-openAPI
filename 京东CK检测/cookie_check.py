import requests
import urllib.parse
import json
import time

# 假设你的Cookie信息放在本地 cookies.txt，每行一个Cookie，格式如：pt_key=xxx;pt_pin=yyy;
# 你也可以直接在代码中写明Cookies列表。
def load_cookies():
    cookies_list = []
    try:
        with open("cookies.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "pt_key=" in line and "pt_pin=" in line:
                    cookies_list.append(line)
    except FileNotFoundError:
        print("请准备好 cookies.txt 文件，每行一个完整ck。")
        exit(1)
    return cookies_list

def check_ck(cookie):
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    headers = {
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            try:
                data = r.json()
            except Exception:
                print("响应非标准JSON，判为失效。")
                return False, None
            if data.get('retcode') == "1001":
                # 失效
                return False, None
            elif data.get('retcode') == "0" and data.get('data') and "userInfo" in data.get('data'):
                nickname = data['data']['userInfo']['baseInfo'].get('nickname', '')
                return True, nickname
            else:
                print("未知返回，不作变动：", data)
                return None, None
        else:
            print(f"请求异常: {r.status_code}")
            return None, None
    except Exception as e:
        print("网络错误:", e)
        return None, None

def get_pin(cookie):
    pin_value = ""
    for ck in cookie.split(";"):
        if "pt_pin=" in ck:
            pin_value = ck.strip().split("pt_pin=")[-1]
            break
    return urllib.parse.unquote(pin_value)

if __name__ == "__main__":
    all_cookies = load_cookies()
    if not all_cookies:
        print("没有读到任何ck！")
        exit(1)
    print(f"检测到 {len(all_cookies)} 个ck，开始检测：\n")
    for idx, cookie in enumerate(all_cookies, 1):
        pin = get_pin(cookie)
        print(f"账号{idx} : {pin} 检测中...")
        status, nickname = check_ck(cookie)
        if status is True:
            print(f"✅ 账号{idx} ({pin})  正常，昵称: {nickname}")
        elif status is False:
            print(f"❌ 账号{idx} ({pin})  已过期/失效")
        else:
            print(f"⚠️ 账号{idx} ({pin})  检测异常")
        time.sleep(2)
    print("\n检测完毕！")