#!/usr/bin/python
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2016
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from scipy.misc import imsave
import sys

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return filtered_y**2

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( max(y-thickness/2, 0), min(y+thickness/2, image.size[1]-1 ) ):
            image.putpixel((x, t), color)
    return image

def emission_probability(edge_strength, col, row):
	value = edge_strength.item((row, col))
	max_value = max(edge_strength[:,col])
	value = value/float(max_value*1.5)
	return value

def transmission_probability(row, row1, parameter):
	value = (0.99 - (abs(row1 - row)*parameter)/float(row+1))
	if value < 0:
		value = 0.01
	return value

def construct_ridge(edge_strength, parameter):
	ridge = [0]*len(edge_strength[0])
	expected_ridge = edge_strength.argmax(axis = 0)
	ridge[0] = expected_ridge[0]
	for i in range(1, len(ridge)):
		max_value = 0
		for j in range(len(edge_strength)):
			temp = emission_probability(edge_strength, i, j)*transmission_probability(ridge[i-1], j, parameter)
			if (temp > max_value):
				ridge[i] = j
				max_value = temp
	std_value = std(ridge, ddof = 1)
	return ridge, std_value

def construct_ridge2(edge_strength, input_row, input_col):

	return

# main program
#
(input_filename, output_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# # compute edge strength mask
edge_strength = edge_strength(input_image)
imsave('edges.jpg', edge_strength)

# # You'll need to add code here to figure out the results! For now,
# # just create a horizontal centered line.
red_ridge = edge_strength.argmax(axis = 0)

# Checking solution for different parameters and choosing best one
parameter_list = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
blue_ridge = []
min_std = sys.maxint
for parameter in parameter_list:
	ridge, std_temp = construct_ridge(edge_strength, parameter)
	if min_std > std_temp:
		min_std = std_temp
		blue_ridge = ridge

# output answer
imsave(output_filename, draw_edge(input_image, red_ridge, (255, 0, 0), 5))
imsave(output_filename, draw_edge(input_image, blue_ridge, (0, 0, 255), 5))