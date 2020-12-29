import csv
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib import rc
import re
from numpy import *
import numpy as np
import pandas as pd
import seaborn as sns

sns.set()  # 声明使用 Seaborn 样式

weatherScore = {
    '晴': 1,
    '多云': 1,
    '阴': 2,
    '小雨': 3,
    '小到中雨': 3,
    '中雨': 4,
    '阵雨': 3,
    '雷阵雨': 3,
    '雨': 3,
    '中到大雨': 4,
    '大雨': 4,
    '大到暴雨': 4,
    '暴雨': 4,
    '冻雨': 3,
    '雨夹雪': 3,
    '小雪': 3,
    '小雪-中雪': 3,
    '中雪': 4,
    '中到大雪': 4,
    '大雪': 4
}

weatherList = [[] for i in range(7)]

tempList = [[] for i in range(7)]

windList = [[] for i in range(2531)]

pm25List = [[] for i in range(7)]
pm25DayList = []

""" 
def gradeOfIAQI(iaqi):
    if iaqi <= 50:
        return 1
    elif iaqi <= 100:
        return 2
    elif iaqi <= 150:
        return 3
    elif iaqi <= 200:
        return 4
    elif iaqi <= 300:
        return 5
    else:
        return 6
 """

def date_transder(my_str):
    pattern = re.compile('(\d+)\D(\d+)\D(\d+)')
    dd = pattern.findall(my_str)
    date_strr = dd[0][0] + '/' + str(int(dd[0][1])) + '/' + str(int(dd[0][2]))
    return date_strr


def getWeather():

    # PM2.5
    with open('changsha-air-quality.csv', newline='',
              encoding='utf-8') as csvfile1:
        spamreader1 = csv.reader(csvfile1, delimiter=' ', quotechar='|')
        # pm25_per_year = []
        index = 0
        for row1 in spamreader1:
            if row1[0].split(',')[0] == 'date':
                continue
            elif row1[0].split(',')[0] == 'year':
                index += 1
                continue
            else:
                pm25 = int(row1[0].split(',')[1])
                pm25List[index].append(pm25)
                # print(pm25)
                pm25DayList.append(row1[0].split(',')[0])
            # print(row1[0].split(',')[1])

        # print(len(pm25DayList))
        # print(len(pm25List[0]))
        # print(len(pm25_per_year))
        count = 0

        for i in range(14, 21, 1):
            for j in range(1, 13, 1):
                time = i * 100 + j
                with open(str(time) + '.csv', newline='',
                          encoding='utf-8') as csvfile2:
                    spamreader2 = csv.reader(csvfile2,
                                             delimiter=' ',
                                             quotechar='|')
                    for row2 in spamreader2:
                        if row2[0].split(',')[0] == 'date':
                            continue

                        # 清除空白日期
                        # print(date_transder(row2[0].split(',')[0]) + ' ' + pm25DayList[count])
                        if date_transder(
                                row2[0].split(',')[0]) != pm25DayList[count]:
                            continue

                        # weather
                        w1 = row2[0].split(',')[1].split('/')[0]
                        w2 = row2[0].split(',')[1].split('/')[1]
                        weatherList[i - 14].append(weatherScore[w1])
                        weatherList[i - 14].append(weatherScore[w2])

                        # temperature
                        temp = list(
                            map(
                                int,
                                re.findall(r"-?[0-9]\d*",
                                           row2[0].split(',')[2])))
                        tempDay = mean(temp)
                        tempList[i - 14].append(tempDay)

                        # wind
                        wind = list(
                            map(
                                int,
                                re.findall(r"\d+\.?\d*",
                                           row2[0].split(',')[3])))
                        # print(wind)
                        # print(count)
                        windList[count] = wind[:]


                        count += 1
                        # print(windScale)

                        # if w1 not in weather:
                        #     weather.append(w1)
                        # if w2 not in weather:
                        #     weather.append(w2)
                    # print(count)

        # print(tempList)
        # print(len(tempList))
        # print(windList)
        # print([i for item in windList for i in item])
        # print(pd.value_counts([i for item in windList for i in item]))
        # print(len([i for item in windList for i in item]))


