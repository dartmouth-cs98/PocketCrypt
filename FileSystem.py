import json
import os

class FileSystem:
	
	def __init__( self ):
		self.key = None
		self.files = None


	def addFile( self, addr ):
		if addr not in self.files:
			self.files.append( addr )


	def obj( self ):
		return { 
			"key": self.key if self.key else None,
			"files": self.files if self.files else None
		}


