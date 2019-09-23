from FileSystem import FileSystem
from cryptography.fernet import Fernet

# def saveKey():
# 		# generate a random key
# 		key = Fernet.generate_key()

# 		# save the key
# 		created = writeData( "key", key )

# 		if created:
# 			print( "Key created!" )
# 		else:
# 			print( "Key overwritten!" )


fs = FileSystem( "metadata.json" )

fs.writeData( { "testKey1": "testValue1", "testKey2": { "testValue22": 22 } } )