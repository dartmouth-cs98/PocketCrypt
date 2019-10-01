# Google API test

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import io
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveHandler():

	'''
	Initialize the GoogleDrive connection, build
	Following the quickstart tutorial at
	https://developers.google.com/drive/api/v3/quickstart/python
	'''
	def __init__(self):
		self.creds = None
		try:
			if os.path.exists('token.pickle'):	# token.pickle stores user's access info
				with open('token.pickle', 'rb') as access_token:
					self.creds = pickle.load(access_token)
			if self.creds == None or not self.creds.valid:
				if self.creds != None and self.creds.expired and self.creds.refresh_token != None:
					self.creds.refresh(Request())
				else:
					flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
					self.creds = flow.run_local_server()
				with open('token.pickle', 'wb') as access_token:
					pickle.dump(self.creds, access_token)
			self.service = build('drive', 'v3', credentials=self.creds)
		except Exception as e:
			print("> Error initializing GoogleDriveHandler.")
			print(e)		

	'''
	Upload a file to GoogleDrive
	'''
	def upload_file(self, file_name, local_file_path):
		found = False
		pc_id = None
		response = self.service.files().list(q="mimeType = 'application/vnd.google-apps.folder'", spaces='drive', fields='nextPageToken, files(id, name)').execute()
		for file in response.get('files', []):
			if file.get('name') == "PocketCrypt":
				found = True
				pc_id = file.get('id')
				break
		if not found:
			print("> Could not find PocketCrypt folder; creating new folder called PocketCrypt.")
			pc_id = self.create_new_folder("PocketCrypt")
		if pc_id != None:
			try:
				file_metadata = {'name': file_name, 'parents': [pc_id]}
				media = MediaFileUpload(local_file_path, mimetype='application/octet-stream')
				file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
				print("> File uploaded to Google Drive.")
				return file.get('id')	
			except Exception as e:
				print("> Error uploading file to Google Drive.")
				print(e)
				return None

	'''
	Upsert file in Google Drive
	'''
	def upsert_file(self, file_name, local_file_path):
		found = False
		f_id = None
		query_string = "name = '" + str(file_name) + "'"
		try:
			response = self.service.files().list(q=query_string, spaces='drive', fields='nextPageToken, files(id, name)').execute()
			for file in response.get('files', []):
				if file.get('name') == str(file_name):
					found = True
					f_id = file.get('id')
					break
			if not found:
				print("> File not found. Uploading now...")
				return(self.upload_file(file_name, local_file_path))	# simple upload
			if f_id != None:	# found
				print("> File found. Deleting old version and uploading new file now...")
				self.delete_file(f_id)	# delete other file first
				return(self.upload_file(file_name, local_file_path))
		except Exception as e:
			print("> Could not upsert file to Google Drive.")
			print(e)
			return None

	'''
	Download a file from GoogleDrive
	'''
	def download_file(self, file_name):
		found = False
		f_id = None
		query_string = "name = '" + str(file_name) + "'"
		try:
			response = self.service.files().list(q=query_string, spaces='drive', fields='nextPageToken, files(id, name)').execute()
			for file in response.get('files', []):
				if file.get('name') == str(file_name):
					found = True
					f_id = file.get('id')
					break
		if f_id != None:
			try:
				request = self.service.files().get_media(fileId=f_id)
				fh = io.FileIO(file_name, 'wb')
				downloader = MediaIoBaseDownload(fh, request)
				done = False
				while done == False:
				    status, done = downloader.next_chunk()
				    print("Download " + str(int(status.progress() * 100)) + "%.")
				print("> File downloaded to device.")
				return True
			except Exception as e:
				print("> Error downloading file from Google Drive.")
				print(e)
				return False

	'''
	Delete a file on GoogleDrive
	'''	
	def delete_file(self, file_name):
		found = False
		f_id = None
		query_string = "name = '" + str(file_name) + "'"
		try:
			response = self.service.files().list(q=query_string, spaces='drive', fields='nextPageToken, files(id, name)').execute()
			for file in response.get('files', []):
				if file.get('name') == str(file_name):
					found = True
					f_id = file.get('id')
					break
		if f_id != None:
			try:
				self.service.files().delete(fileId=f_id).execute()
				print("> File deleted from Google Drive.")
				return True
			except Exception as e:
				print("> Error deleting file from Google Drive.")
				print(e)
				return False

	'''
	Create new folder in GoogleDrive
	'''
	def create_new_folder(self, folder_name):
		try:
			folder_metadata = {
				'name': folder_name,
				'mimeType': 'application/vnd.google-apps.folder'
			}
			folder = self.service.files().create(body=folder_metadata, fields='id').execute()
			print("> New folder created.")
			return folder.get('id')
		except Exception as e:
			print("> Error creating folder on Google Drive.")
			print(e)
			return None

gd_handler = GoogleDriveHandler()
# file_id = gd_handler.upload_file("test.dms", "test.dms")
# new_file_id = gd_handler.upsert_file("test.dms", "test.dms")
# file_id = gd_handler.upload_file("test.dms", "test.dms")
print(gd_handler.download_file(new_file_id, "new_test.dms"))
# gd_handler.create_new_folder("helloworld")
# print(gd_handler.delete_file(file_id))


