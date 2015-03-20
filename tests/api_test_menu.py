
import sys, os
import unittest
import urllib2
from oauthlib.common import urlencode, urldecode
from oauthlib import oauth1
from oauthlib.oauth1 import SIGNATURE_PLAINTEXT, SIGNATURE_TYPE_AUTH_HEADER, SIGNATURE_TYPE_BODY, SIGNATURE_TYPE_QUERY
import requests
import json
import urllib
from urlparse import parse_qs

#BASE_URL = "http://10.30.239.237:8080/oauth"
BASE_URL = 'http://localhost:8080/v1'
BASE_URL_OAUTH = "http://10.30.233.214:8080/oauth"
CLIENT_KEY = "b3af4e669daf880fb16563e6f36051b105188d413"
CLIENT_SECRET = "c168e65c18d75b35d8999b534a3776cf"
REQUEST_TOKEN_ENDPOINT = "/request_token"
ACCESS_TOKEN_ENDPOINT = "/access_token"
STACKSYNC_AUTHORIZE_ENDPOINT = "/authorize"


client = oauth1.Client(CLIENT_KEY,
                       client_secret=CLIENT_SECRET,
                       signature_type=SIGNATURE_TYPE_QUERY,
                       signature_method=SIGNATURE_PLAINTEXT,
                       resource_owner_key='GmOFBjhSzC0A2rxrnM6gQWKnm6m3Ew',
                       resource_owner_secret='RtA8hMYzgxnpoMxd8kBUtVQmcSvM4D')




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
        print "0. Quit"
        choice = raw_input(" >>  ")
        exec_menu(choice)
    return
  
# Back to main menu
def back():
    menu_actions['main_menu']()

def create_new_file():
    name = raw_input("File name:  ")
    if name:
	parent = raw_input("Parent id:  ")
	if parent:
	    url = BASE_URL +"/file?name="+name+"&parent="+parent
	else:
	    url = BASE_URL +"/file?name="+name
	uri, headers, _ = client.sign(url, http_method='GET')
	
	content_file = raw_input("Content file:  ")
        headers['StackSync-API'] = "v2"
        headers['Content-Type'] = "text/plain"

	r = requests.post(uri,content_file, headers=headers)
	print 'response', r
        print 'response', r.text
    else:
    	print 'Can not create a new file without name'

def update_file_data():
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)+'/data'
    uri, headers, _ = client.sign(url, http_method='GET')
    content_file = raw_input("Content file:  ")
    headers['StackSync-API'] = "v2"

    headers['Content-Type'] = "text/plain"
    r = requests.put(uri,content_file, headers=headers)
    print 'response', r
    print 'response', r.text

def update_file_metadata():
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)
    uri, headers, _ = client.sign(url, http_method='GET')
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
    r = requests.put(uri, json.dumps(parameters), headers=headers)
    print 'response', r
    print 'response', r.text

def get_metadata_file():
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)
    uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "application/json"
    r = requests.get(uri, headers=headers)
    print 'response', r
    print 'response', r.text

def get_file_data():
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)+'/data'
    uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"  
    headers['Content-Type'] = "application/json"
    r = requests.get(uri, headers=headers)
    print 'response', r
    print 'response', r.text
def create_new_folder():
    url = BASE_URL +'/folder'
    uri, headers, _ = client.sign(url, http_method='GET')
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
	r = requests.post(uri, json.dumps(parameters), headers=headers)
	print 'response', r
        print 'response', r.text
def share_folder():
	None

def unshare_folder():
	None

def update_folder_metadata():
    folder_id = raw_input("Folder id:  ")
    url = BASE_URL +'/folder/'+str(folder_id)
    uri, headers, _ = client.sign(url, http_method='GET')
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
	r = requests.put(uri,json.dumps(parameters), headers=headers)
	print 'response', r
	print 'response', r.text

def delete_file():
    file_id = raw_input("File id:  ")
    url = BASE_URL +'/file/'+str(file_id)
    uri, headers, _ = client.sign(url, http_method='GET')
    headers['StackSync-API'] = "v2"
    headers['Content-Type'] = "text/plain"
    r = requests.delete(uri, headers=headers)
    print 'response', r
    print 'response', r.text

def get_folder():
    folder_id = raw_input("Folder id: ")
    url =BASE_URL+'/folder/' + str(folder_id)
    #url ='http://localhost:8080/v1/file/578/data'
    #url ='http://localhost:8080/v1/file?name=tiririri.txt'

    uri, headers, _ = client.sign(url,
                                   http_method='GET')
    headers['StackSync-API'] = "v2"
    
    headers['Content-Type'] = "text/plain"
    r = requests.get(uri, headers=headers)
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
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
