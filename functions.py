import os
import json
from math import sin, cos, radians, atan2, sqrt, ceil
from statistics import mean, variance, stdev
import matplotlib.pyplot as plt
import matplotlib
import numpy
import pandas
from scipy import stats, interpolate
from datetime import datetime
import time

os.chdir("C:\\Users\\Krystof\\Desktop\\Diplomka\\Testovací jízda")
input = open('cz.eman.android.oneapp.lib.addon.drives.json','r')
file = json.load(input)


def single_dict_to_gpx(file):
    f = open("jizda" + file["_id"] + ".gpx", "w", newline="")
    f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?><gpx version="1.1" creator="Krystof Brzak"><trk>'
            '<name>jizda' + str(file["_id"]) + '</name>')
    data = file["content"]["data"]["mapData"]
    f.write('<trkseg>')
    for item in data:
        f.write('<trkpt lat="' + str(item["latitude"]) + '" lon="' + str(item["longitude"]) + '"></trkpt>')
    f.write('</trkseg></trk></gpx>')

    
def dict_to_gpx(file):
    for ride in file:
        f = open("jizda"+str(ride["id"])+".gpx", "w", newline="")
        f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?><gpx version="1.1" creator="Krystof Brzak"><trk>'
                '<name>jizda'+str(ride["id"])+'</name>')
        data = ride["content"]["data"]["mapData"]
        f.write('<trkseg>')
        for item in data:
            f.write('<trkpt lat="'+str(item["latitude"])+'" lon="'+str(item["longitude"])+'"></trkpt>')
        f.write('</trkseg></trk></gpx>')


def dict_to_gpx_whole(file):
    f = open("jizdy.json", "w", newline="")
    f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?><gpx version="1.1" creator="Krystof Brzak">')

    for ride in file:
        f.write("<trk><name>"+str(ride["id"])+"</name></trkseg>")
        for item in ride["content"]["data"]["mapData"]:
            f.write('<trkpt lat="'+str(item["latitude"])+'" lon="'+str(item["longitude"])+'"></trkpt>')
        f.write("</trkseg></trk>")
    f.write("</gpx>")

'''
    input.seek(0)
    input.truncate()
    input.write(json.dumps(file, indent=4, sort_keys=True, ensure_ascii=False))
    input.close()
'''


def prep_for_harvesine(oneappfile, openstreetmapfile):
    #oneappjson = json.load(oneappfile)
    oneappjson = oneappfile
    openstreetjson = json.load(openstreetmapfile)

    oneappfield = []
    openstreetmapfield = []

    for unit in oneappjson["content"]["data"]["mapData"]:
        oneappfield.append(dict(latitude=unit["latitude"], longitude=unit["longitude"]))

    for feature in openstreetjson["features"]:
        if "highway" not in feature["properties"]:
            pass
        else:
            d = ["primary", "secondary", "tertiary", "residential", "motorway", "trunk", "unclassified", "motorway_link"
                 , "trunk_link", "service"]
            if any(x in feature["properties"]["highway"] for x in d):
                if type(feature["geometry"]["coordinates"][0]) == list:
                    for latlong in feature["geometry"]["coordinates"]:
                        # longit = latlong[0]
                        # lati = latlong[1]

                        if "maxspeed" in feature["properties"]:
                            openstreetmapfield.append(
                                dict(latitude=latlong[1], longitude=latlong[0], roadtype=feature["properties"]["highway"],
                                     maxspeed=feature["properties"]["maxspeed"]))
                        elif "maxspeed" not in feature["properties"]:
                            openstreetmapfield.append(
                                dict(latitude=latlong[1], longitude=latlong[0], roadtype=feature["properties"]["highway"],
                                     maxspeed="unknown"))
                elif type(feature["geometry"]["coordinates"][0]) == float:
                    if "maxspeed" in feature["properties"]:
                        openstreetmapfield.append(
                            dict(latitude=feature["geometry"]["coordinates"][1], longitude=feature["geometry"]["coordinates"][0], roadtype=feature["properties"]["highway"],
                                 maxspeed=feature["properties"]["maxspeed"]))
                    elif "maxspeed" not in feature["properties"]:
                        openstreetmapfield.append(
                            dict(latitude=feature["geometry"]["coordinates"][1], longitude=feature["geometry"]["coordinates"][0], roadtype=feature["properties"]["highway"],
                                 maxspeed="unknown"))
            else:
                pass
    print(openstreetmapfield)
    return [oneappfield, openstreetmapfield]


