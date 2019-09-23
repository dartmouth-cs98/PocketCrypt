import json
import os

class FileSystem:
	
	def __init__( self, metadataAddr ):
		self.metadataAddr = metadataAddr
		self.data = None
		self.updateLocalData() # pull down metadata

		print( "File system loaded. Data: ")
		print( self.data )


	# update cached data to match metadata file
	def updateLocalData( self ):
		empty = not os.path.exists( self.metadataAddr ) or os.stat( self.metadataAddr ).st_size == 0
		if empty: # protect from JSON decoding empty file
			self.data = {}
		else:
			try:
				data_file = open( "metadata.json", "r+" )
			except IOError:
				print ( "Unable to read metadata." )
				self.data = None
				return
			with data_file:
				try:
					self.data = json.load( data_file )
				except Exception:
					print( "Error decoding meatadata file." )
					self.data = None
					return


	# update metadata file to match cached data
	def updateFileData( self ):
		with open( "metadata.json", "w" ) as data_file:
			data_file.write( json.dumps( self.data, indent=3 ) )


	# updates the metadata file with each key, value pair given in dict of { k: v } pairs to metadata file
	def writeData( self, kvPairs ):
		# manipulate data
		for key, value in kvPairs.items():
			self.data[ key ] = value

		# save metadata
		self.updateFileData()


	def getValue( self, key ):
		return self.data[ key ]
		

