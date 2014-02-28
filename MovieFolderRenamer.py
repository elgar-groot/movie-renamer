#!/usr/bin/python

import os
from glob import *
from shutil import *
import sys
from re import *

from httplib import *
import json

class MovieFolderRenamer:
	'''A class that can update all movie folder names in a specified folder 
	to include the year, so Couchpotato will recognize them.
	Makes use of omdbapi.com'''

	def __init__(self, movie_folder):
		self.connection = HTTPConnection("www.omdbapi.com")
		self.movie_folder = movie_folder if movie_folder[-1]=='/' else movie_folder+'/' 
		self.re = compile('.*\([0-9]{4}\)')

	def rename_folder(self, folder):

		name = os.path.basename(folder).replace(' ', '%20')
		self.connection.request("GET", "/?s=" + name)
		answer = self.connection.getresponse().read()

		try:
			js = json.loads(answer)
			year = js['Search'][0]['Year']
			new_name = name + ' ('+year+')'
			os.rename(folder, self.movie_folder+new_name)
			print 'Renaming', name, ' << ', new_name
		except:
			print 'Unable to rename: ', name


	def rename(self):
		folders = glob(self.movie_folder+'*')
		for folder in folders:
			if( self.re.match(folder) == None):
				self.rename_folder(folder)

def main():
	try:
		movie_folder = sys.argv[1]
		renamer = MovieFolderRenamer(movie_folder)
		renamer.rename()

	except IndexError as err:
		print >>sys.stderr, "Usage: {0} path_to_moviefolder".format(sys.argv[0])
		return 1

# main method call
if __name__ == "__main__":
	main()
