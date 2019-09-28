from FSManager import FSManager
from cryptography.fernet import Fernet

def printHelp( command=None):
	if command == "create":
		print( "> Create a file system using the commmand \"create <system>\"." )
	elif command == "show":
		print( "> Show data for a file system using the commmand \"show <system>\"." )
		print( "> Show all file systems using the commmand \"show all systems\"." )
	elif command == "encrypt":
		print( "> Encrypt a file system using the commmand \"encrypt <system>\"." )
	elif command == "add":
		print( "> Add a file to a file system using the commmand \"add <file> to <system>\"." )
	elif command == "update":
		print( "> Update an encrypted file system using the commmand \"update <system>\"." )
	elif command == "watch":
		print( "> Contually watch and update a file system using the commmand \"watch <system>\". \"q\" to exit." )
	elif command == "import":
		print( "> Import and decrypt a file system from the crypt using the commmand \"add <file> to <system>\"." )
	elif command == "clear":
		print( "> Clear files for a specific system by using the commmand \"clear <system>\"." )
		print( "> Clear all metadata by using the commmand \"clear all data\"." )
	elif command == "remove":
		print( "> Remove a file for a specific system by using the commmand \"remove <file> from <system>\"." )

	else:
		print( "> Read the readme, silly! The commands are create, show, encrypt, add, update, watch, import, clear, and remove. Type any of these into the prompt to see more help for each one!" )

fsm = FSManager( "metadata.json" )


while True:
	i = input( "> Awaiting command...\n" )
	if str.lower( i ) == "q":
		fsm.saveSystems()
		print( "> Safely quit." )
		break
	elif str.lower( i ) == "help":
		printHelp()
	else: #command
		spl = i.split( ' ' )
		if spl[ 0 ] == "create":
			if len( spl ) != 2:
				print( "> Invalid command format." )
				printHelp( "create" )
			else:
				fsm.createFileSystem( spl[ 1 ] )
		
		elif spl[ 0 ] == "show":
			if spl == [ 'show', 'all', 'systems' ]:
				fsm.showAllSystems()
			elif len( spl ) == 2:
				fsm.showFileSystem( spl[ 1 ] )
			else:
				print( "> Invalid command format." )
				printHelp( "show" )
		
		elif spl[ 0 ] == "encrypt":
			if len( spl ) != 2:
				print( "> Invalid command format." )
				printHelp( "encrypt" )
			else:
				fsm.encryptFileSystem( spl[ 1 ] )

		elif spl[ 0 ] == "add":
			if len( spl ) != 4 or spl[ 2 ] != "to":
				print( "> Invalid command format." )
				printHelp( "add" )
			else:
				fsm.addFileToSystem( spl[ 3 ], spl[ 1 ] )
		
		elif spl[ 0 ] == "remove":
			if len( spl ) != 4 or spl[ 2 ] != "from":
				print( "> Invalid command format." )
				printHelp( "remove" )
			else:
				fsm.removeFileFromSystem( spl[ 3 ], spl[ 1 ] )

		elif spl[ 0 ] == "update":
			if len( spl ) != 2:
				print( "> Invalid command format." )
				printHelp( "update" )
			else:
				fsm.updateFileSystem( spl[ 1 ] )

		elif spl[ 0 ] == "watch":
			if len( spl ) != 2:
				print( "> Invalid command format." )
				printHelp( "update" )
			else:
				fsm.watchFileSystem( spl[ 1 ] )
		
		elif spl[ 0 ] == "import":
			if len( spl ) != 2:
				print( "> Invalid command format." )
				printHelp( "import" )
			else:
				fsm.importFileSystem( spl[ 1 ] )

		elif spl[ 0 ] == "clear":
			if spl == [ 'clear', 'all', 'data' ]:
				fsm.clearAllData()
			elif len( spl ) == 2:
				fsm.clearFilesFromSystem( spl[ 1 ] )
			else:
				print( "> Invalid command format." )
				printHelp( "clear" )

		else:
			print( "> Command not recognized. Type \"help\" for help!" )
		

	






