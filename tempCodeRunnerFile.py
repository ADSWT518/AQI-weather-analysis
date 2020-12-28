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

windList = [[] for i in range(7)]

pm25List = [[] for i in range(7)]
pm25DayList = []


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

                        windList[i - 14].append(wind[0])
                        windList[i - 14].append(wind[1])

                        count += 1
                        # print(windScale)

                        # if w1 not in weather:
                        #     weather.append(w1)
                        # if w2 not in weather:
                        #     weather.append(w2)
                    # print(count)

        # print(tempList)
        # print(len(tempList))

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
        if PM[int(index / 2)] <= 150:
            continue
        if W[index] == 1:
            pm25ForWeather[0].append(PM[int(index / 2)])
        elif W[index] == 2:
            pm25ForWeather[1].append(PM[int(index / 2)])
        elif W[index] == 3:
            pm25ForWeather[2].append(PM[int(index / 2)])
        elif W[index] == 4:
            pm25ForWeather[3].append(PM[int(index / 2)])
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

    pm25ForWind = [[] for i in range(6)]

    PM = [i for item in pm25List for i in item]
    W = [i for item in windList for i in item]

    for index in range(len(W)):
        if W[index] == 1:
            pm25ForWind[0].append(gradeOfIAQI(PM[int(index / 2)]))
        elif W[index] == 2:
            pm25ForWind[1].append(gradeOfIAQI(PM[int(index / 2)]))
        elif W[index] == 3:
            pm25ForWind[2].append(gradeOfIAQI(PM[int(index / 2)]))
        elif W[index] == 4:
            pm25ForWind[3].append(gradeOfIAQI(PM[int(index / 2)]))
        elif W[index] == 5:
            pm25ForWind[4].append(gradeOfIAQI(PM[int(index / 2)]))
        elif W[index] == 6:
            pm25ForWind[5].append(gradeOfIAQI(PM[int(index / 2)]))
        else:
            print("WTF?")

    print(len(pm25ForWind))
    print(len(pm25ForWind[0]))

    plt.title('Scores by group and gender')

    N = 6
    ind = np.arange(N)  #[ 0  1  2  3  4  5  6  7  8  9 10 11 12]
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'))

    plt.ylabel('Scores')
    plt.yticks(np.arange(0, 81, 20))

    # 表示所有1级空气中风速的占比
    g1 = (pm25ForWind[0].count(1), pm25ForWind[0].count(2),
          pm25ForWind[0].count(3), pm25ForWind[0].count(4),
          pm25ForWind[0].count(5), pm25ForWind[0].count(6))
    g2 = (pm25ForWind[1].count(1), pm25ForWind[1].count(2),
          pm25ForWind[1].count(3), pm25ForWind[1].count(4),
          pm25ForWind[1].count(5), pm25ForWind[1].count(6))
    g3 = (pm25ForWind[2].count(1), pm25ForWind[2].count(2),
          pm25ForWind[2].count(3), pm25ForWind[2].count(4),
          pm25ForWind[2].count(5), pm25ForWind[2].count(6))
    g4 = (pm25ForWind[3].count(1), pm25ForWind[3].count(2),
          pm25ForWind[3].count(3), pm25ForWind[3].count(4),
          pm25ForWind[3].count(5), pm25ForWind[3].count(6))
    g5 = (pm25ForWind[4].count(1), pm25ForWind[4].count(2),
          pm25ForWind[4].count(3), pm25ForWind[4].count(4),
          pm25ForWind[4].count(5), pm25ForWind[4].count(6))
    g6 = (pm25ForWind[5].count(1), pm25ForWind[5].count(2),
          pm25ForWind[5].count(3), pm25ForWind[5].count(4),
          pm25ForWind[5].count(5), pm25ForWind[5].count(6))
    print(g1)
    d = []
    for i in range(0, len(g1)):
        sum = g1[i] + g2[i] + g3[i] + g4[i] + g5[i] + g6[i]
        d.append(sum)

    width = 0.35  # 设置条形图一个长条的宽度
    p1 = plt.bar(ind, g1, width)
    p2 = plt.bar(ind, g2, width, bottom=g1)
    p3 = plt.bar(ind, g3, width, bottom=g1 + g2)
    p4 = plt.bar(ind, g4, width, bottom=g1 + g2 + g3)
    p5 = plt.bar(ind, g5, width, bottom=g1 + g2 + g3 + g4)
    p6 = plt.bar(ind, g6, width, bottom=g1 + g2 + g3 + g4 + g5)

    plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]),
               ('g1', 'g2', 'g3', 'g4', 'g5', 'g6'),
               loc=3)

    plt.show()


if __name__ == '__main__':
    getWeather()
    # display1()

    # display2()

    display3()
    # print(len(weatherList))
    # print(len(pm25List))

    #print(weather)