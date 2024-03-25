import sys
import os
import json

from autoServer import getJwxtTicketFromAutoServer
from jwxt.services import getJwxtCookieFromTicketUrl, checkJwxtCookies
import spider0

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

username = input("请输入学号: ")
password = input("请输入密码: ")


if __name__ == '__main__':
    with open('cookies.txt', 'r') as f:
        cookies = f.read()

    if cookies:
        print(f"存在cookies 正在验证是否有效")
        cookies = json.loads(cookies)
        if checkJwxtCookies(cookies):
            print("登陆成功")
        else:
            print(f"cookies过期 正在重新获取")

            # https://jwxt.neuq.edu.cn/eams/teach/grade/course/person!search.action?semesterId=83&projectType=
            success, locationUrl = getJwxtTicketFromAutoServer(username, password)  # 输入账户/密码
            if success:
                print("Login successful! Location:", locationUrl)
            else:
                print("Login failed. Error:", locationUrl)  # 这里的 locationUrl 包含错误消息
            success, cookies = getJwxtCookieFromTicketUrl(locationUrl)
            if success:
                with open('cookies.txt', 'w') as f:
                    f.write(json.dumps(cookies))
    else:
        print(f"没有cookies 正在尝试登录")

        success, locationUrl = getJwxtTicketFromAutoServer(username, password)  # 输入账户/密码
        if success:
            print("Login successful! Location:", locationUrl)
        else:
            print("Login failed. Error:", locationUrl)  # 这里的 locationUrl 包含错误消息
        success, cookies = getJwxtCookieFromTicketUrl(locationUrl)
        if success:
            with open('cookies.txt', 'w') as f:
                f.write(json.dumps(cookies))

spider0.scrape_grades()  # 爬取成绩
