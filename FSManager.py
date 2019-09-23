import json
import os
from FileSystem import FileSystem

class FSManager:

	def __init__( self, metadataAddr ):
		self.metadataAddr = metadataAddr
		self.systems = {}

	
	# update current file system to match metadata file
	def loadFileSystem( self, name ):
		if name in self.systems:
			cfrm = input( "File system '{}' already loaded, overwrite cached data? (Y/n)\n" )
			if str.lower( cfrm ) != "y":
				print( "Operation aborted." )
				return

		empty = not os.path.exists( self.metadataAddr ) or os.stat( self.metadataAddr ).st_size == 0
		if empty: # protect from JSON decoding empty file
			self.systems[ name ] = None
		if not empty:
			try:
				data_file = open( "metadata.json", "r+" )
			except IOError:
				print ( "Unable to read metadata." )
				self.systems[ name ] = None
				return
			with data_file:
				try:
					rawJSON = json.load( data_file )[ name ]
				except Exception:
					print( "Error decoding meatadata file." )
					self.systems[ name ] = None
					return
			# wrap the file system data in FileSystem object
			newSystem = FileSystem()
			newSystem.files = rawJSON.get( 'files', {} )
			newSystem.key = rawJSON.get( 'key', {} )
			self.systems[ name ] = newSystem

		print( "File system '{}' loaded.".format( name ) )
		print( json.dumps( self.systems[ name ].obj(), indent=2 ) )


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