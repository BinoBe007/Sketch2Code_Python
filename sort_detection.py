import json
from operator import itemgetter
from layout_algorithm import *
fp='static/json/sorted/sorted_data.json'
def sort_detection_list(detection_list, filename, filenames):
    size = len(detection_list)
    for i in range(size):
        min_index = i
        for j in range(i + 1, size):
            if detection_list[min_index]["ymin"] > detection_list[j]["ymin"] and detection_list[min_index]["xmin"] > detection_list[j]["xmin"]:
                min_index = j
    detection_list[i], detection_list[min_index] = detection_list[min_index], detection_list[i]

    #detection_list.sort(key=lambda item: item.get("xmin"))
    f = itemgetter('ymin','xmin')
    detection_list.sort(key=f)

    print(detection_list)
    dump_json(detection_list, filename)
    readJSON(filenames)

def dump_json(detection_list, filename):
    with open(fp, 'w') as outfile:
        json.dump(detection_list, outfile, indent = 4)
        #print(detection_list)
    
