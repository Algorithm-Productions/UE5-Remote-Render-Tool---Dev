import datetime
import os
import time


def getFrameTimes(path, firstTime):
    files = os.listdir(path)
    returnList = []
    prevDate = firstTime

    for filename in files:
        file = os.path.join(path, filename)
        if os.path.isfile(file):
            currDate = datetime.datetime.fromtimestamp(os.path.getmtime(file))
            delta = currDate - prevDate
            prevDate = currDate
            returnList.append(delta.total_seconds())

    return returnList


def getFrameTimesV2(dates):
    returnList = []

    for idx, date in enumerate(dates):
        if idx == 0:
            continue
        returnList.append((dates[idx] - dates[idx - 1]).total_seconds())

    return returnList


def genTimes(n=100):
    timeList = []
    for i in range(n):
        timeList.append(datetime.datetime.now())
        time.sleep(2)
        print(i)

    print(timeList)
    return timeList


firstDate = datetime.datetime.now()
time.sleep(2)
print(getFrameTimes("D:/Renders/Testing", firstDate))
