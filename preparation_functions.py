from scipy import interpolate
from random import uniform


def validate_json(file):
    for ride in file:
        if "id" and "content" in ride:
            if "mapData" in ride["content"]:
                return True
        else:
            return False


def prepare_json_spec(file):
    if isinstance(file, dict):
        if "id" in file:
            file["_id"] = file.pop("id")
        elif "_id" in file:
            pass

        content = file["content"]
        data = file["content"]["data"]

        file.pop("partialUserKey")
        file.pop("addonId")
        content.pop("version")

        try:
            data.pop("totalDistance")
            data.pop("tankLevelPrimary")
            data.pop("serviceOilTime")
            data.pop("serviceOilDistance")
            data.pop("serviceInspectionTime")
            data.pop("serviceInspectionDistance")
        except KeyError:
            pass

        if isinstance(data["maxPower"], dict):
            maxPower = data["maxPower"]["$numberInt"]
            data["maxPower"].pop("$numberInt")
            data["maxPower"] = maxPower

        if "fuelPricePrimary" in data:
            if isinstance(data["fuelPricePrimary"], dict):
                fuelPricePrimary = data["fuelPricePrimary"]["$numberInt"]
                data["fuelPricePrimary"].pop("$numberInt")
                data["fuelPricePrimary"] = fuelPricePrimary

        if isinstance(file["updated"], dict):
            updated = file["updated"]["$numberLong"]
            file["updated"].pop("$numberLong")
            file["updated"] = updated

        id = file["itemId"]
        file["_id"] = id
        file.pop("itemId")

    return file


