import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib.collections import PathCollection
from datetime import datetime
import numpy


def plot_residential_drives(residential_drives, highway_drives, countryside_drives):

    #print(residential_drives[0][0]["speed"])
    plt.close()

    for drive in residential_drives:
        speed = []
        time = []
        maxspeed = []

        for sample in drive:
            if sample["speed"] == "null":
                pass
            else:
                speed.insert(-1, sample["speed"])
                t = datetime.utcfromtimestamp(float(sample["time"])/1000).strftime("%Y-%m-%d %H:%M:%S.%f")
                #t = sample["time"]
                time.insert(-1, t)
                maxspeed.insert(-1, int(sample["maxspeed"]))

                print(sample["roadtype"])
        print(time)
        time = numpy.array(time)
        dates = date2num(time)

        #for t in time:
            #pandas.Timestamp(t).to_pydatetime()

        #time = [datetime.fromtimestamp(ts) for ts in time]
        #time = matplotlib.dates.date2num(time)
        plt.plot_date(dates, speed)
        #plt.plot(dates, maxspeed)
        #plt.gcf().autofmt_xdate()
        #matplotlib.axes.Axes.autoscale(self, enable=True, axis='both', tight=None)
        plt.legend("Time/Speed")
        plt.show()

def plot_whole_drive(drive):
    speed = []
    time = []
    rpm = []
    consumption = []
    efficiency = []
    latitude = []
    longitude = []
    leftG = []
    rightG = []
    outputPower = []

    maxspeed = []
    roadtype = []

    x = drive["content"]["data"]["mapData"]
    for sample in x:

        if sample["speed"] != "null" and sample["time"] != "null" and sample["rpm"] != "null" and\
                    sample["consumption"] != "null" and sample["efficiency"] != "null" and sample["latitude"] != "null"\
                    and sample["longitude"] != "null" and sample["leftG"] != "null" and sample["rightG"] != "null"\
                    and sample["outputPower"] != "null":
            timesample = sample["time"] / 1000
            speed.append(sample["speed"])
            time.append(timesample)
            #maxspeed.insert(0, sample["maxspeed"])
            #roadtype.insert(-1, sample["roadtype"])
            rpm.append(sample["rpm"])
            consumption.append(sample["consumption"])
            efficiency.append(sample["efficiency"])
            latitude.append(sample["latitude"])
            longitude.append(sample["longitude"])
            leftG.append(sample["leftG"])
            rightG.append(sample["rightG"])
            outputPower.append(sample["outputPower"])

        else:
            pass

    plt.subplot(2,1,1)
    plt.plot(time, speed, '.-')
    #plt.plot(time, maxspeed)
    plt.title("Speed and rounds plots"+str(drive["_id"]))
    plt.ylabel("Speed")
    plt.xlabel("Time")

    plt.subplot(2,1,2)
    plt.plot(time, rpm, '.-')
    plt.legend("Time/Speed")
    plt.ylabel("Round per minute")
    plt.xlabel("Time")

    plt.show()


def plot_speed_against_rounds(drive):
    speed = []
    rpm = []
    x = drive["content"]["data"]["mapData"]
    for sample in x:

        if sample["speed"] != "null" and sample["speed"] != 0 and sample["rpm"] != "null":
            speed.insert(0, sample["speed"])
            rpm.insert(0, sample["rpm"])

        else:
            pass

    plt.plot(speed, rpm, '-.')
    plt.legend("Rpm/Speed")
    plt.ylabel("Rounds")
    plt.xlabel("Speed")

    plt.show()


def universal_visualization(drive, variablenames):
    first = []
    second = []
    x = drive["content"]["data"]["mapData"]
    for sample in x:
        if sample[variablenames[1]] != "null" and sample[variablenames[0]] != "null":
            first.append(sample[str(variablenames[1])])
            second.append(sample[str(variablenames[0])])
        else:
            pass
    plt.plot(first, second, '.-')
    plt.legend(str(variablenames[0])+"/"+str(variablenames[1]))
    plt.ylabel(str(variablenames[0]))
    plt.xlabel(str(variablenames[1])) #always time

    plt.show()


def universal_visualization_colored(drive, variablenames):
    first = []
    second = []
    color = []
    newcolor = []
    x = drive["content"]["data"]["mapData"]
    for sample in x:
        if sample[variablenames[1]] != "null" and sample[variablenames[0]] != "null":
            first.append(sample[str(variablenames[1])])
            second.append(sample[str(variablenames[0])])
            color.append(sample['label'])
        else:
            pass

    for col in color:
        if col == 0:
            newcolor.append("darkviolet")
        if col == 1:
            newcolor.append("yellow")
        if col == 2:
            newcolor.append("red")
        if col == 3:
            newcolor.append("skyblue")
        if col == 4:
            newcolor.append("green")
        if col == 5:
            newcolor.append("orange")

    plt.scatter(first, second, marker='.', c=newcolor)
    plt.legend(str(variablenames[0])+"/"+str(variablenames[1]))
    plt.ylabel(str(variablenames[0]))
    plt.xlabel(str(variablenames[1])) #always time

    plt.show()


