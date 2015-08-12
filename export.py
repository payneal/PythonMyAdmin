#!/usr/bin/env python3
#import os

#input: filename(string), python dict
#output: creates file and writes dict if it doesn't exist, else append to file.
def writeToFile(filename, dictin):
	try:
		openfile = open(filename, 'a')
		openfile.write(str(dictin)+'\n')
		openfile.close()
		return 1
	except:
		return 0

