import json
import os
from FileSystem import FileSystem
from cryptography.fernet import Fernet

class FSManager:

	def __init__( self, metadataAddr ):
		self.metadataAddr = metadataAddr
		self.systems = {}

	
	def importMetadata( self ):
		empty = not os.path.exists( self.metadataAddr ) or os.stat( self.metadataAddr ).st_size == 0
		if empty: # protect from JSON decoding empty file
			return None
		try:
			data_file = open( "metadata.json", "r+" )
		except IOError:
			print ( "Unable to read metadata." )
			return None
		with data_file:
			try:
				data = json.load( data_file )
			except Exception:
				print( "Error decoding metadata file." )
				return None
			return data
	
	# update current file system to match metadata file
	def loadFileSystem( self, fsName ):
		# check if already loaded
		if fsName in self.systems:
			cfrm = input( "File system '{}' already loaded, overwrite cached data? (Y/n)\n".format( fsName ) )
			if str.lower( cfrm ) != "y":
				print( "Operation aborted." )
				return

		# import metadata
		dataJSON = self.importMetadata()
		if not dataJSON:
			print( "Unable to import metadata." )
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

		# grab all systems from metadata file
		dataObj = self.importMetadata()
		if not dataObj:
			print( "Can't save, unable to import metadata." )
			return

		# serialize all cached systems
		serLocalSystems = { name: fs.obj() for name, fs in self.systems.items() }

		# make appropriate changes to existing systems
		for fs in dataObj:
			if fs in serLocalSystems:
				dataObj[ fs ] = serLocalSystems[ fs ] # overwrite with local changes
				del serLocalSystems[ fs ]
		
		# tack on any new systems
		for fs, data in serLocalSystems.items():
			dataObj[ fs ] = data

		# overwrite metadata file, preserve existing un-loaded systems
		with open( self.metadataAddr, "w" ) as data_file:
			data_file.write( json.dumps( dataObj, indent=3 ) )

		print( "Systems saved." )


	# updates the metadata file with each key-value pair given in dict
	def addFileToSystem( self, fsName, addr ):
		self.systems[ fsName ].addFile( addr )

		# save metadata
		self.saveSystems()