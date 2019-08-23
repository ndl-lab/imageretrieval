#!/usr/bin/env python3
import os
import glob
import shutil
from keras.applications.densenet import DenseNet121
from keras.applications.densenet import preprocess_input
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense, Convolution2D, MaxPooling2D, GlobalAveragePooling2D
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from keras.backend import tensorflow_backend as backend
import numpy as np
import sys
import shutil
import random
import csv
import argparse
import pickle
from tqdm import tqdm
import xml.etree.ElementTree as ET


DATASETDIR="dataset"

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="1"
batch_size = 8
nb_classes = 2
import tensorflow as tf
from keras import backend as K
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
sess = tf.Session(config=config)
K.set_session(sess)

img_rows, img_cols = 224,224
channels = 3

def read_xml(xml_path,pid,komanum,imgnum):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    width=int(root.find("./size/width").text)
    height=int(root.find("./size/height").text)
    #print(pid)
    for obj in root.findall("./object"):
        pose = obj.find("pose").text
        if pose!=imgnum:
            continue
        bndbox=obj.find("bndbox")
        xmin=int(bndbox.find("xmin").text)
        xmax=int(bndbox.find("xmax").text)
        ymin=int(bndbox.find("ymin").text)
        ymax=int(bndbox.find("ymax").text)
        wp=(xmax-xmin)*1000//width/10
        hp=(ymax-ymin)*1000//height/10
        xminp=xmin*1000//width/10
        yminp=ymin*1000//height/10
        iiifurl="https://www.dl.ndl.go.jp/api/iiif/"+pid+"/R"+komanum.zfill(7)+"/pct:%3.1f,%3.1f,%3.1f,%3.1f/400,/0/default.jpg"% (xminp,yminp,wp,hp)
        uri=pid+"/R"+komanum.zfill(7)+"/pct:%3.1f,%3.1f,%3.1f,%3.1f/"% (xminp,yminp,wp,hp)
        #print(uri)
        return uri

if __name__ == '__main__':
    np.random.seed(777)
    base_model = DenseNet121(include_top=False, weights='imagenet',pooling='avg',classes=1000)
    #top_model = Sequential()
    #top_model.add(Dense(1000, activation='softmax'))
    #pseudomodel = Model(inputs=base_model.input,outputs=top_model(base_model.output))
    for datasetname in glob.glob(os.path.join(DATASETDIR,"*")):
    #for datasetname in ["dataset11"]:
        print(datasetname)
        path_test_prefix=datasetname
        outputfilename="features/features_"+datasetname+".pkl"
        inputs = []
        filenames=[]
        urilist=[]
        dic={}
        counter=0
        for img_path in tqdm(glob.glob(os.path.join(path_test_prefix,"*.jpg"))):
            imgname=os.path.basename(img_path)
            pid=imgname.split("_")[0]
            koma=imgname.split("_")[1][:-4]
            imgnum=imgname.split("_")[2][:-4]
            counter+=1
            #print(img_path)
            xml_path=os.path.join(path_test_prefix,pid+"_"+koma+".xml")
            iiifuri=read_xml(xml_path,pid,koma,imgnum)
            urilist.append(iiifuri)
            img = image.load_img(img_path,target_size=(img_rows, img_cols))
            img = image.img_to_array(img)
            img /= 255.0
            inputs.append(img.copy())
            filenames.append(os.path.basename(img_path))
            if counter%batch_size==0:
                inputs = np.array(inputs)
                # CNNを構築
                pred=base_model.predict(inputs,batch_size)
                #labels=pseudomodel.predict(inputs,batch_size)
                pred=pred.reshape((len(filenames),1024))
                for index,fname in enumerate(filenames):
                    #print(fname,urilist[index])
                    dic[fname]={"iiifuri":urilist[index],"vec":pred[index]}
                inputs=[]
                filenames=[]
                urilist=[]
        with open(outputfilename, 'wb') as f:
            pickle.dump(dic,f)
            #backend.clear_session()

