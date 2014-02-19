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



class Test(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.values = {'name':'Docuemnts'}
        self.values_parent = {'name':'Docuemnts', 'parent':'Cristian Cots'}
        self.keys = ('name', 'path', 'id', 'mimetype', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')

        self.post_keys = ('name', 'path', 'id', 'parent', 'user')
    '''
    Files Resource
    '''

    def test_put_file(self):
        '''**** PUT ****'''
        # Without parameters. So no update anything
        req = requests.put(common_url + 'file/123', headers=headers_param)
        assert req.json()['ERROR']
        # with name parameter
        req = requests.put(common_url + 'file/123', data=self.values, headers=headers_param)
        assert req.status_code == 200
        # check dict keys
        content = req.json()
        for k in self.keys:
            assert content.has_key(k), k
    
        # with name and parent parameters
        req = requests.put(common_url + 'file/123', data=self.values_parent, headers=headers_param)
        assert req.status_code == 200
        # without file_id
        req = requests.put(common_url + 'file', self.values, headers=headers_param)
        assert req.status_code == 400
    def test_get_file(self):   
        '''**** GET ****'''
        # with file_id
        req = requests.get(common_url + 'file/123', headers=headers_param)
        assert req.status_code == 200
        content = req.json()
        # check dict keys
        for k in self.keys:
            assert content.has_key(k), k
        # without file_id
        req = requests.get(common_url + 'file', headers=headers_param)
        assert req.status_code == 400
        
        # TODO: Test to pass a file_id which not exists. 
    def test_post_file(self):       
        '''**** POST ****'''
        # with name parameter
        req = requests.post(common_url + 'file', self.values, headers=headers_param)
        assert req.status_code == 200
        content = req.json()
        for k in self.post_keys:
            assert content.has_key(k)
        
        # with parent and name parameters
        req = requests.post(common_url + 'file', self.values_parent, headers=headers_param)
        assert req.status_code == 200
        # without parameters
        req = requests.post(common_url + 'file', headers=headers_param)
        assert req.status_code == 400
        
    def test_delete_file(self):           
        '''**** DELETE ****'''
        # with file_id 
        req = requests.delete(common_url + 'file/123', headers=headers_param)
        assert req.status_code == 200
        content = req.json()
    
        for k in self.keys:
            assert content.has_key(k), k
            
        # without file_id
        req = requests.delete(common_url + 'file', headers=headers_param)
        assert req.status_code == 400
    '''
    Folder Resource
    '''
    
    def test_post_folder(self):
        '''**** POST ****'''
        # without parameters
        req = requests.post(common_url + 'folder', headers=headers_param)
        assert req.status_code == 400
        
        # with name parameter
        req = requests.post(common_url + 'folder', self.values, headers=headers_param)
        assert req.status_code == 200
        
        # Check keys of dict
        content = req.json()
        for k in self.post_keys:
            assert content.has_key(k), k
        
        # with parent and name parameters
        req = requests.post(common_url + 'folder', self.values_parent, headers=headers_param)
        assert req.status_code == 200
        
    def test_delete_folder(self):
        '''**** DELETE ****'''
    
        # with file_id 
        req = requests.delete(common_url + 'folder/123', headers=headers_param)
        assert req.status_code == 200
        content = req.json()
        for k in self.keys:
            assert content.has_key(k), k 
        # without file_id
        req = requests.delete(common_url + 'folder', headers=headers_param)
        assert req.status_code == 400
    def test_get_folder(self):   
        '''**** GET ****'''
        
        # Get folder metadata. With folder_id
        req = requests.get(common_url + 'folder/123', headers=headers_param)
        assert req.status_code == 200
        content = req.json()
        # check dict keys
        for k in self.keys:
            assert content.has_key(k), k
        # Get folder metadata. Without folder_id
        req = requests.get(common_url + 'folder', headers=headers_param)
        assert req.status_code == 400
        # TODO: Test to pass a folder_id which not exists. NOT FOUND 404
        
    def test_put_folder(self):   
    
        '''**** PUT ****'''
        
        # Without parameters. So no update anything
        req = requests.put(common_url + 'folder/123', headers=headers_param)
        assert req.json()['ERROR']
        # with name parameter
        req = requests.put(common_url + 'folder/123', data=self.values, headers=headers_param)
        print req
        assert req.status_code == 200
        # check dict keys
        content = req.json()
        for k in self.keys:
            assert content.has_key(k), k
    
        # with name and parent parameters
        req = requests.put(common_url + 'folder/123', data=self.values_parent, headers=headers_param)
        assert req.status_code == 200
        # without file_id
        req = requests.put(common_url + 'folder', self.values, headers=headers_param)
        assert req.status_code == 400
        
    '''
    Versions Resource
    '''
    def test_get_versions(self):
    
        '''**** GET ****'''
        # with a specific version
        req = requests.get(common_url + 'folder/123/versions/123', headers=headers_param)
        assert req.status_code == 200
        content = req.json()
        try:
            for k in self.keys:
                assert content.has_key(k), k
        except:
            assert False, "It's mandatory return a dict, so only one version"
        # without specific version
        req = requests.get(common_url + 'folder/123/versions', headers=headers_param)
        content = req.json()
        assert req.status_code == 200
        for dict in content:
            for k in self.keys:
                assert dict.has_key(k), k    
        # wrong rute
    '''
    Contents Resource
    '''
    # GET
    def test_get_contents(self):
        keys = ('name', 'path', 'id', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified', 'contents')
        contents_key = ('name', 'path', 'id', 'status', 'version', 'parent', 'user', 'client_modified', 'server_modified')
    
        '''**** GET ****'''
        # with a specific version
        req = requests.get(common_url + 'folder/123/contents', headers=headers_param)
        assert req.status_code == 200
        content = req.json()
        # without specific version
        for k in keys:
            assert content.has_key(k), k
            if k == 'contents':
                for content_dict in content[k]:
                    if not content_dict:
                        # Empty folder
                        assert True
                        break
                    for key in contents_key:
                        assert content_dict.has_key(key), key
    '''
    Data Resource
    '''
    
    def test_put_data(self):
        '''**** PUT ****'''
        file_content = {"content":"There are the content of file"}
    
        req = requests.put(common_url + 'file/123/data', data=file_content, headers=headers_param)
        assert req.status_code == 200, str(req.status_code) + req.text
        req = requests.put(common_url + 'file/123/data', headers=headers_param)
        assert req.status_code == 400, req.status_code
    def test_get_data(self):    
        '''**** GET ****'''
        req = requests.get(common_url + 'file/123/data', headers=headers_param)
        assert req.status_code == 200, req.status_code
        req = requests.get(common_url + 'file/123/versions/132/data', headers=headers_param)
        assert req.status_code == 200, req.status_code
      
        
    



if __name__ == "__main__":
    unittest.main()


# urllib2.Request(url[, data][, headers][, origin_req_host][, unverifiable])
