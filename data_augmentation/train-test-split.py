#!/usr/bin/python

#Performs train-test-split on a folder of images

'''This script divides an entire folder of simulated gym equipment images (5 classes)
into train/test/validation sets.
In this setup we:

-put all of our equipment images together in /images/data_full5

This script will:
-put our train set images in /images/data5/train
-put our test set images in /images/data5/test
-put our validation set images in /images/data5/validate
'''

import os
import random

random.seed(42)

#load list of all files in full catalog of generated data (X files)

path_alldata = 'images/data_full5/'
files_alldata = os.listdir(path_alldata)
files_alldata.sort()

if files_alldata[0] == '.DS_Store':
	files_alldata.pop(0)

random.shuffle(files_alldata) #randomly shuffles the ordering of filenames

#splits data into 3 lists of filenames for train-test-validate
split_1 = int(0.8*len(files_alldata))
split_2 = int(0.9*len(files_alldata))
train_filenames = files_alldata[:split_1]
test_filenames = files_alldata[split_1:split_2]
validate_filenames = files_alldata[split_2:]

#move files into new folders (train, test, validate)
path_train = 'images/data5/train/'
path_test = 'images/data5/test/'
path_validate = 'images/data5/validate/'


i=0
for file in train_filenames:
	path_file = os.path.join(path_alldata, file)
	new_path_file = os.path.join(path_train, file)
	os.system('cp ' + path_file + ' ' + new_path_file)
	i += 1
	print "train ," , i

i=0
for file in test_filenames:
	path_file = os.path.join(path_alldata, file)
	new_path_file = os.path.join(path_test, file)
	os.system('cp ' + path_file + ' ' + new_path_file)
	i += 1
	print "test ," , i

i=0
for file in validate_filenames:
	path_file = os.path.join(path_alldata, file)
	new_path_file = os.path.join(path_validate, file)
	os.system('cp ' + path_file + ' ' + new_path_file)
	i += 1
	print "validate ," , i

