import pymongo
import re

pattern = re.compile(r'KODIAQ', re.I)
    pattern1 = re.compile(r'KAROQ', re.I)
    pattern2 = re.compile(r'SUPERB', re.I)
    pattern3 = re.compile(r'FABIA', re.I)
    pattern4 = re.compile(r'OCTAVIA', re.I)
    pattern6 = re.compile(r'RAPID', re.I)

    #kodiaq = collectionSpec.find()
    kodiaq_diesel_count = collectionSpec.count_documents({"content.data.vehicleType": pattern, "content.data.engineTypePrimary": "PETROLDIESEL"})

    #kodiaq = collectionSpec.find()
    kodiaq_gasoline_count = collectionSpec.count_documents({"content.data.vehicleType": pattern, "content.data.engineTypePrimary": "PETROLGASOLINE"})

    karoq_diesel_count = collectionSpec.count_documents({"content.data.vehicleType": pattern1, "content.data.engineTypePrimary": "PETROLDIESEL"})

    karoq_gasoline_count = collectionSpec.count_documents({"content.data.vehicleType": pattern1, "content.data.engineTypePrimary": "PETROLGASOLINE"})

    superb_diesel_count = collectionSpec.count_documents({"content.data.vehicleType": pattern2, "content.data.engineTypePrimary": "PETROLDIESEL"})

    superb_gasoline_count = collectionSpec.count_documents({"content.data.vehicleType": pattern2, "content.data.engineTypePrimary": "PETROLGASOLINE"})

    fabia_diesel_count = collectionSpec.count_documents({"content.data.vehicleType": pattern3, "content.data.engineTypePrimary": "PETROLDIESEL"})

    fabia_gasoline_count = collectionSpec.count_documents({"content.data.vehicleType": pattern3, "content.data.engineTypePrimary": "PETROLGASOLINE"})

    octavia_diesel_count = collectionSpec.count_documents({"content.data.vehicleType": pattern4, "content.data.engineTypePrimary": "PETROLDIESEL"})

    octavia_gasoline_count = collectionSpec.count_documents({"content.data.vehicleType": pattern4, "content.data.engineTypePrimary": "PETROLGASOLINE"})

    rapid_diesel_count = collectionSpec.count_documents({"content.data.vehicleType": pattern6, "content.data.engineTypePrimary": "PETROLDIESEL"})

    rapid_gasoline_count = collectionSpec.count_documents({"content.data.vehicleType": pattern6, "content.data.engineTypePrimary": "PETROLGASOLINE"})

    benzin_count = collectionSpec.count_documents({"content.data.engineTypePrimary": "PETROLGASOLINE"})

    diesel_count = collectionSpec.count_documents({"content.data.engineTypePrimary": "PETROLDIESEL"})

    cng_count = collectionSpec.count_documents({"content.data.engineTypePrimary": "GASCNG"})

    power = collectionSpec.distinct("content.data.maxPower")
    #print(power)

    type = collectionSpec.distinct("content.data.vehicleType")

'''
   {"$unwind": "$content.data"},
   '''
patt = [
    {"$group": {"_id": "$content.data.vehicleType", "count": {"$sum": 1}}}]
'''
agg = collectionSpec.aggregate(patt)

poweragg = collectionSpec.aggregate([{"$group": {"_id": "$content.data.engineTypePrimary", "count": {"$sum": 1}}}])
powerfuelagg = collectionSpec.aggregate([
    {"$group": {"_id": {"type": "$content.data.vehicleType", "fuel": "$content.data.engineTypePrimary", "power": "$content.data.maxPower"},
                "count": {"$sum": 1}}},
    {"$sort": bson.SON([("count", -1), ("id", -1)])}
])


'''
# collectionDrives.delete_many({"content.data.mapData.100": {"$exists": "true"}})
# ridesabovehundred = collectionDrives.count_documents({"content.data.mapData.99": {"$exists": "true"}})
# collectionDrives.delete_many({"$where": "this.content.data.mapData.length < 100"})
'''
rideswithvalidsamples = collectionDrives.count_documents({"content.data.mapData":{"$all": [
    {"$elemMatch": {"consumption": {"$ne":"null"} ,"efficiency": {"$ne":"null"} ,"fontAcc": {"$ne":"null"} ,
                    "latitude": {"$ne":"null"} ,"leftG": {"$ne":"null"} ,"longitude": {"$ne":"null"} ,
                    "outputPower": {"$ne":"null"}, "refuel": {"$ne":"null"}, "rightG": {"$ne":"null"},
     "rpm": {"$ne":"null"}, "speed": {"$ne":"null"}, "stopped": {"$ne":"null"}, "false": {"$ne":"null"}, "time":{"$ne":"null"}
}}
                                                                                     ]}})
'''