def universal_2subplots_visualization(drive1, drive2, variablenames1, variablenames2):
    first1 = []
    second1 = []
    first2 = []
    second2 = []
    x1 = drive1["content"]["data"]["mapData"]
    for sample in x1:
        if sample[variablenames1[1]] != "null" and sample[variablenames1[0]] != "null":
            first1.append(sample[str(variablenames1[1])])
            second1.append(sample[str(variablenames1[0])])
        else:
            pass
    x2 = drive2["content"]["data"]["mapData"]
    for sample in x2:
        if sample[variablenames2[1]] != "null" and sample[variablenames2[0]] != "null":
            first2.append(sample[str(variablenames2[1])])
            second2.append(sample[str(variablenames2[0])])
        else:
            pass

    fr = plt.subplot(2, 1, 1)
    fr.plot(first1, second1, '.-')
    # plt.plot(time, maxspeed)
    #fr.title("Speed and rounds plots" + str(drive1["_id"]))
    fr.set_ylabel(str(variablenames1[0]))
    fr.set_xlabel(str(variablenames1[1]))  # always time

    sec = plt.subplot(2, 1, 2, sharex=fr, sharey=fr)
    sec.plot(first2, second2, '.-')
    sec.legend("Time/Speed")
    sec.set_ylabel(str(variablenames2[0]))
    sec.set_xlabel(str(variablenames2[1]))  # always time

    plt.show()


def universal_2subplots_visualization_colored(drive1, drive2, variablenames1, variablenames2):
    first1 = []
    second1 = []
    first2 = []
    second2 = []
    color = []
    newcolor = []

    x1 = drive1["content"]["data"]["mapData"]
    for sample in x1:
        if sample[variablenames1[1]] != "null" and sample[variablenames1[0]] != "null":
            first1.append(sample[str(variablenames1[1])])
            second1.append(sample[str(variablenames1[0])])
            color.append(sample['label'])
        else:
            pass
    x2 = drive2["content"]["data"]["mapData"]
    for sample in x2:
        if sample[variablenames2[1]] != "null" and sample[variablenames2[0]] != "null":
            first2.append(sample[str(variablenames2[1])])
            second2.append(sample[str(variablenames2[0])])
        else:
            pass
    print(color)

    for col in color:
        if col == 0:
            newcolor.append("darkviolet")
        if col == 1:
            newcolor.append("skyblue")
        if col == 2:
            newcolor.append("yellow")
        if col == 3:
            newcolor.append("red")
        if col == 4:
            newcolor.append("green")
        if col == 5:
            newcolor.append("orange")

    fr = plt.subplot(2, 1, 1)
    fr.scatter(first1, second1, marker='.', c=newcolor)
    # plt.plot(time, maxspeed)
    #fr.title("Speed and rounds plots" + str(drive1["_id"]))
    fr.set_ylabel(str(variablenames1[0]))
    fr.set_xlabel(str(variablenames1[1]))  # always time

    sec = plt.subplot(2, 1, 2)
    sec.scatter(first2, second2, marker='.', c=newcolor)
    sec.legend("Time/Speed")
    sec.set_ylabel(str(variablenames2[0]))
    sec.set_xlabel(str(variablenames2[1]))  # always time

    plt.show()


def visualize_all_2plots(ride1, ride2):
    universal_2subplots_visualization(ride1, ride2, ["consumption", "time"], ["consumption", "time"])
    universal_2subplots_visualization(ride1, ride2, ["rpm", "time"], ["rpm", "time"])
    universal_2subplots_visualization(ride1, ride2, ["speed", "time"], ["speed", "time"])
    universal_2subplots_visualization(ride1, ride2, ["efficiency", "time"], ["efficiency", "time"])
    universal_2subplots_visualization(ride1, ride2, ["fontAcc", "time"], ["fontAcc", "time"])
    universal_2subplots_visualization(ride1, ride2, ["sideG", "time"], ["sideG", "time"])


def visualize_all_1plot(ride):
    universal_visualization(ride, ["consumption", "time"])
    universal_visualization(ride, ["rpm", "time"])
    universal_visualization(ride, ["speed", "time"])
    universal_visualization(ride, ["efficiency", "time"])
    universal_visualization(ride, ["fontAcc", "time"])
    universal_visualization(ride, ["sideG", "time"])


def visualize_two_variables(first, second):
    plt.plot(first, second)
    plt.show()


def show_clusters(X):
    plt.scatter(X[:, 0], X[:, 1], c=X[:, 7], alpha=0.1)
    plt.xlabel("Speed")
    plt.ylabel("Rpm")
    plt.legend()
    plt.show()
    colors = []

    lo = plt.scatter(X, X, marker='x', color=colors[0])
    ll = plt.scatter(X, X, marker='o', color=colors[0])
    l = plt.scatter(X, X, marker='o', color=colors[1])
    a = plt.scatter(X, X, marker='o', color=colors[2])
    h = plt.scatter(X, X, marker='o', color=colors[3])
    hh = plt.scatter(X, X, marker='o', color=colors[4])
    ho = plt.scatter(X, X, marker='x', color=colors[4])

    plt.legend((lo, ll, l, a, h, hh, ho),
               ('Low Outlier', 'LoLo', 'Lo', 'Average', 'Hi', 'HiHi', 'High Outlier'),
               scatterpoints=1,
               loc='lower left',
               ncol=3,
               fontsize=8)

    plt.show()