def harvesine(oneappfield, openstreetmapfield):
    pocet_odchylek = 0
    for index, a in enumerate(oneappfield):
        closest_point = 40000.0
        roadtype = "none"
        for idx, one in enumerate(openstreetmapfield):
            '''haversin vzorec'''
            lon1 = one["longitude"]
            lon2 = oneappfield[index]["longitude"]
            lat1 = one["latitude"]
            lat2 = oneappfield[index]["latitude"]

            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            delta_lat = abs(lat2 - lat1)
            delta_lon = abs(lon2 - lon1)

            a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            r = 6372.8
            distance = r * c

            if distance < closest_point:
                closest_point = distance
                roadtype = openstreetmapfield[idx]["roadtype"]
                if "maxspeed" in openstreetmapfield[idx]:
                    maxspeed = openstreetmapfield[idx]["maxspeed"]
                else:
                    maxspeed = "unknown"
            else:
                pass

        if closest_point > 0.2:
            pocet_odchylek += 1
        else:
            pass
        d = {"roadtype": roadtype}
        e = {"deviation": closest_point}
        f = {"maxspeed": maxspeed}

        oneappfield[index].update(d)
        oneappfield[index].update(e)
        oneappfield[index].update(f)

    print(oneappfield)

    return oneappfield


def replace_with_speed(oneappfield):
    for n in oneappfield:
        if n["maxspeed"] == "unknown":
            if n["roadtype"] == "residential" or n["roadtype"] == "service":
                n["maxspeed"] = 50
            elif n["roadtype"] == "primary" or n["roadtype"] == "secondary" or n["roadtype"] == "tertiary" \
                    or n["roadtype"] == "unclassified" or n["roadtype"] == "motorway_link":

                n["maxspeed"] = 90
            elif n["roadtype"] == "motorway":
                n["maxspeed"] = 130
        else:
            n["maxspeed"] = int(n["maxspeed"])
    '''
    for idx, sample in enumerate(oneappfield):

        if (idx >= 1) and (idx < len(oneappfield) - 1):

            if (oneappfield[idx - 1]["roadtype"] == oneappfield[idx + 1]["roadtype"]) and (oneappfield[idx - 1] != sample["roadtype"]):
                sample["roadtype"] = oneappfield[idx - 1]["roadtype"]
                sample["maxspeed"] = oneappfield[idx - 1]["maxspeed"]
                n["roadtype"] = oneappfield[idx - 1]["roadtype"]
                n["maxspeed"] = oneappfield[idx - 1]["maxspeed"]
            else:
                pass
        else:
            pass
    '''

    print(oneappfield)
    return oneappfield


def generate_overpass_request(oneappjson):
    f = open("overpass_request.txt", mode="w")
    f.write("( way (around: 10,")
    for idx, n in enumerate(oneappjson["content"]["data"]["mapData"]):
        if idx < len(oneappjson["content"]["data"]["mapData"])-1:
            f.write(str(n["latitude"])+","+str(n["longitude"])+",")
        elif idx == len(oneappjson["content"]["data"]["mapData"])-1:
            f.write(str(n["latitude"])+","+str(n["longitude"]))
    f.write(") [highway];>;);out;")
    print("file created")


def divide_by_roadtype(x):
    residential_drives = []
    highway_drives = []
    countryside_drives = []
    x = x["content"]["data"]["mapData"]

    for idx, sample in enumerate(x):
        if sample["roadtype"] == "residential" or sample["roadtype"] == "service":
            if idx == 0:
                residential_drives.append([sample])

            if x[idx - 1]["roadtype"] == "residential" or x[idx - 1]["roadtype"] == "service":
                residential_drives[0].insert(0, sample)

            else:
                residential_drives.append([sample])

        elif sample["roadtype"] == "motorway":
            if x[idx - 1]["roadtype"] == "motorway":
                highway_drives[1].insert(-1, sample)
            else:
                highway_drives.append([sample])

        elif sample["roadtype"] != "motorway" and sample["roadtype"] != "service" and sample["roadtype"] != "residential":
            if x[idx - 1]["roadtype"] == "highway":
                countryside_drives[0].insert(0, sample)
            else:
                countryside_drives.append([sample])

    print(residential_drives, len(residential_drives))
    return residential_drives, highway_drives, countryside_drives



def perform_least_squares(drive):

    time_array = []
    rpm_array = []

    x = drive["content"]["data"]["mapData"]
    for sample in x:

        if sample["speed"] != "null" and sample["speed"] != 0 and sample["rpm"] != "null":
            timesample = sample["time"] / 1000
            #speed.insert(0, sample["speed"])
            time_array.insert(0, timesample)
            #maxspeed.insert(0, sample["maxspeed"])
            #roadtype.insert(-1, sample["roadtype"])
            rpm_array.insert(-1, sample["rpm"])

        else:
            pass

    time_array = numpy.array(time_array)
    rpm_array = numpy.array(rpm_array)

    slope, intercept, r_value, p_value, std_err = stats.linregress(time_array, rpm_array)

    def func(x, A, c, d):
        return A*numpy.exp(c*x) + d

    plt.plot(time_array, rpm_array)

    x_lin = numpy.linspace(time_array.min(), time_array.max(), 50)

    A, c, d = -1, -1e-2, 1
    y_trial1 = func(x_lin, A, c, d)
    y_trial2 = func(x_lin, 50, -1e-3, 6)
    y_trial3 = func(x_lin, 300, -3e-3, 80)

    #plt.plot(x_lin, y_trial1, label="Trial1")
    #plt.plot(x_lin, y_trial2, label="Trial2")
    #plt.plot(x_lin, y_trial3, label="Trial3")
    plt.plot(time_array, intercept + slope*time_array, label="Regression")
    plt.legend()
    plt.show()


