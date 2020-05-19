from math import ceil

from scipy.interpolate import interpolate


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

    # FIRST VERSION
    missing_position = 0
    without_position = False
    only_few_missing = False

    for idx, item in enumerate(doc["content"]["data"]["mapData"]):
        if item["latitude"] == "null" and item["longitude"] == "null":
            missing_position += 1
        if idx > 0:
            if item["time"] > doc["content"]["data"]["mapData"][idx - 1]["time"]:
                del doc["content"]["data"]["mapData"][idx]
    prc = missing_position / len(doc["content"]["data"]["mapData"])
    if prc >= 0.9:
        without_position = True
    elif 0.0 < prc < 0.9:
        only_few_missing = True
    else:
        pass

    # SECOND VERSION

    for sample in doc["content"]["data"]["mapData"]:
        if sample["time"] != "null":
            times.append(sample["time"])
        if sample["speed"] != "null":
            speeds.append(sample["speed"])
        if sample["rpm"] != "null":
            rounds.append(sample["rpm"])
        if sample["consumption"] != "null":
            consumption.append(sample["consumption"])
        if sample["efficiency"] != "null":
            efficiency.append(sample["efficiency"])
        if only_few_missing is True and without_position is False:
            if sample["latitude"] != "null":
                latitude.append(sample["latitude"])
            if sample["longitude"] != "null":
                longitude.append(sample["longitude"])
        if only_few_missing is False and without_position is True:
            pass
        if sample["sideG"] != "null":
            sideG.append(sample["sideG"])
        if sample["outputPower"] != "null":
            outputPower.append(sample["outputPower"])

    def interpolation(x, x_axis, y_axis):
        tck = interpolate.splrep(x_axis, y_axis, s=0)
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


def resampling_second(doc):
    times = []
    speeds = []
    rounds = []
    consumption = []
    efficiency = []
    latitude = []
    longitude = []
    sideG = []
    outputPower = []

    for sample in doc["content"]["data"]["mapData"]:
        if sample["time"] != "null":
            times.append(sample["time"])
        if sample["speed"] != "null":
            speeds.append(sample["speed"])
        if sample["rpm"] != "null":
            rounds.append(sample["rpm"])
        if sample["consumption"] != "null":
            consumption.append(sample["consumption"])
        if sample["efficiency"] != "null":
            efficiency.append(sample["efficiency"])
        if sample["latitude"] != "null":
            latitude.append(sample["latitude"])
        if sample["longitude"] != "null":
            longitude.append(sample["longitude"])
        if sample["sideG"] != "null":
            sideG.append(sample["sideG"])
        if sample["outputPower"] != "null":
            outputPower.append(sample["outputPower"])

    def interpolation(x, x_axis, y_axis):
        tck = interpolate.splrep(x_axis, y_axis)
        return list(interpolate.splev(x, tck))

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

        target_timestamps = []

        time_points.append(times[counter])
        speed_points.append(speeds[counter])
        round_points.append(rounds[counter])
        consumption_points.append(consumption[counter])
        efficiency_points.append(efficiency[counter])
        latitude_points.append(latitude[counter])
        longitude_points.append(longitude[counter])
        sideG_points.append(sideG[counter])
        power_points.append(outputPower[counter])

        if len(times) > counter + 1:
            time_points.append(times[counter + 1])
            speed_points.append(speeds[counter + 1])
            round_points.append(rounds[counter + 1])
            consumption_points.append(consumption[counter + 1])
            efficiency_points.append(efficiency[counter + 1])
            latitude_points.append(latitude[counter + 1])
            longitude_points.append(longitude[counter + 1])
            sideG_points.append(sideG[counter + 1])
            power_points.append(outputPower[counter + 1])

        if len(times) > counter + 2:
            time_points.append(times[counter + 2])
            speed_points.append(speeds[counter + 2])
            round_points.append(rounds[counter + 2])
            consumption_points.append(consumption[counter + 2])
            efficiency_points.append(efficiency[counter + 2])
            latitude_points.append(latitude[counter + 2])
            longitude_points.append(longitude[counter + 2])
            sideG_points.append(sideG[counter + 2])
            power_points.append(outputPower[counter + 2])

        if len(times) > counter + 3:
            time_points.append(times[counter + 3])
            speed_points.append(speeds[counter + 3])
            round_points.append(rounds[counter + 3])
            consumption_points.append(consumption[counter + 3])
            efficiency_points.append(efficiency[counter + 3])
            latitude_points.append(latitude[counter + 3])
            longitude_points.append(longitude[counter + 3])
            sideG_points.append(sideG[counter + 3])
            power_points.append(outputPower[counter + 3])

        '''
        if len(times) > counter + 4:
            time_points.append(times[counter + 4])
            speed_points.append(speeds[counter + 4])
            round_points.append(rounds[counter + 4])
            consumption_points.append(consumption[counter + 4])
            efficiency_points.append(efficiency[counter + 4])
            latitude_points.append(latitude[counter + 4])
            longitude_points.append(longitude[counter + 4])
            leftG_points.append(leftG[counter + 4])
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
            latitude_iter = interpolation(target_timestamps, time_points, latitude_points)
            longitude_iter = interpolation(target_timestamps, time_points, longitude_points)
            sideG_iter = interpolation(target_timestamps, time_points, sideG_points)
            power_iter = interpolation(target_timestamps, time_points, power_points)

            for one in speed_iter:
                new_speed.append(one)

            for one in rounds_iter:
                new_rounds.append(one)

            for one in consumption_iter:
                new_consumption.append(one)

            for one in efficiency_iter:
                new_efficiency.append(one)

            for one in latitude_iter:
                new_latitude.append(one)

            for one in longitude_iter:
                new_longitude.append(one)

            for one in sideG_iter:
                new_sideG.append(one)

            for one in power_iter:
                new_outputPower.append(one)

            for onetts in target_timestamps:
                new_time.append(onetts)
        else:
            continue

    if len(new_speed) == len(new_time) == len(new_rounds) == len(new_efficiency) == len(new_latitude) == len(
            new_longitude) \
            == len(new_sideG) == len(new_consumption) == len(new_outputPower):
        doc["content"]["data"]["mapData"].clear()
        for sp, ti, rp, eff, lat, lon, sg, con, op in zip(new_speed, new_time, new_rounds, new_efficiency,
                                                              new_latitude, new_longitude, new_sideG,
                                                              new_consumption, new_outputPower):
            dictionary = {"speed": sp,
                          "time": ti,
                          "rpm": rp,
                          "efficiency": eff,
                          "latitude": lat,
                          "longitude": lon,
                          "sideG": sg,
                          "consumption": con,
                          "outputPower": op}
            doc["content"]["data"]["mapData"].append(dictionary)
    return doc
