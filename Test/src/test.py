'''
Created on 10/02/2014

@author: Edgar Zamora Gomez
'''
import urllib
import urllib2
import requests
import json
import unittest
'''
Test calls to StackSync API
'''

'''Global Variables'''
common_url = 'http://localhost:8080/api/'
auth_token = '657AD54T651ZE68745'
headers_param = {'StackSync-API':'v2', 'X-Auth-Token':auth_token}

'''
Files Resource
'''
def test_file_resource():
    values = {'name' : 'Michael Foord'}
    values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
    keys = ('name', 'path', 'id', 'mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')
    post_keys = ('name', 'path', 'id', 'parent', 'user')


    '''**** PUT ****'''
    #Without parameters. So no update anything
    req = requests.put(common_url+'file/123', headers=headers_param)
    assert req.json()['ERROR']
    #with name parameter
    req = requests.put(common_url+'file/123', data=values, headers=headers_param)
    assert req.status_code == 200
    #check dict keys
    content = req.json()
    for k in keys:
        assert content.has_key(k), k

    #with name and parent parameters
    req = requests.put(common_url+'file/123', data=values_parent, headers=headers_param)
    assert req.status_code == 200
    #without file_id
    req = requests.put(common_url+'file', values, headers=headers_param)
    assert req.status_code == 400
    
    '''**** GET ****'''
    #with file_id
    req = requests.get(common_url+'file/123', headers=headers_param)
    assert req.status_code == 200
    content = req.json()
    #check dict keys
    for k in keys:
        assert content.has_key(k), k
    #without file_id
    req = requests.get(common_url+'file', headers=headers_param)
    assert req.status_code == 400
    
    #TODO: Test to pass a file_id which not exists. 
    
    '''**** POST ****'''
    #with name parameter
    req = requests.post(common_url+'file', values, headers=headers_param)
    assert req.status_code == 200
    content = req.json()
    for k in post_keys:
        assert content.has_key(k)
    
    #with parent and name parameters
    req = requests.post(common_url+'file', values_parent, headers=headers_param)
    assert req.status_code == 200
    #without parameters
    req = requests.post(common_url+'file', headers=headers_param)
    assert req.status_code == 400
    
    '''**** DELETE ****'''
    #with file_id 
    req = requests.delete(common_url+'file/123', headers=headers_param)
    assert req.status_code == 200
    content = req.json()

    for k in keys:
        assert content.has_key(k), k
        
    #without file_id
    req = requests.delete(common_url+'file', headers=headers_param)
    assert req.status_code == 400
'''
Folder Resource
'''
def test_folder_resource():
    values ={'name':'Docuemnts'}
    values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
    keys = ('name', 'path', 'id', 'mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')
    post_keys = ('name', 'path', 'id', 'parent', 'user')

    '''**** POST ****'''
    #without parameters
    req = requests.post(common_url+'folder', headers=headers_param)
    assert req.status_code == 400
    
    #with name parameter
    req = requests.post(common_url+'folder', values, headers=headers_param)
    assert req.status_code == 200
    
    #Check keys of dict
    content = req.json()
    for k in post_keys:
        assert content.has_key(k), k
    
    #with parent and name parameters
    req = requests.post(common_url+'folder', values_parent, headers=headers_param)
    assert req.status_code == 200

    '''**** DELETE ****'''

    #with file_id 
    req = requests.delete(common_url+'folder/123', headers=headers_param)
    assert req.status_code == 200
    content = req.json()
    for k in keys:
        assert content.has_key(k), k 
    #without file_id
    req = requests.delete(common_url+'folder', headers=headers_param)
    assert req.status_code == 400
    
    '''**** GET ****'''
    
    #Get folder metadata. With folder_id
    req = requests.get(common_url+'folder/123', headers=headers_param)
    assert req.status_code == 200
    content = req.json()
    #check dict keys
    for k in keys:
        assert content.has_key(k), k
    #Get folder metadata. Without folder_id
    req = requests.get(common_url+'folder', headers=headers_param)
    assert req.status_code == 400
    #TODO: Test to pass a folder_id which not exists. NOT FOUND 404
    

    '''**** PUT ****'''
    
    #Without parameters. So no update anything
    req = requests.put(common_url+'folder/123', headers=headers_param)
    assert req.json()['ERROR']
    #with name parameter
    req = requests.put(common_url+'folder/123', data=values, headers=headers_param)
    print req
    assert req.status_code == 200
    #check dict keys
    content = req.json()
    for k in keys:
        assert content.has_key(k), k

    #with name and parent parameters
    req = requests.put(common_url+'folder/123', data=values_parent, headers=headers_param)
    assert req.status_code == 200
    #without file_id
    req = requests.put(common_url+'folder', values, headers=headers_param)
    assert req.status_code == 400
    
'''
Versions Resource
'''
def test_versions_resource():
    keys = ('name', 'path', 'id', 'size','mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')

    '''**** GET ****'''
    #with a specific version
    req = requests.get(common_url+'folder/123/versions/123', headers=headers_param)
    assert req.status_code == 200
    content = req.json()
    try:
        for k in keys:
            assert content.has_key(k), k
    except:
        assert False, "It's mandatory return a dict, so only one version"
    #without specific version
    req = requests.get(common_url+'folder/123/versions', headers=headers_param)
    content = req.json()
    assert req.status_code == 200
    for dict in content:
        for k in keys:
            assert dict.has_key(k), k    
    #wrong rute
'''
Contents Resource
'''
#GET
def test_contents_resource():
    keys = ('name', 'path', 'id', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified', 'contents')
    contents_key =  ('name', 'path', 'id', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')

    '''**** GET ****'''
    #with a specific version
    req = requests.get(common_url+'folder/123/contents', headers=headers_param)
    assert req.status_code == 200
    content = req.json()
    #without specific version
    for k in keys:
        assert content.has_key(k), k
        if k == 'contents':
            for content_dict in content[k]:
                if not content_dict:
                    #Empty folder
                    assert True
                    break
                for key in contents_key:
                    assert content_dict.has_key(key), key
'''
Data Resource
'''

def test_data_resource():
    '''**** PUT ****'''
    file_content = {"content":"There are the content of file"}

    req = requests.put(common_url+'file/123/data', data=file_content, headers=headers_param)
    assert req.status_code == 200, str(req.status_code)+req.text
    req = requests.put(common_url+'file/123/data', headers=headers_param)
    assert req.status_code == 400, req.status_code
    
    '''**** GET ****'''
    req = requests.get(common_url+'file/123/data', headers=headers_param)
    assert req.status_code == 200, req.status_code
    req = requests.get(common_url+'file/123/versions/132/data', headers=headers_param)
    assert req.status_code == 200, req.status_code

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()
        
    def test_file_resource(self):
        test_file_resource()
    def test_folder_resource(self):
        test_folder_resource()
    def test_versions_resource(self):
        test_versions_resource()
    def test_data_resource(self):
        test_data_resource()
    def test_contents_resource(self):
        test_contents_resource()    
        
    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()



if __name__ == "__main__":
    unittest.main()


# urllib2.Request(url[, data][, headers][, origin_req_host][, unverifiable])