def basic_stats_onedrive(drive):
    '''SAMPLING'''
    differences = []
    rpms = []
    odchylky_fce = 0
    valid = 0
    averagecons = []
    efektivita = []

    length = len(drive["content"]["data"]["mapData"])

    for idx, samp in enumerate(drive["content"]["data"]["mapData"]):
        if (length - idx) != 1:
            # print(samp["time"])
            diff = abs(samp["time"] - drive["content"]["data"]["mapData"][idx + 1]["time"])
            differences.append(diff)
            if samp["speed"] != "null" and samp["rpm"] != "null" and samp["time"] != "null" and \
                    samp["latitude"] != "null" and samp["longitude"] != "null":
                valid += 1
            else:
                continue

        elif (length - idx) == 1:
            if samp["speed"] != "null" and samp["rpm"] != "null" and samp["time"] != "null" and \
                    samp["latitude"] != "null" and samp["longitude"] != "null":
                valid += 1
            else:
                continue

        if "rpm" in samp:
            rpms.append(samp["rpm"])
        if "consumption" in samp:
            averagecons.append(samp["consumption"])
        if "efficiency" in samp:
            efektivita.append(samp["efficiency"])

    for differ in differences:
        if abs(differ-mean(differences)) >= 30:
            odchylky_fce += 1
        else:
            continue

    drivetime = int(abs(drive["content"]["data"]["mapData"][0]["time"] - drive["content"]["data"]["mapData"][-1]["time"]))
    average = mean(differences)
    vari = variance(differences, average)
    validni = valid / length

    rpms_average = mean(rpms)


    print("\nID:"+str(drive["_id"]))
    print("Pocet vzorku:" + str(length)+"    Prumerna frekvence:" +str(average)+ "   Variance:"+str(vari))
    print("Prumerna spotreba:" + str(mean(averagecons)) + "  Prumerne otacky:" + str(drive["content"]["data"]["avgEngineSpeed"]) + "     Rozptyl otacek:" + str(variance(rpms, rpms_average)) + "      Sm. odchylka otacek:" + str(stdev(rpms)))
    print("Efektivita: "+str(mean(efektivita)) + "% validnich vzorku:" + str(validni) + "  Doba jizdy:" + str(drivetime//60)+":"+str(drivetime%60) + "     Pocet odchylek nad 30 vterin:"+str(odchylky_fce))


def advanced_stats(drive):
    rpms = []
    for sample in drive["content"]["data"]["mapData"]:
        rpms.append(sample["rpm"])

    average = mean(rpms)
    dispersion = variance(rpms, average)
    print(dispersion)

def count_frequency_gaps(drive):
    '''CALCULATE FREQUENCY FIRST'''
    differences = []
    above_fifteen = 0
    pozice = 0
    druhapozice = 0
    tretipozice = 0
    ctvrtapozice = 0
    patapozice = 0


    if "mapData" not in drive["content"]["data"]:
        return drive, False
    else:
        length = len(drive["content"]["data"]["mapData"])

        for idx, samp in enumerate(drive["content"]["data"]["mapData"]):
            if (length - idx) != 1:
                # print(samp["time"])
                diff = abs(samp["time"] - drive["content"]["data"]["mapData"][idx + 1]["time"])
                differences.append(diff)
                if diff >= 15:
                    if above_fifteen == 0:
                        pozice = idx
                    elif above_fifteen == 1:
                        druhapozice = idx
                    elif above_fifteen == 2:
                        tretipozice = idx
                    elif above_fifteen == 3:
                        ctvrtapozice = idx
                    elif above_fifteen == 4:
                        patapozice = idx
                    above_fifteen += 1
            elif (length - idx) == 1:
                break

        if above_fifteen == 1:
            #print(pozice)
            before_gap = pozice + 1
            after_gap = length - (pozice + 1)
            return above_fifteen, before_gap, after_gap, 0, 0, 0, 0

        elif above_fifteen == 2:
            first_part = pozice + 1
            second_part = length - (pozice + 1) - (length - (druhapozice + 1))
            third_part = length - (druhapozice + 1)
            return above_fifteen, first_part, second_part, third_part, 0, 0, 0

        elif above_fifteen == 3:
            first_part = pozice + 1
            second_part = length - (pozice + 1) - (length - (druhapozice + 1))
            third_part = length - (druhapozice + 1) - (length - (tretipozice + 1))
            fourth_part = length - (tretipozice + 1)
            return above_fifteen, first_part, second_part, third_part, fourth_part, 0, 0

        elif above_fifteen == 4:
            first_part = pozice + 1
            second_part = length - (pozice + 1) - (length - (druhapozice + 1))
            third_part = length - (druhapozice + 1) - (length - (tretipozice + 1))
            fourth_part = length - (tretipozice + 1) - (length - (ctvrtapozice + 1))
            fifth_part = length - (ctvrtapozice + 1)
            return above_fifteen, first_part, second_part, third_part, fourth_part, fifth_part, 0

        elif above_fifteen == 5:
            first_part = pozice + 1
            second_part = length - (pozice + 1) - (length - (druhapozice + 1))
            third_part = length - (druhapozice + 1) - (length - (tretipozice + 1))
            fourth_part = length - (tretipozice + 1) - (length - (ctvrtapozice + 1))
            fifth_part = length - (ctvrtapozice + 1) - (length - (patapozice + 1))
            sixth_part = length - (patapozice + 1)
            return above_fifteen, first_part, second_part, third_part, fourth_part, fifth_part, sixth_part


            '''
            if before_gap >= 0.9:
                for idex, smpl in enumerate(drive["content"]["data"]["mapData"]):
                    if idex > pozice:
                        drive["content"]["data"]["mapData"].remove(smpl)
                #print(str(before_gap) + "% GAP " + str(after_gap) + "%")

            elif after_gap >= 0.9:
                for idex, smpl in enumerate(drive["content"]["data"]["mapData"]):
                    if idex <= pozice:
                        drive["content"]["data"]["mapData"].remove(smpl)
                #print(str(before_gap) + "% GAP " + str(after_gap) + "%")
            
            return drive, True
            '''
        else:
            return above_fifteen, 0, 0, 0, 0, 0, 0
            #print(differences)


def delete_frequency_gaps(drive):

    def create_subdrive(subdrivecount, samples):
        adder = 1000000000000*subdrivecount
        id = int(drive["_id"])+adder
        if "endLocation" in drive["content"]["data"]:
            endloc = drive["content"]["data"]["endLocation"]
        else:
            endloc = "None"

        if "startLocation" in drive["content"]["data"]:
            startloc = drive["content"]["data"]["startLocation"]
        else:
            startloc = "None"

        if "platform" in drive["content"]:
            platform = drive["content"]["platform"]
        else:
            platform = "Unknown"
        subdrive = \
        {
            "_id": str(id),
            "content": {
                "data": {
                    "avgConsumptionPrimary": 0,
                    "avgConsumptionSecondary": 0,
                    "avgEcoHmi": 0,
                    "avgEngineSpeed": 0,
                    "avgLeftG": 0,
                    "avgOutputPower": 0,
                    "avgRightG": 0,
                    "avgVehicleSpeed": 0,
                    "comment": "subdrive",
                    "driveCostPrimary": 0,
                    "driveCostSecondary": 0,
                    "driveTime": 0,
                    "endLocation": endloc,
                    "endTime": 0,
                    "isMib": "true",
                    "isVisible": drive["content"]["data"]["isVisible"],
                    "mapData": list(samples),
                    "startLocation": startloc,
                    "temperature": drive["content"]["data"]["temperature"],
                    "totalDistance": 0,
                    "totalDistanceLast": drive["content"]["data"]["totalDistanceLast"],
                    "totalDistanceStart": drive["content"]["data"]["totalDistanceStart"],
                    "type": drive["content"]["data"]["type"],
                    "vin": drive["content"]["data"]["vin"],
                },
                "platform": platform
            },
            "updated": drive["updated"],
            "userId": drive["userId"]
        }
        return subdrive

    '''CALCULATE FREQUENCY FIRST'''
    differences = []
    above_fifteen = 0
    pozice = 0
    druhapozice = 0
    tretipozice = 0
    ctvrtapozice = 0
    patapozice = 0

    length = len(drive["content"]["data"]["mapData"])

    for idx, samp in enumerate(drive["content"]["data"]["mapData"]):
        if (length - idx) != 1:
            # print(samp["time"])
            diff = abs(samp["time"] - drive["content"]["data"]["mapData"][idx + 1]["time"])
            differences.append(diff)
            if diff >= 15:
                if above_fifteen == 0:
                    pozice = idx
                elif above_fifteen == 1:
                    druhapozice = idx
                elif above_fifteen == 2:
                    tretipozice = idx
                elif above_fifteen == 3:
                    ctvrtapozice = idx
                elif above_fifteen == 4:
                    patapozice = idx
                above_fifteen += 1
        elif (length - idx) == 1:
            break

    if above_fifteen == 0:
        return above_fifteen, "0", "0", "0", "0", "0", "0"

    if above_fifteen == 1:
        before_gap = pozice + 1
        after_gap = length - (pozice + 1)
        if before_gap >= 100:
            firstsub = create_subdrive(1, drive["content"]["data"]["mapData"][0:pozice+1])
        elif before_gap < 100:
            firstsub = "0"

        if after_gap >= 100:
            secondsub = create_subdrive(2, drive["content"]["data"]["mapData"][pozice+1:length])
        elif after_gap < 100:
            secondsub = "0"

        return above_fifteen, firstsub, secondsub, "0", "0", "0", "0"

    elif above_fifteen == 2:
        first_part = pozice + 1
        second_part = length - (pozice + 1) - (length - (druhapozice + 1))
        third_part = length - (druhapozice + 1)
        if first_part >= 100:
            firstsub = create_subdrive(1, drive["content"]["data"]["mapData"][0:pozice+1])
        elif first_part < 100:
            firstsub = "0"
        if second_part >= 100:
            secondsub = create_subdrive(2, drive["content"]["data"]["mapData"][pozice+1:druhapozice+1])
        elif second_part < 100:
            secondsub = "0"
        if third_part >= 100:
            thirdsub = create_subdrive(3, drive["content"]["data"]["mapData"][druhapozice+1:length])
        elif third_part < 100:
            thirdsub = "0"

        return above_fifteen, firstsub, secondsub, thirdsub, "0", "0", "0"

    elif above_fifteen == 3:
        first_part = pozice + 1
        second_part = length - (pozice + 1) - (length - (druhapozice + 1))
        third_part = length - (druhapozice + 1) - (length - (tretipozice + 1))
        fourth_part = length - (tretipozice + 1)
        if first_part >= 100:
            firstsub = create_subdrive(1, drive["content"]["data"]["mapData"][0:pozice+1])
        else:
            firstsub = "0"
        if second_part >= 100:
            secondsub = create_subdrive(2, drive["content"]["data"]["mapData"][pozice+1:druhapozice+1])
        else:
            secondsub = "0"
        if third_part >= 100:
            thirdsub = create_subdrive(3, drive["content"]["data"]["mapData"][druhapozice+1:tretipozice+1])
        else:
            thirdsub = "0"
        if fourth_part >= 100:
            fourthsub = create_subdrive(4, drive["content"]["data"]["mapData"][tretipozice+1:length])
        else:
            fourthsub = "0"

        return above_fifteen, firstsub, secondsub, thirdsub, fourthsub, "0", "0"

    elif above_fifteen == 4:
        first_part = pozice + 1
        second_part = length - (pozice + 1) - (length - (druhapozice + 1))
        third_part = length - (druhapozice + 1) - (length - (tretipozice + 1))
        fourth_part = length - (tretipozice + 1) - (length - (ctvrtapozice + 1))
        fifth_part = length - (ctvrtapozice + 1)

        if first_part >= 100:
            firstsub = create_subdrive(1, drive["content"]["data"]["mapData"][0:pozice+1])
        else:
            firstsub = "0"
        if second_part >= 100:
            secondsub = create_subdrive(2, drive["content"]["data"]["mapData"][pozice+1:druhapozice+1])
        else:
            secondsub = "0"
        if third_part >= 100:
            thirdsub = create_subdrive(3, drive["content"]["data"]["mapData"][druhapozice+1:tretipozice+1])
        else:
            thirdsub = "0"
        if fourth_part >= 100:
            fourthsub = create_subdrive(4, drive["content"]["data"]["mapData"][tretipozice+1:ctvrtapozice+1])
        else:
            fourthsub = "0"
        if fifth_part >= 100:
            fifthsub = create_subdrive(5, drive["content"]["data"]["mapData"][ctvrtapozice+1:length])
        else:
            fifthsub = "0"

        return above_fifteen, firstsub, secondsub, thirdsub, fourthsub, fifthsub, "0"

    elif above_fifteen == 5:
        first_part = pozice + 1
        second_part = length - (pozice + 1) - (length - (druhapozice + 1))
        third_part = length - (druhapozice + 1) - (length - (tretipozice + 1))
        fourth_part = length - (tretipozice + 1) - (length - (ctvrtapozice + 1))
        fifth_part = length - (ctvrtapozice + 1) - (length - (patapozice + 1))
        sixth_part = length - (patapozice + 1)

        if first_part >= 100:
            firstsub = create_subdrive(1, drive["content"]["data"]["mapData"][0:pozice + 1])
        else:
            firstsub = "0"
        if second_part >= 100:
            secondsub = create_subdrive(2, drive["content"]["data"]["mapData"][pozice+1:druhapozice + 1])
        else:
            secondsub = "0"
        if third_part >= 100:
            thirdsub = create_subdrive(3, drive["content"]["data"]["mapData"][druhapozice+1:tretipozice + 1])
        else:
            thirdsub = "0"
        if fourth_part >= 100:
            fourthsub = create_subdrive(4, drive["content"]["data"]["mapData"][tretipozice+1:ctvrtapozice + 1])
        else:
            fourthsub = "0"
        if fifth_part >= 100:
            fifthsub = create_subdrive(5, drive["content"]["data"]["mapData"][ctvrtapozice+1:patapozice + 1])
        else:
            fifthsub = "0"
        if sixth_part >= 100:
            sixthsub = create_subdrive(6, drive["content"]["data"]["mapData"][patapozice+1:length])
        else:
            sixthsub = "0"

        return above_fifteen, firstsub, secondsub, thirdsub, fourthsub, fifthsub, sixthsub

    elif above_fifteen > 5:
        return above_fifteen, "0", "0", "0", "0", "0", "0"

    '''Function for cubic interpolation and resampling of drives'''


def resampling(doc):
    times = []
    speeds = []
    rounds = []
    consumption = []
    efficiency = []
    latitude = []
    longitude = []
    sideG = []
    outputPower = []
    frontAcc = []

    #FIRST VERSION
    missing_position = 0
    without_position = False
    only_few_missing = False

    for idx, item in enumerate(doc["content"]["data"]["mapData"]):
        if item["latitude"] == "null" and item["longitude"] == "null":
            missing_position += 1
        if idx > 0:
            if item["time"] > doc["content"]["data"]["mapData"][idx-1]["time"]:
                del doc["content"]["data"]["mapData"][idx]
    prc = missing_position / len(doc["content"]["data"]["mapData"])
    if prc >= 0.9:
        without_position = True
    elif 0.0 < prc < 0.9:
        only_few_missing = True
    else:
        pass

    #SECOND VERSION

    for sample in doc["content"]["data"]["mapData"]:
        if only_few_missing is True:
            if sample["speed"] != "null" and sample["time"] != "null" and sample["rpm"] != "null" and sample["consumption"]\
                    != "null" and sample["efficiency"] != "null" and sample["sideG"] != "null" and sample["outputPower"] != "null" and sample["latitude"] != "null" and sample["longitude"] != "null" and sample["fontAcc"] != "null":
                speeds.append(sample["speed"])
                times.append(sample["time"])
                rounds.append(sample["rpm"])
                consumption.append(sample["consumption"])
                efficiency.append(sample["efficiency"])
                sideG.append(sample["sideG"])
                outputPower.append(sample["outputPower"])
                latitude.append(sample["latitude"])
                longitude.append(sample["longitude"])
                frontAcc.append(sample["fontAcc"])

        elif only_few_missing is False:
            if sample["speed"] != "null" and sample["time"] != "null" and sample["rpm"] != "null" and sample["consumption"]\
                    != "null" and sample["efficiency"] != "null" and sample["sideG"] != "null" and sample["outputPower"] != "null" and sample["fontAcc"] != "null":
                frontAcc.append(sample["fontAcc"])
                speeds.append(sample["speed"])
                times.append(sample["time"])
                rounds.append(sample["rpm"])
                consumption.append(sample["consumption"])
                efficiency.append(sample["efficiency"])
                sideG.append(sample["sideG"])
                outputPower.append(sample["outputPower"])
            if without_position is True:
                pass
            elif without_position is False:
                if sample["latitude"] != "null":
                    latitude.append(sample["latitude"])
                if sample["longitude"] != "null":
                    longitude.append(sample["longitude"])

    def interpolation(x, x_axis, y_axis):
        tck = interpolate.splrep(x_axis, y_axis, k=3, s=0.0)
        result = interpolate.splev(x, tck)
        return list(result)

    counter = 0
    new_time = []
    new_speed = []
    new_rounds = []
    new_consumption = []
    new_efficiency = []
    new_latitude = []
    new_longitude = []
    new_sideG = []
    new_outputPower = []
    new_frontAcc = []

    while counter < len(times):
        time_points = []
        speed_points = []
        round_points = []
        consumption_points = []
        efficiency_points = []
        latitude_points = []
        longitude_points = []
        sideG_points = []
        power_points = []
        frontAcc_points = []

        target_timestamps = []

        time_points.append(times[counter])
        speed_points.append(speeds[counter])
        round_points.append(rounds[counter])
        consumption_points.append(consumption[counter])
        efficiency_points.append(efficiency[counter])
        if without_position is False:
            latitude_points.append(latitude[counter])
            longitude_points.append(longitude[counter])
        elif without_position is True:
            pass
        sideG_points.append(sideG[counter])
        power_points.append(outputPower[counter])
        frontAcc_points.append(frontAcc[counter])

        if len(times) > counter + 1:
            time_points.append(times[counter + 1])
            speed_points.append(speeds[counter + 1])
            round_points.append(rounds[counter + 1])
            consumption_points.append(consumption[counter + 1])
            efficiency_points.append(efficiency[counter + 1])
            if without_position is False:
                latitude_points.append(latitude[counter+1])
                longitude_points.append(longitude[counter+1])
            elif without_position is True:
                pass
            sideG_points.append(sideG[counter + 1])
            power_points.append(outputPower[counter + 1])
            frontAcc_points.append(frontAcc[counter+1])

        if len(times) > counter + 2:
            time_points.append(times[counter + 2])
            speed_points.append(speeds[counter + 2])
            round_points.append(rounds[counter + 2])
            consumption_points.append(consumption[counter + 2])
            efficiency_points.append(efficiency[counter + 2])
            if without_position is False:
                latitude_points.append(latitude[counter+2])
                longitude_points.append(longitude[counter+2])
            elif without_position is True:
                pass
            sideG_points.append(sideG[counter + 2])
            power_points.append(outputPower[counter + 2])
            frontAcc_points.append(frontAcc[counter+2])

        if len(times) > counter + 3:
            time_points.append(times[counter + 3])
            speed_points.append(speeds[counter + 3])
            round_points.append(rounds[counter + 3])
            consumption_points.append(consumption[counter + 3])
            efficiency_points.append(efficiency[counter + 3])
            if without_position is False:
                latitude_points.append(latitude[counter+3])
                longitude_points.append(longitude[counter+3])
            elif without_position is True:
                pass
            sideG_points.append(sideG[counter + 3])
            power_points.append(outputPower[counter + 3])
            frontAcc_points.append(frontAcc[counter+3])

        '''
        if len(times) > counter + 4:
            time_points.append(times[counter + 4])
            speed_points.append(speeds[counter + 4])
            round_points.append(rounds[counter + 4])
            consumption_points.append(consumption[counter + 4])
            efficiency_points.append(efficiency[counter + 4])
            latitude_points.append(latitude[counter + 4])
            longitude_points.append(longitude[counter + 4])
            sideG_points.append(sideG[counter + 4])
            rightG_points.append(rightG[counter + 4])
            power_points.append(outputPower[counter + 4])
        '''

        if len(time_points) >= 4:
            for x in range(ceil(time_points[0]), ceil(time_points[3])):
                if x % 2 == 0:
                    target_timestamps.append(x)
        else:
            break

        counter += 3

        if len(target_timestamps) >= 1:
            speed_iter = interpolation(target_timestamps, time_points, speed_points)
            rounds_iter = interpolation(target_timestamps, time_points, round_points)
            consumption_iter = interpolation(target_timestamps, time_points, consumption_points)
            efficiency_iter = interpolation(target_timestamps, time_points, efficiency_points)
            if without_position is True:
                pass
            elif without_position is False:
                latitude_iter = interpolation(target_timestamps, time_points, latitude_points)
                longitude_iter = interpolation(target_timestamps, time_points, longitude_points)
            sideG_iter = interpolation(target_timestamps, time_points, sideG_points)
            power_iter = interpolation(target_timestamps, time_points, power_points)
            frontAcc_iter = interpolation(target_timestamps, time_points, frontAcc_points)

            for one, two, three, four in zip(speed_iter, rounds_iter, consumption_iter, efficiency_iter):
                new_speed.append(one)
                new_rounds.append(two)
                new_consumption.append(three)
                new_efficiency.append(four)

            if without_position is True:
                for one in target_timestamps:
                    new_latitude.append("null")
                    new_longitude.append("null")
            elif without_position is False:
                for one in latitude_iter:
                    new_latitude.append(one)
                for one in longitude_iter:
                    new_longitude.append(one)

            for one in sideG_iter:
                new_sideG.append(one)

            for one in power_iter:
                new_outputPower.append(one)

            for one in frontAcc_iter:
                new_frontAcc.append(one)

            for onetts in target_timestamps:
                new_time.append(onetts)
        else:
            continue

    if len(new_speed) == len(new_time) == len(new_rounds) == len(new_efficiency) == len(new_latitude) == len(
            new_longitude) \
            == len(new_sideG) == len(new_consumption) == len(new_outputPower) == len(new_frontAcc):

        doc["content"]["data"]["mapData"].clear()
        for sp, ti, rp, eff, lat, lon, sg, con, op, fa in zip(new_speed, new_time, new_rounds, new_efficiency,
                                                              new_latitude, new_longitude, new_sideG,
                                                              new_consumption, new_outputPower, new_frontAcc):
            dictionary = {"speed": sp,
                          "time": ti,
                          "rpm": rp,
                          "efficiency": eff,
                          "latitude": lat,
                          "longitude": lon,
                          "sideG": sg,
                          "consumption": con,
                          "outputPower": op,
                          "fontAcc": fa}
            doc["content"]["data"]["mapData"].append(dictionary)
        return doc
    else:
        pass

    '''REMOVE ERRORS/GAPS IN FREQUENCY'''

def resampling_new(doc):
    times = []
    speeds = []
    rounds = []
    consumption = []
    efficiency = []
    latitude = []
    longitude = []
    sideG = []
    outputPower = []
    frontAcc = []

    #FIRST VERSION
    missing_position = 0
    without_position = False
    only_few_missing = False

    for idx, item in enumerate(doc["content"]["data"]["mapData"]):
        if item["latitude"] == "null" and item["longitude"] == "null":
            missing_position += 1
        if idx > 0:
            if item["time"] > doc["content"]["data"]["mapData"][idx-1]["time"]:
                del doc["content"]["data"]["mapData"][idx]
    prc = missing_position / len(doc["content"]["data"]["mapData"])
    if prc >= 0.9:
        without_position = True
    elif 0.0 < prc < 0.9:
        only_few_missing = True
    else:
        pass

    #SECOND VERSION

    for sample in doc["content"]["data"]["mapData"]:
        if only_few_missing is True:
            if sample["speed"] != "null" and sample["time"] != "null" and sample["rpm"] != "null" and sample["consumption"]\
                    != "null" and sample["efficiency"] != "null" and sample["sideG"] != "null" and sample["outputPower"] != "null" and sample["latitude"] != "null" and sample["longitude"] != "null" and sample["fontAcc"] != "null":
                speeds.append(sample["speed"])
                times.append(sample["time"])
                rounds.append(sample["rpm"])
                consumption.append(sample["consumption"])
                efficiency.append(sample["efficiency"])
                sideG.append(sample["sideG"])
                outputPower.append(sample["outputPower"])
                latitude.append(sample["latitude"])
                longitude.append(sample["longitude"])
                frontAcc.append(sample["fontAcc"])

        elif only_few_missing is False:
            if sample["speed"] != "null" and sample["time"] != "null" and sample["rpm"] != "null" and sample["consumption"]\
                    != "null" and sample["efficiency"] != "null" and sample["sideG"] != "null" and sample["outputPower"] != "null" and sample["fontAcc"] != "null":
                frontAcc.append(sample["fontAcc"])
                speeds.append(sample["speed"])
                times.append(sample["time"])
                rounds.append(sample["rpm"])
                consumption.append(sample["consumption"])
                efficiency.append(sample["efficiency"])
                sideG.append(sample["sideG"])
                outputPower.append(sample["outputPower"])
            if without_position is True:
                pass
            elif without_position is False:
                if sample["latitude"] != "null":
                    latitude.append(sample["latitude"])
                if sample["longitude"] != "null":
                    longitude.append(sample["longitude"])

    def interpolation(x, x_axis, y_axis):
        tck = interpolate.splrep(x_axis, y_axis, k=3, s=0)
        result = interpolate.splev(x, tck)
        return list(result)

    target_timestamps = []
    for x in range(ceil(times[0]), ceil(times[-1])):
        if x % 2 == 0:
            target_timestamps.append(x)
    
    new_speed = interpolation(target_timestamps, times, speeds)
    new_rounds = interpolation(target_timestamps, times, rounds)
    new_consumption = interpolation(target_timestamps, times, consumption)
    new_efficiency = interpolation(target_timestamps, times, efficiency)
    if without_position is True:
        pass
    elif without_position is False:
        new_latitude = interpolation(target_timestamps, times, latitude)
        new_longitude = interpolation(target_timestamps, times, longitude)
    new_sideG = interpolation(target_timestamps, times, sideG)
    new_outputPower = interpolation(target_timestamps, times, outputPower)
    new_frontAcc = interpolation(target_timestamps, times, frontAcc)

            

    if len(new_speed) == len(target_timestamps) == len(new_rounds) == len(new_efficiency) == len(new_latitude) == len(
        new_longitude) == len(new_sideG) == len(new_consumption) == len(new_outputPower) == len(new_frontAcc):

        doc["content"]["data"]["mapData"].clear()
        for sp, ti, rp, eff, lat, lon, sg, con, op, fa in zip(new_speed, target_timestamps, new_rounds, new_efficiency,
                                                              new_latitude, new_longitude, new_sideG,
                                                              new_consumption, new_outputPower, new_frontAcc):
            dictionary = {"speed": sp,
                          "time": ti,
                          "rpm": rp,
                          "efficiency": eff,
                          "latitude": lat,
                          "longitude": lon,
                          "sideG": sg,
                          "consumption": con,
                          "outputPower": op,
                          "fontAcc": fa}
            doc["content"]["data"]["mapData"].append(dictionary)
        return doc
    else:
        pass

input.close()
