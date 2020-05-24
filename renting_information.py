import re
import pandas as pd
import requests

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    pattern = re.compile(' <div.*?class="content__list--item".*?data-house_code="(.*?)".*?title="(.*?)".*?<i>/</i>(.*?)<i>/</i>.*?<em>(.*?)</em>.*?</div>.*?</div>',
        re.S)
    items = re.findall(pattern, html)
    return items

def main():
    data=pd.DataFrame(columns=['编号','小区', '面积', '价格'])
    for i in range(1,10):
        url = 'https://sh.zu.ke.com/ditiezufang/li143685058s100021841/pg' + str(
            i) + 'rco11rt200600000001l0/#contentList'
        html = get_one_page(url)
        item = parse_one_page(html)
        data = data.append(pd.DataFrame.from_records(item, columns=['编号', '小区', '面积', '价格']), ignore_index=True)

    for column in data.columns:
        data[column]=data[column].str.replace(r'[/\s+/g]','').replace('\"','')
    data.to_csv('最新租房信息.csv')
    print(data)

main()