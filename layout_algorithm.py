
#Jul 5, 2020 
__author__ = 'Biniam Behailu - biniambehailu3@gmail.com'

import cv2
import json
import os
from pathlib import Path
import glob
def UIBuilder(component_collection, filename):
    opening_tag = '<!DOCTYPE html>\n<html>\n\t<head>\n\t<!-- Required meta tags -->\n\t<meta charset="utf-8">\n\t<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n\t<title>Generated Page</title>\n\t<link rel="stylesheet " href="css/bootstrap.min.css ">\n\t<!-- Bootstrap CSS -->\n\t</head>\n\t<body>\n\t<div class="container" style="border:1px #fff solid;"> \n\t'
    closing_tag = '</div>\n\t<!-- JavaScript Library -->\n\t<script src="js/jquery-3.3.1.slim.min.js"></script>\n\t<script src="js/popper.min.js"></script>\n\t<script src="js/bootstrap.min.js"></script>\n\t</body>\n\t</html>\n\t'
    output_tag = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nulla sapien, consequat vestibulum ornare ac, volutpat eget lacus. Curabitur sit amet odio quis lorem sodales imperdiet. Nulla porta turpis et mauris fermentum vulputate. Phasellus maximus elit a mi laoreet pharetra. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Curabitur posuere, tortor quis eleifend sagittis, erat odio finibus mauris, in venenatis nunc orci a est. Integer quis tellus pharetra, finibus purus ut, vulputate diam.</p>"
    td = open('template_dictionary.json','r')
    template_dictionary = json.load(td)
    long_paragraph = '<p style = "text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nulla sapien, consequat vestibulum ornare ac, volutpat eget lacus. Curabitur sit amet odio quis lorem sodales imperdiet. Nulla porta turpis et mauris fermentum vulputate. Phasellus maximus elit a mi laoreet pharetra. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Curabitur posuere, tortor quis eleifend sagittis, erat odio finibus mauris, in venenatis nunc orci a est. Integer quis tellus pharetra, finibus purus ut, vulputate diam.</p>'
    tag=""
    row_tag ='<div class="row">'

    end_tag ='</div>'

    #print("LEN ", len(col_tag))
    for row in component_collection:
        #print(len(row))
        tag = tag + row_tag+"\n"
        for cols in row:
            #print(row.index(cols))
            #print("UI BUILDER ===>",cols)
            for col in range(len(cols)):
                col_tag =''
                temp_tag=''
                if col == 0:
                    f=4
                    col_tag = '    <div class="col-lg-{}">'.format(cols[col]['col_val'])
                    tag = tag + col_tag+"\n"
                    #print(col)
                elif col == 1:
                    iu=0
                    if len(cols[col]) == 1:
                        #print("none")
                        #tag = tag + "none"+"\n"
                        tag = tag +"    "+end_tag+"\n"
                    elif len(cols[col]) > 1:
                        #print(cols[col]["name"])
                        for dk in template_dictionary.keys():
                        

                            if cols[col]["name"] == dk:
                                
                                if dk == "Paragraph" and int(cols[col]["width"]) >=600:
                                    
                                    temp_tag = "    "+temp_tag + long_paragraph
                                    tag = tag + "    "+temp_tag+"\n"
                                    tag = tag +"    "+end_tag+"\n"
                                elif dk == "Image":
                                    var = template_dictionary[dk].replace("200",str(cols[col]["height"]))
                                    temp_tag = "    "+temp_tag + var
                                    tag = tag + "    "+temp_tag+"\n"
                                    tag = tag +"    "+end_tag+"\n"
                                elif dk == "Carousel":
                                    
                                    var = template_dictionary[dk].replace("300",str(cols[col]["height"]))
                                    temp_tag = "    "+temp_tag + var
                                    tag = tag + "    "+temp_tag+"\n"
                                    tag = tag +"    "+end_tag+"\n"
                                else:
                                    
                                    temp_tag = "    "+temp_tag + template_dictionary[dk]
                                    tag = tag + "    "+temp_tag+"\n"
                                    tag = tag +"    "+end_tag+"\n"
        
                #print(col)
        tag = tag +end_tag+"<br/>"+"\n"
        output_tag = opening_tag+tag+closing_tag
        #print("_____________________________")
            
              
    #print(type(output_tag))
    path = "static/output/"
    filename = Path(filename).stem
    file_name = filename
    output_file_path = "{}{}.html".format(path, file_name)
    
    if os.path.exists(output_file_path):
         os.remove(output_file_path)
    else:
        print("The file does not exists")
    
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(output_tag)


