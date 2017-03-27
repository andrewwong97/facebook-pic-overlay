#!/usr/bin/env python

from PIL import Image
import os, sys

SIZE = 500

def resize_square(im):
	# if  square, make 500x500
	width, height = im.size
	if width > height:
		height = int((SIZE*1.0/width) * height)
		width = SIZE
	else: 
		width = int((SIZE*1.0/height) * width)
		height = SIZE

	im = im.resize((width, height), Image.ANTIALIAS)

def batch():
	''' 
	To run, script must be outside photos directory.
	First command line argument: photos directory

	Usage: python filters.py dirname filter.png

	where filter.png is the name of the filter and it lies within the photo directory
	'''
	
	try:
		foldername = sys.argv[1]
	except IndexError:
		print 'No directory specified. Usage: python filters.py foldername filtername(default=filter.png)'
		sys.exit(1)

	try:
		os.listdir(foldername)
	except OSError, e:
		print 'Not a directory: ' + foldername + '. Usage: python filters.py foldername filtername(default=filter.png)'
		sys.exit(1)
	
	try:
		os.makedirs(foldername + '/out')
	except OSError, e:
		pass

	try:
		filter_path = sys.argv[2]
	except IndexError:
		filter_path = 'filter.png'

	fb_filter = Image.open(foldername + '/' + filter_path)
	for file in os.listdir(foldername):
		# if ends with a valid extension
		if file.endswith('.png') or file.endswith('.jpeg') \
		or file.endswith('.jpg') or file.endswith('.JPG'):
			if 'filter' not in file:
				im = Image.open(foldername + '/' + file)
				print 'Adding', filter_path, 'to ' + file + '...'

				# resize fb filter to image size
				fb_filter = fb_filter.resize(im.size, Image.ANTIALIAS)

				# save regular filter on photo
				im.paste(fb_filter, (0, 0), fb_filter)
				im.save(os.path.join(foldername + '/out', file))

				# black and white
				im = im.convert('L').convert('RGBA')
				# add color filter
				im.paste(fb_filter, (0, 0), fb_filter)
				im.save(os.path.join(foldername + '/out', 'bw_' + file))


if __name__ == '__main__':
	batch()

