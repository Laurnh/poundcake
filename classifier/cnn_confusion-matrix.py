#!/usr/bin/python

#Generate a confusion matrix for the 3-layer CNN

'''This script validates our model using a small validation set of "real-life" gym equipment photos
In this setup, we:
- put the benchpress photos in images/images_test/benchpress
- put the hyperextension bench photos in images/images_test/hyperext-bench
- put the leg press photos (training set) in images/images_test/leg-press
- put the plyometric photos (training set) in images/images_test/plyo-box
- put the power-rack photos (training set) in images/images_test/power-rack
'''

#from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

#from PIL import Image
import os
import numpy as np
from sklearn.metrics import confusion_matrix

# dimensions of our images.
img_width, img_height = 150, 150


if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

#compile the 3-layer CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(5))
model.add(Activation('softmax'))

#load weights into new model
model.load_weights('first_try_multiclass.h5')

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

#GENERATE CONFUSION MATRIX, ITERATE OVER ALL TEST IMAGES
#path to folder where test images are located
path = '/Users/lalooair/ohana/data_sci_proj/insight/gym/images/images_test/'
files = os.listdir(path)

y_true = [] #list of ground truth labels, will be plugged into sklearn confusion matrix
y_pred = [] #list of predicted labels
dict_labels = {0: 'benchpress', 1: 'hyperext-bench', 2: 'leg-press', 3: 'plyo-box', 4: 'power-rack'}

#iterate over every subfolder, and every image in each subfolder
#subfolders correspond to each class
for file in files:
    if os.path.isdir(os.path.join(path, file)):
    	label_true = file #label all files in this folder as name of folder
    	path_subfolder = path + file
    	subfiles = os.listdir(path_subfolder) #list of all files in subfolder
    	for subfile in subfiles:
    		if subfile == '.DS_Store':
    			continue
    		img_path = os.path.join(path_subfolder, subfile)
    		#load image
    		img = image.load_img(img_path, target_size = (img_width, img_height))
    		img_tensor = image.img_to_array(img)
    		img_tensor = np.expand_dims(img_tensor, axis=0)
    		img_tensor /= 255

    		pred = model.predict(img_tensor) #make prediction
    		label_pred = dict_labels[np.argmax(pred[0])]

    		y_true.append(label_true) #append true label
    		y_pred.append(label_pred) #append predicted label


#generate, print the confusion matrix
cm = confusion_matrix(y_true, y_pred, labels=['benchpress','hyperext-bench','leg-press','plyo-box','power-rack'])
print cm

