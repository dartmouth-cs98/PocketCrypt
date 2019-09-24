from FSManager import FSManager
from cryptography.fernet import Fernet


fsm = FSManager( "metadata.json" )


fsm.loadFileSystem( "myFileSystem" )
fsm.addFileToSystem( "myFileSystem", "myFile.txt")
fsm.addFileToSystem( "myFileSystem", "myFile1.txt")
fsm.loadFileSystem( "myNewFileSystem" )
fsm.addFileToSystem( "myNewFileSystem", "myFile.txt")

fsm.encryptFileSystem( "myFileSystem" )
fsm.encryptFileSystem( "myNewFileSystem" )


# fsm.saveSystems()





