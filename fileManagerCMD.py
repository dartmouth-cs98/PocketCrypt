from FSManager import FSManager
from cryptography.fernet import Fernet


def saveKey( fs ):
	# generate a random key
	key = Fernet.generate_key()

	# check if key already exists
	if fs.getValue( "key" ):
		cfrm = input( "Key already exists! Overwrite? (Y/n)\n" )
		if str.lower( cfrm ) == "y":
			fs.writeData( { "key": key.decode() } )
			print( "Key overwritten." )
		else:
			print( "Operation aborted." )
	return key


FSManager = FSManager( "metadata.json" )

# FSManager.loadFileSystem( "myFileSystem" )

# FSManager.addFileToSystem( 'myFileSystem', "myFile.txt")

FSManager.loadFileSystem( "myNewFileSystem" )

# FSManager.saveSystems()





