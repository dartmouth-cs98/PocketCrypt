import dropbox
import requests

APP_KEY = 'agpcqbqfaerrw2d'
APP_SECRET = 'xphukzhg2lon8bx'

class DropboxHandler():

	'''
	Authenticates user, grabs access token, and creates new dbx object
	'''
	def __init__(self, db_access_token):
		try:
			self.access_token = db_access_token
			self.dbx = dropbox.Dropbox(db_access_token)
			print("> DropboxHandler initiated!")
		except Exception as e:
			print("> Access token invalid.")
			try:
				auth_flow = dropbox.oauth.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)	# request user input
				authorize_url = auth_flow.start()
				print("> 1. Go to: " + authorize_url)
				print ("> 2. Click \"Allow\" (you might have to log in first).")
				print (">. 3. Copy the authorization code.")
				auth_code = input("> Enter the authorization code here: ").strip()
				oauth_result = auth_flow.finish(auth_code)
				self.access_token = oauth_result.access_token	# initialize access token
				self.dbx = dropbox.Dropbox(self.access_token)	# create dbx w/ token
			except Exception as e:
				print("> Error initializing DropboxHandler.")
				print(e)

	'''
	Retrieve all filenames as a list
	'''
	def retrieve_all_files(self):
		try:
			return self.dbx.files_list_folder('').entries
		except Exception as e:
			print("> Error retrieving all files.")
			print(e)
			return None

	'''
	Given a file, upload it to dbx
	'''
	def upload_file(self, f, dbx_path):
		try:
			if dbx_path[0] != '/':
				dbx_path = '/' + dbx_path
			with open(f, 'rb') as b_file:
				self.dbx.files_upload(b_file.read(), dbx_path)
			return True
		except Exception as e:
			print("> Error uploading file to Dropbox.")
			print(e)
			return False

	'''
	Delete a file in dbx
	'''
	def delete_file_or_folder(self, dbx_path):
		try:
			if dbx_path[0] != '/':
				dbx_path = '/' + dbx_path
			return self.dbx.files_delete(dbx_path)
		except Exception as e:
			print("> Error deleting file/folder in Dropbox.")
			print(e)
			return None

	'''
	Create new folder in dbx account
	'''
	def create_new_folder(self, dbx_path):
		try:
			if dbx_path[0] != '/':
				dbx_path = '/' + dbx_path
			return self.dbx.files_create_folder(dbx_path)
		except Exception as e:
			print("> Error creating new folder in Dropbox.")
			print(e)
			return None

	'''
	Download a file from dbx to provided path
	'''
	def download_file(self, to_local_path, dbx_path):
		try:
			if dbx_path[0] != '/':
				dbx_path = '/' + dbx_path
			return self.dbx.files_download_to_file(to_local_path, dbx_path)
		except Exception as e:
			print("> Error downloading file from Dropbox to " + str(to_local_path))
			print(e)
			return None

db_handler = DropboxHandler('tNRzKhT8LTAAAAAAAAAAMRSVfjKZdxsuFmv0R5hp1wA')

# db_handler = DropboxHandler()
# db_handler.upload_file("ee07a22a2938efcd83cf4abd4c412007.dms", "/ee07a22a2938efcd83cf4abd4c412007.dms")
# db_handler.create_new_folder("/helloworld")
# db_handler.download_file("../ee07a22a2938efcd83cf4abd4c412007.dms", "/ee07a22a2938efcd83cf4abd4c412007.dms")
# db_handler.delete_file("/ee07a22a2938efcd83cf4abd4c412007.dms")









