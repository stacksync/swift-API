import xmlrpclib
import time

class StacksyncServerController():
    """
    Handles requests on objects
    """
    def __init__(self, serverIp, serverPort, **kwargs):
        
        #Create Sync server connection
        self.xmlIp = serverIp
        self.xml = serverPort
        self.rpcServer = xmlrpclib.ServerProxy("http://"+serverIp+':'+str(serverPort))
        
    def getMetadata(self, user, requestId, fileId, includeList, includeDeleted, includeChunks, version):
        response = self.rpcServer.XmlRpcSyncHandler.getMetadata(user, requestId, fileId, includeList, includeDeleted, includeChunks, version);
        return response.encode('utf-8')
    
    def putMetadataFile(self, user, requestId, fileName, parent, overwrite, checksum, fileSize, mimetype, chunks):
        response = self.rpcServer.XmlRpcSyncHandler.putMetadataFile(user, requestId, fileName, parent, overwrite, checksum, fileSize, mimetype, chunks);
        return response.encode('utf-8')
    
    def getVersions(self, user, requestId, fileId):
        response = self.rpcServer.XmlRpcSyncHandler.getVersions(user, requestId, fileId);
        return response.encode('utf-8')
    
    def doDelete(self, user, requestId, fileId):
        response = self.rpcServer.XmlRpcSyncHandler.deleteMetadataFile(user, requestId, fileId);
        return response.encode('utf-8')
    
    def putMetadataFolder(self, user, requestId, folderName, parent):
        response = self.rpcServer.XmlRpcSyncHandler.putMetadataFolder(user, requestId, folderName, parent);
        return response.encode('utf-8')
    
    def restoreMetadata(self, user, requestId, fileId, version):
        response = self.rpcServer.XmlRpcSyncHandler.restoreMetadata(user, requestId, fileId, version);
        return response.encode('utf-8')
    
    def touchNewFile(self, user, fileName, parent):
        requestId = self.__getRequestId()
        response = self.rpcServer.XmlRpcSyncHandler_v2.touchNewFile(user, requestId, fileName, parent);
        return response.encode('utf-8')
    
    def __generateDateTime(self):   
        delta = int(round(time.time() * 1000))
        return delta
    
    def __getRequestId(self):
        requestId = "Api-web_" + str(self.__generateDateTime())   
        return requestId