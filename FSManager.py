import json
import os
from FileSystem import FileSystem
from cryptography.fernet import Fernet

class FSManager:

	def __init__( self, metadataAddr ):
		self.metadataAddr = metadataAddr
		self.systems = {}

	
	# safe way to import metadata
	def importMetadata( self ):
		# check metadata file exists
		exists = os.path.exists( self.metadataAddr )
		if not exists:
			cfrm = input( "Unable to locate metadata file '{}'. Create one? (Y/n)\n".format( self.metadataAddr ) )
			if str.lower( cfrm ) != "y":
				print( "Operation aborted." )
				return
			try:
				data_file = open( self.metadataAddr, "w" )
				data_file.close()
			except IOError:
				print ( "Unable to create metadata file." )
				return None
		
		# check metadata file has content to protect from JSON errors
		if os.stat( self.metadataAddr ).st_size == 0:
			if exists:
				print( "Initializing metadata file." )
			try:
				data_file = open( self.metadataAddr, "w" )
			except IOError:
				print ( "Unable to initialize metadata file." )
				return None
			with data_file:
				data_file.write( "{}" )

		try:
			data_file = open( self.metadataAddr, "r+" )
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
		if dataJSON is None:
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
		if dataObj is None:
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

		# overwrite metadata file
		with open( self.metadataAddr, "w" ) as data_file:
			data_file.write( json.dumps( dataObj, indent=3 ) )

		print( "Systems saved." )


	# add a file address to a given system
	def addFileToSystem( self, fsName, addr ):
		if fsName not in self.systems:
			cfrm = input( "System '{}' not in local cache. Load it? (Y/n)\n".format( fsName ) )
			if str.lower( cfrm ) == "y":
				self.loadFileSystem( fsName )
		else:
			self.systems[ fsName ].addFile( addr )
			# save metadata
			self.saveSystems()

	
	# commit a file system
	# def commitFileSystem( self, fsName ):

		# identify every file
		