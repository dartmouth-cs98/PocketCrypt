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
	def encryptFileSystem( self, fsName ):

		# sync local -> file -> local
		self.saveSystems()
		self.data = self.importMetadata()
		if self.data is None:
			print( "Unable to commit, couldn't import metadata." )
			return

		# encrypt each file
		for fAddr in self.data[ 'systems' ][ fsName ][ 'files' ]:
			# check file exists
			if not os.path.exists( fAddr ):
				print( "File '{}' not found.".format( fAddr ) )
				return
			else:
				# assign a globally unique ID to the file (32 chars)
				uuids = []
				for __, data in self.data[ 'systems' ].items():
					for __, id in data[ 'files' ].items():
						uuids.append( id )
				while True:
					uuid = "{}".format( hex( random.getrandbits( 128 ) ) )[ 2 : ]
					if uuid not in uuids:
						break
				self.data[ 'systems' ][ fsName ][ 'files' ][ fAddr ] = uuid

			# encrypt file using filesystem's key
			with open( fAddr, "rb") as f:
				bData = f.read()
			
			fHandler = Fernet( self.data[ 'systems' ][ fsName ][ 'key' ] )
			encryptedBData = fHandler.encrypt(bData)

			# write encrypted binary to shadow file in crypt
			with open( "crypt/{}".format( uuid ), "wb+") as cryptFile:
				cryptFile.write(encryptedBData)


		# write systems
		self.saveSystems()
 
	




				


			