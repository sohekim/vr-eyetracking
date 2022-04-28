################################################
## 2. analyze hitting points
## get data of which object they are looking at
##
## we need:
## 1. eye tracking data file end with csv that we
##    previously got(only has timestamp and 2d
##    hitting points
## 2. folder contains image sequence and json files
##
## In our example, we pause the video twice,
## If you didn't pause the video at all
## Go to "No Pause" at line 137 and follow the instructions
################################################

import matplotlib.pyplot as plt
import csv
import os
import  sys
import json
from shapely.geometry import Point, Polygon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches


################################################
# remove string does not contain sym from list
################################################
def remove_from_list(alist, sym):
    for item in alist:
        if sym not in item:
            alist.remove(item)

################################################
# include string contain sym from list
################################################
def include_to_list(alist, sym):
    temp = []
    for item in alist:
        if sym  in item:
            temp.append(item)
    return temp


################################################
# convert a list of list to a list of tuple
################################################
def convert_to_tuple_list(alist):
    temp = []
    for item in alist:

        temp.append(tuple(item))
    return temp

################################################
# convert rectangle(2 points) to polygon (4points)
################################################
def convert_to_box(points):
    temp = []
    t1 = points[0]
    t2 = points[1]
    if t1[0] < t2[0]:
        x1 = t1[0]
        x2 = t2[0]
    else:
        x2 = t1[0]
        x1 = t2[0]
    if t1[1] < t2[1]:
        y1 = t1[1]
        y2 = t2[1]
    else:
        y2 = t1[1]
        y1 = t2[1]

    temp.append((x1, y1))
    temp.append((x2, y1))
    temp.append((x2, y2))
    temp.append((x1, y2))


    return temp


################################################
# change variables here
################################################
interval = 500000 # half second
count = 0
# datafile is the path of eye tracking file that has 2d hitting points
datafile = '/Users/soheekim/Desktop/vr/vr_research/data/081/WSU_ED_002_EYE2/vr_data_20220405T173944.csv'
# folder path that contains image and json of annotation
annot_dir_curr = '/Users/soheekim/Desktop/vr/vr_research/vid/frames'
# folder to generate pics
pics_folder_path = '/Users/soheekim/Desktop/vr/vr_research/untitled'

# we pause the video from start1 to end1 and start2 to end2
# if you only pause the video once, just set start2 and end2 to 0
# if you didn't pause the video at all, go to "No Pause" at line 137 and follow the instructions
# df = {'start1':1, 'end1':11, 'start2':33.9, 'end2':34.9}

if not os.path.exists(pics_folder_path + 'pics'):
    os.makedirs(pics_folder_path + 'pics')
    print('creating pics folder...')
arr = os.listdir()
print('list all files in current folder: ', pics_folder_path)


# read timestamp and hitting point csv file
print('open eye tracking data file '+datafile+"...")
time_eye_dict = {}
f = open(datafile, 'r', encoding="utf-8")
reader = csv.reader(f)
start_timestamp = 0
for row in reader:
    if start_timestamp ==0:
        start_timestamp = int(row[0])
    time_eye_dict[int(row[0])] = [float(row[1]), float(row[2])]

poly_file_names = os.listdir(annot_dir_curr)
poly_json_file_names = include_to_list(poly_file_names, 'json')
poly_json_file_names.sort()
print('open image sequence folder ' + annot_dir_curr+"...")


result_scene_dict = {'timestamp':[], 'image':[]}

for key, value in time_eye_dict.items():
    hitting_point = Point(value[0], value[1])

    curr_img = 'image'
    curr_time = (key - start_timestamp) / interval
    curr_time = int(curr_time)
    num = ''


    ####### No Pause. Replace this block of code with this line:
    num = str(curr_time).zfill(2)
    ########

    result_scene_dict['timestamp'].append(key)
    result_scene_dict['image'].append(num)

    # print(num)

    if os.path.exists(annot_dir_curr + '/' + curr_img+num + '.json'):
        curr_img += num
    else:
        curr_img = prev

    # if os.path.exists(annot_dir_curr + '/' + curr_img+num + '.json'):
    #     # print(annot_dir_curr + '/' + curr_img+num + '.json')
    #     curr_img += num
    # else:
    #     curr_img += '00'
    #     # curr_img = prev

    with open(annot_dir_curr + '/' + curr_img + '.json') as img_f:
        d = json.load(img_f)
        for shape in d['shapes']:
            points = shape['points']
            points = convert_to_tuple_list(points)
            label = shape['label']
            if len(points) > 2:
                poly = Polygon(points)
            else:
                poly = Polygon(convert_to_box(points))
            if hitting_point.within(poly) == True:
                flag = 'True'
            else:
                flag = 'False'
            if label in result_scene_dict:
                while len(result_scene_dict[label]) < (len(result_scene_dict['timestamp'])-1):
                    result_scene_dict[label].append('NA')
                result_scene_dict[label].append(flag)
            else:
                result_scene_dict[label] = ['NA']*(len(result_scene_dict['timestamp'])-1)
                result_scene_dict[label].append(flag)


        prev = curr_img

print(result_scene_dict.keys())
print(len(result_scene_dict.get('timestamp')))
print(len(result_scene_dict.get('image')))
print(len(result_scene_dict.get('P')))
print(len(result_scene_dict.get('P1')))

# newP1 = {'P1' : result_scene_dict.get('P1')[0:len(result_scene_dict.get('timestamp'))]}
# result_scene_dict.update(newP1)
# print(len(result_scene_dict.get('P1')))
# curr_df = pd.DataFrame(result_scene_dict, columns=['timestamp', 'image', 'P', 'P1'])
curr_df = pd.DataFrame(result_scene_dict)
curr_df.to_csv(datafile+'_result.csv', sep=',', encoding='utf-8')







print('finish')