def prepare_json(file):
    if isinstance(file, list):
        for j in file:
            if "id" in j:
                j["_id"] = j.pop("id")
            elif "_id" in j:
                pass

        for ride in file:
            for item in ride["content"]["data"]["mapData"]:
                realtime = item["time"]["$numberLong"]
                item["time"].pop("$numberLong")
                item["time"] = realtime

                if 'consumption' not in item:
                    item['consumption'] = "null"
                if 'efficiency' not in item:
                    item['efficiency'] = "null"
                if 'fontAcc' not in item:
                    item['fontAcc'] = "null"
                if 'latitude' not in item:
                    item['latitude'] = "null"
                if 'leftG' not in item:
                    item['leftG'] = "null"
                if 'outputPower' not in item:
                    item['outputPower'] = "null"
                if 'longitude' not in item:
                    item['longitude'] = "null"
                if 'refuel' not in item:
                    item['refuel'] = "null"
                if 'rightG' not in item:
                    item['rightG'] = "null"
                if 'rpm' not in item:
                    item['rpm'] = "null"
                if 'speed' not in item:
                    item['speed'] = "null"
                if 'stopped' not in item:
                    item['stopped'] = "null"
                if 'time' not in item:
                    item['time'] = "null"
                else:
                    pass

            for item in ride["content"]["data"]["mapData"]:
                try:
                    val = float(item['speed'])
                    item["speed"] *= 3600
                    rounded_speed = round(item["speed"], 2)
                    item["speed"] = rounded_speed

                    adjusted_timestamp = float(item["time"]) / 1000

                    item["speed"] = adjusted_timestamp


                except ValueError:
                    pass

    if isinstance(file, dict):
        if "id" in file:
            file["_id"] = file.pop("id")
        elif "_id" in file:
            pass

        file.pop("partialUserKey")
        file.pop("addonId")
        if "driveCostSecondary" in file["content"]["data"]:
            file["content"]["data"].pop("driveCostSecondary")
        file["content"].pop("version")

        #if "driveTime" in file['content']['data']:
        try:
            drivetime = file['content']['data']['driveTime']
        except KeyError:
            return file

        data = file["content"]["data"]

        if isinstance(data["driveTime"], dict):
            '''
            if "maxConsumptionTime" in data:
                if data["maxConsumptionTime"] is not None:
                    maxconsumptime = data["maxConsumptionTime"]["$numberLong"]
                    data["maxConsumptionTime"].pop("$numberLong")
                    data["maxConsumptionTime"] = maxconsumptime
                else:
                    pass
            else:
                pass
            '''
            try:
                avgConsumptionSecondary = data["avgConsumptionSecondary"]["$numberInt"]
                data["avgConsumptionSecondary"].pop("$numberInt")
                data["avgConsumptionSecondary"] = avgConsumptionSecondary
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                totalDistance = data["totalDistance"]["$numberInt"]
                data["totalDistance"].pop("$numberInt")
                data["totalDistance"] = totalDistance
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                totalDistanceStart = data["totalDistanceStart"]["$numberInt"]
                data["totalDistanceStart"].pop("$numberInt")
                data["totalDistanceStart"] = totalDistanceStart
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                totalDistanceLast = data["totalDistanceLast"]["$numberInt"]
                data["totalDistanceLast"].pop("$numberInt")
                data["totalDistanceLast"] = totalDistanceLast
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxconsump = data["maxConsumption"]["$numberInt"]
                data["maxConsumption"].pop("$numberInt")
                data["maxConsumption"] = maxconsump
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxconsumptime = data["maxConsumptionTime"]["$numberLong"]
                data["maxConsumptionTime"].pop("$numberLong")
                data["maxConsumptionTime"] = maxconsumptime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxconsumptime = data["maxConsumptionTime"]["$numberInt"]
                data["maxConsumptionTime"].pop("$numberInt")
                data["maxConsumptionTime"] = maxconsumptime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxenginespeedtime = data["maxEngineSpeedTime"]["$numberLong"]
                data["maxEngineSpeedTime"].pop("$numberLong")
                data["maxEngineSpeedTime"] = maxenginespeedtime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxenginespeed = data["maxEngineSpeed"]["$numberInt"]
                data["maxEngineSpeed"].pop("$numberInt")
                data["maxEngineSpeed"] = maxenginespeed
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxfrontacctime = data["maxFrontAccTime"]["$numberLong"]
                data["maxFrontAccTime"].pop("$numberLong")
                data["maxFrontAccTime"] = maxfrontacctime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxfrontacc = data["maxFrontAcc"]["$numberInt"]
                data["maxFrontAcc"].pop("$numberInt")
                data["maxFrontAcc"] = maxfrontacc
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxLeftAccTime = data["maxLeftAccTime"]["$numberLong"]
                data["maxLeftAccTime"].pop("$numberLong")
                data["maxLeftAccTime"] = maxLeftAccTime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxVehicleSpeedTime = data["maxVehicleSpeedTime"]["$numberLong"]
                data["maxVehicleSpeedTime"].pop("$numberLong")
                data["maxVehicleSpeedTime"] = maxVehicleSpeedTime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxVehicleSpeed = data["maxVehicleSpeed"]["$numberInt"]
                data["maxVehicleSpeed"].pop("$numberInt")
                data["maxVehicleSpeed"] = maxVehicleSpeed
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                drivetime = data["driveTime"]["$numberInt"]
                data["driveTime"].pop("$numberInt")
                data["driveTime"] = drivetime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                endtime = data["endTime"]["$numberLong"]
                data["endTime"].pop("$numberLong")
                data["endTime"] = endtime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                starttime = data["startTime"]["$numberLong"]
                data["startTime"].pop("$numberLong")
                data["startTime"] = starttime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                updated = file["updated"]["$numberLong"]
                file["updated"].pop("$numberLong")
                file["updated"] = updated
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxRearAccTime = data["maxRearAccTime"]["$numberLong"]
                data["maxRearAccTime"].pop("$numberLong")
                data["maxRearAccTime"] = maxRearAccTime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxRightAccTime = data["maxRightAccTime"]["$numberLong"]
                data["maxRightAccTime"].pop("$numberLong")
                data["maxRightAccTime"] = maxRightAccTime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxOutputPowerTime = data["maxOutputPowerTime"]["$numberLong"]
                data["maxOutputPowerTime"].pop("$numberLong")
                data["maxOutputPowerTime"] = maxOutputPowerTime
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                maxOutputPower = data["maxOutputPower"]["$numberInt"]
                data["maxOutputPower"].pop("$numberInt")
                data["maxOutputPower"] = maxOutputPower
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                avgOutputPower = data["avgOutputPower"]["$numberInt"]
                data["avgOutputPower"].pop("$numberInt")
                data["avgOutputPower"] = avgOutputPower
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                avgVehicleSpeed = data["avgVehicleSpeed"]["$numberInt"]
                data["avgVehicleSpeed"].pop("$numberInt")
                data["avgVehicleSpeed"] = avgVehicleSpeed
            except KeyError:
                pass
            except TypeError:
                pass

        else:
            updated = file["updated"]["$numberLong"]
            file["updated"].pop("$numberLong")
            file["updated"] = updated

        id = file["itemId"]
        file["_id"] = id
        file.pop("itemId")

        try:
            updated = file["updated"]["$numberLong"]
            file["updated"].pop("$numberLong")
            file["updated"] = updated
        except KeyError:
            pass
        except TypeError:
            pass

        if "mapData" not in file["content"]["data"]:
            file["content"]["data"]["mapData"] = []
        else:

            for item in file["content"]["data"]["mapData"]:
                if isinstance(item["time"], int):
                    pass
                elif isinstance(item["time"], dict):
                    realtime = item["time"]["$numberLong"]
                    item["time"].pop("$numberLong")
                    item["time"] = realtime

                try:
                    consumption = item["consumption"]["$numberLong"]
                    item["consumption"].pop("$numberLong")
                    item["consumption"] = consumption
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    consumption = item["consumption"]["$numberLong"]
                    item["consumption"].pop("$numberLong")
                    item["consumption"] = consumption
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    consumption = item["consumption"]["$numberInt"]
                    item["consumption"].pop("$numberInt")
                    item["consumption"] = consumption
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    efficiency = item["efficiency"]["$numberInt"]
                    item["efficiency"].pop("$numberInt")
                    item["efficiency"] = efficiency
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    fontAcc = item["fontAcc"]["$numberInt"]
                    item["fontAcc"].pop("$numberInt")
                    item["fontAcc"] = fontAcc
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    leftG = item["leftG"]["$numberInt"]
                    item["leftG"].pop("$numberInt")
                    item["leftG"] = leftG
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    outputPower = item["outputPower"]["$numberInt"]
                    item["outputPower"].pop("$numberInt")
                    item["outputPower"] = outputPower
                except KeyError:
                    pass
                except TypeError:
                    pass


                try:
                    speed = item["speed"]["$numberInt"]
                    item["speed"].pop("$numberInt")
                    item["speed"] = speed
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    rpm = item["rpm"]["$numberInt"]
                    item["rpm"].pop("$numberInt")
                    item["rpm"] = rpm
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    rightG = item["rightG"]["$numberInt"]
                    item["rightG"].pop("$numberInt")
                    item["rightG"] = rightG
                except KeyError:
                    pass
                except TypeError:
                    pass

                try:
                    rearAcc = item["rearAcc"]["$numberInt"]
                    item["rearAcc"].pop("$numberInt")
                    item["rearAcc"] = rearAcc
                except KeyError:
                    pass
                except TypeError:
                    pass

                if 'consumption' not in item:
                    item['consumption'] = "null"
                if 'efficiency' not in item:
                    item['efficiency'] = "null"
                if 'fontAcc' not in item:
                    item['fontAcc'] = "null"
                if 'latitude' not in item:
                    item['latitude'] = "null"
                if 'leftG' not in item:
                    item['leftG'] = "null"
                if 'outputPower' not in item:
                    item['outputPower'] = "null"
                if 'longitude' not in item:
                    item['longitude'] = "null"
                if 'refuel' not in item:
                    item['refuel'] = "null"
                if 'rightG' not in item:
                    item['rightG'] = "null"
                if 'rpm' not in item:
                    item['rpm'] = "null"
                if 'speed' not in item:
                    item['speed'] = "null"
                if 'stopped' not in item:
                    item['stopped'] = "null"
                if 'time' not in item:
                    item['time'] = "null"
                else:
                    pass

            for item in file["content"]["data"]["mapData"]:
                try:
                    #val = float(item['speed'])

                    if isinstance(item['speed'], float):
                        item["speed"] *= 3600
                        rounded_speed = round(item["speed"], 2)
                        item["speed"] = rounded_speed

                    adjusted_timestamp = float(item["time"]) / 1000
                    item["time"] = adjusted_timestamp

                except ValueError:
                    pass
    else:
        pass
    return file


