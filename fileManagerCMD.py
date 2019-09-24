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


fsm = FSManager( "metadata.json" )


fsm.loadFileSystem( "myFileSystem" )
fsm.addFileToSystem( 'myFileSystem', "myFile.txt")
# fsm.loadFileSystem( "myNewFileSystem" )

# fsm.commitFileSystem( "myFileSystem" )

fsm.saveSystems()





