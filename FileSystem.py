import json
import os

class FileSystem:
	
	def __init__( self, metadataAddr ):
		self.metadataAddr = metadataAddr


	# updates the metadata file with each key, value pair given in dict of { k: v } pairs to metadata file
	def writeData( self, kvPairs ):
		# import data
		empty = not os.path.exists( self.metadataAddr ) or os.stat( self.metadataAddr ).st_size == 0
		if empty: # protect from JSON decoding empty file
			data = {}
		else:
			try:
				data_file = open( "metadata.json", "r+" )
			except IOError:
				print ( "Unable to read metadata" )
				return
			with data_file:
				try:
					data = json.load( data_file )
				except Exception:
					print( "Error decoding meatadata file." )
					return

		# manipulate data
		for key, value in kvPairs.items():
			data[ key ] = value

		# save to file
		with open ( "metadata.json", "w" ) as data_file:
			data = data_file.write( json.dumps( data, indent=3 ) )

		return

	# returns None or value in metadata
	def getData( self, key ):
		# import data
		empty = not os.path.exists( self.metadataAddr ) or os.stat( self.metadataAddr ).st_size == 0
		if empty: # protect from JSON decoding empty file
			return None
		else:
			try:
				data_file = open( "metadata.json", "r+" )
			except IOError:
				print ( "Unable to read metadata" )
				return
			with data_file:
				try:
					data = json.load( data_file )
				except Exception:
					print( "Error decoding meatadata file." )
					return
			return data[ key ]
		