def delete_begin_end(document):
    n = 0
    length = len(document["content"]["data"]["mapData"]) - 1
    while length > n and document["content"]["data"]["mapData"][n]["consumption"] == "null":
        n += 1

    del document["content"]["data"]["mapData"][0:n]


    m = len(document["content"]["data"]["mapData"]) - 1
    while m > 0 and document["content"]["data"]["mapData"][m]["consumption"] == "null":
        m -= 1

    del document["content"]["data"]["mapData"][-1:m]
    return document


def unify_side_g(document):
    for sample in document["content"]["data"]["mapData"]:
        rg = sample["rightG"]
        lg = sample["leftG"]

        (lg - pg) / 2#prumerne zrychleni doleva
        - (lg - pg) / 2

        if isinstance(rg, (float, int)) and isinstance(lg, str):
            sample["sideG"] = rg
        elif isinstance(lg, (float, int)) and isinstance(rg, str):
            sample["sideG"] = abs(lg)
        elif isinstance(rg, str) and isinstance(lg, str):
            sample["sideG"] = "null"
        elif isinstance(rg, (float, int)) and isinstance(lg, (float, int)):
            sample["sideG"] = lg + rg
        del sample["rightG"]
        del sample["leftG"]
    return document


def handle_consumption_nulls(document):
    for idx, sample in enumerate(document["content"]["data"]["mapData"]):
        cons = sample["consumption"]
        rpm = sample["rpm"]
        speed = sample["speed"]

        if cons == "null" and speed != "null" and rpm != "null":
            if speed < 3:
                sample["consumption"] = uniform(1.0, 2.0)

    return document


