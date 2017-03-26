#!/usr/bin/env python

from PIL import Image
import os, sys

SIZE = 500

def batch():
	''' 
	To run, script must be outside photos directory.
	First command line argument: photos directory

	Usage: python filters.py dirname
	'''
	
	try:
		foldername = sys.argv[1]
	except IndexError:
		print 'No directory specified. Usage: python filters.py dirname'
		sys.exit(1)

	try:
		os.listdir(foldername)
	except OSError, e:
		print 'Not a directory: ' + foldername + '. Usage: python filters.py dirname'
		sys.exit(1)
	
	try:
		os.makedirs(foldername + '/out')
	except OSError, e:
		pass

	fb_filter = Image.open(foldername + "/filter.png")
	for file in os.listdir(foldername):
		# if ends with a valid extension
		if file.endswith('.png') or file.endswith('.jpeg') \
		or file.endswith('.jpg') or file.endswith('.JPG'):
			if file != 'filter.png':
				im = Image.open(foldername + '/' + file)
				width, height = im.size

				if width > height:
					height = int((SIZE*1.0/width) * height)
					width = SIZE
				else: 
					width = int((SIZE*1.0/height) * width)
					height = SIZE

				im = im.resize((width, height), Image.ANTIALIAS)
				
				im.paste(fb_filter, (0, 0), fb_filter)
				print 'Adding filter to ' + file + '...'
				im.save(os.path.join(foldername + '/out', file))


if __name__ == '__main__':
	batch()

