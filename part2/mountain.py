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

def conditional_probability_of_row(sample_edge_strength, col, edge_strength):
	max_val = 999999
	max_row = 0
	for row in range(edge_strength.shape[0]):
		prob_edge_str_given_row = sample_edge_strength/sum(edge_strength[row])
		if (prob_edge_str_given_row < max_val):
			max_val = prob_edge_str_given_row
			max_row = row
	return max_row	
'''
def transition_prob_of_row(row, edge_strength):
	max_val = 0;
	for row1 in range(len(edge_strength.shape[0])):
		tr_prob = transmission_probability(row, row1,1.5)
		if tr_prob > max_val:
			max_val = tr_prob
			m'''
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

def construct_ridge2(edge_strength):
	#getting a sample particle
	sampled_edge_strength=[]
	rows = []
	columns = []
      	while (len(columns) <  edge_strength.shape[1] ):
		row = random.randint(0, len(edge_strength));
		column = random.randint(0,len(edge_strength[0]))
		if column not in columns :
			rows.append(row)
			columns.append(column)
			sampled_edge_strength.append(edge_strength[row][column])
		#print len(columns)	
	print sampled_edge_strength
	
	max_val = 0
	#smoothing particles now
	for t in range(1,50):
		for col in range(len(columns)):
			for j in range(len(edge_strength)):
				temp  =  emission_probability(edge_strength,columns[col] , j) * transmission_probability(rows[col-1],rows[col] , 1.5)

				if (temp > max_val):
					max_val = temp
					rows[col] = j 
			#conditional_probability_of_row(sampled_edge_strength[col], columns[col], edge_strength) 
		
	print rows				
	return rows

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
'''for parameter in parameter_list:
	ridge, std_temp = construct_ridge(edge_strength, parameter)
	if min_std > std_temp:
		min_std = std_temp
		blue_ridge = ridge

'''
blue_ridge = construct_ridge2(edge_strength)
# output answer
imsave(output_filename, draw_edge(input_image, red_ridge, (255, 0, 0), 5))
imsave(output_filename, draw_edge(input_image, blue_ridge, (0, 0, 255), 5))
