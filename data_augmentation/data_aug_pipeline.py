#!/usr/bin/python

#loop over images to generate large datasets of composited images
#pipeline for gym equipment images (foreground) to be combined w/ gym interiors (background) images.
#for each equipment image, combine it with a random sample of 25 (out of a possible 156) backgrounds.

from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import math
import os
import random

#make sure you set a different random seed for each class, so the randomly set of gym interiors is
#different for each class.
#random.seed(42) #bench press
#random.seed(43) #power-rack
#random.seed(44) #leg-press
#random.seed(45) #plyo-box
random.seed(46) #hyperext-bench

#crop the image by a centered, square boundary box
#img is a PIL object
#(0,0) is in upper left corner of image
#boundary box is defined  as a 4-tuple (left, upper, right, lower)
#if image is already square with same size as square_size, returns original image.
def centeredSquareCrop(img, square_size):
    width, height = img.size
    if (width == height) and (width == square_size):
        return img

    left = math.ceil((width - square_size)/2.)
    upper = math.ceil((height - square_size)/2.)
    right = math.floor((width + square_size)/2.)
    lower = math.floor((height + square_size)/2.)

    crop_dimensions = (left, upper, right, lower)
    img = img.crop(crop_dimensions)
    return img

#adaptively resize an image to prep it for a centered, squared crop
#takes into account whether or not square fits into image, square partially fits, or
#square is larger than image.
#if image is already square, just returns original image resized to square_size.
#img is a PIL object
def adaptive_resize(img, square_size): 
    width_height = img.size
    smallest_side = min(width_height)
    largest_side = max(width_height)

    if (smallest_side == largest_side):
        #if image is square, resize to square_size
        img = img.resize((square_size, square_size))
        return img
    elif (square_size < smallest_side):
        #if square fits inside image, scale smallest_side down to square_size
        #preserve aspect ratio
        resize_ratio = float(square_size) / float(smallest_side)
        resize_x = int(math.floor((width_height[0]*resize_ratio)))
        resize_y = int(math.floor((width_height[1]*resize_ratio)))
        img = img.resize((resize_x, resize_y))
        return img
    elif (square_size > smallest_side) and (square_size < largest_side):
        #if square partially fits inside image
        #stretch smallest_side to square_size
        img = img.resize((square_size, width_height[1]))
        return img
    elif (square_size > largest_side):
        #if image fits inside square
        #stretch both sides to square_size
        img = img.resize((square_size, square_size))
        return img
    else:
        img = img.resize((square_size, square_size))
        return img

#adaptively resize an image to a square with size largest_side (the largest side of img).
#keeps original image centered, adds white background around it as padding to create a sqaure shape.
#if image is already square, just returns original image.
#img is a PIL object
def adaptive_padding(img):
    img_size = img.size
    width = img_size[0]
    height = img_size[1]

    if(width != height):
        largest_side = width if (width > height) else height

        background = Image.new('RGBA', (largest_side, largest_side), (255, 255, 255, 255))
        #offset denotes position of upper-left corner (WRT to background) of pasted img
        offset = (int(round(((largest_side - width) / 2), 0)), int(round(((largest_side - height) / 2),0)))

        background.paste(img, offset)
        return background

    else:
        return img

#Use Python Image Library (PIL) to make images transparent
#use this to prep equipment images to be added to a variety of different background images
#works by converting all white/near-white pixels into transparent pixels
#input images should have white/near-white backgrounds
#threshold controls the degree to which "near-white" pixels are converted into transparent pixels
#(max threshold value is 255=white)
def make_transparent(img, threshold):
    img = img.convert("RGBA")
    datas = img.getdata()

    #transforms white-ish pixels to transparent
    newData = []
    for item in datas:
        if item[0] >= threshold and item[1] >= threshold and item[2] >= threshold:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

#alpha premultiplication
def premultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255:
                r = r * a // 255
                g = g * a // 255
                b = b * a // 255
                pixels[x, y] = (r, g, b, a)

    return 0

#alpha premultiplication
def unmultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255 and a != 0:
                r = 255 if r >= a else 255 * r // a
                g = 255 if g >= a else 255 * g // a
                b = 255 if b >= a else 255 * b // a
                pixels[x, y] = (r, g, b, a)

    return 0

#below: generate large datasets/batches of composite images

#set the size (pixels) of the output images
square_size = 300

#load list of files from database of images of gym interiors (156 files)
path_gym = '/Users/lalooair/ohana/data_sci_proj/insight/gym/images/db_gym-interiors/'
files_gym = os.listdir(path_gym)
files_gym.sort()

if files_gym[0] == '.DS_Store':
    files_gym.pop(0)

#load list of files from database of images of selected class of gym equipment
path_equipment = '/Users/lalooair/ohana/data_sci_proj/insight/gym/images/db_hyperext-bench/'
files_equipment = os.listdir(path_equipment)
files_equipment.sort()

if files_equipment[0] == '.DS_Store':
    files_equipment.pop(0)


#loop over all equipment images in list, 'files_equipment'
for file in files_equipment:
    print file
    #select random subset of 25 gym interiors
    list_gym_images = random.sample(files_gym, 25)
    #loop over each gym interior image
    for gym_image in list_gym_images:
        path_gym_image = os.path.join(path_gym, gym_image)
        path_file = os.path.join(path_equipment, file)

        foreground = Image.open(path_file)
        background = Image.open(path_gym_image)

        #preprocess gym interiors image as the background
        background = adaptive_resize(background, square_size)
        background = centeredSquareCrop(background, square_size)
        background = background.resize((square_size, square_size))

        #preprocess gym equipment image as the foreground
        #use alpha premultiplication here (premultiply, unmultiply)
        foreground = adaptive_padding(foreground)
        foreground = make_transparent(foreground, 200)
        premultiply(foreground)
        foreground = foreground.resize((square_size, square_size))
        unmultiply(foreground)
        foreground = ImageEnhance.Contrast(foreground).enhance(1.1)

        #alpha compositing
        #combine foreground and background
        background = background.convert("RGBA")
        foreground = foreground.convert("RGBA")
        composite_img = Image.alpha_composite(background, foreground)

        #blend/blur composite image with a Gaussian filter
        composite_img = composite_img.filter(ImageFilter.GaussianBlur(radius=0.7))

        #generate new filename for composite image
        gym_filename, _ = os.path.splitext(gym_image)
        equip_filename, _ = os.path.splitext(file)
        path_composite = '/Users/lalooair/ohana/data_sci_proj/insight/gym/images/data_hyperext-bench/'
        composite_filename = os.path.join(path_composite, equip_filename + '-' + gym_filename + '.jpg')

        #save final composite image
        composite_img.save(composite_filename, 'JPEG')