def handle_4nulls_in_motion(document):
    mapData = document["content"]["data"]["mapData"]
    for idx, sample in enumerate(mapData):
        eff = sample["efficiency"]
        rpm = sample["rpm"]
        speed = sample["speed"]
        facc = sample["fontAcc"]

        if len(mapData) - 1 > idx > 0 and eff == "null" and rpm == "null" and speed == "null" and facc == "null":
            before = mapData[idx-1]
            after = mapData[idx+1]
            if before["efficiency"] != "null" and before["rpm"] != "null" and \
                before["speed"] != "null" and before["fontAcc"] != "null":
                if after["efficiency"] != "null" and after["rpm"] != "null" and \
                        after["speed"] != "null" and after["fontAcc"] != "null":
                    if abs((before["efficiency"] - after["efficiency"])) < 20 and\
                            abs((before["rpm"] - after["rpm"])) < 400 and abs((before["speed"]\
                            - after["speed"])) < 20 and abs((before["fontAcc"]\
                            - after["fontAcc"])) < 0.2 and (abs(before["time"] - after["time"])) <= 15:
                        
                        timesource = [before["time"], after["time"]]
                        rpmsource = [before["rpm"], after["rpm"]]
                        speedsource = [before["speed"], after["speed"]]
                        fontAccsource = [before["fontAcc"], after["fontAcc"]]
                        effisource = [before["efficiency"], after["efficiency"]]

                        f1 = interpolate.interp1d(timesource, rpmsource)
                        f2 = interpolate.interp1d(timesource, speedsource)
                        f3 = interpolate.interp1d(timesource, fontAccsource)
                        f4 = interpolate.interp1d(timesource, effisource)

                        sample["rpm"] = f1(mapData[idx]["time"]).item(0)
                        sample["speed"] = f2(mapData[idx]["time"]).item(0)
                        sample["fontAcc"] = f3(mapData[idx]["time"]).item(0)
                        sample["efficiency"] = f4(mapData[idx]["time"]).item(0)
    return document


