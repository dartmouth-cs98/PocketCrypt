import json
import random
import os
import time
from cryptography.fernet import Fernet

class FSManager:

	def __init__( self, metadataAddr ):
		self.metadataAddr = metadataAddr
		self.data = { 'systems': {} }

	
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
				data_file.write( json.dumps( { "systems": {} }, indent=3 ) )

		# decode the JSON
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
		if fsName in self.data[ 'systems' ]:
			cfrm = input( "File system '{}' already loaded, overwrite cached data? (Y/n)\n".format( fsName ) )
			if str.lower( cfrm ) != "y":
				print( "Operation aborted." )
				return

		# import metadata
		newData = self.importMetadata()
		if newData is None:
			print( "Unable to import metadata." )
			return

		if fsName not in newData[ 'systems' ]:
			isNew = True
			cfrm = input( "File system '{}' doesn't exist. Initialize one? (Y/n)\n".format( fsName ) )
			if str.lower( cfrm ) != "y":
				print( "Operation aborted." )
				return
		else:
			isNew = False

		# create new filesystem in memory
		newSystem = {}
		if isNew:
			newSystem[ 'files' ] = {}
			newSystem[ 'key' ] = Fernet.generate_key().decode() # UTF-8
		else:
			newSystem[ 'files' ] = newData[ 'systems' ][ fsName ][ 'files' ]
			newSystem[ 'key' ] = newData[ 'systems' ][ fsName ][ 'key' ]
		
		self.data[ 'systems' ][ fsName ] = newSystem

		print( "File system '{}' loaded.".format( fsName ) )
		print( json.dumps( self.data[ 'systems' ][ fsName ], indent=2 ) )


	# update metadata file to match given list of file systems
	def saveSystems( self ):

		# grab data metadata file
		existingData = self.importMetadata()
		if existingData is None:
			print( "Can't save, unable to import existing metadata." )
			return

		# make appropriate changes to existing systems
		for fs in existingData[ 'systems' ]:
			if fs in self.data[ 'systems' ]:
				existingData[ 'systems' ][ fs ] = self.data[ 'systems' ][ fs ] # overwrite with local changes
		
		# tack on any new systems
		for fs, data in self.data[ 'systems' ].items():
			existingData[ 'systems' ][ fs ] = data

		# overwrite metadata file
		with open( self.metadataAddr, "w" ) as data_file:
			data_file.write( json.dumps( existingData, indent=3 ) )

		print( "Systems saved." )


	# add a file address to a given system
	def addFileToSystem( self, fsName, addr ):
		if fsName not in self.data[ 'systems' ]:
			cfrm = input( "System '{}' not in memory. Load it? (Y/n)\n".format( fsName ) )
			if str.lower( cfrm ) == "y":
				self.loadFileSystem( fsName )
		else:
			if addr not in self.data[ 'systems' ][ fsName ][ 'files' ]:
				self.data[ 'systems' ][ fsName ][ 'files' ][ addr ] = None # UID assigned during encrypting
			# save metadata
			self.saveSystems()

	
	# commit a file system
	# def encryptFileSystem( self, fsName ):

	# 	# ensure systems are written
	# 	self.saveSystems()

	# 	# fetch metadata for each file under the system
	# 	dataJSON = self.importMetadata()
	# 	if dataJSON is None:
	# 		print( "Unable to commit, couldn't import metadata." )
	# 		return
	# 	files = dataJSON[ 'systems' ][ fsName ][ 'files' ]

	# 	for f in files:
	# 		# check file exists
	# 		if not os.path.exists( f ):
	# 			print( "File '{}' not found.".format( f ) )
	# 			return
	# 		else:
	# 			# assign a globally unique ID to the file (32 chars)
	# 			# while True:
	# 			uuid = "{}".format( hex( random.getrandbits( 128 ) ) )[ 2 : ]
	# 				# if uuid not in ( id for  in ):
	# 				# 	break
	# 			files[ f ] = uuid
	# 			print( uuid )
		
	# 	# write systems
	# 	self.saveSystems()
					

				


			