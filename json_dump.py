import json
fp = 'static/json/'   
detection_list=[]       
def data_dump(object_list, dump_file):
    key_val = ["id","name","accuracy","xmin","ymin","xmax","ymax","width","height"]
    result_val= dict(zip(key_val,object_list))
    detection_list.append(result_val)
    
    
    with open(fp+'{}'.format(dump_file)+'.json', 'w') as outfile:
        json.dump(detection_list, outfile, sort_keys = False, indent = 4)
        outfile.close()
        #print(detection_list)


