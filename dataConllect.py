#coding=utf-8
import io
import sys
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding='gb18030')  #改变标准输出的默认编码, 防止控制台打印乱码


def get_soup(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  #若请求不成功,抛出HTTPError 异常
        #r.encoding = 'gbk'  #与该网站编码匹配
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except HTTPError:
        return "Request Error"


def get_data():
    soup = get_soup(url)
    all_weather = soup.find('div',
                            class_="wdetail").find('table').find_all("tr")
    data = list()
    for tr in all_weather[1:]:
        td_li = tr.find_all("td")
        for td in td_li:
            s = td.get_text()
            data.append("".join(s.split()))
    res = np.array(data).reshape(-1, 4)
    return res


def saveTocsv(data, fileName):
    '''
    将天气数据保存至csv文件
    '''
    result_weather = pd.DataFrame(data, columns=['date', 'tq', 'temp', 'wind'])
    result_weather.to_csv(fileName, index=False, encoding='utf-8')
    print('Save all weather success!')


if __name__ == '__main__':
    for i in range(14, 21, 1):
        for j in range(1, 13, 1):
            if j < 10:
                url = "http://www.tianqihoubao.com/lishi/changsha/month/20" + str(
                    i) + '0' + str(j) + ".html"
            else:
                url = "http://www.tianqihoubao.com/lishi/changsha/month/20" + str(
                    i) + str(j) + ".html"
            print(url)
            data = get_data()
            if j < 10:
                saveTocsv(data, str(i) + '0' + str(j) + ".csv")
            else:
                saveTocsv(data, str(i) + str(j) + ".csv")
