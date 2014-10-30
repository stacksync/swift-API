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



class Test_FILE(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.values = {'name':'Docuemnts'}
        self.values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
        self.keys = ('name', 'path', 'id', 'mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')

        self.post_keys = ('name', 'path', 'id', 'parent', 'user')
    '''
    Files Resource
    '''

    def test_put_without_parameters(self):
        '''**** PUT ****'''
        # Without parameters. So no update anything
        req = requests.put(common_url + 'file/123', headers=headers_param)
        assert req.json()['ERROR']
    def test_put_with_name(self):
        # with name parameter
        req = requests.put(common_url + 'file/123', data=self.values, headers=headers_param)
        assert req.status_code == 200
    def test_put_check_keys(self):
        req = requests.put(common_url + 'file/123', data=self.values, headers=headers_param)
        # check dict keys
        content = req.json()
        for k in self.keys:
            assert content.has_key(k), k
    def test_put_with_name_parent(self):
        # with name and parent parameters
        req = requests.put(common_url + 'file/123', data=self.values_parent, headers=headers_param)
        assert req.status_code == 200
        
    def test_put_without_file(self):
        # without file_id
        req = requests.put(common_url + 'file', self.values, headers=headers_param)
        assert req.status_code == 400
    def test_get_file(self):   
        '''**** GET ****'''
        # with file_id
        req = requests.get(common_url + 'file/123', headers=headers_param)
        assert req.status_code == 200
        
    def test_get_check_keys(self):   
        req = requests.get(common_url + 'file/123', headers=headers_param)
        content = req.json()
        # check dict keys
        for k in self.keys:
            assert content.has_key(k), k
    def test_get_without_fileid(self):
        # without file_id
        req = requests.get(common_url + 'file', headers=headers_param)
        assert req.status_code == 400
        
        # TODO: Test to pass a file_id which not exists. 
    def test_post_with_name(self):       
        '''**** POST ****'''
        # with name parameter
        req = requests.post(common_url + 'file', self.values, headers=headers_param)
        assert req.status_code == 200
        content = req.json()
        for k in self.post_keys:
            assert content.has_key(k)
    def test_post_check_keys(self):
        req = requests.post(common_url + 'file', self.values, headers=headers_param)
        content = req.json()
        for k in self.post_keys:
            assert content.has_key(k)
    def test_post_with_name_parent(self):     
        # with parent and name parameters
        req = requests.post(common_url + 'file', self.values_parent, headers=headers_param)
        assert req.status_code == 200
    def test_post_without_parameters(self):
        # without parameters
        req = requests.post(common_url + 'file', headers=headers_param)
        assert req.status_code == 400
        
    def test_delete_file(self):           
        '''**** DELETE ****'''
        # with file_id 
        req = requests.delete(common_url + 'file/123', headers=headers_param)
        assert req.status_code == 200
        
    def test_delete_check_keys(self):
        req = requests.delete(common_url + 'file/123', headers=headers_param)
        content = req.json()
        for k in self.keys:
            assert content.has_key(k), k
    def test_delete_without_fileid(self):        
        # without file_id
        req = requests.delete(common_url + 'file', headers=headers_param)
        assert req.status_code == 400
        
        
class Test_FOLDER(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.values = {'name':'Docuemnts'}
        self.values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
        self.keys = ('name', 'path', 'id', 'mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')

        self.post_keys = ('name', 'path', 'id', 'parent', 'user')
    '''
    Folder Resource
    '''
    
    def test_post_without_parameters(self):
        '''**** POST ****'''
        # without parameters
        req = requests.post(common_url + 'folder', headers=headers_param)
        assert req.status_code == 400
    def test_post_with_name(self):  
        # with name parameter
        req = requests.post(common_url + 'folder', self.values, headers=headers_param)
        assert req.status_code == 200
    def test_post_check_keys(self):
        req = requests.post(common_url + 'folder', self.values, headers=headers_param)
        # Check keys of dict
        content = req.json()
        for k in self.post_keys:
            assert content.has_key(k), k
    def test_post_with_name_parent(self):    
        # with parent and name parameters
        req = requests.post(common_url + 'folder', self.values_parent, headers=headers_param)
        assert req.status_code == 200
        
    def test_delete_with_folderid(self):
        '''**** DELETE ****'''
        # with file_id 
        req = requests.delete(common_url + 'folder/123', headers=headers_param)
        assert req.status_code == 200
    def test_delete_check_keys(self):
        req = requests.delete(common_url + 'folder/123', headers=headers_param)
        content = req.json()
        for k in self.keys:
            assert content.has_key(k), k 
    def test_delete_without_folderid(self):
        # without file_id
        req = requests.delete(common_url + 'folder', headers=headers_param)
        assert req.status_code == 400
        
    def test_get_with_folderid(self):   
        '''**** GET ****'''
        
        # Get folder metadata. With folder_id
        req = requests.get(common_url + 'folder/123', headers=headers_param)
        assert req.status_code == 200
    def test_get_check_keys(self):
        req = requests.get(common_url + 'folder/123', headers=headers_param)
        content = req.json()
        # check dict keys
        for k in self.keys:
            assert content.has_key(k), k
    def test_get_without_folderid(self):
        # Get folder metadata. Without folder_id
        req = requests.get(common_url + 'folder', headers=headers_param)
        assert req.status_code == 400
        # TODO: Test to pass a folder_id which not exists. NOT FOUND 404
        
    def test_put_without_parameters(self):   
        '''**** PUT ****'''
        # Without parameters. So no update anything
        req = requests.put(common_url + 'folder/123', headers=headers_param)
        assert req.json()['ERROR']
    def test_put_with_name(self):
        # with name parameter
        req = requests.put(common_url + 'folder/123', data=self.values, headers=headers_param)
        assert req.status_code == 200
    def test_put_check_keys(self):
        req = requests.put(common_url + 'folder/123', data=self.values, headers=headers_param)
        # check dict keys
        content = req.json()
        for k in self.keys:
            assert content.has_key(k), k
    def test_put_with_name_parent(self):
        # with name and parent parameters
        req = requests.put(common_url + 'folder/123', data=self.values_parent, headers=headers_param)
        assert req.status_code == 200
    def test_put_without_folderid(self):
        # without file_id
        req = requests.put(common_url + 'folder', self.values, headers=headers_param)
        assert req.status_code == 400
    
class Test_VERSIONS(unittest.TestCase):    
    '''
    Versions Resource
    '''
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.values = {'name':'Docuemnts'}
        self.values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
        self.keys = ('name', 'path', 'id', 'mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')

        self.post_keys = ('name', 'path', 'id', 'parent', 'user')
        
    def test_get_specific_versions(self):    
        '''**** GET ****'''
        # with a specific version
        req = requests.get(common_url + 'folder/123/versions/123', headers=headers_param)
        assert req.status_code == 200
    def test_get_check_keys_specific_version(self):
        req = requests.get(common_url + 'folder/123/versions/123', headers=headers_param)
        content = req.json()
        try:
            for k in self.keys:
                assert content.has_key(k), k
        except:
            assert False, "It's mandatory return a dict, so only one version"
    def test_get_without_specific_version(self):
        # without specific version
        req = requests.get(common_url + 'folder/123/versions', headers=headers_param)
        assert req.status_code == 200
    def test_get_check_keys_without_specific_version(self):
        req = requests.get(common_url + 'folder/123/versions', headers=headers_param)
        content = req.json()
        for dict in content:
            for k in self.keys:
                assert dict.has_key(k), k    
        # wrong rute
        
class Test_CONTENTS(unittest.TestCase):    
    '''
    Versions Resource
    '''
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.values = {'name':'Docuemnts'}
        self.values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
        
        self.keys = ('name', 'path', 'id', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified', 'contents')
        self.contents_key = ('name', 'path', 'id', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')         

    # GET
    def test_get_contents(self):
        '''**** GET ****'''
        # with a specific version
        req = requests.get(common_url + 'folder/123/contents', headers=headers_param)
        assert req.status_code == 200
    def test_get_check_keys(self):
        req = requests.get(common_url + 'folder/123/contents', headers=headers_param)

        content = req.json()

        # without specific version
        for k in self.keys:
            assert content.has_key(k), k
            if k == 'contents':
                for content_dict in content[k]:
                    if not content_dict:
                        # Empty folder
                        assert True
                        break
                    for key in self.contents_key:
                        assert content_dict.has_key(key), key
    '''
    Data Resource
    '''
class Test_DATA(unittest.TestCase):    
    '''
    Versions Resource
    '''
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.values = {'name':'Docuemnts'}
        self.values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
        self.keys = ('name', 'path', 'id', 'mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')

        self.post_keys = ('name', 'path', 'id', 'parent', 'user')   
    def test_put_with_file_content(self):
        '''**** PUT ****'''
        file_content = {"content":"There are the content of file"}
    
        req = requests.put(common_url + 'file/123/data', data=file_content, headers=headers_param)
        assert req.status_code == 200, str(req.status_code) + req.text
    def test_put_without_file_content(self):
        req = requests.put(common_url + 'file/123/data', headers=headers_param)
        assert req.status_code == 400, req.status_code
        
    def test_get_file_data(self):    
        '''**** GET ****'''
        req = requests.get(common_url + 'file/123/data', headers=headers_param)
        assert req.status_code == 200, req.status_code
    def test_get_file_version_data(self):
        req = requests.get(common_url + 'file/123/versions/132/data', headers=headers_param)
        assert req.status_code == 200, req.status_code
      
        
    



if __name__ == "__main__":
    unittest.main()


# urllib2.Request(url[, data][, headers][, origin_req_host][, unverifiable])
