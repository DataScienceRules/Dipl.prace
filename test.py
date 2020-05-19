import json, random
import ijson
from statistics import mean, variance

import numpy
import matplotlib.pyplot as plt
'''


interpoluj vzorkovani na dve vteriny, ne linearne ale kubicky, prevzorkovat
zjistit a osetrit u 28200 jizd ktere lze upravit a pouzit
'''
from scipy import optimize
from scipy.stats.stats import pearsonr
from venv.visualization_functions import visualize_all_1plot, visualize_all_2plots, visualize_two_variables, universal_visualization, universal_visualization_colored, universal_2subplots_visualization_colored
from venv.preparation_functions import prepare_json, unify_side_g, handle_4nulls_in_motion, delete_begin_end, \
    handle_consumption_nulls, eliminate_extremes, handle_nulls_in_motion, dict_into_lists, remove_all_nulls,\
    count_extremes, smooth_negative_values, group_samples_together_listoflists
from venv.functions import basic_stats_onedrive
import pymongo
from venv.functions import single_dict_to_gpx, count_frequency_gaps, resampling, delete_frequency_gaps, resampling_new
from venv.analysis_functions import probability_distribution, kmeans_clustering, kmeans_predicting, agglomerative_clustering,\
    principal_component_analysis, agglomerative_experiment1, dbscan, optics_clustering
import bson
import re, os, math
from random import uniform

from sklearn.cluster import OPTICS, DBSCAN, KMeans, MiniBatchKMeans
from sklearn.preprocessing import StandardScaler, scale
from sklearn import tree
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()

print("MongoDB Client connected")


#if 'OneApp' in dblist:
    #print("Database exists")
#else:
mydb = myclient['OneApp']
print("Database created")
collectionDrives = mydb["Drives"]
collectionSpec = mydb["CarSpec"]
collectionDrivesResampled = mydb["DrivesResampled"]
collectionDrivesDivided = mydb["DrivesDivided"]


