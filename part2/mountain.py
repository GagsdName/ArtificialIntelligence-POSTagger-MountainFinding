#!/usr/bin/python
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2016
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from scipy.misc import imsave
import operator
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

def emission_probability(max_value, w1, row):
	value = w1.item(row)
	value = value/float(max_value)
	return value

def transition_probability(row, rows):
	list_dist = [0]*len(rows)
	dist_dict = {}
	for i in range(len(rows)):
		if rows[i] == row:
			dist_dict.update({i: float(0.8)})	
		else:
			dist_dict.update({i: float(1)/abs(rows[i]*rows[i] - row*row)})
	return dist_dict

def probability_distribution(col, rows, row0, row2, w1):
	p_list = [0]*len(rows)
	max_value = max(w1)
	value_dict = {}
	if row0 != -1:
		trans_row0 = transition_probability(row0, rows)
	if row2 != -1:
		trans_row2 = transition_probability(row2, rows)
	for i in range(len(rows)):
		if row0 == -1:
			value = trans_row2[i]*emission_probability(max_value, w1, rows[i])
			value_dict.update({i : value})
		elif row2 == -1:
			value = trans_row0[i]*emission_probability(max_value, w1, rows[i])
			value_dict.update({i : value})
		else:
			value = trans_row2[i]*trans_row0[i]*(emission_probability(max_value, w1, rows[i]))
			value_dict.update({i : value})
	sum_values = sum(value_dict.values())
	for i in range(len(rows)):
		p_list[i] = float(value_dict[i])/sum_values
	return p_list

def construct_ridge2(edge_strength):
	#getting a sample particle
	ridge = random.choice(len(edge_strength), len(edge_strength[0]), replace=True)
	#smoothing particles now
	for t in range(len(edge_strength[0])):
		print t
		for i in range(len(ridge)):
			rows = []
			row0 = ridge[i-1] if i-1>=0 else -1
			row2 = ridge[i+1] if i+1 < len(ridge)-1 else -1
			if row0 != -1:
				rows += get_pruned_rows(row0, len(edge_strength)/4)
			if row2 != -1:
				rows += get_pruned_rows(row2, len(edge_strength)/4)
			rows= list(set(rows))
			p_list = probability_distribution(i, rows,row0, row2, edge_strength[:,i])
			ridge[i] = random.choice(rows, p=p_list)
		print std(ridge, ddof=1)
	return ridge

def get_pruned_rows(rowi, prune):
	rows = []
	start = 0 if rowi-prune < 0 else rowi-prune
	end = len(edge_strength) - 1 if rowi+prune > len(edge_strength) - 1 else rowi+prune
	rows = range(start, end)
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
# output answer
blue_ridge = construct_ridge2(edge_strength)

green_ridge = construct_ridge3(edge_strength)
imsave(output_filename, draw_edge(input_image, red_ridge, (255, 0, 0), 5))
imsave(output_filename, draw_edge(input_image, blue_ridge, (0, 0, 255), 5))
