import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 设置显示选项
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列


def scrape_grades():
    semester_mapping = {
        "2005-2006学年第一学期": "1",
        "2005-2006学年第二学期": "2",
        "2006-2007学年第一学期": "4",
        "2006-2007学年第二学期": "5",
        "2007-2008学年第一学期": "7",
        "2007-2008学年第二学期": "8",
        "2008-2009学年第一学期": "10",
        "2008-2009学年第二学期": "11",
        "2009-2010学年第一学期": "13",
        "2009-2010学年第二学期": "14",
        "2010-2011学年第一学期": "16",
        "2010-2011学年第二学期": "17",
        "2011-2012学年第一学期": "19",
        "2011-2012学年第二学期": "20",
        "2012-2013学年第一学期": "22",
        "2012-2013学年第二学期": "23",
        "2013-2014学年第一学期": "25",
        "2013-2014学年第二学期": "26",
        "2014-2015学年第一学期": "28",
        "2014-2015学年第二学期": "29",
        "2015-2016学年第一学期": "31",
        "2015-2016学年第二学期": "32",
        "2016-2017学年第一学期": "34",
        "2016-2017学年第二学期": "35",
        "2017-2018学年第一学期": "37",
        "2017-2018学年第二学期": "38",
        "2018-2019学年第一学期": "40",
        "2018-2019学年第二学期": "41",
        "2019-2020学年第一学期": "43",
        "2019-2020学年第二学期": "44",
        "2020-2021学年第一学期": "46",
        "2020-2021学年第二学期": "47",
        "2021-2022学年第一学期": "49",
        "2021-2022学年第二学期": "50",
        "2022-2023学年第一学期": "61",
        "2022-2023学年第二学期": "81",
        "2023-2024学年第一学期": "82",
        "2023-2024学年第二学期": "83",
        "2024-2025学年第一学期": "84",
        "2024-2025学年第二学期": "85",
        "2025-2026学年第一学期": "86",
        "2025-2026学年第二学期": "87",
        "2026-2027学年第一学期": "101",
        "2026-2027学年第二学期": "102",
    }

    # 获取用户输入的 semesterId 对应的值
    semester_text = input("请输入学期名称（如：2023-2024学年第一学期）：")
    semester_id = semester_mapping.get(semester_text)

    # 如果未找到对应的值，则给出提示并退出程序
    if not semester_id:
        print("未找到对应的学期名称，请检查输入。")
        exit()

    semesterId = semester_id
    projectType = None

    with open('cookies.txt', 'r') as f:
        cookies = f.read()

    cookies = json.loads(cookies)

    courseUrl = f'https://jwxt.neuq.edu.cn/eams/teach/grade/course/person!search.action?semesterId={semesterId}&projectType={projectType}'
    # 这里semesterId还需要改
    # myActionUrl = 'https://jwxt.neuq.edu.cn/eams/teach/grade/course/person.action'

    # ↑上面url里面是
    # <div id="semesterGrade"class="ajax_container"></div>
    # <script>bg.ready(function()bg.Go('/eams/teach/grade/course/person!search.action?semesterld=82&projectType='semesterGrade'));</script>

    '''response = requests.get(myActionUrl, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div_tag = soup.find('div')
        if div_tag:
            print("score:", div_tag)
        else:
            print("empty")
    else:
        print("failure:", response.status_code)'''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }

    response = requests.get(courseUrl, cookies=cookies, headers=headers)

    try:
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            div_content = soup.find('div', string=lambda text: '总平均绩点' in text and '校内专用绩点' in text)

            # 提取<table>中的内容并转换为DataFrame
            table = soup.find('table', class_='gridtable')
            table_data = []

            headers = [th.get_text(strip=True) for th in table.select('thead tr th')]

            # 判断<tbody>是否存在
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                    if row_data:
                        table_data.append(row_data)
            if headers:
                df = pd.DataFrame(table_data, columns=headers)
                df.to_csv('myScore.txt', sep='\t', index=False)
                if div_content:
                    print("\n查询到的绩点:", div_content.get_text(strip=True))
                else:
                    print("未找到绩点信息。")
                print("\n查询到的成绩如下:\n")
                print(df)
                print("已将成绩保存至myScore.txt")

        #        if df:
        #            print("\n转换后的表格:", df)
        #        else:
        #            print("not found")
        else:
            print("连接失败:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("请求异常:", e)
