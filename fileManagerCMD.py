from FSManager import FSManager
from cryptography.fernet import Fernet

def printHelp( command=None):
	if command == "create":
		print( "Create a file system using the commmand \"create <system>\"." )
	elif command == "show":
		print( "Show data for a file system using the commmand \"show <system>\"." )
	elif command == "encrypt":
		print( "Encrypt a file system using the commmand \"encrypt <system>\"." )
	elif command == "add":
		print( "Add a file to a file system using the commmand \"add <file> to <system>\"." )
	elif spl[ 0 ] == "update":
		print( "Update an encrypted file system using the commmand \"add <file> to <system>\"." )
	elif spl[ 0 ] == "watch":
		print( "Contually watch and update a file system using the commmand \"watch <system>\". \"q\" to exit." )
	else:
		print( "You want some help? You got some!" )

fsm = FSManager( "metadata.json" )

# fsm.createFileSystem( "myFileSystem" )
# fsm.addFileToSystem( "myFileSystem", "myFile.txt")
# fsm.addFileToSystem( "myFileSystem", "myFile1.txt")
# fsm.loadFileSystem( "myNewFileSystem" )
# fsm.addFileToSystem( "myNewFileSystem", "myFile.txt")

# fsm.encryptFileSystem( "myFileSystem" )
# fsm.encryptFileSystem( "myNewFileSystem" )
 
# fsm.updateFileSystem( "myFileSystem" )

# fsm.saveSystems()

# add tab functionality
while True:
	i = input( "Awaiting command...\n" )
	if str.lower( i ) == "q":
		fsm.saveSystems()
		print( "Safely quit." )
		break
	elif str.lower( i ) == "help":
		printHelp()
	else: #command
		spl = i.split( ' ' )
		if spl[ 0 ] == "create":
			if len( spl ) != 2:
				print( "Invalid command format." )
				printHelp( "create" )
			else:
				fsm.createFileSystem( spl[ 1 ] )
		
		elif spl[ 0 ] == "show":
			if len( spl ) != 2:
				print( "Invalid command format." )
				printHelp( "show" )
			else:
				fsm.showFileSystem( spl[ 1 ] )
		
		elif spl[ 0 ] == "encrypt":
			if len( spl ) != 2:
				print( "Invalid command format." )
				printHelp( "encrypt" )
			else:
				fsm.encryptFileSystem( spl[ 1 ] )

		elif spl[ 0 ] == "add":
			if len( spl ) != 4 or spl[ 2 ] != "to":
				print( "Invalid command format." )
				printHelp( "add" )
			else:
				fsm.addFileToSystem( spl[ 3 ], spl[ 1 ] )

		elif spl[ 0 ] == "update":
			if len( spl ) != 2:
				print( "Invalid command format." )
				printHelp( "update" )
			else:
				fsm.updateFileSystem( spl[ 1 ] )

		elif spl[ 0 ] == "watch":
			if len( spl ) != 2:
				print( "Invalid command format." )
				printHelp( "update" )
			else:
				fsm.watchFileSystem( spl[ 1 ] )

		else:
			print( "Command not recognized. Type \"help\" for help!" )
		

	






