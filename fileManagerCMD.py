#!/usr/bin/env python

from FSManager import FSManager
import os
import argparse
import sys
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

class PocketCrypt():
	
	def __init__( self ):

		# get address for metadata file (TODO: ENV VAR will distiguish from default location)
		metadataAddr = "metadata.json"

		# check metadata file exists
		exists = os.path.exists( metadataAddr )
		if not exists:
			cfrm = input( "Unable to locate metadata file '{}'. Create one? (Y/n)\n".format( metadataAddr ) )
			if str.lower( cfrm ) != "y":
				print( "> Operation aborted." )
			else:
				try:
					open( metadataAddr, "w" ).close()
				except IOError:
					print ( "> Unable to create metadata file." )

		self.fsm = FSManager( metadataAddr )
		print( "> Initialized PocketCrypt with metadata file: '{}'".format( metadataAddr ))

		parser = argparse.ArgumentParser( description='PocketCrypt!', usage='''pc <command> [<args>]''')
		parser.add_argument( 'command', help='Subcommand to run' )
		args = parser.parse_args( sys.argv[ 1 : 2 ] )
		if not hasattr( self, args.command ):
			print( '> Unrecognized command.' )
			parser.print_help()
			exit( 1 )
		getattr( self, args.command )()


	def create( self ):
		parser = argparse.ArgumentParser( description='Create a File System' )
		parser.add_argument( 'fsName', help='Name of File System' )
		args = parser.parse_args( sys.argv[ 2 : ] )
		self.fsm.createFileSystem( args.fsName )

	def equip( self ):
		parser = argparse.ArgumentParser( description='Eqiup a File System' )
		parser.add_argument( 'fsName', help='Name of File System' )
		args = parser.parse_args( sys.argv[ 2 : ] )
		print( "equipping {}".format( args.fsName ) )
		self.fsm.equipFileSystem( args.fsName )

	def show( self ):
		parser = argparse.ArgumentParser( description='Show details of equipped File System' )
		parser.add_argument( 'fsName', help='Name of File System' )
		args = parser.parse_args( sys.argv[ 2 : ] )
		print( "showing {}".format( args.fsName ) )
		# fsm.showFileSystem( spl[ 1 ] )

	def encrypt( self ):
		parser = argparse.ArgumentParser( description='Encrypt an entire File System' )
		parser.add_argument( 'fsName', help='Name of File System' )
		args = parser.parse_args( sys.argv[ 2 : ] )
		print( "encrypting {}".format( args.fsName ) )
		# fsm.encryptFileSystem( spl[ 1 ] )

	def add( self ):
		parser = argparse.ArgumentParser( description='Add a file to the currently equipped File System.' )
		parser.add_argument( 'fileName', help='Address of file to add' )
		args = parser.parse_args( sys.argv[ 2 : ] )
		print( "adding {} to file system".format( args.fileName )  )
		# fsm.addFileToSystem( spl[ 3 ], spl[ 1 ] )

	def remove( self ):
		parser = argparse.ArgumentParser( description='Remove a file from the currently equipped File System.' )
		parser.add_argument( 'fileName', help='Address of file to remove' )
		args = parser.parse_args( sys.argv[ 2 : ] )
		print( "removing {} to file system".format( args.fileName )  )
		# fsm.removeFileFromSystem( spl[ 3 ], spl[ 1 ] )

	def update( self ):
		parser = argparse.ArgumentParser( description='Check the equipped File System and re-encrypt and sync any files that are out-of-date.' )
		parser.parse_args( sys.argv[ 2 : ] )
		# fsm.updateFileSystem( spl[ 1 ] )

	def watch( self ):
		parser = argparse.ArgumentParser( description='Continually watch all files in equipped File System and re-encrypt and sync as they are modified.' )
		parser.parse_args( sys.argv[ 2 : ] )
		# fsm.watchFileSystem( spl[ 1 ] )


	def decrypt( self ):
		parser = argparse.ArgumentParser( description='Import a File System from the cloud and decrypt it.' )
		parser.add_argument( 'fsName', help='Name of File System to decrypt' )
		parser.parse_args( sys.argv[ 2 : ] )
		# fsm.importFileSystem( spl[ 1 ] )
		# TODO: Add option for File System destination
	

	def clear( self ):
		parser = argparse.ArgumentParser( description='Clear all files from a given File System.' )
		parser.add_argument( 'fsName', help='Name of File System to clear' )
		parser.parse_args( sys.argv[ 2 : ] )
		# fsm.clearFilesFromSystem( spl[ 1 ] )


if __name__ == '__main__':
	PocketCrypt()
