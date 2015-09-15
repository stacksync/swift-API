# encoding: utf-8
from __future__ import unicode_literals
import sys, os
import unittest
import urllib2

from oauthlib.common import urlencode, urldecode, quote, unquote
from oauthlib import oauth1
from oauthlib.oauth1 import SIGNATURE_PLAINTEXT, SIGNATURE_TYPE_AUTH_HEADER, SIGNATURE_TYPE_BODY, SIGNATURE_TYPE_QUERY
import requests
import json
import urllib
from urlparse import parse_qs
import urlparse
from requests_oauthlib import OAuth1, OAuth1Session
BASE_URL = 'http://10.30.239.237:8080/v1'
BASE_URL_OAUTH = "http://10.30.239.237:8080/oauth"
CLIENT_KEY = "b3af4e669daf880fb16563e6f36051b105188d413"
CLIENT_SECRET = "c168e65c18d75b35d8999b534a3776cf"
REQUEST_TOKEN_ENDPOINT = "/request_token"
ACCESS_TOKEN_ENDPOINT = "/access_token"
STACKSYNC_AUTHORIZE_ENDPOINT = "/authorize"


oauth = OAuth1(CLIENT_KEY,
                   client_secret=CLIENT_SECRET,
                   #resource_owner_key='etTcuMo1xTxcBkXFlSLEX5ESasmLxP',
                   resource_owner_key='Sl3UV1wBax51bkgrwiIeq79RRHJ5iI',
                   #resource_owner_secret='mQEiJmn7KtoOSqJxHOiX8dWmHQ0J1U')
                   resource_owner_secret='cq4TCf6jcB8CadhmMXbqmOaO3crh1n')


# Main definition - constants
menu_actions  = {}


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('clear')

    print "Welcome,\n"
    print "Please choose the menu you want to start:"
    print "1. Menu 1"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)

    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return

# Menu 1
def menu1():
    while True:
        print "Hello Menu 1 !\n"
        print "2. Create new file"
        print "3. Update file data"
        print "4. Update file metadata"
        print "5. Get metadata file"
        print "6. Get file data (caution with the length of the file)"
        print "7. Create new folder"
        print "8. Share folder"
        print "9. Unshare folder"
        print "10. Update folder metadata"
        print "11. Delete a file"
        print "12. Get folder"
        print "13. Upload a new File"
        print "14. Upload File Data"
        print "0. Quit"
        choice = raw_input(" >>  ")
        exec_menu(choice)
    return

# Back to main menu
def back():
    menu_actions['main_menu']()

def create_new_file():

    headers = {}
    name = raw_input("File name:  ").decode('utf-8')
    if name:
    	parent = raw_input("Parent id:  ")
        print parent
    	if parent:
            url = BASE_URL +"/file?name="+name+"&parant="+parent
        else:
            url = BASE_URL +"/file?name="+name

        print url
        content_file = raw_input("Content file:  ")
        headers['StackSync-API'] = "v2"
        headers['Content-Type'] = "text/plain"
        #uri = urlencode(uri)
        r = requests.post(url=url, data=content_file, headers=headers, auth=oauth)
        print 'response', r
        print 'response', r.text
    else:
        print 'Can not create a new file without name'

def upload_new_file():
    headers = {}
    name = raw_input("File name:  ")
    if name:
        parent = raw_input("Parent id:  ")
	if parent:
	    url = BASE_URL +"/file?name="+name+"&parent="+parent
	else:
	    url = BASE_URL +"/file?name="+name
        #uri, headers, _ = client.sign(url, http_method='GET')
        path = raw_input("Absolute path of the file:  ")
        with open (path, "r") as myfile:
            data=myfile.read()
        #files = {'file': open(path, 'rb')}
        headers['StackSync-API'] = "v2"
        r = requests.post(url, data=data, headers=headers, auth=oauth)
        print 'response', r
        print 'response', r.text
    else:
    	print 'Can not create a new file without name'
