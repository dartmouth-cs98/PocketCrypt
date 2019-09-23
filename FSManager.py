import json
import os
from FileSystem import FileSystem
from cryptography.fernet import Fernet

class FSManager:

	def __init__( self, metadataAddr ):
		self.metadataAddr = metadataAddr
		self.systems = {}

	
	# update current file system to match metadata file
	def loadFileSystem( self, fsName ):
		if fsName in self.systems:
			cfrm = input( "File system '{}' already loaded, overwrite cached data? (Y/n)\n".format( fsName ) )
			if str.lower( cfrm ) != "y":
				print( "Operation aborted." )
				return

		empty = not os.path.exists( self.metadataAddr ) or os.stat( self.metadataAddr ).st_size == 0
		if empty: # protect from JSON decoding empty file
			self.systems[ fsName ] = None
		if not empty:
			try:
				data_file = open( "metadata.json", "r+" )
			except IOError:
				print ( "Unable to read metadata." )
				self.systems[ fsName ] = None
				return
			with data_file:
				try:
					dataJSON = json.load( data_file )
				except Exception:
					print( "Error decoding meatadata file." )
					self.systems[ fsName ] = None
					return

			if fsName not in dataJSON:
				isNew = True
				cfrm = input( "File system '{}' doesn't exist. Initialize one? (Y/n)\n".format( fsName ) )
				if str.lower( cfrm ) != "y":
					print( "Operation aborted." )
					return
			else:
				isNew = False

			# wrap the file system data in a FileSystem object
			newSystem = FileSystem()
			if isNew:
				newSystem.files = {}
				newSystem.key = Fernet.generate_key().decode() # UTF-8
			else:
				newSystem.files = dataJSON[ fsName ][ 'files' ]
				newSystem.key = dataJSON[ fsName ][ 'key' ]
			
			self.systems[ fsName ] = newSystem

		print( "File system '{}' loaded.".format( fsName ) )
		print( json.dumps( self.systems[ fsName ].obj(), indent=2 ) )


	# update metadata file to match given list of file systems
	def saveSystems( self ):
		# serialize all systems
		obj = { name: fs.obj() for name, fs in self.systems.items() }

		# overwrite metadata file
		with open( self.metadataAddr, "w" ) as data_file:
			data_file.write( json.dumps( obj, indent=3 ) )

		print( "Systems saved." )


	# updates the metadata file with each key-value pair given in dict
	def addFileToSystem( self, fsName, addr ):
		self.systems[ fsName ].addFile( addr )

		# save metadata
		self.saveSystems()