#!/usr/bin/python

'''This script trains a 3-layer CNN on 5 classes of gym equipment photos
In this setup, we:
- put the benchpress photos (training set) in images/data5/train/benchpress
- put the benchpress photos (test set) in images/data5/test/benchpress

- put the hyperextension bench photos (training set) in images/data5/train/hyperext-bench
- put the hyperextension bench photos (test set) in images/data5/train/hyperext-bench

- put the leg press photos (training set) in images/data5/train/leg-press
- put the leg press photos (test set) in images/data5/test/leg-press

- put the plyometric box photos (training set) in images/data5/train/plyo-box
- put the plyometric box photos (test set) in images/data5/train/plyo-box

- put the power-rack photos (training set) in images/data5/train/power-rack
- put the power-rack photos (test set) in images/data5/train/power-rack
'''

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K


# dimensions of our images.
img_width, img_height = 150, 150

train_data_dir = 'images/data5/train'
validation_data_dir = 'images/data5/test'
nb_train_samples = 4382
nb_validation_samples = 548
epochs = 50
batch_size = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

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

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

#generate training data 
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

#generate test data
validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

#fit the model
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

#save the model so it can easily be compiled later for predictions
model.save_weights('first_try_multiclass.h5')


#print the indices that Keras assigns to each class (need this for making predictions)
classes = train_generator.class_indices
print(classes)