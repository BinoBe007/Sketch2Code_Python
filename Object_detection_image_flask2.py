######## Image Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 1/15/18
# Description: 
# This program uses a TensorFlow-trained neural network to perform object detection.
# It loads the classifier and uses it to perform object detection on an image.
# It draws boxes, scores, and labels around the objects of interest in the image.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.

# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import json
from pathlib import Path
import glob
# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util
from sort_detection import *

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'
#PATH_TO_IMAGE = 'input'
output_path = 'static/detections/'

#input_resizer(IMAGE_NAME)
# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Path to image
#PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)

# Number of classes the object detector can identify
NUM_CLASSES = 14

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')


# Load image using OpenCV and
# expand image dimensions to have shape: [1, None, None, 3]
# i.e. a single-column array, where each item in the column has the pixel RGB value



#mywidth = 1366



def detector(filepath,filename):

    image = cv2.imread(filepath)
    image_expanded = np.expand_dims(image, axis=0)
    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    #cv2.imshow("image", image)
    # Draw the results of the detection (aka 'visulaize the results')

    coordinates =vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=4, 
        min_score_thresh=0.70)



        
    '''
    def export_detection(coordinates_list=[]):
        filePath = 'RESULTS/detection_output.json'
        with open('RESULTS//detection_output.json', 'a') as outfile:
            json.dump(coordinates_list, outfile, sort_keys = True, indent = 4)
    '''
    min_score_thresh0=0.70
    data = []

    coordinates_list = {}
    result_val={}

    #print([category_index.get(i) for i in classes[0]])
    #print(image.size)
    #print(image.shape)

    fp = 'static/json/'
   
            
    for index,value in enumerate(classes[0]):
        if scores[0,index] > min_score_thresh0:
            ymin, xmin, ymax, xmax = boxes[0,index]
            height, width, channels = image.shape
            ymin = int(ymin*height)
            ymax = int(ymax*height)
            xmin = int(xmin*width)
            xmax = int(xmax*width)

            #Conversion
            width = xmax - xmin
            height = ymax - ymin
            new_score = (scores[0,index]*100)
            new_score = round(new_score,2)


            lists = [xmin, ymin, xmax, ymax, new_score,width,height]
            key_val = ["xmin","ymin","xmax","ymax","accuracy","width","height"]
            result_val= dict(zip(key_val,lists))
            
            new_result_val = category_index.get(value)
            result_val.update(new_result_val)
            data.append(result_val)
            dump_file = Path(filename).stem
            print(data)
            
            with open(fp+'{}'.format(dump_file)+'.json', 'w') as outfile:
                json.dump(data, outfile, sort_keys = True, indent = 4)
                print(fp+'{}'.format(dump_file)+'.json')
            cv2.imwrite(output_path + filename, image)

            f = open(fp+'{}'.format(dump_file)+'.json','r')
            detection_list = data
            sort_detection_list(detection_list, dump_file, filename)

    # All the results have been drawn on image. Now display the image.


