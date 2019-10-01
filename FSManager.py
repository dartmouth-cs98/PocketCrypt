import json
import random
# import msvcrt
import os
import shutil
from datetime import datetime
import time
from tinydb import TinyDB, Query
from tinydb.operations import set as tinySet
from cryptography.fernet import Fernet
from google_handler import GoogleDriveHandler
from dropbox_handler import DropboxHandler

# helper function to see if 'q' is in keyboard buffer
def qInBuffer():
	return True
	while msvcrt.kbhit(): # exists letters in keyboard buffer
		if msvcrt.getch().decode() == 'q': # pop a letter
			return True
	return False

class FSManager:

	def __init__( self, metadataAddr ):
		self.db = TinyDB( metadataAddr )
		self.db.table( 'systems' )
		self.db.table( 'settings' )
	

	# create new file system and save it
	def createFileSystem( self, fsName, equip ):

		# check already exists
		info = self.getSystemInfo( fsName )
		if info is not None:
			cfrm = input( "> File system '{}' already exists, overwrite saved data? (Yes/no)\n".format( fsName ) )
			if str.lower( cfrm ) != "yes":
				print( "> Operation aborted." )
				return			

		# create new filesystem
		systems = self.db.table( 'systems' )
		System = Query()
		systems.upsert( {
			'name': fsName,
			'key': Fernet.generate_key().decode() # UTF-8
		}, System.name == fsName )
		print( "> File system '{}' created.".format( fsName ) )

		# equip if desired
		if equip:
			self.equipFileSystem( fsName )
		# print( "> Unable to create system '{}'.".format( args.fsName ) )

	# equip a given file system
	def equipFileSystem( self, fsName ):

		# ensure existence of file system
		info = self.getSystemInfo( fsName )
		if info is None:
			cfrm = input( "> System '{}' not found. Create and equip it? (Y/n)\n".format( fsName ) )
			if str.lower( cfrm ) == "y":
				self.createFileSystem( fsName, False )
			else:
				print( "> Operation aborted" )
				return
		
		# update equipped system
		self.setSetting( 'equipped', fsName )

		print( "> Equipped '{}'".format( fsName ) )

	# get the info for a given file system
	def getSystemInfo( self, fsName ):
		# all systems are documents with name: ...
		systems = self.db.table( 'systems' )
		System = Query()
		res = systems.search( System.name == fsName )
		if len( res ) != 1 or 'name' not in res[ 0 ]:
			return None 
		return res[ 0 ]

	# get the value of a given internal setting
	def getSetting( self, key ):

		# all settings are documents with key: ..., value: ...
		settings = self.db.table( 'settings' )
		Setting = Query()
		res = settings.search( Setting.key == key )
		if len( res ) != 1 or 'key' not in res[ 0 ] or 'value' not in res[ 0 ]:
			return None 
		return res[ 0 ][ 'value' ]

	# set the value of a given internal setting
	def setSetting( self, key, value ):
		# all settings are documents with key: ..., value: ...
		settings = self.db.table( 'settings' )
		Setting = Query()
		settings.upsert( { 'key': key, 'value': value }, Setting.key == key )

	# get the equipped system and ensure it exists
	def getEquippedSystem( self ):
		
		# check settings table for equipped system
		equippedSystem = self.getSetting( 'equipped' )
		if equippedSystem is None:
			print( "> No file system equipped. Equip one using the 'equip' command!" )
			return
	
		# ensure existence of system
		systems = self.db.table( 'systems' )
		System = Query()
		if not systems.contains( System.name == equippedSystem ):
			cfrm = input( "> Equipped system no longer exists. Create and equip it? (Y/n)\n" )
			if str.lower( cfrm ) == "y":
				self.createFileSystem( equippedSystem, True )
			return equippedSystem
		return equippedSystem

	# show all data about the eqquiped file system
	def showEquippedSystem( self ):

		# get equipped system
		equippedSystem = self.getEquippedSystem()
		
		# get data for equipped system
		info = self.getSystemInfo( equippedSystem )

		if info is None:
			return

		print( json.dumps( info, indent=1 )[ 1: -1 ] )
		# print data
		# print( "> *** {} ***".format( fsName ) )
		# print( ">  - key: {}".format( fsData[ 'key' ] ) )
		# print( ">  - files:" )
		# for fileName, fileData in fsData[ 'files' ].items():
		# 	if fileData:
		# 		fMessage = "encrypted as '{}' at {} UTC".format( fileData[ 'uuid' ],
		# 													 datetime.fromtimestamp( fileData[ 'time' ] ) )
		# 	else:
		# 		fMessage = "not yet encrypted"
		# 	print( ">    - {} {}".format( fileName, fMessage) )

	# show all data about all systems
	def showAllSystems( self ):
		systems = self.db.table( 'systems' )
		print( json.dumps( systems.all(), indent=1 ) )

	# add a file to the equipped system
	def addFileToEquippedSystem( self, addr ):

		# get equipped system
		equippedSystem = self.getEquippedSystem()

		# pull current files
		info = self.getSystemInfo( equippedSystem )
		if info is None:
			return
		files = info[ 'files' ] if 'files' in info else {}

		# ensure non-existence of file
		if addr in files:
			print("> File '{}' already exists in system '{}'".format( addr, equippedSystem ) )
			return
		
		# append file locally
		files[ addr ] = {}
		
		# save to database
		System = Query()
		self.db.table( 'systems' ).update( { 'files': files }, System.name == equippedSystem )

		print( "> File '{}' added to system '{}'.".format( addr, equippedSystem ) )
		
	def removeFileFromEquippedSystem( self, addr ):

		# get equipped system
		equippedSystem = self.getEquippedSystem()
		info = self.getSystemInfo( equippedSystem )

		# ensure existence of file
		files = info[ 'files' ] if 'files' in info else {}
		if addr not in files:
			print( "> File '{}' not found in system '{}'".format( addr, equippedSystem ) )
			return
		
		# remove locally
		del files[ addr ]

		# save to database
		System = Query()
		self.db.table( 'systems' ).update( { 'files': files }, System.name == equippedSystem )
	
	# encrypt currently equipped file system (or a single file)
	def encryptEquippedFileSystem( self, update=False ):

		# get files for equipped system
		equippedSystem = self.getEquippedSystem()
		if equippedSystem is None:
			return
		info = self.getSystemInfo( equippedSystem )
		if info is None:
			print( "> Error: No info found for system '{}'".format( equippedSystem ) )
		files = [ fName for fName, _ in info[ 'files' ].items() ] if 'files' in info else []
		filesInfo = info[ 'files' ] if 'files' in info else []
		if len( files ) == 0:
			print( "> No files to encrypt! Add some using the 'add' command." )
			return

		# get existing filename UUIDs
		existingUUIDs = self.getSetting( 'uuids' )
		if existingUUIDs is None:
			existingUUIDs = []

		# encrypt each file (if appropriate)
		for fAddr in files:
			# determine if appropriate
			encryptIt = False
			if update:
				if 'encrypted' in filesInfo[ fAddr ]:
					if os.path.getmtime( fAddr ) > filesInfo[ fAddr ][ 'encrypted' ]:
						print( "> Change detected in '{}', re-encrypting file.".format( fAddr ) )
						encryptIt = True
			else:
				encryptIt = True

			if encryptIt:
				# check file exists
				if not os.path.exists( fAddr ):
					print( "> File '{}' not found.".format( fAddr ) )
					return
					
				# assign a globally unique ID to the file (32 chars)
				if 'uuid' in filesInfo[ fAddr ]:
					uuid = filesInfo[ fAddr ][ 'uuid' ]
				else:
					while True:
						uuid = "{}".format( hex( random.getrandbits( 128 ) ) )[ 2 : ]
						if uuid not in existingUUIDs:
							break
				
				# encrypt file using filesystem's key
				if 'key' not in info:
					print( "> Error: File system '{}' doesn't have a key".format( equippedSystem ) )
					return
				key = info[ 'key' ]
				with open( fAddr, "rb") as f:
					bData = f.read()
				fHandler = Fernet( key )
				encryptedBData = fHandler.encrypt(bData)

				# write encrypted binary to shadow file in crypt
				if not os.path.exists( 'crypt' ):
					os.mkdir( 'crypt' )
				with open( "crypt/{}".format( uuid ), "wb+") as cryptFile:
					cryptFile.write( encryptedBData )

				print( "> File '{}' encrypted as '{}' using key '{}'.".format( fAddr, uuid, key ) )

				# take timestamp and record in seconds
				filesInfo[ fAddr ][ 'encrypted' ] = round( time.time() )

				# record UUID and add to list of UUIDs
				existingUUIDs.append( uuid )
				if 'uuid' in filesInfo[ fAddr ]: # remove old uuid from master list
					oldUUID = filesInfo[ fAddr ][ 'uuid' ]
					del( existingUUIDs[ existingUUIDs.index( oldUUID ) ] )
				filesInfo[ fAddr ][ 'uuid' ] = uuid
		
		# update database
		self.setSetting( 'uuids', existingUUIDs )
		systems = self.db.table( 'systems' )
		System = Query()
		systems.update( { 'files': filesInfo }, System.name == equippedSystem )

	# continually watch and update a filesystem
	def watchEquippedFileSystem( self ):
		equippedSystem = self.getEquippedSystem()
		while True:
			if qInBuffer():
				print( "> No longer watching '{}'.".format( equippedSystem ) )
				break
			self.encryptEquippedFileSystem( True )
			time.sleep( 1 )

	# import a filesystem from crypt
	def decryptEquippedFileSystem( self, dest="./" ):

		# identify files
		equippedSystem = self.getEquippedSystem()
		info = self.getSystemInfo( equippedSystem )
		if info is None:
			return
		filesInfo = info[ 'files' ] if 'files' in info else []
		if len( filesInfo ) == 0:
			print( "> No files to decrypt! Add some using the 'add' command." )
			return
		
		# prepare destination
		if dest[ -1 ] != '/': # add in '/'
			dest += '/'

		# make sure destination path exists
		if not os.path.exists( dest ):
			print( "> Error: Destination path doesn't exist" )
			return
		
		# make folder for system
		dest +=  "{}/".format( equippedSystem )
		if os.path.exists( dest ):
			cfrm = input( "Folder '{}' already exists. Overwrite it? (Yes/n)\n".format( dest ) )
			if str.lower( cfrm ) != "yes":
				print( "> Operation aborted." )
				return
			else:
				shutil.rmtree( dest )
		os.mkdir( dest )
				
		# import each file
		key = info[ 'key' ]
		for fileName, fileData in filesInfo.items():
			uuid = fileData[ 'uuid' ]
			print( "> Creating {}/{} by decrypting {}".format( dest, fileName, uuid ) )
			
			# import encrypted file from the crypt
			try:
				encryptedFile = open( "crypt/{}".format( uuid ), "rb" )
			except Exception:
				print( "> Unable to open encrypted file." )
				return
			with encryptedFile:
				bData = encryptedFile.read()
			
			# decrypt it using key
			fHandler = Fernet( key )
			decryptedBData = fHandler.decrypt(bData)
			
			# write encrypted binary to plaintext file
			with open( "{}{}".format( dest, fileName ), "wb+") as plainFile:
				plainFile.write( decryptedBData )

	# purge the database
	def clearAllData( self ):
		self.db.purge()
	
	# delete all content associated with a filesystem
	def deleteFileSystem( self, fsName ):
		
		# verify existence
		info = self.getSystemInfo( fsName )
		if info is None:
			cfrm = input( "> File system '{}' not found".format( fsName ) )
			if str.lower( cfrm ) != "yes":
				print( "> Operation aborted" )
				return
		
		# remove document from database
		System = Query()
		self.db.table( 'systems' ).remove( System.name == fsName )

		# delete associated encrypted files
		uuidsToDelete = [ info[ 'files' ][ fileName ].get( 'uuid', None ) for fileName in info[ 'files' ] ] if 'files' in info else []
		existingUUIDs = self.getSetting( 'uuids' )
		for uuid in uuidsToDelete:
			try: # delete the file in the crypt
				os.remove( "crypt/{}".format( uuid ) )
			except:
				pass
			if uuid in existingUUIDs:
				del existingUUIDs[ existingUUIDs.index( uuid ) ]
			else:
				print( "> Warning... there wasn't a UUID to delete..." )		
		
		# update db with new list of UUIDs
		self.setSetting( 'uuids', existingUUIDs )
	
	# push encrypted files for equipped file system to cloud backup service
	def pushEquippedFileSystem( self, cloudService ):

		# update file system
		self.encryptEquippedFileSystem( True )

		# initialize chosen session
		if cloudService == 'drive':
			cloudHandler = GoogleDriveHandler()

		elif cloudService == 'dropbox':
			# get access token if exists
			# accessToken = self.getSetting( 'dbAccessToken' )
			# if accessToken is None:
				# print( "> Initializing dropbox for first time")
			# cloudHandler = DropboxHandler( accessToken )
			cloudHandler = DropboxHandler()
			
			# update saved access code
			self.setSetting( 'dbAccessCode', cloudHandler.access_token )
		else:
			print( "> Error: Unrecognized cloud service" )
			return

		# get UUIDs for equipped system
		equippedSystem = self.getEquippedSystem()
		if equippedSystem is None:
			return
		info = self.getSystemInfo( equippedSystem )
		if info is None:
			print( "> Error: No info found for system '{}'".format( equippedSystem ) )
		filesInfo = info[ 'files' ] if 'files' in info else []
		fileUUIDs = {}
		for fileName, fInfo in filesInfo.items():
			if 'uuid' in fInfo:
				fileUUIDs[ fileName ] = fInfo[ 'uuid' ]

		if len( fileUUIDs ) == 0:
			print( "> No encrypted files to push! Encrypt the equipped filesystem using the 'encrypt' command." )
			return

		print( fileUUIDs )

		# push and timestamp (seconds) each file being pushed
		for fileName, uuid in fileUUIDs.items():

			# push file
			if cloudService == 'drive':
				res = cloudHandler.upsert_file( uuid, "C:/Users/IAMFRANK/Documents/Workspace/cs98/crypt" )
			else:
				res = cloudHandler.upsert_file( uuid, "crypt/{}".format( uuid ), uuid )
			if res is not None:
				print("> Upload successful." )
			else:
				print("> Upload failed." )
				return

			filesInfo[ fileName ][ 'pushed' ] = round( time.time() )
			print( "> Pushing '{}' ({}) to {}".format( uuid, fileName, cloudService ) )

		# update the database
		systems = self.db.table( 'systems' )
		System = Query()
		systems.update( { 'files': filesInfo }, System.name == equippedSystem )

	# pull from the cloud the encrypted file system
	def pullEquippedFileSystem( self, cloudService ):
		# initialize chosen session
		if cloudService == 'drive':
			cloudHandler = GoogleDriveHandler()

		elif cloudService == 'dropbox':
			# get access token if exists
			# accessToken = self.getSetting( 'dbAccessToken' )
			# if accessToken is None:
				# print( "> Initializing dropbox for first time")
			# cloudHandler = DropboxHandler( accessToken )
			cloudHandler = DropboxHandler()
			
			# update saved access code
			self.setSetting( 'dbAccessCode', cloudHandler.access_token )
		else:
			print( "> Error: Unrecognized cloud service" )
			return

		# get UUIDs for equipped system
		equippedSystem = self.getEquippedSystem()
		if equippedSystem is None:
			return
		info = self.getSystemInfo( equippedSystem )
		if info is None:
			print( "> Error: No info found for system '{}'".format( equippedSystem ) )
		filesInfo = info[ 'files' ] if 'files' in info else []
		fileUUIDs = {}
		for fileName, fInfo in filesInfo.items():
			if 'uuid' in fInfo:
				fileUUIDs[ fileName ] = fInfo[ 'uuid' ]

		if len( fileUUIDs ) == 0:
			print( "> No encrypted files to pull! Encrypt the equipped filesystem using the 'encrypt' command and push it using 'push'" )
			return

		# pull and timestamp (seconds) each file being pushed
		for fileName, uuid in fileUUIDs.items():

			# ensure last encryption was before it was pushed
			if 'encrypted' not in filesInfo[ fileName ]:
				print( "> File system not yet encrypted! Encrypt it using 'encrypt' and push using 'push'." )
				return
			if ( filesInfo[ fileName ][ 'encrypted' ] >= filesInfo[ fileName ][ 'pushed' ] ):
				cfrm = input( "> Looks like file '{}' was re-encrypted locally after it was pushed. Resync by pushing now?".format( fileName ) )
				if str.lower( cfrm ) != "yes":
					print( "> Operation aborted." )
					return
				self.pushEquippedFileSystem( cloudService )
				return

			# create crypt if doesn't exist
			if not os.path.exists( 'crypt' ):
				os.mkdir( 'crypt' )

			# pull file
			if cloudService == 'drive':
				res = cloudHandler.download_file( uuid )
			elif cloudService == 'dropbox':
				res = cloudHandler.download_file( "crypt/{}".format( uuid ), uuid )
			else:
				print( "> Error: Unrecognized cloud service" )
				return
			
			if res is not None:
				print("> Download successful." )
			else:
				print(" Download failed." )
				return

			# timestamp with pulled time
			filesInfo[ fileName ][ 'pulled' ] = round( time.time() )
			print( "> Pulling '{}' ({}) from {}".format( uuid, fileName, cloudService ) )

		# update the database
		systems = self.db.table( 'systems' )
		System = Query()
		systems.update( { 'files': filesInfo }, System.name == equippedSystem )