def upload_file_data():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +"/file/"+file_id+"/data"
    #uri, headers, _ = client.sign(url, http_method='GET')
    path = raw_input("Absolute path of the file:  ")
    with open (path, "r") as myfile:
        data=myfile.read()
    #files = {'file': open(path, 'rb')}
    headers['StackSync-API'] = "v2"
    r = requests.put(url, data=data, headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text

def update_file_data():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)+'/data'
    #uri, headers, _ = client.sign(url, http_method='GET')
    content_file = raw_input("Content file:  ")
    headers['StackSync-API'] = "v2"

    headers['Content-Type'] = "text/plain"
    r = requests.put(url,content_file, headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text

def update_file_metadata():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)
    #uri, headers, _ = client.sign(url, http_method='GET')
    new_name = raw_input("New name:  ")
    new_parent = raw_input("New parent id: ")
    if not new_name and not new_parent:
	print 'Can not update metadata without any parameter'
    else:
	if not new_parent:
            parameters = {"name":str(new_name)}
	elif not new_name:
	    parameters = {"parent":new_parent}
	else:
	    parameters = {"name":str(new_name), "parent":new_parent}
    print parameters
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "application/json"
    r = requests.put(url, json.dumps(parameters), headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text

def get_metadata_file():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)
    # uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "application/json"
    r = requests.get(url, headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text

def get_file_data():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)+'/data'
    # uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "application/json"
    r = requests.get(url, headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text
def create_new_folder():
    headers = {}
    url = BASE_URL +'/folder'
    # uri, headers, _ = client.sign(url, http_method='GET')
    new_name = raw_input("Name:  ")
    new_parent = raw_input("Parent id: ")
    if not new_name:
	print 'Can not create folder without name'
    else:
	if not new_parent:
   	    parameters = {"name":str(new_name)}
	else:
	    parameters = {"name":str(new_name), "parent":new_parent}
        headers['StackSync-API'] = "v2"
        headers['Content-Type'] = "application/json"
	r = requests.post(url, json.dumps(parameters), headers=headers, auth=oauth)
	print 'response', r
        print 'response', r.text
def share_folder():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/folder/'+str(file_id)+'/share'
    # uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "application/json"
    emails = raw_input("mails to share (separated by comma):  ")
    shared_to = emails.split(",")
    r = requests.post(url, json.dumps(shared_to), headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text
def unshare_folder():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/folder/'+str(file_id)+'/unshare'
    # uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "application/json"
    emails = raw_input("mails to unshare (separated by comma):  ")
    shared_to = emails.split(",")
    r = requests.post(url, json.dumps(shared_to), headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text

def update_folder_metadata():
    headers = {}
    folder_id = raw_input("Folder id:  ")
    url = BASE_URL +'/folder/'+str(folder_id)
    # uri, headers, _ = client.sign(url, http_method='GET')
    new_name = raw_input("New name:  ")
    new_parent = raw_input("New parent id: ")
    if not new_name and not new_parent:
	print 'Can not update metadata without any parameter'
    else:
	if not new_parent:
 	    parameters = {"name":str(new_name)}
	elif not name:
	    parameters = {"parent":new_parent}
	else:
	    parameters = {"name":str(new_name), "parent":new_parent}
        headers['StackSync-API'] = "v2"

        headers['Content-Type'] = "application/json"
	r = requests.put(url,json.dumps(parameters), headers=headers, auth=oauth)
	print 'response', r
	print 'response', r.text

def delete_file():
    headers = {}
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)
    # uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "text/plain"
    r = requests.delete(url, headers=headers, auth=oauth)
    print 'response', r
    print 'response', r.text

def get_folder():
    headers = {}
    folder_id = raw_input("Folder id: ")
    if folder_id and folder_id != 0:
        url = BASE_URL+'/folder/' + str(folder_id)+'/contents'
    else: # if no folder_id provided -> list root
        url = BASE_URL+'/folder/0'

    headers['StackSync-API'] = "v2"

    r = requests.get(url, headers=headers, auth=oauth)
    print 'response status', r
    print 'response', r.text


# Exit program
def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': create_new_file,
    '3': update_file_data,
    '4': update_file_metadata,
    '5': get_metadata_file,
    '6': get_file_data,
    '7': create_new_folder,
    '8': share_folder,
    '9': unshare_folder,
    '10': update_folder_metadata,
    '11': delete_file,
    '12': get_folder,
    '13': upload_new_file,
    '14': upload_file_data,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