def grid(detection_list, filename):
    #print(xmin)
    #print(img.shape)
    img = cv2.imread("static/uploads/"+filename,1)
    x = img.shape[1]
    n=0
    c_grid = []
    overlay = img.copy()
    for i in range (0,x):
        #img = cv2.line(img,(n ,0), (n,img.shape[0]), (255, 0, 0), 3)
        xmin = n
        #print(tl_x)
        ymin = 0
        n = n+80
        xmax = n
        if i==12:
            break
        #print(br_x)

        ymax = img.shape[0]
        c_grid.append([xmin, ymin, xmax, ymax])
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

    row_calculator(img, filename, c_grid, detection_list)
        #imgs = cv2.addWeighted(overlay, 0.4, img, 1 - 0.4, 0)

def row_calculator(img, filename, c_grid, detection_list):
    in_one_row =  0   
    not_in_one_row =  0
    
    row_list=[]
    col_list=[]
    row_col_list=[]
    col=0
    ff=0
    temp=4
    checker = "false"
   
    for i in range (len(detection_list)):
        
        #######################################################################################################
        #Calculating the covered grids
        #######################################################################################################
        
        cv2.rectangle(img, (detection_list[i]["xmin"], detection_list[i]["ymin"]), (detection_list[i]["xmax"], detection_list[i]["ymax"]), (0, 255, 0), -1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, detection_list[i]["name"], (detection_list[i]["xmin"] ,detection_list[i]["ymin"]), font, 1, (0,0,0), 3, cv2.LINE_AA)
        #print("Value of i : ",i)
        #filename = Path(filename).stem
        cv2.imwrite("static/grid/"+filename, img)

        if i<len(detection_list)-1:
            center_box_i = int((detection_list[i]["ymin"] + detection_list[i]["ymax"]) /2)
            center_box_i1 = int((detection_list[i+1]["ymin"] + detection_list[i+1]["ymax"]) /2)
            mid = detection_list[i]["ymax"] - detection_list[i]["ymin"]

            top_difference = detection_list[i+1]["ymin"] - detection_list[i]["ymin"] 
            bottom_difference = detection_list[i+1]["ymax"] - detection_list[i]["ymax"] 
        
            #print("MAMAMAMAMA", detection_list[i]["name"],detection_list[i]["ymin"] ,center_box_i1, top_difference)
            #print("MY List = ",row_list)

            row_list.append(detection_list[i])

            if detection_list[i]["ymin"] < center_box_i1 and top_difference > mid or detection_list[i+1]["ymin"] < center_box_i and top_difference > mid:
               
                #print("YES")
                #print("ROW List = ",row_list)
                not_in_one_row+=1
                temp = row_list.copy()
                if row_list != []:
                    row_col_list.append(temp)
                    row_list.clear()
                    temp=0
                    #print("New ROW List = ",row_col_list) 
            else:
                temp+=1
                in_one_row+=1
        else:
            #print("BBBBBBBBBBBBBBBBBBBBBBBBBBBB", len(detection_list), i, temp)
            if temp >= 1:
                row_list.append(detection_list[i])
                #print("___________", "ROWS = ",temp, row_list)
                row_col_list.append(row_list)
            elif i==len(detection_list)-1 and temp == 0:
                row_list.append(detection_list[i])
                #print("AAEAEAEAEAEAE", len(row_list))
                row_col_list.append(row_list)
            continue

    #print("ROW COL LIST = ", row_col_list)
    
    col_sort(c_grid, row_col_list,filename)
   
   #Column sort
def col_sort(c_grid, row_col_list,filename):
    for i in row_col_list:
        '''x = row_col_list.count(i)
        if(x==2):
            row_col_list.pop(row_col_list.index(i))'''
        if len(i) > 1:
            i.sort(key=lambda item: item.get("xmin"))
    #print("SORTED = ",row_col_list)
    
    column_overlap(c_grid, row_col_list, filename)

def column_overlap(c_grid, detection_list, filename):
    for i in range(len(detection_list)):
        for j in range(len(detection_list[i])):
            #print(len(detection_list[i]))
            
            if  len(detection_list[i]) >= 1:
                if j == len(detection_list[i])-1:
                    #print("yes",len(detection_list[i])-1)
                    #if detection_list[i][j]["xmax"] > detection_list[i][j+1]["xmin"]:
                    continue
                else:
                    #print("Bino = ",detection_list[i][j+1]["ymax"])
                    if detection_list[i][j]["xmax"] >= detection_list[i][j+1]["xmin"]:
                        #print("Overlap = ",detection_list[i][j]["xmax"],detection_list[i][j+1]["xmin"])
                        overlap = detection_list[i][j]["xmax"] - detection_list[i][j+1]["xmin"]
                        half_overlap = int(overlap/2)
                        detection_list[i][j]["xmax"] = detection_list[i][j]["xmax"] - overlap
                        detection_list[i][j+1]["xmin"] = detection_list[i][j+1]["xmin"] + 2
                        detection_list[i][j]["width"] = detection_list[i][j]["xmax"] - detection_list[i][j]["xmin"]
                        detection_list[i][j+1]["width"] = detection_list[i][j+1]["xmax"] - detection_list[i][j+1]["xmin"]
                        #print(overlap)
                            
                    
                
    #print("OVERLAP FIX == ",detection_list)                

    col_calculator(c_grid, detection_list, filename)


