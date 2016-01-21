#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import httplib2
import sys
import logging
import pprint
from apiclient.http import MediaFileUpload

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
#from oauth2client.tools import run


root = logging.getLogger()

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


# For this example, the file to upload is a command-line argument
client_id = '530533340348.apps.googleusercontent.com'
client_secret = 'jsS3p0NgPDN6oIIz-SfhZxtF'   

file_to_upload = sys.argv[1]

# The scope URL for read/write access to a user's drive data
scope = 'https://www.googleapis.com/auth/drive'

# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

def main():

  # Create a Storage object. This object holds the credentials that your
  # application needs to authorize access to the user's data. The name of the
  # credentials file is provided. If the file does not exist, it is
  # created. This object can only hold credentials for a single user, so
  # as-written, this script can only handle a single user.
  storage = Storage('credentials.dat')

  # The get() function returns the credentials for the Storage object. If no
  # credentials were found, None is returned.
  credentials = storage.get()
  
  #logging.error("file name "+file_to_upload)

  # If no credentials are found or the credentials are invalid due to
  # expiration, new credentials need to be obtained from the authorization
  # server. The oauth2client.tools.run() function attempts to open an
  # authorization server page in your default web browser. The server
  # asks the user to grant your application access to the user's data.
  # If the user grants access, the run() function returns new credentials.
  # The new credentials are also stored in the supplied Storage object,
  # which updates the credentials.dat file.
  if credentials is None or credentials.invalid:
    credentials = run(flow, storage)

  # Create an httplib2.Http object to handle our HTTP requests, and authorize it
  # using the credentials.authorize() function.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # The apiclient.discovery.build() function returns an instance of an API service
  # object can be used to make API calls. The object is constructed with
  # methods specific to the drive API. The arguments provided are:
  #   name of the API ('drive')
  #   version of the API you are using ('v3')
  #   authorized httplib2.Http() object that can be used for API calls
  drive_service = build('drive', 'v2', http=http)

  try:

    # Upload File to drive    
    # Insert a file
    media_body = MediaFileUpload(file_to_upload, mimetype='image/jpeg', resumable=True)
    body = {
      'title': file_to_upload,
      'description': 'general image',
      'mimeType': 'image/jpeg'
    }
    
    file = drive_service.files().insert(body=body, media_body=media_body).execute()
    print 'OK'
    #pprint.pprint(file)

  except AccessTokenRefreshError:
    # The AccessTokenRefreshError exception is raised if the credentials
    # have been revoked by the user or they have expired.
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')

if __name__ == '__main__':
  main()