def handle_nulls_in_motion(document):
    mapData = document["content"]["data"]["mapData"]
    for idx, sample in enumerate(mapData):
        eff = sample["efficiency"]
        rpm = sample["rpm"]
        speed = sample["speed"]
        facc = sample["fontAcc"]
        outputp = sample["outputPower"]
        sideg = sample["sideG"]
        cons = sample["consumption"]
        



        if len(mapData) - 1 > idx > 0:
            before = mapData[idx - 1]
            after = mapData[idx + 1]
            if (abs(before["time"] - after["time"])) <= 20:

                timesource = [before["time"], after["time"]]
                if eff == "null":
                    if before["efficiency"] != "null" and after["efficiency"] != "null":
                        if abs((before["efficiency"] - after["efficiency"])) < 20:
                            effisource = [before["efficiency"], after["efficiency"]]
                            f1 = interpolate.interp1d(timesource, effisource)
                            sample["efficiency"] = f1(mapData[idx]["time"]).item(0)
                if rpm == "null":
                    if before["rpm"] != "null" and after["rpm"] != "null":
                        if abs((before["rpm"] - after["rpm"])) < 400:
                            rpmsource = [before["rpm"], after["rpm"]]
                            f2 = interpolate.interp1d(timesource, rpmsource)
                            sample["rpm"] = f2(mapData[idx]["time"]).item(0)
                if speed == "null":
                    if before["speed"] != "null" and after["speed"] != "null":
                        if abs((before["speed"] - after["speed"])) < 30:
                            speedsource = [before["speed"], after["speed"]]
                            f3 = interpolate.interp1d(timesource, speedsource)
                            sample["speed"] = f3(mapData[idx]["time"]).item(0)
                if facc == "null":
                    if before["fontAcc"] != "null" and after["fontAcc"] != "null":
                        if abs((before["fontAcc"] - after["fontAcc"])) < 0.3:
                            fontAccsource = [before["fontAcc"], after["fontAcc"]]
                            f4 = interpolate.interp1d(timesource, fontAccsource)
                            sample["fontAcc"] = f4(mapData[idx]["time"]).item(0)
                if sideg == "null":
                    if before["sideG"] != "null" and after["sideG"] != "null":
                        if abs((before["sideG"] - after["sideG"])) < 0.2:
                            sideGsource = [before["sideG"], after["sideG"]]
                            f5 = interpolate.interp1d(timesource, sideGsource)
                            sample["sideG"] = f5(mapData[idx]["time"]).item(0)
                if outputp == "null":
                    if before["outputPower"] != "null" and after["outputPower"] != "null":
                        if abs((before["outputPower"] - after["outputPower"])) < 50:
                            outputPowersource = [before["outputPower"], after["outputPower"]]
                            f6 = interpolate.interp1d(timesource, outputPowersource)
                            sample["outputPower"] = f6(mapData[idx]["time"]).item(0)
                if cons == "null":
                    if before["consumption"] != "null" and after["consumption"] != "null":
                        if abs((before["consumption"] - after["consumption"])) < 5.0:
                            consumptionsource = [before["consumption"], after["consumption"]]
                            f6 = interpolate.interp1d(timesource, consumptionsource)
                            sample["consumption"] = f6(mapData[idx]["time"]).item(0)
    return document


def eliminate_extremes(document):
    invalid = [0, 0, 0, 0, 0, 0, 0]
    sample_count = 0

    maxfontacc = 0
    minfontacc = 0

    maxsideG = 0
    minsideG = 0

    maxconsumption = 0

    for sample in document["content"]["data"]["mapData"]:

        if isinstance(sample["consumption"], (int, float)) and sample["consumption"] < 70:
            if sample["consumption"] > maxconsumption:
                maxconsumption = sample["consumption"]

        if isinstance(sample["fontAcc"], (int, float)):
            if -1.7 < sample["fontAcc"] < 0:
                if sample["fontAcc"] < minfontacc:
                    minfontacc = sample["fontAcc"]
            if 1.7 > sample["fontAcc"] > 0:
                if sample["fontAcc"] > maxfontacc:
                    maxfontacc = sample["fontAcc"]

        if isinstance(sample["sideG"], (int, float)):
            if -1.7 < sample["sideG"] < 0:
                if sample["sideG"] < minsideG:
                    minsideG = sample["sideG"]
            if 1.7 > sample["sideG"] > 0:
                if sample["sideG"] > maxsideG:
                    maxsideG = sample["sideG"]

    for sample in document["content"]["data"]["mapData"]:
        sample_count += 1

        if isinstance(sample["consumption"], (float, int)):
            if 0.0 > sample["consumption"]:
                sample["consumption"] = 0
                invalid[0] += 1
            elif sample["consumption"] > 70.0:
                invalid[0] += 1
                sample["consumption"] = maxconsumption
        if isinstance(sample["efficiency"], (float, int)):
            if 100 < sample["efficiency"] or sample["efficiency"] < 0:
                sample["efficiency"] = "null"
                invalid[1] += 1
        if isinstance(sample["fontAcc"], (float, int)):
            if 1.7 < sample["fontAcc"]:
                invalid[2] += 1
                sample["fontAcc"] = maxfontacc

            if sample["fontAcc"] < -1.7:
                invalid[2] += 1
                sample["fontAcc"] = minfontacc

        if isinstance(sample["sideG"], (float, int)):
            if 1.7 < sample["sideG"]:
                sample["sideG"] = maxsideG
                invalid[3] += 1
            if sample["sideG"] < -1.7:
                sample["sideG"] = minsideG
                invalid[3] += 1
        if isinstance(sample["rpm"], (float, int)):
            if 10000 < sample["rpm"] or sample["rpm"] < 0:
                #sample["rpm"] = "null"
                invalid[4] += 1
        if isinstance(sample["outputPower"], (float, int)):
            if 250 < sample["outputPower"] or sample["outputPower"] < 0:
                #sample["outputPower"] = "null"
                invalid[5] += 1
    #print(invalid)
    return document