def col_calculator(c_grid, detection_lists,filename):

    #print(detection_list)
    component_collection=[]

    for i in detection_lists:
        grid = [1,2,3,4,5,6,7,8,9,10,11,12]
        ug = [1,2,3,4,5,6,7,8,9,10,11,12]
        
        if len(i) == 1:
            row=[]
            
            #row.clear()
            non_covered = 0
            covered = 0
            #print(i[j])
            tt=0
            t=0
            temp=0
            temp1=0
            for k in c_grid:
                grid_no = c_grid.index(k)+1
                grid_center=int((k[0] + k[2])/2)
                if(i[0]["xmin"] <= k[2] and k[0] <= i[0]["xmax"] and i[0]["xmax"] >= grid_center  and i[0]["xmin"] <= grid_center):
                    if t==0:
                        #print("YES YES YES",t)
                        covered+=1
                        #print("COVERED Grid", covered)
                        #UIBuilder(covered, non_covered, i[j])
                        if covered == len(c_grid):
                            row.append([{ "col_val":covered },i[0]])

                    elif t == 1 and non_covered > 0:
                        covered+=1
                        row.append([{ "col_val":non_covered },{"none":0}])
                        t=2
                        non_covered=0
                    elif t == 2:
                        covered+=1
                else:
                    if t == 0:
                        t=1
                        non_covered+=1
                        if covered > 0:
                            row.append([{ "col_val":covered },i[0]])
                            covered = 0
                            tt=20
                    elif t == 1:
                        non_covered+=1
                        tt=20
                            
                    elif t == 2 :
                        if covered > 0:
                            row.append([{ "col_val":covered },i[0]])
                            covered=0

                        non_covered+=1
            if t==2 and covered > 0:
                    row.append([{ "col_val":covered },i[0]])
                    covered=0
            if tt==20:
                row.append([{ "col_val":non_covered },{"none":0}])  
                non_covered=0
                
            component_collection.append(row)   
        elif len(i) > 1:
            ind = 0
            space = 0
            row = []
            for j in range(len(i)):
                c_grid_arr_temp = []
                u_grid_arr_temp = []
                #print(j)
                non_covered = 0
                covered = 0
                c_grid_no = 0
                u_grid_no = 0
                c_grid_arr = []
                u_grid_arr = []

                #print(i[j])
                tt = 0
                t = 0
                temp = 0
                for k in c_grid:
                    
                    grid_center=int((k[0] + k[2])/2)
                    if(i[j]["xmin"] <= k[2] and k[0] <= i[j]["xmax"] and i[j]["xmax"] >= grid_center  and i[j]["xmin"] <= grid_center):
                        covered+=1
                        c_grid_no = c_grid.index(k)+1
                        #print("COVERED GRID NO = ", c_grid_no)
                        c_grid_arr.append(c_grid_no)
       
                c_grid_arr_temp.append(c_grid_arr)
                u_grid_arr_temp.append(u_grid_arr)
                #print(c_grid_arr_temp)
                #print(ug)
                    
                for cg in c_grid_arr_temp:
                    for c in cg:
                        for u in ug:
                            if c == u:
                                #print("Hel ",i[i.index(j)])
                                if cg.index(c)+1 < len(cg):
                                    #print(u)
                                    grid.pop(grid.index(u))
                                    #print("Hel ",cg.index(c)+1)
                                    #print("t at 1st If = ",grid)
                                    
                                elif cg.index(c)+1 == len(cg):
                                    #print("t at 2nd If = ",grid)
                                    grid.insert(grid.index(u), cg)
                                    grid.pop(grid.index(u))  
            for g in grid:
                if type(g) == list:
                    if space > 0:
                        #print([{ "col_val":space },{"none":0}])
                        row.append([{ "col_val":space },{"none":0}])
                        space = 0
                        
                        #print([{ "col_val":len(g) },i[ind]])
                        row.append([{ "col_val":len(g) },i[ind]])
                        ind+=1
                    else:
                        #print([{ "col_val":len(g) },i[ind]])
                        row.append([{ "col_val":len(g) },i[ind]])
                        ind+=1
                else:
                    space+=1
                    
                    if grid.index(g) == len(grid)-1:
                        
                        row.append([{ "col_val":space },{"none":0}])

              

            component_collection.append(row)

    #print("ROW COLLECTION = ",component_collection)
    UIBuilder(component_collection,filename)

def readJSON(filename):
    f = open('static/json/sorted/sorted_data.json','r')
    detection_list = json.load(f)
    
    grid(detection_list,filename)
    
    



#img1 = cv2.imread('sample3.png',1)
#cv2.imshow('Image', img1)

cv2.waitKey(0)
cv2.destroyAllWindows()

