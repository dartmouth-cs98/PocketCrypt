import json
import os

class FileSystem:
	
	def addFile( self, addr ):
		if addr not in self.files:
			self.files.append( addr )


	def obj( self ):
		return { 
			"key": self.key if self.key else None,
			"files": self.files if self.files else []
		}