def main_func():






    '''
    IMPORTANT !!!
    ID: 
    VIN: 
    SAMPLES: 3201
    
    '''


    def count_gaps():
        documents = collectionDrivesDivided.find({})
        zerogaps = 0
        onegap = 0
        twogaps = 0
        threegaps = 0
        fourgaps = 0
        fivegaps = 0
        sixgaps = 0
        abovefivegaps = 0

        beforegapabove100 = 0
        aftergapabove100 = 0

        firstabove100 = 0
        secondabove100 = 0
        thirdabove100 = 0

        first = 0
        second = 0
        third = 0
        fourth = 0

        first5 = 0
        second5 = 0
        third5 = 0
        fourth5 = 0
        fifth5 = 0

        first6 = 0
        second6 = 0
        third6 = 0
        fourth6 = 0
        fifth6 = 0
        sixth6 = 0

        highestid = 0
        lowestid = 9223370542601346590

        for document in documents:
            id = int(document["_id"])
            if id > highestid:
                highestid = id
            if id < lowestid:
                lowestid = id
            gaps, firstgap, secondgap, thirdgap, fourthgap, fifthgap, sixthgap = count_frequency_gaps(document)
            if gaps == 0:
                zerogaps += 1
            if gaps == 1:
                #print(document["_id"])

                onegap += 1
                if firstgap >= 100:
                    beforegapabove100 += 1
                if secondgap >= 100:
                    aftergapabove100 += 1
            if gaps == 2:
                twogaps += 1
                if firstgap >= 100:
                    firstabove100 += 1
                if secondgap >= 100:
                    secondabove100 += 1
                if thirdgap >= 100:
                    thirdabove100 += 1
            if gaps == 3:
                threegaps += 1
                if firstgap >= 100:
                    first += 1
                if secondgap >= 100:
                    second += 1
                if thirdgap >= 100:
                    third += 1
                if fourthgap >= 100:
                    fourth += 1
            if gaps == 4:
                fourgaps += 1
                if firstgap >= 100:
                    first5 += 1
                if secondgap >= 100:
                    second5 += 1
                if thirdgap >= 100:
                    third5 += 1
                if fourthgap >= 100:
                    fourth5 += 1
                if fifthgap >= 100:
                    fifth5 += 1
            if gaps == 5:
                fivegaps += 1
                if firstgap >= 100:
                    first6 += 1
                if secondgap >= 100:
                    second6 += 1
                if thirdgap >= 100:
                    third6 += 1
                if fourthgap >= 100:
                    fourth6 += 1
                if fifthgap >= 100:
                    fifth6 += 1
                if sixthgap >= 100:
                    sixth6 += 1
            if gaps > 5:
                abovefivegaps += 1

        print("No gaps: "+str(zerogaps))
        print("One gap: " + str(onegap))
        print("Two gaps: " + str(twogaps))
        print("Three gaps: " + str(threegaps))
        print("Four gaps: " + str(fourgaps))
        print("Five gaps: " + str(fivegaps))
        print("\nRides with one gap - useful before gap: "+str(beforegapabove100)+", useful after gap: "+str(aftergapabove100))
        print("\nRides with two gaps - useful first part: " + str(firstabove100) + ", useful second part: " + str(
            secondabove100) + ", useful third part: " + str(thirdabove100))
        print("\nRides with three gaps - useful first part: " + str(first) + ", useful second part: " + str(
            second) + ", useful third part: " + str(third) + ", useful fourth part: "+str(fourth))
        print("\nRides with four gaps - useful first part: " + str(first5) + ", useful second part: " + str(
            second5) + ", useful third part: " + str(third5) + ", useful fourth part: " + str(fourth5) + ", useful fifth part: " + str(fifth5))
        print("\nRides with five gaps - useful first part: " + str(first6) + ", useful second part: " + str(
            second6) + ", useful third part: " + str(third6) + ", useful fourth part: " + str(
            fourth6) + ", useful fourth part: " + str(fifth6) + ", useful sixth part: " + str(sixth6))

        print(fourgaps)
        print(fivegaps)
        print(abovefivegaps)
        print(highestid)
        print(lowestid)

    #count_gaps()

    def remove_gaps(document):
        gaps, firstsubride, secondsubride, thirdsubride, fourthsubride, fifthsubride, sixthsubride = delete_frequency_gaps(document)

        if gaps == 0:
            try:
                collectionDrivesDivided.insert_one(document)
            except pymongo.errors.DuplicateKeyError:
                pass

        elif gaps == 1:
            if firstsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(firstsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            else:
                pass

            if secondsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(secondsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            else:
                pass

        elif gaps == 2:
            if firstsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(firstsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            else:
                pass
            if secondsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(secondsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            else:
                pass
            if thirdsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(thirdsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            else:
                pass
        elif gaps == 3:
            if firstsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(firstsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if secondsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(secondsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if thirdsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(thirdsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if fourthsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(fourthsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass

        elif gaps == 4:
            if firstsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(firstsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if secondsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(secondsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if thirdsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(thirdsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if fourthsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(fourthsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if fifthsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(fifthsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass

        elif gaps == 5:
            if firstsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(firstsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if secondsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(secondsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if thirdsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(thirdsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if fourthsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(fourthsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if fifthsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(fifthsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass
            if sixthsubride != "0":
                try:
                    collectionDrivesDivided.insert_one(sixthsubride)
                except pymongo.errors.DuplicateKeyError:
                    pass

        elif gaps > 5:
            pass


    def count_valid_samples(document):
        length = len(document["content"]["data"]["mapData"])
        percentages = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for sample in document["content"]["data"]["mapData"]:
            if sample['consumption'] == "null":
                percentages[0] += 1
            if sample['efficiency'] == "null":
                percentages[1] += 1
            if sample['fontAcc'] == "null":
                percentages[2] += 1
            if sample['latitude'] == "null":
                percentages[3] += 1
            if sample['leftG'] == "null":
                percentages[4] += 1
            if sample['outputPower'] == "null":
                percentages[5] += 1
            if sample['longitude'] == "null":
                percentages[6] += 1
            if sample['refuel'] == "null":
                percentages[7] += 1
            if sample['rightG'] == "null":
                percentages[8] += 1
            if sample['rpm'] == "null":
                percentages[9] += 1
            if sample['speed'] == "null":
                percentages[10] += 1
            if sample['stopped'] == "null":
                percentages[11] += 1
            if sample['time'] == "null":
                percentages[12] += 1

        weak_variable_count = 0
        outputfield = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        percentages = [per/length for per in percentages]
        for idx, per in enumerate(percentages):
            if per >= 0.2:
                outputfield[idx] += 1
                weak_variable_count += 1
            else:
                pass

        if weak_variable_count == 8:
            collectionDrivesDivided.delete_one({"_id": document["_id"]})

        if weak_variable_count == 7:
            collectionDrivesDivided.delete_one({"_id": document["_id"]})

        if weak_variable_count == 6:
            collectionDrivesDivided.delete_one({"_id": document["_id"]})
        if weak_variable_count == 5:
            collectionDrivesDivided.delete_one({"_id": document["_id"]})
        #if weak_variable_count <= 4 and weak_variable_count >= 1:
            #pass
        if weak_variable_count == 4:
            if outputfield[3] == 1 and outputfield[6] == 1 and outputfield[5] == 1 and outputfield[0] == 1:
                pass
            else:
                collectionDrivesDivided.delete_one({"_id": document["_id"]})
        if weak_variable_count == 3:
            print(document)
            print(outputfield)
            '''
            if outputfield[3] == 1 and outputfield[6] == 1 and outputfield[5] == 1 and outputfield[0] == 1:
                pass
            else:
                collectionDrivesDivided.delete_one({"_id": document["_id"]})
            
            if outputfield[3] >= 0.2 and outputfield[6] >= 0.2:
                print(document["_id"])
            if outputfield[5] >= 0.2 and outputfield[1] >= 0.2:
                print(document["_id"])
            if outputfield[5] >= 0.2 and outputfield[0] >= 0.2:
                print(document["_id"])
            if outputfield[0] >= 0.2 and outputfield[1] >= 0.2:
                print(document["_id"])
            else:
                collectionDrivesDivided.delete_one({"_id": document["_id"]})
            '''
        return weak_variable_count, outputfield


        #return list of variables that exceed the percentage



    #documents = collectionDrives.find({})
    '''
    #matice = [[0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0]]
    matice = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pocetbezpolohy = 0
    bezspotreby = 0
    
    #collectionDrivesResampled.remove({})
    documents = collectionDrivesDivided.find({})

    for idex, document in enumerate(documents):
        weak_variables, output_field = count_valid_samples(document)
        #delete samples with 5 missing values
        #collectionDrivesResampled.insert_one(resampling(document))
        print(output_field)
    '''
    def matrix_of_correlations2(sampleset):
        mat = []
        for id, one in enumerate(sampleset):
            firstcol = []
            for idx, two in enumerate(sampleset):
                corr, nic = pearsonr(one, two)
                firstcol.append(round(corr, 2))
            mat.append(firstcol)
            print(firstcol)

    def matrix_of_correlations(document):
        origin = group_samples_together_listoflists(document)
        mat = []
        for id, one in enumerate(origin):
            firstcol = []
            for idx, two in enumerate(origin):
                corr, nic = pearsonr(one, two)
                firstcol.append(corr)
            mat.append(firstcol)
            print(firstcol)

    #matrix_of_correlations(collectionDrivesResampled.find_one({"_id": "9223371498821004586"}))
    #print("\b")
    #matrix_of_correlations(collectionDrivesResampled.find_one({"_id": "9223370470471682174"}))

    def vehicles_overview():
        specs = collectionSpec.find({})
        for one in specs:
            if "engineTypePrimary" not in one["content"]["data"]:
                collectionSpec.delete_one({"_id": one["_id"]})
        powerfuelagg = collectionSpec.aggregate([
            {"$group": {"_id": {"type": "$content.data.vehicleType", "fuel": "$content.data.engineTypePrimary",
                                "power": "$content.data.maxPower"},
                        "count": {"$sum": 1}}},
            {"$sort": bson.SON([("count", -1), ("id", -1)])}
        ])
        pocet = 0
        for one in powerfuelagg:
            pocet+=1
            print(one)
        print(pocet)
    #vehicles_overview()

    def find_kodiaqs110():
        specifikace = collectionSpec.find({})
        vins = []
        ids = []
        for spec in specifikace:
            if spec["content"]["data"]["engineTypePrimary"] == "PETROLDIESEL" and spec["content"]["data"]\
                    ["maxPower"] == 110 and (spec["content"]["data"]["vehicleType"] == "KODIAQ"):
                vins.append(spec["content"]["data"]["vin"])
            else:
                pass

        print(collectionDrivesResampled.count_documents({"content.data.mapData": {"$size": 0}}))
        collectionDrivesResampled.delete_many({"content.data.mapData": {"$size": 0}})
        pocetjizd = 0
        pocetvzorku = 0
        nad500 = 0
        nad60speed = 0
        effiandid = []
        alldrives = []
        for vin in vins:
            jizdy = collectionDrivesResampled.find({"content.data.vin": vin})
            for idx, jizda in enumerate(jizdy):
                pocetjizd += 1
                alldrives.append(jizda["_id"])
                jedna = []
                avgc = []
                avge = []
                avgs = []
                jedna.append(jizda["_id"])
                delka = len(jizda["content"]["data"]["mapData"])
                jedna.append(delka)
                pocetvzorku += delka
                if delka >= 500:
                    nad500 += 1

                for one in jizda["content"]["data"]["mapData"]:
                    avgc.append(one["consumption"])
                    avge.append(one["efficiency"])
                    avgs.append(one["speed"])

                if mean(avgs) >= 60:
                    nad60speed += 1

                effiandid.append([mean(avge), jizda["_id"]])
        return alldrives

    def find_octavias110():
        specifikace = collectionSpec.find({})
        vins = []
        ids = []
        for spec in specifikace:
            if spec["content"]["data"]["engineTypePrimary"] == "PETROLGASOLINE" and spec["content"]["data"]["maxPower"] ==\
                    110 and (spec["content"]["data"]["vehicleType"] == "OCTAVIA" or spec["content"]["data"]["vehicleType"] == "OCTAVIACOMBI" or spec["content"]["data"]["vehicleType"] == "OCTAVIACOMBIRS"):
                vins.append(spec["content"]["data"]["vin"])
            else:
                pass

        print(collectionDrivesResampled.count_documents({"content.data.mapData": {"$size": 0}}))
        collectionDrivesResampled.delete_many({"content.data.mapData": {"$size": 0}})
        pocetjizd = 0
        pocetvzorku = 0
        nad500 = 0
        nad60speed = 0
        effiandid = []
        alldrives = []
        for vin in vins:
            jizdy = collectionDrivesResampled.find({"content.data.vin": vin})
            for idx, jizda in enumerate(jizdy):
                pocetjizd += 1
                alldrives.append(jizda["_id"])
                jedna = []
                avgc = []
                avge = []
                avgs = []
                jedna.append(jizda["_id"])
                delka = len(jizda["content"]["data"]["mapData"])
                jedna.append(delka)
                pocetvzorku += delka
                if delka >= 500:
                    nad500 += 1

                for one in jizda["content"]["data"]["mapData"]:
                    avgc.append(one["consumption"])
                    avge.append(one["efficiency"])
                    avgs.append(one["speed"])

                if mean(avgs) >= 60:
                    nad60speed += 1

                effiandid.append([mean(avge), jizda["_id"]])
                #ids.append(jedna)

        print(pocetjizd)
        print(nad500)
        print(nad60speed)
        print(pocetvzorku)
        #print(sorted(effiandid, key=lambda x: x[0]))
        return alldrives

    def select_random_drives(drives):
        selected = random.sample(drives, 1000)
        print(selected)
        return selected

    def kodiaq_testing_sample():
        testing_group = ['9223371470833214777', '9223375471837199319', '9223370477896267835', '9223371472164549385', '9223370505696723244', '9223370487340121887', '9223372490922184616', '9223373512865794897', '9223371473561534919', '9223372476542228016', '9223372523754228248', '9223370520212465942', '9223371470959455836', '9223372486786364314', '9223375506285957715', '9223370510457349254', '9223370474814068702', '9223370470617347184', '9223372475396231789', '9223372527362167486', '9223371471519620679', '9223371478412829738', '9223370515398188378', '9223370473811181767', '9223370489025429839', '9223372490925534467', '9223373473043793995', '9223370473811365525', '9223370473430171176', '9223370538055482449', '9223370514682332332', '9223372473811233552', '9223372473811354009', '9223371475355492622', '9223373527351130920', '9223371489731387560', '9223371536131127326', '9223371470963767529', '9223370514682337813', '9223371471593799940', '9223371473811204017', '9223370527113203963', '9223372505696725031', '9223372472074273864', '9223370528367073378', '9223370470603592571', '9223371487821641101', '9223371490925521158', '9223370473811191802', '9223370514682333705', '9223370470881570896', '9223373490925577723', '9223372470627538882', '9223371473811233552', '9223373472168846660', '9223371472018650425', '9223373476394803733', '9223370472818566368', '9223370477802753492', '9223370490925559468', '9223371487138438650', '9223374499560169052', '9223370489885978161', '9223373475815433555', '9223372523666053134', '9223371474510021091', '9223372472876785971', '9223372473549111805', '9223371488031265683', '9223371501767518871', '9223371476420728528', '9223370519964202927', '9223371471494554729', '9223373487388155997', '9223371490925541001', '9223374514156857831', '9223372490033239700', '9223370477552043614', '9223372474233473621', '9223372505696699913', '9223376473549107571', '9223373531974266516', '9223372477780302409', '9223370472669309903', '9223370486364550012', '9223370470814237951', '9223372473766623112', '9223370499462939453', '9223375527780967674', '9223372536131127326', '9223372522648034970', '9223371477780306419', '9223371475922967626', '9223371473811180779', '9223374472522489629', '9223371490925528742', '9223372476152110562', '9223370512353535959', '9223371474510018585', '9223371472003522828']

        return testing_group

    def octavia_testing_sample():
        testing_group = ['9223372498105784557', '9223371519727514510', '9223370477013289726', '9223370506911655837', '9223374478611574514', '9223370476413980697', '9223372475552722493', '9223372521879608035', '9223370470545780729', '9223371500544121081', '9223371511250306073', '9223370490918630467', '9223370519871575576', '9223371473054553466', '9223370512910184076', '9223372471595910784', '9223371501454796450', '9223372511851900410', '9223372473054451851', '9223372500710558864', '9223370477782847362', '9223372497235742081', '9223374471218467996', '9223372475552754412', '9223371477176355001', '9223375523089147150', '9223372474284802272', '9223372503783997910', '9223371475552835198', '9223370508713491157', '9223370490067133051', '9223370502449311902', '9223370475501344803', '9223370473054502476', '9223370477530278458', '9223370508713473500', '9223370473054613848', '9223370504936356584', '9223370476316701672', '9223371525476410781', '9223370475501345353', '9223370474194548135', '9223372507953839696', '9223371476406619880', '9223370476335835840', '9223370499906660251', '9223370510832659686', '9223371505023530445', '9223370508541849947', '9223374508737075014', '9223372489694608622', '9223371523160699792', '9223370490918625993', '9223370477321839665', '9223370503469882861', '9223373486788655292', '9223371473054523638', '9223370521761410962', '9223372490915120744', '9223373477949775306', '9223371472941825689', '9223371488913850104', '9223370476413982548', '9223371511851900410', '9223372472362967436', '9223370517488701527', '9223370472443736414', '9223371512212112093', '9223372473315385153', '9223372475552762559', '9223374523248999043', '9223371476413989599', '9223370488913850538', '9223375508713451244', '9223373470964487829', '9223370477788453452', '9223371508645809708', '9223371488913838882', '9223372499906624732', '9223370473054494556', '9223370507240783011', '9223370474093896696', '9223372508713466986', '9223372475552653376', '9223370473725216136', '9223371478403599873', '9223370507170307795', '9223371477466493931', '9223370478403555921', '9223371490291448425', '9223370519987570013', '9223373524659594614', '9223370472968319349', '9223374532551127776', '9223371490918635026', '9223370473054505732', '9223372486431731422', '9223371476025550739', '9223372515631817954', '9223371470875423980']
        #print(len(testing_group))
        return testing_group

    def testing_group_into_lists(testing_group):
        lists = [[],[],[],[],[],[],[]]
        for ride in testing_group:
            sublists = group_samples_together_listoflists(collectionDrivesResampled.find_one(ride))
            for idx, sublist in enumerate(sublists):
                lists[idx] += sublist
        return lists

    def testing_group_into_matrix(testing_group):
        matrix = []
        for ride in testing_group:
            subarray = dict_into_lists(collectionDrivesResampled.find_one(ride))
            matrix += subarray
        return matrix


    #octavie110 = find_octavias110()
    octavie110 = 0


    #trainingDataIds = select_random_drives(octavie110)
    #onethousand = testing_group_into_matrix(trainingDataIds)

    '''
    allremaining = []
    for id in octavie110:
        if id not in trainingDataIds:
            allremaining.append(id)
        else:
            pass
    '''
    #all_remaining_data = testing_group_into_matrix(allremaining)


    #thesample = testing_group_into_matrix(octavia_testing_sample())
    #kmeans = kmeans_clustering(principal_component_analysis(thesample))
    '''
    print(thesample)
    print(kmeans.labels_)

    print(np.shape(thesample))
    print(np.shape(kmeans.labels_))

    thesample = np.array(thesample).transpose()
    final = np.vstack((thesample, kmeans.labels_)).transpose()
    print(final)
    '''


    #thesecondsample = testing_group_into_matrix(kodiaq_testing_sample())
    #thelists = testing_group_into_lists(octavia_testing_sample())
    #matrix_of_correlations2(thelists)
    #print(thesample[0])
    #for one in thesample:
        #probability_distribution(one)


    #agglomerative_clustering(thesample)
    #X2 = np.array(thesample)
    #X3 = np.array(thesecondsample)
    #X4 = np.array(onethousand)
    #print(X2[3])

    #model = kmeans_clustering(principal_component_analysis(onethousand))
    #predikce = kmeans_predicting(model, principal_component_analysis(all_remaining_data))
    #print(predikce)


    def create_labels_file(labels):
        os.chdir("C:\\Users\\Krystof\\PycharmProjects\\Dipl\\venv")
        with open("k-means_labels.txt", mode="w", encoding="utf-8") as labelsfile:
            for one in list(labels):
                labelsfile.write(str(one))

    #create_labels_file(labels)
    def hnus():
        os.chdir("C:\\Users\\Krystof\\PycharmProjects\\Dipl\\venv")
        with open('k-means_labels.txt', 'r', encoding='utf-8') as labelsfile:
            lf = labelsfile.read()
            print(lf)
            lf = list(lf)
            for idx, label in enumerate(lf):
                if label == '0':
                    lf[idx] = 1
                if label == '1':
                    lf[idx] = 5
                if label == '2':
                    lf[idx] = 3
                if label == '3':
                    lf[idx] = 0
                if label == '4':
                    lf[idx] = 4
                if label == '5':
                    lf[idx] = 2
            print(lf)

    def count_cluster_shares(alldrives):
        matrix = []
        amatrix = []
        bmatrix = []
        cmatrix = []
        dmatrix = []
        ematrix = []
        fmatrix = []
        for jizda in alldrives:
            doc = collectionDrivesResampled.find_one({"_id": jizda})
            length = len(doc["content"]["data"]["mapData"])
            a = 0
            b = 0
            c = 0
            d = 0
            e = 0
            f = 0
            for smpl in doc["content"]["data"]["mapData"]:
                values = [smpl['speed'], smpl['rpm'], smpl['efficiency'], smpl['sideG'], smpl['consumption'], smpl['outputPower'], smpl['fontAcc']]
                if smpl['label'] == 3:
                    a += 1
                    amatrix.append(values)
                if smpl['label'] == 0:
                    b += 1
                    bmatrix.append(values)
                if smpl['label'] == 1:
                    c += 1
                    cmatrix.append(values)
                if smpl['label'] == 2:
                    d += 1
                    dmatrix.append(values)
                if smpl['label'] == 4:
                    e += 1
                    ematrix.append(values)
                if smpl['label'] == 5:
                    f += 1
                    fmatrix.append(values)
            a = a / length
            b = b / length
            c = c / length
            d = d / length
            e = e / length
            f = f / length
            ride = [jizda, a,b,c,d,e,f]

            matrix.append(ride)

        print(np.mean(amatrix, axis=0))
        print(np.mean(bmatrix, axis=0))
        print(np.mean(cmatrix, axis=0))
        print(np.mean(dmatrix, axis=0))
        print(np.mean(ematrix, axis=0))
        print(np.mean(fmatrix, axis=0))
        avgmatrix = np.array(matrix)[:, [1,2,3,4,5,6]]
        print(np.mean(avgmatrix.astype(np.float), axis=0))
        print(np.var(avgmatrix.astype(np.float), axis=0))
        return np.array(matrix)

    def agglhnus():
        result = agglomerative_experiment1(count_cluster_shares())
        np.set_printoptions(suppress=True)
        sortedarr = result[numpy.argsort(result[:, 7])]
        sortedarr=(sortedarr.tolist())
        for row in sortedarr:
            row[0] = int(row[0])
            print(row)

    #returnmatrix, labels = agglomerative_experiment1(count_cluster_shares(octavie110))
    #print(returnmatrix.shape)
    def ride_labels_to_db(returnmatrix, labels):
        howmany = 0
        ids = []
        classes = []
        for idx, row in enumerate(octavie110):
            collectionDrivesResampled.update_one({"_id": row}, {"$set": {"content.data.label": int(labels[idx])}})
            doc = collectionDrivesResampled.find_one({"_id": row})
            if float(sum(d['speed'] for d in doc["content"]["data"]["mapData"])) / len(doc["content"]["data"]["mapData"]) >= 60:
                howmany += 1
                #returnmatrix = np.delete(returnmatrix, idx, 0)
                ids.append([doc['_id'], returnmatrix[idx][7]])
                classes.append(returnmatrix[idx])

        print(howmany)

        ids = sorted(ids, key=lambda x: x[1])

    '''
    alldocs = collectionDrivesResampled.find({"content.data.label": 3})
    for doc in alldocs:
        if float(sum(d['speed'] for d in doc["content"]["data"]["mapData"])) / len(doc["content"]["data"]["mapData"]) >= 60:
            #universal_visualization_colored(doc, ["speed", 'time'])
            universal_2subplots_visualization_colored(doc, doc, ["speed", 'time'], ["rpm", 'time'])
            break
        
    first = []
    second = []
    third = []
    fourth = []

    for one in ids:
        if one[1] == 0.0:
            first.append(one)
        if one[1] == 1.0:
            second.append(one)
        if one[1] == 2.0:
            third.append(one)
        if one[1] == 3.0:
            fourth.append(one)

    selected1 = random.sample(first, 1)
    selected2 = random.sample(second, 1)
    selected3 = random.sample(third, 1)
    selected4 = random.sample(fourth, 1)

    exdrive = collectionDrivesResampled.find_one({'_id':selected1[0][0]})
    universal_visualization(exdrive, ["speed", 'time'])
    exdrive = collectionDrivesResampled.find_one({'_id': selected2[0][0]})
    universal_visualization(exdrive, ["speed", 'time'])
    exdrive = collectionDrivesResampled.find_one({'_id': selected3[0][0]})
    universal_visualization(exdrive, ["speed", 'time'])
    exdrive = collectionDrivesResampled.find_one({'_id': selected4[0][0]})
    universal_visualization(exdrive, ["speed", 'time'])
    '''


    #X2 = np.array(thesample)
    #X2 = np.array(onethousand)
    #X = np.stack((thelists[0], thelists[1], thelists[2], thelists[3], thelists[4], thelists[5], thelists[6]), axis=0)
    #principal_component_analysis(X2)
    #labels = principal_component_analysis(X2)
    #principal_component_analysis(X3)
    #kmeans_clustering(principal_component_analysis(X2))
    #kmeans_clustering(principal_component_analysis(X3))
    #optics_clustering(principal_component_analysis(X2))
    #X2 = np.array(X2)
    #X2 = np.transpose(X2)
    #labels = np.expand_dims(labels, axis=0)
    #print(X2)
    #print(X2.shape)
    #print(labels)
    #print(labels.shape)
    #X2 = np.transpose(X2)

    #print(np.shape(all_remaining_data))
    #print(np.shape(predikce))
    #X4 = np.transpose(X4)
    #X4 = np.vstack((X4, np.transpose(model.labels_)))
    #print(X2)
    #agglomerative_experiment1(principal_component_analysis(X2))
    #dbscan(principal_component_analysis(X3))
    #optics_clustering(principal_component_analysis(X3))
    #print(X[0:3])

    def labels_to_db(ids, labels):
        labelid = 0
        for id in ids:
            drive = collectionDrivesResampled.find_one({"_id": id})
            for sample in drive['content']['data']['mapData']:
                sample['label'] = int(labels[labelid])
                labelid += 1

            collectionDrivesResampled.update_one({"_id": id}, {"$set": {"content.data.mapData": drive["content"]["data"]["mapData"]}})

    #labels_to_db(trainingDataIds, model.labels_)
    #labels_to_db(allremaining, predikce)
    #labels_to_db(octavia_testing_sample(), kmeans.labels_)

    def plot_colored_octavia_rides():
        for ide in octavia_testing_sample():
            doc = collectionDrivesResampled.find_one({"_id": ide})
            if float(sum(d['speed'] for d in doc["content"]["data"]["mapData"])) / len(doc["content"]["data"]["mapData"]) >= 60:
                universal_2subplots_visualization_colored(doc, doc, ["speed", 'time'], ["rpm", 'time'])
        print("done")

    def print_cluster_attributes(X):
        X = np.transpose(X)
        sorted_array = X[numpy.argsort(X[:, 7])]
        clusters = [[], [], [], [], [], [], [], []]
        for idx, one in enumerate(sorted_array):
            if one[7] == 0:
                clusters[0].append(list(one))
            if one[7] == 1:
                clusters[1].append(list(one))
            if one[7] == 2:
                clusters[2].append(list(one))
            if one[7] == 3:
                clusters[3].append(list(one))
            if one[7] == 4:
                clusters[4].append(list(one))
            if one[7] == 5:
                clusters[5].append(list(one))
            if one[7] == 6:
                clusters[6].append(list(one))
            if one[7] == 7:
                clusters[7].append(list(one))

        #print(clusters)

        for cluster in clusters:
            cluster = np.array(cluster)
            print(np.mean(cluster, axis=0))
            print(np.var(cluster, axis=0))
            print(len(cluster))

        colors = ['lightblue', 'purple', 'yellow', 'red', 'green']#, 'orange'
        labels = ['A', 'B', 'C', 'D', 'E']#, 'F'
        for cluster, color, label in zip(clusters, colors, labels):
            centroid = np.mean(cluster, axis=0)
            cluster = np.transpose(cluster)
            plt.scatter(cluster[0, :], cluster[1, :], marker='o', color=color, label='Cluster '+label, alpha=0.1)
            plt.plot(centroid[0], centroid[1], fillstyle='full', marker='o', markeredgecolor='black', markeredgewidth=2.0, markerfacecolor=color, markersize=10.0)
        leg = plt.legend()
        for lh in leg.legendHandles:
            lh.set_alpha(1)
        plt.xlabel('Speed')
        plt.ylabel('Rpm')
        plt.show()

        for cluster, color, label in zip(clusters, colors, labels):
            centroid = np.mean(cluster, axis=0)
            cluster = np.transpose(cluster)
            plt.scatter(cluster[6, :], cluster[0, :], marker='o', color=color, label='Cluster ' + label, alpha=0.1)
            plt.plot(centroid[6], centroid[0], fillstyle='full', marker='o', markeredgecolor='black',
                     markeredgewidth=2.0, markerfacecolor=color, markersize=10.0)
        leg = plt.legend()
        for lh in leg.legendHandles:
            lh.set_alpha(1)
        plt.xlabel('Speed')
        plt.ylabel('Acceleration')
        plt.show()

        for cluster, color, label in zip(clusters, colors, labels):
            centroid = np.mean(cluster, axis=0)
            cluster = np.transpose(cluster)
            plt.scatter(cluster[1, :], cluster[2, :], marker='o', color=color, label='Cluster ' + label, alpha=0.1)
            plt.plot(centroid[1], centroid[2], fillstyle='full', marker='o', markeredgecolor='black', markeredgewidth=2.0, markerfacecolor=color, markersize=10.0)
        leg = plt.legend()
        for lh in leg.legendHandles:
            lh.set_alpha(1)
        plt.xlabel('Rpm')
        plt.ylabel('Consumption')
        plt.show()

        for cluster, color, label in zip(clusters, colors, labels):
            centroid = np.mean(cluster, axis=0)
            cluster = np.transpose(cluster)
            plt.scatter(cluster[0, :], cluster[2, :], marker='o', color=color, label='Cluster ' + label, alpha=0.1)
            plt.plot(centroid[0], centroid[2], fillstyle='full', marker='o', markeredgecolor='black',
                     markeredgewidth=2.0, markerfacecolor=color, markersize=10.0)
        leg = plt.legend()
        for lh in leg.legendHandles:
            lh.set_alpha(1)
        plt.xlabel('Speed')
        plt.ylabel('Consumption')
        plt.show()

        for cluster, color, label in zip(clusters, colors, labels):
            centroid = np.mean(cluster, axis=0)
            cluster = np.transpose(cluster)
            plt.scatter(cluster[1, :], cluster[6, :], marker='o', color=color, label='Cluster ' + label, alpha=0.1)
            plt.plot(centroid[1], centroid[6], fillstyle='full', marker='o', markeredgecolor='black',
                     markeredgewidth=2.0, markerfacecolor=color, markersize=10.0)
        leg = plt.legend()
        for lh in leg.legendHandles:
            lh.set_alpha(1)
        plt.xlabel('Rpm')
        plt.ylabel('FrontAcc')
        plt.show()

    #print_cluster_attributes(np.transpose(final))
    plot_colored_octavia_rides()

    '''
    plt.plot(thelists[0],thelists[1],'.')
    plt.show()
    plt.plot(thelists[2], thelists[6], '.')
    plt.show()
    
    numpy.set_printoptions(suppress=True, precision=2)
    C = np.cov(X)
    eva, eve = np.linalg.eig(C)
    print(C)
    print(eva)
    print(eve)
    Ext = np.matrix.transpose(eve)
    Ncm = np.dot(np.dot(Ext, C), eve)
    print(Ncm)
    origin = [0, 0]
    eig_vec0 = eve[:, 0]
    eig_vec1 = eve[:, 1]

    eig_vec2 = eve[:, 2]
    eig_vec4 = eve[:, 4]
    eig_vec6 = eve[:, 6]

    #plt.plot(thelists[0], thelists[1], ".")
    plt.quiver(*origin, *eig_vec0, color=['r'], scale=0.1)
    plt.quiver(*origin, *eig_vec1, color=['b'], scale=0.1)
    plt.show()
    '''

    '''

    print(ids.sort(key=lambda x: x[2]))
    print(ids)
    #identifikator, pocet vzorku, prumerna spotreba, prumerna efektivita
    print(len(ids))

    doc = collectionDrivesDivided.find_one({"_id": "9223370505255134559"})
    universal_visualization(doc, ["speed", "time"])
    universal_visualization(doc, ["fontAcc", "time"])
    '''

    def eliminate_extremes_old():
        odlehle = collectionDrivesDivided.find({})
        invalid = [0,0,0,0,0,0,0]
        sample_count = 0

        for idx, on in enumerate(odlehle):
            on = unify_side_g(on)
            maxfontacc = 0
            minfontacc = 0

            maxsideG = 0
            minsideG = 0

            maxconsumption = 0

            #delete samples when car is standing at the beginning of the ride
            n = 0
            while on["content"]["data"]["mapData"][n]["consumption"] == "null" and\
                    3 > on["content"]["data"]["mapData"][n]["speed"] >= 0:
                del on["content"]["data"]["mapData"][n]
                n += 1

            m = len(on["content"]["data"]["mapData"]) - 1
            while on["content"]["data"]["mapData"][m]["consumption"] == "null" and \
                    3 > on["content"]["data"]["mapData"][m]["speed"] >= 0:
                del on["content"]["data"]["mapData"][m]
                m -= 1

            for sample in on["content"]["data"]["mapData"]:

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
        
                    
                        
                        
            #print(maxconsumption)
            #print(maxfontacc)
            #print(minfontacc)


            for sample in on["content"]["data"]["mapData"]:
                sample_count += 1

                if isinstance(sample["consumption"], (float, int)):
                        if 0.0 > sample["consumption"]:
                            sample["consumption"] = 0
                            invalid[0] += 1
                        elif sample["consumption"] > 100.0:
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
                        if 1.7 < sample["sideG"] or sample["sideG"] < -1.7:
                            sample["sideG"] = "null"
                            invalid[3] += 1
                            #print(on["_id"])
                if isinstance(sample["rpm"], (float, int)):
                        if 10000 < sample["rpm"] or sample["rpm"] < 0:
                            sample["rpm"] = "null"
                            invalid[4] += 1
                if isinstance(sample["outputPower"], (float, int)):
                        if 250 < sample["outputPower"] or sample["outputPower"] < 0:
                            sample["outputPower"] = "null"
                            invalid[5] += 1

            #collectionDrivesDivided.update_one({"_id": on["_id"]}, {"$set": {"content.data.mapData": on["content"]["data"]["mapData"]}})
            #print(idx)
        print(invalid)
        print(sample_count)


    def count_null_values(document):
        invalid = [0, 0, 0, 0, 0, 0, 0]
        invalid_samples = 0
        sample_count = 0

        for sample in document["content"]["data"]["mapData"]:
            sample_count += 1

            if sample["consumption"] == "null" or sample["efficiency"] == "null" or sample["fontAcc"] == "null"\
                    or sample["sideG"] == "null" or sample["outputPower"] == "null" or sample["rpm"] == "null":
                invalid_samples += 1


            if sample["consumption"] == "null":
                invalid[0] += 1
            if sample["efficiency"] == "null":
                invalid[1] += 1
            if sample["fontAcc"] == "null":
                invalid[2] += 1
            if sample["sideG"] == "null":
                invalid[3] += 1
            if sample["outputPower"] == "null":
                invalid[4] += 1
            if sample["rpm"] == "null":
                invalid[5] += 1

        print(invalid)
        print(invalid_samples)
        print(sample_count)



    def funkce():
        odlehle = collectionDrivesDivided.find({})
        invalid = [0, 0, 0, 0, 0, 0, 0]
        sample_count = 0

        for idx, on in enumerate(odlehle):

            for sample in on["content"]["data"]["mapData"]:
                sample_count += 1

                if sample["speed"] == "null" and sample["rpm"] == "null" and sample["efficiency"] == "null" and \
                        sample["sideG"] == "null" and sample["outputPower"] == "null" and sample["outputPower"] == "null":
                    del sample
            #collectionDrivesDivided.update_one({"_id": on["_id"]},
                                               #{"$set": {"content.data.mapData": on["content"]["data"]["mapData"]}})


    def all_prep_functions():
        all = collectionDrives.find({})
        collectionDrivesDivided.delete_many({})
        collectionDrivesResampled.delete_many({})
        for one in all:
            one = remove_all_nulls(handle_consumption_nulls(eliminate_extremes(handle_nulls_in_motion(unify_side_g(delete_begin_end(one))))))
            remove_gaps(one)

        divided = collectionDrivesDivided.find({})
        for one in divided:
            one = resampling(remove_all_nulls(delete_begin_end(one)))
            collectionDrivesResampled.insert_one(one)

        tut = collectionDrivesResampled.find({})

        for one in tut:
            smoothed = smooth_negative_values(one)
            collectionDrivesResampled.update_one({"_id": smoothed["_id"]},
                                        {"$set": {"content.data.mapData": smoothed["content"]["data"]["mapData"]}})

        sectut = collectionDrivesResampled.find({})
        invalid_samples = [0, 0, 0, 0, 0, 0]
        for one in sectut:
            invalid = count_extremes(one)
            if invalid[0] > 3:
                print(one["_id"])
            for idx, on in enumerate(invalid):
                invalid_samples[idx] += on
        print(invalid_samples)

    '''9223371476340612604
    9223371476340618597
    9223371476340620429
    9223371476340621614
    9223376476340630871
    9223374476340635534
    9223371476340640610
    9223371476340644885'''

    "9223370470471681625"
    '''
    allres = collectionDrivesResampled.find({})
    for doc in allres:
        doc = smooth_negative_values(doc)
        collectionDrivesResampled.update_one({"_id": doc["_id"]},
                                    {"$set": {"content.data.mapData": doc["content"]["data"]["mapData"]}})
    '''
    "9223370470471682174"
    rideid = "9223371498821004586"
    # pup2 = collectionDrivesResampled.find_one({"_id": "9223370470471682174"})
    # pup2 = remove_all_nulls(handle_consumption_nulls(eliminate_extremes(handle_nulls_in_motion(unify_side_g(delete_begin_end(pup2))))))
    pup1 = collectionDrivesDivided.find_one({"_id": rideid})


        #collectionDrivesResampled.delete_many({"content.data.mapData.0": {"$exists": "true"}})
        #collectionDrivesDivided.delete_many({"$where": "this.content.data.mapData.length < 100"})
        #radici skript
        #collectionDrives.delete_many({"content.data.mapData": { "$exists": "true", "$size": 0}})


    #visualize_all_1plot(rideid)

    #"9223370470484619488"

    '''
    k = group_samples_together(nebobik)
    print(k)
    for one in k[1:5]:
        probability_distribution(sorted(one))

    for one in k[7:-1]:
        probability_distribution(sorted(one))


    
    # OPTICS Clustering

    array = dict_into_lists(nebobik)
    X = np.array(array)

    X = StandardScaler().fit_transform(X)

    clust = DBSCAN(algorithm='kd_tree', eps=0.3, min_samples=80, metric='euclidean').fit(X)
    core_samples_mask = np.zeros_like(clust.labels_, dtype=bool)
    core_samples_mask[clust.core_sample_indices_] = True
    labels = clust.labels_

    unique_labels = set(labels)


    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    for k, col in zip(unique_labels, colors):
        if k == -1:
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)
        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)
        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

    plt.plot(X[clust.labels_ == -1, 0], X[clust.labels_ == -1, 1], 'k+', alpha=0.1)

    plt.title("DBSCAN Clustering, Speed/Rpm")
    plt.show()


    X = np.array(array)
    X = np.transpose(X)

    kmeans = KMeans(n_clusters=3, random_state=0, max_iter=100).fit(X)
    y_menas = kmeans.predict(X)
    centroids = kmeans.cluster_centers_

    plt.scatter(X[:, 0], X[:, 1], c=y_menas, s=20, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=150, alpha=0.5)
    plt.show()
    plt.scatter(X[:, 1], X[:, 2], c=y_menas, s=20, cmap='viridis')
    plt.scatter(centroids[:, 1], centroids[:, 2], c='black', s=150, alpha=0.5)
    plt.show()



    #collectionDrives.update_one({"_id": "9223370470484619488"}, {"$set": {"content.data.mapData": newbobik["content"]["data"]["mapData"]}})
    
    again = collectionDrives.find_one({"_id": "9223370470484619488"})
    for samp in again["content"]["data"]["mapData"]:
        fa = samp["frontAcc"]
        del samp["frontAcc"]
        samp["fontAcc"] = fa
    print(again)

    elex = eliminate_extremes(resampling(again))
    universal_visualization(elex, ["consumption","time"])
    
    alldocs = collectionDrives.find()
    for one in alldocs:
        print(one)
        one = handle_consumption_nulls(handle_4nulls_in_motion(unify_side_g(delete_begin_end(one))))
        print(one)

    kik = collectionDrives.find_one({"_id": "9223370470484619488"})
    print(delete_begin_end(kik))
    print(len(delete_begin_end(kik)["content"]["data"]["mapData"]))

    
    print(collectionDrivesDivided.count_documents({"content.data.mapData.speed": "null"}))
    print(collectionDrivesDivided.count_documents({"$or": [{"content.data.mapData.fontAcc": "null"}, {"content.data.mapData.efficiency": "null"}, {"content.data.mapData.rpm": "null"}, {"content.data.mapData.outputPower": "null"}, {"content.data.mapData.sideG": "null"}, {"content.data.mapData.speed": "null"}]}))
    
    print(collectionDrivesDivided.count_documents({"$and": [{"content.data.mapData.fontAcc": "null"},
                                                           {"content.data.mapData.efficiency": "null"},
                                                           {"content.data.mapData.rpm": "null"},
                                                           {"content.data.mapData.outputPower": "null"},
                                                           {"content.data.mapData.sideG": "null"},
                                                           {"content.data.mapData.speed": "null"}]}))
    '''


    #collectionDrives.update_one({"_id": dockie["_id"]}, {"$set": {"content.data.mapData": new["content"]["data"]["mapData"]}})


    '''
    {"$and": [{"content.data.mapData.consumption": "null"},
              {"content.data.mapData.rpm": "null"},
              {"content.data.mapData.outputPower": "null"},
              {"content.data.mapData.speed": "null"}]}'''
    #print(collectionDrivesDivided.count_documents({"content.data.mapData.sideG": "null", "content.data.mapData.efficiency": "null"}))
    #print(collectionDrivesDivided.count_documents(
        #{"content.data.mapData.sideG": "null", "content.data.mapData.efficiency": "null", "content.data.mapData.fontAcc": "null", "content.data.mapData.outputPower": "null", "content.data.mapData.rpm": "null"}))



    # collectionDrivesDivided.update_one({"_id": on["_id"]},{"$set":{"content.data.mapData": on["content"]["data"]["mapData"]}})

    #print(collectionDrivesDivided.count_documents({"content.data.mapData.consumption": {"$gte": 100}}))
    #eliminuj_odlehle()

    '''
    pole = ["null", "null","null","null","null", 2, 5, 6, "null","null"]
    n = 0
    while pole[n] == "null":
        print(n)
        n += 1
    else:
        print("no longer null")

    
    
    seen = []
    unique = []
    duplicates = []
    docu = collectionDrivesDivided.find_one({"_id":"9223375473811364226"})
    for index, one in enumerate(docu["content"]["data"]["mapData"]):
        if one not in seen:
            unique.append(index)
            seen.append(index)
        elif one in seen:
            duplicates.append(index)
    print(duplicates)

    
        for idx, sample in enumerate(document["content"]["data"]["mapData"]):
            if sample["consumption"] == "null" and sample["efficiency"] == "null" and sample["rpm"] == "null" and sample["speed"] == "null" and sample["outputPower"] == "null":
                del document["content"]["data"]["mapData"][idx]
        collectionDrives.update_one({"_id": document["_id"]}, {"$set": {"content.data.mapData": document["content"]["data"]["mapData"]}})
        #print(document)

    docs = collectionDrives.find({})
    for doc in docs:
        remove_gaps(doc)
    '''
    #count_gaps()


    ''' 
        if weak_variables == 2 and output_field[3] == 1 and output_field[6] == 1:
            pocetbezpolohy += 1

        if weak_variables == 1 and output_field[1] == 1:
            bezspotreby += 1
        
        if weak_variables == 0:
            matice[0] += 1
        if weak_variables == 1:
            matice[1] += 1
        if weak_variables == 2:
            matice[2] += 1
        if weak_variables == 3:
            matice[3] += 1
        if weak_variables == 4:
            matice[4] += 1
        if weak_variables == 5:
            matice[5] += 1
        if weak_variables == 6:
            matice[6] += 1
        if weak_variables == 7:
            matice[7] += 1
        if weak_variables == 8:
            matice[8] += 1
        if weak_variables == 9:
            matice[9] += 1
        if weak_variables == 10:
            matice[10] += 1
        if weak_variables == 11:
            matice[11] += 1
        if weak_variables == 12:
            matice[12] += 1
    
    print("validni dokumenty")
    print(matice)
    print("pocetbezpolohy" + str(pocetbezpolohy))
    print("bezspotreby" + str(bezspotreby))
    

    collectionDrivesDivided.remove({})
    documents = collectionDrives.find({})
    citac = 0
    for document in documents:
        remove_gaps(document)
        citac += 1
    print("done")
    print(citac)
    '''
    #count_gaps()

    '''
    pocetdoc = 0
    neco = collectionDrivesDivided.find(
        {"content.data.mapData":{"$exists": "true"}, "$where":"this.content.data.mapData.length<500"})
    for one in neco:
        pocetdoc += 1

    pocetdoc2 = 0
    neco = collectionDrivesDivided.find(
        {"content.data.mapData": {"$exists": "true"}, "$where": "this.content.data.mapData.length<200"})
    for one in neco:
        pocetdoc2 += 1

    pocetdoc3 = 0
    neco = collectionDrivesDivided.find(
        {"content.data.mapData": {"$exists": "true"}, "$where": "this.content.data.mapData.length>1000"})
    for one in neco:
        pocetdoc3 += 1

    print("Do 500:" + str(pocetdoc))
    print("Do 200:" + str(pocetdoc2))
    print("Nad 1000:" + str(pocetdoc3))
    '''

    HE = [9223370470473209210, 9223370478680501677, 9223370470475539172, 9223370472087780809, 9223370471240799735,
          9223370475493493310, 9223370476098812480, 9223370478379205761, 9223370489183073276, 9223370470493191549,
          9223370476077720992]
    LE = [9223370490872344260, 9223370476700887180, 9223370473640547545, 9223370473496558129,
          9223370472766308139, 9223370477602207538, 9223370475405324541, 9223370470730278240, 9223370473832637302,
          9223370477611018109]
    RE = [9223370505255134559,9223370525044951675]

    def inverse_proportionality(HE):
        for ride in HE:
            doc = collectionDrivesResampled.find_one({"_id": str(ride)})
            length = len(doc["content"]["data"]["mapData"])
            speed = []
            frequencies = []
            time = []
            for idx, one in enumerate(doc["content"]["data"]["mapData"]):
                speed.append(one["speed"])
                time.append(one["time"])


                if (length - idx) != 1:
                    # print(samp["time"])
                    diff = abs(one["time"] - doc["content"]["data"]["mapData"][idx + 1]["time"])
                    frequencies.append(diff)

                elif (length - idx) == 1:
                    break

            frequencies.append(0)

            plt.subplot(2, 1, 1)
            plt.plot(time, speed, '.-')
            # plt.plot(time, maxspeed)
            plt.title("Speed and gaps plots " + str(doc["_id"]))
            plt.ylabel("Speed")
            plt.xlabel("Time")

            plt.subplot(2, 1, 2)
            plt.plot(time, frequencies, '.-')
            plt.legend("Time/Speed")
            plt.ylabel("Gaps between samples")
            plt.xlabel("Time")

            plt.show()

            #from scipy.stats.stats import pearsonr
            #print(pearsonr(speed, frequencies))

    #inverse_proportionality(RE)



    def make_new_collection():

        doc = collectionDrives.find({})

        for file in doc:
            collectionDrivesResampled.insert_one(resampling(file))

        #plt.subplot(new_time, new_speed)
        #plt.show()
        '''
        plt.subplot(2, 1, 1)
        plt.plot(new_time, new_outputPower, '.-')
        # plt.plot(time, maxspeed)
        plt.title("Speed and rounds plots")
        plt.ylabel("Speed")
        plt.xlabel("Time")

        plt.subplot(2, 1, 2)
        plt.plot(new_time, new_rightG, '.-')
        plt.legend("Time/Speed")
        plt.ylabel("Round per minute")
        plt.xlabel("Time")

        plt.show()
        '''

    '''
        for i in range(0, 6):
            x_points.append(times[int(idx + i)])
            y_points.append(times[int(idx + i)])
        print(x_points)
        print(y_points)
    '''

    '''
    print(speeds[0], speeds[1], speeds[2], speeds[3])
    print([times[0], times[1], times[2], times[3]])
    print(interpolate([math.ceil(times[0]), math.ceil(times[0]+2), math.ceil(times[0]+4), math.ceil(times[0]+6)]))
    print([math.ceil(times[0]), math.ceil(times[0] + 2), math.ceil(times[0] + 4), math.ceil(times[0] + 6)])

    plt.plot([times[0], times[1], times[2], times[3], times[4], times[5]], [speeds[0], speeds[1], speeds[2], speeds[3], speeds[4], speeds[5]], ".-")
    plt.plot([math.ceil(times[0]), math.ceil(times[0]+2), math.ceil(times[0]+4), math.ceil(times[0]+6), math.ceil(times[0]+8), math.ceil(times[0]+10), math.ceil(times[0]+12), math.ceil(times[0]+14), math.ceil(times[0]+16), math.ceil(times[0]+18)], interpolate[math.ceil(times[0]), math.ceil(times[0]+2), math.ceil(times[0]+4), math.ceil(times[0]+6), math.ceil(times[0]+8), math.ceil(times[0]+10), math.ceil(times[0]+12), math.ceil(times[0]+14), math.ceil(times[0]+16), math.ceil(times[0]+18)], ".-")
    plt.show()
    '''
    def compute_efficiencies():
        colours = []
        all = collectionDrives.find({})
        for one in all:
            delka = len(one["content"]["data"]["mapData"])
            red = 0
            green = 0
            yellow = 0
            for smpl in one["content"]["data"]["mapData"]:
                # if smpl["efficiency"] < 20:
                if smpl["efficiency"] == "null":
                    smpl["class"] = "null"
                elif "efficiency" not in smpl:
                    smpl["class"] = "red"
                else:

                    if smpl["efficiency"] < 60.0:
                        smpl["class"] = "red"
                        red += 1
                    elif 90 > smpl["efficiency"] >= 60.0:
                        smpl["class"] = "yellow"
                        yellow += 1
                    elif smpl["efficiency"] >= 80.0:
                        smpl["class"] = "green"
                        green += 1

            sub = []
            sub.append(one["_id"])
            sub.append(green/delka)
            sub.append(yellow / delka)
            sub.append(red / delka)
            colours.append(sub)
        #print(sorted(colours, key=itemgetter(3)))

    #compute_efficiencies()

    def plot_efficiency_colours(id):
        onedrive = collectionDrives.find_one({"_id": str(id)})
        basic_stats_onedrive(onedrive)
        #plot_whole_drive(onedrive)
        pole = []
        time = []
        speed = []
        rpm = []
        clas = []

        nuly = 0
        for smpl in onedrive["content"]["data"]["mapData"]:
            #if smpl["efficiency"] < 20:
            if smpl["efficiency"] == "null":
                nuly += 1
                smpl["class"] = "null"
            elif "efficiency" not in smpl:
                smpl["class"] = "red"
            else:
                pole.append(smpl["efficiency"])
                if smpl["efficiency"] < 60.0:
                    smpl["class"] = "red"
                    clas.append("red")
                elif 90 > smpl["efficiency"] >= 60.0:
                    smpl["class"] = "yellow"
                    clas.append("yellow")
                elif smpl["efficiency"] >= 80.0:
                    smpl["class"] = "green"
                    clas.append("green")

            time.append(smpl["time"])
            speed.append(smpl["speed"])
            rpm.append(smpl["rpm"])

        #print(onedrive)

        plt.subplot(2, 1, 1)
        for smp in onedrive["content"]["data"]["mapData"]:

            if smp["speed"] == "null":
                smp["rpm"] = 0
            if "class" not in smp:
                smp["class"] = "red"
            elif smp["class"] == "null":
                smp["class"] = "red"

            plt.plot(smp["time"], smp["speed"], '.', markerfacecolor=smp["class"], markeredgecolor=smp["class"])

        plt.title("Speed and rounds plots" + str(onedrive["_id"]))
        plt.ylabel("Speed")
        plt.xlabel("Time")

        plt.subplot(2, 1, 2)
        for smp in onedrive["content"]["data"]["mapData"]:

            if smp["rpm"] == "null":
                smp["rpm"] = 0
            if "class" not in smp:
                smp["class"] = "red"
            elif smp["class"] == "null":
                smp["class"] = "red"

            plt.plot(smp["time"], smp["rpm"], '.', markerfacecolor=smp["class"], markeredgecolor=smp["class"])

        plt.ylabel("Round per minute")
        plt.xlabel("Time")

        plt.show()

        #print(sorted(pole))

    '''
    for iden in HE:
        plot_efficiency_colours(iden)
        jizda = collectionDrives.find_one({"_id": str(iden)})
        vin = jizda["content"]["data"]["vin"]
        auto = collectionSpec.find_one({"content.data.vin": vin})
        try:
            print(auto["content"]["data"]["engineTypePrimary"])
        except TypeError:
            print("Unknown engine")

    for iden in LE:
        plot_efficiency_colours(iden)
        jizda = collectionDrives.find_one({"_id": str(iden)})
        vin = jizda["content"]["data"]["vin"]
        auto = collectionSpec.find_one({"vin": vin})
        print(auto["content"]["data"]["engineTypePrimary"])
    '''

    #for one in vysoke:
        #print(one)
        #plot_whole_drive(one)

    '''
    COUNT SAMPLES IN EACH RIDE
    
    delky = []
    longest = 0
    id = ""
    vzorky = collectionDrives.find({})
    for one in vzorky:
        delka = len(one["content"]["data"]["mapData"])
        delky.append(delka)
        if delka > longest:
            longest = delka
            id = one["_id"]
        else:
            pass

    print(longest)
    print(id)
    
    

    docu = collectionDrives.find_one({"_id": id})
    print(docu["content"]["data"]["avgConsumptionPrimary"])
    vin = docu["content"]["data"]["vin"]
    print(vin)
    auto = collectionSpec.find_one({"content.data.vin": vin})
    print(auto)

    plot_whole_drive(docu)
    #single_dict_to_gpx(docu)

    #print(delky)
    '''
    #print("nad 3000: " + str(collectionDrives.count_documents({"content.data.avgEngineSpeed": {"$gte": 2800}})))
    #neco = collectionDrives.find_one({"content.data.avgEngineSpeed": {"$gte": 2800}})
    #basic_stats_onedrive(neco)
    #plot_whole_drive(neco)
    #plot_speed_against_rounds(neco)



    #print("nad 3000: " + str(collectionDrives.count_documents({"content.data.avgConsumptionPrimary": {"$lte": 3.0}})))
    #nic = collectionDrives.find({"content.data.avgConsumptionPrimary": {"$lte": 4.0}})
    #for ni in nic:
        #basic_stats_onedrive(ni)
        #plot_speed_against_rounds(ni)



    #d = collectionDrives.find_one({"_id": "9223370494130435005"})
    #print(d)
    #basic_stats_onedrive(d)
    '''
    speed = []
    rpm = []
    consumption = []
    for ni in nic:

        for sam in ni["content"]["data"]["mapData"]:
            if sam["speed"] != "null" and sam["rpm"] != "null" and sam['consumption'] != "null":
                speed.append(sam["speed"])
                rpm.append(sam["rpm"])
                consumption.append(sam['consumption'])


    print(len(speed))
    print(len(rpm))

    X = np.array((speed, rpm))
    X = np.transpose(X)

    X = StandardScaler().fit_transform(X)

    clust = DBSCAN(algorithm='kd_tree', eps=0.3, min_samples=80, metric='euclidean').fit(X)
    core_samples_mask = np.zeros_like(clust.labels_, dtype=bool)
    core_samples_mask[clust.core_sample_indices_] = True
    labels = clust.labels_

    unique_labels = set(labels)

    #OPTICS Clustering
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    for k, col in zip(unique_labels, colors):
        if k == -1:
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)
        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)
        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

    plt.plot(X[clust.labels_ == -1, 0], X[clust.labels_ == -1, 1], 'k+', alpha=0.1)


    plt.title("DBSCAN Clustering, Speed/Rpm")
    plt.show()


    ''''''K-MEANS ALGORITHM''''''

    X = np.array((speed, rpm, consumption))
    X = np.transpose(X)

    kmeans = KMeans(n_clusters=3, random_state=0, max_iter=100).fit(X)
    y_menas = kmeans.predict(X)
    centroids = kmeans.cluster_centers_

    plt.scatter(X[:, 0], X[:, 1], c=y_menas, s=20, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=150, alpha=0.5)
    plt.show()
    plt.scatter(X[:, 1], X[:, 2], c=y_menas, s=20, cmap='viridis')
    plt.scatter(centroids[:, 1], centroids[:, 2], c='black', s=150, alpha=0.5)
    plt.show()
    '''


    #Decission Tree Algo
    '''

    Y = [0,1,2]

    for pairid, pair in enumerate([0, 1], [0, 2], [1, 2], [0, 2]):
        X = X[:, pair]
        y = 
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    tree.plot_tree(clf.fit(X, Y))
    '''

    '''
    doc = collectionDrives.find({"content.data.avgEngineSpeed": {"$gte": 2500}})
    limit = 0
    for one in doc:
        if limit < 5:
            basic_stats_onedrive(one)
            plot_whole_drive(one)
            single_dict_to_gpx(one)
        else:
            break
    '''

    "LEAST SQUARES METHOD"
    '''
    leastsqrs = collectionDrives.find_one({"_id":"9223370470791563925"})

    times = []
    rounds = []

    for sample in leastsqrs["content"]["data"]["mapData"]:
        times.append(sample["time"])
        rounds.append(sample["rpm"])


    timeaxis = numpy.array(times)
    roundaxis = numpy.array(rounds)

    def func(x, a, b):
        return a*numpy.sin(b*numpy.pi*x)

    def residual(p, x, y):
        return y - func(x, *p)

    p0 = [20000., 80000.]

    #print(optimize.curve_fit(func, timeaxis, roundaxis))

    popt, pcov = optimize.curve_fit(func, timeaxis, roundaxis)
        #optimize.leastsq(residual, p0, args=(timeaxis, roundaxis))
        #numpy.polyfit(timeaxis, roundaxis, 5)
    print(popt)

    #yn = func(timeaxis, *popt)
    plt.plot(timeaxis, roundaxis)
    plt.plot(timeaxis, func(timeaxis, *popt))
    plt.show()
    '''

    '''LEAST SQUARES WITH NUMPY POLYFIT'''
    '''
    x_axis = numpy.array([1, 2, 3, 4, 5, 6])
    y_axis = numpy.array([4,6,2,3,6,7])

    z = numpy.polyfit(x_axis, y_axis, 3)

    '''



    '''
    longest ride with somewhat stable frequency and almost pure highway is: 9223370529404007235
    stable speed, stable rounds per minute, consumption: 5.1, economic drive
    
    '''



    '''
    LOOP THAT CHECKS SAMPLING FREQUENCY
    
    freq = collectionDrives.find({})
    averages = []
    variances = []
    for doc in freq:
        differences = []
        length = len(doc["content"]["data"]["mapData"])

        for idx, samp in enumerate(doc["content"]["data"]["mapData"]):
            if (length - idx) != 1:
                #print(samp["time"])
                diff = abs(samp["time"] - doc["content"]["data"]["mapData"][idx + 1]["time"])
                differences.append(diff)

            elif (length - idx) == 1:
                pass

        average = mean(differences)
        averages.append(average)
        rozptyl = variance(differences, average)
        variances.append(rozptyl)

        if average < 5.0 and rozptyl < 5.0:
            continue
        else:
            collectionDrives.delete_one(doc)

        #print(average)

    podpet = 0
    nadpet = 0

    for avr, vari in zip(averages, variances):
        if avr < 5.0 and vari < 5.0:
            nadpet += 1
        else:
            podpet += 1

    np = 0
    pp = 0
    for avr in averages:
        if avr > 10.0:
            np += 1
        else:
            pp += 1

    print("Averages above 10 and Variance above 10: "+str(nadpet))
    print("Averages below 10 and Variance below 10: "+str(podpet))

    print(str(np))
    print(str(pp))
    

    print("Averages in sample freq: "+str(averages))
    print("Variances from average:"+str(variances))
    '''



    #LOOP THAT REMOVED ALL DOCUMENTS WITH LESS THAN 100 SAMPLES

    def remove_less_than_hundred():
        for document in collectionDrives.find({}):
            if len(document["content"]["data"]["mapData"]) < 100:
                collectionDrives.delete_one(document)



      
    #LOOP THAT REMOVES ALL DOCUMENTS WITH LESS THAN 98% OF VALID SAMPLES
    def find_valid_samples():
        suitable_document = 0
        pocet_smazanych = 0
                                              
        for document in collectionDrives.find({"content.data.mapData.100": {"$exists": "true"}}):
            dict(document)
            length = len(document["content"]["data"]["mapData"])
            valid = 0
            for sample in document["content"]["data"]["mapData"]:
                if sample["speed"] != "null" and sample["rpm"] != "null" and sample["time"] != "null" and \
                        sample["latitude"] != "null" and sample["longitude"] != "null" and sample["consumption"]\
                        and sample["efficiency"]:
                    valid += 1
                else:
                    pass
            if valid/length >= 0.90:
                suitable_document += 1
            else:
                collectionDrives.delete_one(document)
                pocet_smazanych += 1
                pass

        print("Pocet dokumentu s 90% validnimi vzorky: "+str(suitable_document))
        print(pocet_smazanych)




    #print(len(list(collectionDrives.find({}, {"content.data.mapData.3000": {"$exists": "true"}}))))
    #longer_than_500 = len(list(longer_than_500))
    #print(longer_than_500)

    #longest = collectionDrives.find_one({"content.data.mapData.5000": {"$exists": "true"}})
    #for one in longest["content"]["data"]["mapData"]:
    #print(longest)
    '''
    for dobytek_silnicni in samples:
        dobytek = collectionDrives.find_one({"_id": dobytek_silnicni["_id"]})
        auto = collectionSpec.find_one({"content.data.vin": dobytek_silnicni["content"]["data"]["vin"]})
        plot_whole_drive(dobytek)
        print(dobytek["_id"]+"   "+ str(dobytek["content"]["data"]["avgConsumptionPrimary"]))
        print(auto)
        spotreby = []
        #for s in dobytek_silnicni["content"]["data"]["mapData"]:
            #spotreby.append(s["consumption"])
        print(spotreby)
        #os.chdir("C:\\Users\\Krystof\\Desktop\\Diplomka\\Testovací jízda")
        #single_dict_to_gpx(dobytek)

    '''
    def open_file():
        with open("C:/Users/Krystof/addonitem1", mode="r", buffering=1, encoding="utf-8-sig") as file:
            limit = 10
            adjustable = 0
            added = 0
            invalid = 0
            tenthousand = 36000
            for idx, line in enumerate(file):
                if idx > tenthousand:
                    line = json.loads(line)
                    if line["addonId"] == "cz.eman.android.oneapp.lib.addon.drives":
                        #if line["itemId"] == "9223370475405324541":
                            print(idx)

                            prepare_json(line)
                            print(line)
                            #print(line)
                            #plot_whole_drive(line)
                            #result_file, boolean = delete_frequency_gaps(line)
                            #if boolean is True:
                                #plot_whole_drive(result_file)
                                #print("File changed")
                                #adjustable += 1
                            try:
                                print(line)
                                collectionDrives.insert_one(line)
                                added += 1
                                print(added)
                            except pymongo.errors.DuplicateKeyError:
                                pass
                            except pymongo.errors.InvalidDocument:
                                pass
                            #else:
                                #pass
                                #print("File has no gap or more than one gaps")

                            #break

                        #else:
                            #continue
                    else:
                        continue

                else:
                    continue
            print(adjustable)
            print(added)
            print(invalid)

    #print(collectionDrives.find_one({"_id": "9223370522192597735"}))

    def open_theonefile():
        with open("C:/Users/Krystof/addonitem1", mode="r", buffering=1, encoding="utf-8-sig") as file:

            for idx, line in enumerate(file):
                line = json.loads(line)
                if "itemId" in line:
                    if line["itemId"] == "9223370470484619488":
                        print("got it")
                        collectionDrives.delete_one({"_id": "9223370470484619488"})
                        prepare_json(line)
                        try:
                            print(line)
                            print("inserted")
                            collectionDrives.insert_one(line)
                        except pymongo.errors.DuplicateKeyError:
                            pass
                        except pymongo.errors.InvalidDocument:
                            pass

main_func()


'''
print("\tDIESEL\tGASOLINE")
    print("Kodiaq: "+str(kodiaq_diesel_count)+"\t"+str(kodiaq_gasoline_count))
    print("Karoq: "+str(karoq_diesel_count)+"\t"+str(karoq_gasoline_count))
    print("Superb: " + str(superb_diesel_count) + "\t" + str(superb_gasoline_count))
    print("Fabia: " + str(fabia_diesel_count) + "\t" + str(fabia_gasoline_count))
    print("Octavia: " + str(octavia_diesel_count) + "\t" + str(octavia_gasoline_count))
    print("Rapid: " + str(rapid_diesel_count) + "\t" + str(rapid_gasoline_count))
    
os.chdir("C:\\Users\Krystof\Desktop\Diplomka\Testovací jízda")
with open('cz.eman.android.oneapp.lib.addon.drives - kopie.json', "r", encoding="utf-8") as oneappfile:
    with open('export.geojson', "r", encoding="utf-8") as openstreetmapfile:
        ident = "9223370495970442826"
        add_speed_to_oneapp_json(ident, harvesine(*prep_for_harvesine(oneappfile, openstreetmapfile)))
'''


'''
    file = json.load(file)
    vzorkovaci_fce = []
    odfiltrovane_pole = []
    vzorkovaci_fce_zajizdy = []
    for idex, el in enumerate(file[5]["content"]["data"]["mapData"]):
        if el["speed"] != 0 and el["speed"] != "null":
            odfiltrovane_pole.append(el["time"])
        else:
            pass

    for idx, prvek in enumerate(odfiltrovane_pole):
        if idx > 0:
            rozdil = float(abs(prvek-odfiltrovane_pole[idx-1]))
            rozdil = rozdil//1000
            vzorkovaci_fce_zajizdy.append(rozdil)

    for index, element in enumerate(file[5]["content"]["data"]["mapData"]):
        if index > 0 and element:
            rozdil = float(abs(element["time"]-file[5]["content"]["data"]["mapData"][index-1]["time"]))
            rozdil = rozdil//1000
            vzorkovaci_fce.append(rozdil)

        else:
            pass

    print(vzorkovaci_fce)
    print(mean(vzorkovaci_fce))
    print(stdev(vzorkovaci_fce), len(vzorkovaci_fce))

    print(vzorkovaci_fce_zajizdy)
    print(mean(vzorkovaci_fce_zajizdy))
    print(stdev(vzorkovaci_fce_zajizdy), len(vzorkovaci_fce_zajizdy))
    #print(len(file[5]["content"]["data"]["mapData"][0:300]["speed"] == 0))
'''

'''
#with open('cz.eman.android.oneapp.lib.addon.drives - kopie.json', 'r', encoding="utf-8") as oneappjson:
    first, second = prep_for_harvesine(oneappjson, openstreetjson)
    third = harvesine(first, second)
    fourth = replace_with_speed(third)
    print(fourth)
    pocet = 0
    for k in fourth:
        if k["maxspeed"] == "unknown":
            pocet += 1
        else:
            pass
    print(pocet)
    
'''
'''
os.chdir("C:\\Users\Krystof\Desktop\Diplomka\Testovací jízda")
with open('cz.eman.android.oneapp.lib.addon.drives - kopie.json', "r", encoding="utf-8") as f:
    f = json.load(f)
    print(f)
    cutted = f[5]["content"]["data"]["mapData"]
    print(cutted)

    for item in cutted:
        if "rpm" == "null":
            del item
        elif "speed" == "null":
            del item


    result = json_normalize(cutted, errors='ignore')
    result = pd.DataFrame(result)
    result.dropna()
    result = result[result["rpm"] != "null"]
    result = result[result["time"] != "null"]
    result = result[result["speed"] != "null"]
    ##result[result["speed"] != "null"]
    print(result)

    #data = pd.read_json(cutted, lines=True)
    #item in data[0]["content"]["data"]["mapData"]:
    #print(data)

    #x = numpy.arange(0, 2*numpy.pi, 0.1)
    #y = numpy.sin(x)
    #plt.title("RMP/TIME")
    d = {'one': np.random.rand(10),
        'two': np.random.rand(10)}
    result = result.iloc[610:690]
    #result.plot(x="latitude", y="longitude", style=['o', 'rx'])

    #sigma = linalg.lstsq(result['time'], result['rpm'])
    plt.plot(result['time'], result['speed'], '--bo')
    plt.show()
    print(result)


def to_request():
    with open('openstreetmap_request', 'w', encoding="utf-8") as output:
        for item in cutted:
            output.write("")
            output.write(str(item["latitude"]) + ",")
            output.write(str(item["longitude"]) + ",")
        output.close()


def zkrasluj():
    with open('C:\\Users\Krystof\Desktop\Diplomka\Testovací jízda\export.geojson', 'w+', encoding="utf-8") as osklivy:
        parsted = json.loads(osklivy)
        osklivy.truncate()
        osklivy.write(json.dumps(parsted, indent=4, sort_keys=True))
    osklivy.close()

zkrasluj()


'''