# mib = collectionDrives.count_documents({"content.data.isMib": {"$ne":"false"}})
# kodiaqvins = collectionSpec.find({"content.data.maxPower": 110, "content.data.engineTypePrimary": "PETROLGASOLINE", "content.data.vehicleType": "KODIAQ"}, {"content.data.vin": 1, "_id": 0})
# group = collectionSpec.group(key={"vehicleType": 0}, initial={"count": 0}, condition=None, reduce=None)
# print(list(group))
# print(list(agg))
# print(list(poweragg))
# print(list(powerfuelagg))
# print(list(longestride))
# firstset = list(kodiaqvins)
# print(firstset)
# print(len(firstset))
# print("Pocet jizd nad 100: " + str(ridesabovehundred))
# print("Pocet jizd pod 100: ")
# print("Validni: " + str(rideswithvalidsamples))
# print("S MIB:" + str(mib))
'''

pocet_jizd = []
for one in firstset:
    pocet = collectionDrives.count_documents({"content.data.vin": one["content"]["data"]["vin"]})

    pocet_jizd.append(int(pocet))

print(pocet_jizd)
vozy_co_jeli = 0

for j in pocet_jizd:
    if j > 0:
        vozy_co_jeli += 1
'''

pocet_nad_30 = []
# for one in firstset:
# pocet = collectionDrives.count_documents({"content.data.vin": one["content"]["data"]["vin"], "content.data.avgConsumptionPrimary": {"$gte": 20}})
# pocet_nad_30.append(int(pocet))
# collectionDrives.find({"content.data.vin": one["content"]["data"]["vin"], "content.data.avgConsumptionPrimary": {"$gte": 20}})

# samples = collectionDrives.aggregate({"_id": "$_id", "content.data.vin": one["content"]["data"]["vin"], "content.data.avgConsumptionPrimary": {"$gte": 20}, "samples": {"$size": "$content.data.mapData"}})

# samples = collectionDrives.aggregate([{
# "$project": {"samples": {"$cond": {"if": {"$isArray": "content.data.mapData"}, "then": {"$size": "$content.data.mapData"}, "else": "NA"}}}}])
'''
samples = collectionDrives.aggregate([{"$match": {"content.data.avgConsumptionPrimary": {"$gte": 20}}},
                                      {"$project": {
                                          "content.data.vin": 1,
                                          "samples": {"$size": "$content.data.mapData"}
                                        }
                                      },
                                      {"$sort": {"content.data.avgConsumptionPrimary": -1}}])
'''
'''    samples = collectionDrives.aggregate({"_id": "9223370494130435005",
                                      "content.data.avgConsumptionPrimary": {"$gte": 20},
                                      "samples": {"$size": "$content.data.mapData"}})'''

# samples = list(samples)
# print("Puvodni:" +str(len(samples)))



'''
    #print(samples)
    a = []
    for ride in samples:
        for vin in firstset:
            if ride["content"]["data"]["vin"] == vin["content"]["data"]["vin"]:
                a.append(ride)
            else:
                pass
        else:
            pass

    print(a)
    print("Pocet jizd nad 100 vzorku: "+str(len(a)))
    print("Jizda s nejvetsim poctem vyzorku:")
    print(pocet_nad_30)
    print("Pocet vozu:"+str(len(pocet_jizd)))
    print("Pocet vozu co jelo:"+str(vozy_co_jeli))
    print("Celkem najeto jizd:"+str(sum(pocet_jizd)))
    '''

# = collectionDrives.find({"content.data.mapData.500": {"$exists": "true"}})

# longer_than_500 = collectionDrives.count_documents({"content.data.mapData.500": {"$exists": "true"}})

suitable_document = 0
pocet_smazanych = 0
# print(longer_than_500)

# vysoke = collectionDrives.find({"content.data.avgConsumptionPrimary": {"$gte": 15}})
'''
efficiencies = collectionDrives.find({})
effies = []
for effi in efficiencies:
    effies.append(int(effi['content']['data']['avgEcoHmi']))
    #if 98.0 < effi['content']['data']['avgEcoHmi'] < 100.0:
        #basic_stats_onedrive(effi)
        #plot_whole_drive(effi)

print(sorted(effies))


Drives with highest efficiency: 9223370470473209210, 9223370478680501677, 9223370470475539172*chybna, 9223370472087780809, 9223370471240799735,  9223370475493493310, 9223370476098812480, 9223370478379205761, 9223370489183073276, 9223370470493191549, 9223370476077720992

Drives with lowest efficiency: 9223370519852608205, 9223370490872344260, 9223370476700887180, 9223370473640547545, 9223370473496558129, 9223370472766308139, 9223370477602207538, 9223370475405324541, 9223370470730278240, 9223370473832637302, 9223370477611018109 


'''
#sort samples in documents
collectionDrivesDivided.update_many({},
                                   {"$push":{"content.data.mapData":{
                                       "$each":[],
                                       "$sort": {"time":1}
                                   }}
                                   })