def display1():
    """
    print(len(weatherList))
    print(len(pm25List))
    for index in range(len(weatherList)):
        print(str(len(weatherList[index])) + ' ' + str(len(pm25List[index])))

    """

    rc('mathtext', default='regular')

    # time = np.arange(len([i for item in tempList for i in item]))
    # PM = [i for item in pm25List for i in item]
    # T = [i for item in tempList for i in item]
    # print(len(PM))
    # print(len(T))
    """     """
    fig1 = plt.figure()

    for i in range(2):
        for j in range(4):
            if i == 1 and j == 3:
                break
            time = np.arange(len(tempList[i * 4 + j]))
            PM = pm25List[i * 4 + j]
            T = tempList[i * 4 + j]

            ax1 = fig1.add_subplot(2, 4, i * 4 + j + 1)
            lns1 = ax1.plot(time, PM, '-r', label='PM2.5')
            # lns2 = ax1.plot(time, Rn, '-', label = 'Rn')
            ax2 = ax1.twinx()
            lns2 = ax2.plot(time, T, '-', label='Temperature')

            # added these three lines
            lns = lns1 + lns2
            labs = [l.get_label() for l in lns]
            ax1.legend(lns, labs, loc=0)

            ax1.grid()
            ax1.set_title("PM2.5 and Temperature in 20" + str(14 + i * 4 + j))
            ax1.set_xlabel("Time (day)")
            ax1.set_ylabel(r"PM2.5 (IAQI)")
            ax2.set_ylabel(r"Temperature ($^\circ$C)")
            ax1.set_ylim(0, 400)
            ax2.set_ylim(-10, 50)
    """
    """
    PM = [i for item in pm25List for i in item]
    T = [i for item in tempList for i in item]

    fig2 = plt.figure(0)
    grids = plt.GridSpec(4, 4, wspace=0.5, hspace=0.5)

    # 主图
    mean_plot = fig2.add_subplot(grids[0:3, 1:])
    plt.hist2d(PM, T, bins=50, cmap='viridis')
    plt.colorbar()

    # x轴上的图
    xhist = fig2.add_subplot(grids[-1, 1:])
    plt.hist(PM, bins=30, orientation='vertical')
    xhist.invert_yaxis()

    # y轴上的图
    yhist = fig2.add_subplot(grids[:-1, 0])
    plt.hist(T, bins=30, orientation='horizontal')
    yhist.invert_xaxis()

    mean_plot.set_xlabel(r"PM2.5 (IAQI)")
    mean_plot.set_ylabel(r"Temperature ($^\circ$C)")

    pccs = np.corrcoef(PM, T)
    print(pccs)

    plt.show()
    # plt.savefig('0.png')
    """ """


def display2():
    fig1 = plt.figure()

    pm25ForWeather = [[] for i in range(4)]

    PM = [i for item in pm25List for i in item]
    W = [i for item in weatherList for i in item]

    for index in range(len(W)):
        if PM[int(index / 4)] <= 150:
            continue
        if W[index] == 1:
            pm25ForWeather[0].append(PM[int(index / 4)])
        elif W[index] == 2:
            pm25ForWeather[1].append(PM[int(index / 4)])
        elif W[index] == 3:
            pm25ForWeather[2].append(PM[int(index / 4)])
        elif W[index] == 4:
            pm25ForWeather[3].append(PM[int(index / 4)])
        else:
            print("WTF?")
    print(len(pm25ForWeather))
    print(len(pm25ForWeather[0]))

    for i in range(2):
        for j in range(2):
            time = np.arange(len(tempList[i * 2 + j]))

            pm25PerWeather = pm25ForWeather[i * 2 + j]
            print('\n')
            ax = fig1.add_subplot(2, 2, i * 2 + j + 1)
            # the histogram of the data
            ax.hist(pm25PerWeather,
                    bins=40,
                    facecolor="blue",
                    edgecolor="black",
                    alpha=0.7)
            print(np.mean(pm25PerWeather))
            print(np.var(pm25PerWeather))
            print(len(pm25PerWeather))
            ax.axvline(np.mean(pm25PerWeather),
                       color='r',
                       linestyle='dashed',
                       linewidth=1)

            ax.set_title("PM2.5(>150) when the weather is grade " +
                         str(i * 2 + j + 1))
            ax.set_xlabel(r"PM2.5 (IAQI)")
            ax.set_xlim(140, 400)

    plt.show()


def display3():
    print(pd.value_counts([i for item in windList for i in item]))
    fig1 = plt.figure()

    pm25ForWind = [[] for i in range(6)]

    PM = [i for item in pm25List for i in item]
    # W = [i for item in windList for i in item]

    for index in range(len(windList)):
        if PM[index] <= 150:
            continue
        for j in windList[index]:



            if j == 1:
                pm25ForWind[0].append(PM[index])
            elif j == 2:
                pm25ForWind[1].append(PM[index])
            elif j == 3:
                pm25ForWind[2].append(PM[index])
            elif j == 4:
                pm25ForWind[3].append(PM[index])
            elif j == 5:
                pm25ForWind[4].append(PM[index])
            elif j == 6:
                pm25ForWind[5].append(PM[index])
            else:
                print("WTF?")

    print(len(pm25ForWind))
    print(len(pm25ForWind[0]))

    for i in range(2):
        for j in range(3):
            time = np.arange(len(tempList[i * 3 + j]))

            pm25PerWind = pm25ForWind[i * 3 + j]
            print('\n')
            ax = fig1.add_subplot(2, 3, i * 3 + j + 1)
            # the histogram of the data
            ax.hist(pm25PerWind,
                    bins=30,
                    facecolor="red",
                    edgecolor="black",
                    alpha=0.7)
            print(np.mean(pm25PerWind))
            print(np.var(pm25PerWind))
            print(len(pm25PerWind))
            ax.axvline(np.mean(pm25PerWind),
                       color='b',
                       linestyle='dashed',
                       linewidth=1)

            ax.set_title("PM2.5(>150) when the wind is grade " +
                         str(i * 3 + j + 1))
            ax.set_xlabel(r"PM2.5 (IAQI)")
            ax.set_xlim(140, 400)

    plt.show()



if __name__ == '__main__':
    getWeather()
    # display1()

    # display2()

    display3()
    # print(len(weatherList))
    # print(len(pm25List))

    #print(weather)