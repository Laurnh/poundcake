#!/usr/bin/python

#Organizes all images in a folder into subfolders by class

'''This script divides an entire folder of simulated gym equipment images (5 classes)
into subfolders, one for each class.
In this setup we:

-put all of our equipment images (train set) together in /images/data5/train
-put all of our equipment images (test set) together in /images/data5/test
-put all of our equipment images (validation set) together in /images/data5/validate

-benchpress images are labeled "benchpress001", "benchpress002", ...
-hyperextension bench images are labeled "hyperext-bench001", "hyperext-bench002", ...
-leg press images are labeled "leg-press001", "leg-press002", ...
-plyometric box images are labeled "plyo-box001", "plyo-box002", ...
-power rack images are labeled "power-rack001", "power-rack002", ...

This script will:
-divide our equipment images into subfolders (1 for each class):
	/images/data5/train/
		benchpress/
		hyperext-bench/
		leg-press/
		plyo-box/
		power-rack/
	/images/data5/test/
		benchpress/
		hyperext-bench/
		leg-press/
		plyo-box/
		power-rack/
	/images/data5/validate/
		benchpress/
		hyperext-bench/
		leg-press/
		plyo-box/
		power-rack/
'''

import os
import shutil
import random
import re

random.seed(42)

#load list of all files in current folder
path = 'images/data5_temp/validate/'
files = os.listdir(path)
files.sort()

if files[0] == '.DS_Store':
	files.pop(0)

#compile regular expressions for each class
reg_benchpress = re.compile('benchpress')
reg_powerrack = re.compile('power')
reg_legpress = re.compile('leg')
reg_plyobox = re.compile('plyo')
reg_hyperextbench = re.compile('hyper')

#iterate through list of files, move each file into subfolder corresponding to its class
i=0
new_path_benchpress = 'images/data5/validate/benchpress/'
new_path_powerrack = 'images/data5/validate/power-rack/'
new_path_legpress = 'images/data5/validate/leg-press/'
new_path_plyobox = 'images/data5/validate/plyo-box/'
new_path_hyperextbench = 'images/data5/validate/hyperext-bench'


for file in files:
	print file
	if reg_benchpress.match(file):
		shutil.move(os.path.join(path, file), os.path.join(new_path_benchpress, file))
	elif reg_powerrack.match(file):
		shutil.move(os.path.join(path, file), os.path.join(new_path_powerrack, file))
	elif reg_legpress.match(file):
		shutil.move(os.path.join(path, file), os.path.join(new_path_legpress, file))
	elif reg_plyobox.match(file):
		shutil.move(os.path.join(path, file), os.path.join(new_path_plyobox, file))
	elif reg_hyperextbench.match(file):
		shutil.move(os.path.join(path, file), os.path.join(new_path_hyperextbench, file))
	i += 1
	print "moved ," , i




