Authentication
==============

After successfully receiving the Access Token and Token Secret as explained in the Authentication document, the Consumer is able to access API resources on behalf of the user. 

All request must be signed as explained in the Signing Requests section, and contain the following parameters:

OAuth parameter |  Description
--- | --- 
**oauth_consumer_key** | The Consumer Key.
**oauth_signature_method** |  The signature method the Consumer used to sign the request. Options are “PLAINTEXT” and “HMAC-SHA1”.
**oauth_signature** |  The signature as defined in Signing Requests.
**oauth_timestamp** | The timestamp is expressed in the number of seconds since January 1, 1970 00:00:00 GMT. The timestamp value must be a positive integer and must be equal or greater than the timestamp used in previous requests.
**oauth_nonce** |  Value that is unique for all requests with that timestamp. A nonce is a random string, uniquely generated for each request.
**oauth_version** | OPTIONAL. If present, value must be “1.0” . Service Providers must assume the protocol version to be 1.0 if this parameter is not present.
**oauth_token** |  Access Token obtained after a successful authentication.

Error handling
==============

Errors are returned using standard HTTP error code syntax. Any additional info is included in the body of the return call, JSON-formatted. Error codes not listed here are in the REST API methods listed below.

Standard API errors

Code |  Description
--- | --- 
**400** | Bad input parameter. Error message should indicate which one and why.
**401** | Authorization required. The presented credentials, if any, were not sufficient to access the folder resource. Returned if an application attempts to use an access token after it has expired.
**403** | Forbidden. The requester does not have permission to access the specified resource.
**404** | File or folder not found at the specified path.
**405** | Request method not expected (generally should be GET or POST).
**5xx** | Server error

File
====
## Create a file

An application can create a file by issuing an HTTP POST request. The application needs to provide the file binary in the body and the file name as a query argument. Optionally, it can also provide the parent argument tco loate the file in a specific folder. Otherwise, the file will be placed in the root folder.

### Request

#### URL structure
The URL that represents the file data resource. The URL is
**/file**.

#### Method
POST

#### Request Headers

The request header includes the following information:

FIELD |  Description
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
**Content-Type** | The content type and character encoding of the response. The content type must be **application/json**, and the character encoding must be **UTF-8**.

#### Request Query arguments
JSON input that contains a dictionary with the following keys:

FIELD |  Description | REQUIRED
--- | --- | ---
**name** | The user-visible name of the file to be created. | Yes
**parent** | ID of the folder where the file is going to be created. If no ID is passed, it will use the top-level folder. This parameter should **not** point to a file. | No

#### HTTP Request Example
'''
  POST /file?name=new_file.txt&parent=8474
 
  StackSync-API: v2
  Content-Length: 294

  <file binary>
'''

### Response