def remove_all_nulls(document):
    indices = []
    smpls_less_than_minute = []

    for index, sample in enumerate(document["content"]["data"]["mapData"]):
        if sample["speed"] == "null" and sample["rpm"] == "null" and sample["efficiency"] == "null" and \
                sample["sideG"] == "null" and sample["outputPower"] == "null" and sample["consumption"] == "null"\
                and sample["fontAcc"] == "null":
            del sample

    #for ide, index in enumerate(indices):
        #k = 0
        #group = []
        #while indices[k] - indices[k+1] == -1:

        #document["content"]["data"]["mapData"][ide]
    return document


def dict_into_lists(document):
    array = []
    for sample in document["content"]["data"]["mapData"]:
        a = []
        a.append(sample["speed"])
        a.append(sample["rpm"])
        a.append(sample["consumption"])
        a.append(sample["efficiency"])
        a.append(sample["sideG"])
        a.append(sample["outputPower"])
        a.append(sample["fontAcc"])
        array.append(a)
    return array


def group_samples_together_listoflists(document):
    group = []
    speeds = []
    rounds = []
    consumption = []
    efficiency = []
    sideG = []
    outputPower = []
    frontAcc = []
    for sample in document["content"]["data"]["mapData"]:
        speeds.append(sample["speed"])
        rounds.append(sample["rpm"])
        consumption.append(sample["consumption"])
        efficiency.append(sample["efficiency"])
        sideG.append(sample["sideG"])
        outputPower.append(sample["outputPower"])
        frontAcc.append(sample["fontAcc"])
    group.append(speeds)
    group.append(rounds)
    group.append(consumption)
    group.append(efficiency)
    group.append(sideG)
    group.append(outputPower)
    group.append(frontAcc)
    return group

def count_extremes(document):
    sample_count = 0
    invalid = [0,0,0,0,0,0,0]
    for sample in document["content"]["data"]["mapData"]:
        sample_count += 1


        if isinstance(sample["consumption"], (float, int)):
            if 0.0 > sample["consumption"]:
                invalid[0] += 1
            elif sample["consumption"] > 70.0:
                invalid[0] += 1

        if isinstance(sample["efficiency"], (float, int)):
            if 100 < sample["efficiency"] or sample["efficiency"] < 0:
                invalid[1] += 1
        if isinstance(sample["fontAcc"], (float, int)):
            if 1.7 < sample["fontAcc"]:
                invalid[2] += 1
            if sample["fontAcc"] < -1.7:
                invalid[2] += 1
        if isinstance(sample["sideG"], (float, int)):
            if 1.7 < sample["sideG"]:
                invalid[3] += 1
            if sample["sideG"] < -1.7:
                invalid[3] += 1
        if isinstance(sample["rpm"], (float, int)):
            if 10000 < sample["rpm"] or sample["rpm"] < 0:
                invalid[4] += 1
        if isinstance(sample["outputPower"], (float, int)):
            if 250 < sample["outputPower"] or sample["outputPower"] < 0:
                invalid[5] += 1
        if isinstance(sample["speed"], (float, int)):
            if 250 < sample["speed"] or sample["speed"] < 0:
                invalid[6] += 1
    return invalid


def smooth_negative_values(document):
    for sample in document["content"]["data"]["mapData"]:
        if 0.0 > sample["consumption"]:
            sample["consumption"] = 0.0
        if sample["efficiency"] < 0:
            sample["efficiency"] = 0
        if sample["efficiency"] > 100:
            sample["efficiency"] = 100
        if sample["rpm"] < 0:
            sample["rpm"] = 0
        if sample["outputPower"] < 0:
            sample["outputPower"] = 0
        if sample["speed"] < 0:
            sample["speed"] = 0
    return document




                        
                        

