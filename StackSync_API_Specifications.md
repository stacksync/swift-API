StackSync API Specification
==========================
**Table of Contents**

- [Authentication](#authentication)
- [Error handling](#error-handling)
- [File Resource](#file) 
  - [Create a file](#create-a-file)
  - [Upload file data](#upload-file-data)
  - [Download file data](#download-file-data)
  - [Delete a file](#delete-a-file)
  - [Get file metadata](#get-file-metadata)
  - [Update file metadata](#update-file-metadata)
- [Versions Resource](#versions)
  - [Get file versions](#get-file-versions)
  - [Get file version metadata](#get-file-version-metadata)
  - [Get file version data](#get-file-version-data)
- [Folder Resource](#folder)
  - [Create a folder](#create-a-folder)
  - [Delete a folder](#delete-a-folder)
  - [Get folder metadata](#get-folder-metadata)
  - [Get folder content metadata](#get-folder-content-metadata)
  - [Update folder metadata](#update-folder-metadata)
  - [Share a folder](#share-a-folder)
  - [Unshare a folder](#unshare-a-folder)
  - [Get folder members](#get-folder-members)

#Authentication

After successfully receiving the Access Token and Token Secret as explained in the Authentication document, the Consumer is able to access API resources on behalf of the user. 

All request must be signed as explained in the Signing Requests section, and contain the following parameters:

OAuth PARAMETER |  DESCRIPTION
--- | --- 
**oauth_consumer_key** | The Consumer Key.
**oauth_signature_method** |  The signature method the Consumer used to sign the request. Options are “PLAINTEXT” and “HMAC-SHA1”.
**oauth_signature** |  The signature as defined in Signing Requests.
**oauth_timestamp** | The timestamp is expressed in the number of seconds since January 1, 1970 00:00:00 GMT. The timestamp value must be a positive integer and must be equal or greater than the timestamp used in previous requests.
**oauth_nonce** |  Value that is unique for all requests with that timestamp. A nonce is a random string, uniquely generated for each request.
**oauth_version** | OPTIONAL. If present, value must be “1.0” . Service Providers must assume the protocol version to be 1.0 if this parameter is not present.
**oauth_token** |  Access Token obtained after a successful authentication.

#Error handling

Errors are returned using standard HTTP error code syntax. Any additional info is included in the body of the return call, JSON-formatted. Error codes not listed here are in the REST API methods listed below.

Standard API errors

CODE |  DESCRIPTION
--- | --- 
**400** | Bad input parameter. Error message should indicate which one and why.
**401** | Authorization required. The presented credentials, if any, were not sufficient to access the folder resource. Returned if an application attempts to use an access token after it has expired.
**403** | Forbidden. The requester does not have permission to access the specified resource.
**404** | File or folder not found at the specified path.
**405** | Request method not expected (generally should be GET or POST).
**5xx** | Server error

#File

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

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
**Content-Type** | The content type and character encoding of the response. The content type must be **application/json**, and the character encoding must be **UTF-8**.

#### Request Query arguments
JSON input that contains a dictionary with the following keys:

FIELD |  DESCRIPTION | REQUIRED
--- | --- | ---
**name** | The user-visible name of the file to be created. | Yes
**parent** | ID of the folder where the file is going to be created. If no ID is passed, it will use the top-level folder. This parameter should **not** point to a file. | No

#### HTTP Request Example

```
POST /file?name=new_file.txt&parent=8474
 
StackSync-API: v2
Content-Length: 294

<file binary>
```


### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.
**Location** | The location of the newly created file.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json

HTTP/1.1 201 Created
Content-Type: application/json; charset=UTF-8
Content-Length: 12
Location: https://domain.ext/stacksync/file/32565632156

{
"id":640,
"parent_id":null,
"filename":"Test_for_documentation.txt",
"is_folder":false,
"status":"NEW",
"modified_at":"Tue Apr 28 11:19:23 CEST 2015",
"version":1,
"checksum":464127057,
"size":12,
"mimetype":"text/plain",
"chunks":[
"chk-1A2CE7C68848FB9E16F856AF1D23594E97BE42C9-16007656575193673912"
]
}

```
## Upload file data

An application can upload data to a file by issuing an HTTP PUT request to the file data resource that represents the data for the file. The file binary will be sent in the request body.
Uploading data to a file creates a new file version in the StackSync datastore and associates the uploaded data with the newly created file version.
This approach does not allow the application to resume the upload if the upload does not successfully complete, that is, if all the data is not completely uploaded.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, followed by the file ID and ends with **/data**, for example,
**/file/2148742318/data**

#### Method
PUT

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
#### HTTP Request Example

```
PUT /file/2148742318/data
 
 StackSync-API: v2
Content-Length: 1478

<File content…. >
```


### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json


HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

{
"id":640,
"parent_id":null,
"filename":"Test_for_documentation.txt",
"is_folder":false,
"status":"CHANGED",
"modified_at":"Tue Apr 28 11:28:43 CEST 2015",
"version":2,
"checksum":2343897327,
"size":28,
"mimetype":"text/plain",
"chunks":[
"chk-4C07C64C030175211476CAA50892E950D0BA0D7C-640"
]
}

```
## Download file data

To retrieve file data, an application submits an HTTP GET request to the file data resource that represents the data for the file.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, and ends with **/data**, for example, **/file/2148742318/data**

#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
GET /file/2148742318/data
 
StackSync-API: v2
```


### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
The response body contains the retrieved file data.

#### Response example

```json


HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

<File content…. >


```
## Delete a file

An application can delete a file by issuing an HTTP DELETE request to the URL of the file resource. It's a good idea to precede DELETE requests like this with a caution note in your application's user interface.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, for example,  
**/file/2148742318**.

#### Method
DELETE

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
DELETE https://domain.ext/stacksync/file/2148742318
 
StackSync-API: v2
```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

{
"id":640,
"parent_id":null,
"filename":"Test_for_documentation.txt",
"is_folder":false,
"status":"DELETED",
"modified_at":"Tue Apr 28 11:38:46 CEST 2015",
"version":3,
"checksum":2343897327,
"size":28,
"mimetype":"text/plain",
"chunks":[
]
}

```

## Get file metadata

To retrieve information about a file, an application submits an HTTP GET request to the file resource that represents the file.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, and ends with the file ID, for example, **/file/2148742318**

#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
GET /file/2148742318
 
StackSync-API: v2
```

### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json


HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

{
"id":179,
"parent_id":null,
"filename":"hello.txt",
"is_folder":false,
"status":"CHANGED",
"modified_at":"2015-02-06 10:16:25.693",
"version":9,
"checksum":4015131941,
"size":35,
"mimetype":"text/plain",
"chunks":[
],
"contents":[
]
}
```
## Update file metadata

An application can update various attributes of a file by issuing an HTTP PUT request to the URL that represents the file resource. In addition, the app needs to provide as input, JSON that identifies the new attribute values for the file. Upon receiving the PUT request, the StackSync service examines the input and updates any of the attributes that have been modified.
Here are the file attributes that can be updated:
 * name
 * parent
No other file attributes can be modified using a PUT request.

**Note:** An application can move a file to a different parent folder by changing the value of the parent element.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, and ends with the file ID, for example, **/file/2148742318**.

#### Method
PUT

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
**Content-Type** | The content type and character encoding of the response. The content type must be **application/json**, and the character encoding must be **UTF-8**.

#### Request Body
JSON input that contains a dictionary with the following keys:

FIELD |  DESCRIPTION | REQUIRED
--- | --- | ---
**name** | The user-visible name of the file to be created. | NO
**parent** | ID of the folder where the file is going to be created. If no ID is passed, it will use the top-level folder. This parameter should **not** point to a file. | No

#### HTTP Request Example

```

PUT /file/32565632156
 
StackSync-API: v2
Content-Length: 294
Content-Type: application/json

{
     “name”: “Winter2012_renamed.jpg”,
     “parent”:12386548974
}

```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.
**Location** | The location of the newly created file.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248
Location: https://domain.ext/stacksync/file/

{
"id":641,
"parent_id":null,
"filename":"Test_for_documtation_name_update.txt",
"is_folder":false,
"status":"RENAMED",
"modified_at":"Tue Apr 28 11:52:55 CEST 2015",
"version":2,
"checksum":615384210,
"size":14,
"mimetype":"text/plain",
"chunks":[
"chk-91DD3E155628E931EFB01B0F6BB121A7C21910DE-3836471730894233428"
]
}

```
#Versions

## Get file versions

To retrieve information about a file version, an application submits an HTTP GET request to the file version resource.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, and ends with **/version**, for example, **/file/2148742318/versions**.

#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
GET https://domain.ext/stacksync/file/2148742318/versions
 
StackSync-API: v2
```


### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks
**versions** | A list of all versions

#### Response example

```json


HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

{
"id":179,
"parent_id":null,
"filename":"hello.txt",
"is_folder":false,
"status":"CHANGED",
"modified_at":"2015-02-06 10:16:25.693",
"version":5,
"checksum":4015131941,
"size":35,
"mimetype":"text/plain",
"chunks":[
],
"versions":[
      {
      "id":179,
      "parent_id":null,
      "filename":"hello.txt",
      "is_folder":false,
      "status":"CHANGED",
      "modified_at":"2014-07-17 10:18:13.609",
      "version":4,
      "checksum":3377466444,
      "size":32,
      "mimetype":"text/plain",
      "chunks":[
      ]
      },
      {
      "id":179,
      "parent_id":null,
      "filename":"hello.txt",
      "is_folder":false,
      "status":"CHANGED",
      "modified_at":"2014-07-17 10:14:40.396",
      "version":3,
      "checksum":2978417559,
      "size":30,
      "mimetype":"text/plain",
      "chunks":[
      ]
      },
      {
      "id":179,
      "parent_id":null,
      "filename":"hello.txt",
      "is_folder":false,
      "status":"CHANGED",
      "modified_at":"2014-06-26 11:52:58.251",
      "version":2,
      "checksum":623379771,
      "size":13,
      "mimetype":"text/plain",
      "chunks":[
      ]
      },
      {
      "id":179,
      "parent_id":null,
      "filename":"hello.txt",
      "is_folder":false,
      "status":"NEW",
      "modified_at":"2014-06-26 11:52:58.251",
      "version":1,
      "checksum":310510519,
      "size":9,
      "mimetype":"text/plain",
      "chunks":[
      ]
      }
]
}

```

## Get file version metadata

To retrieve information about a file version, an application submits an HTTP GET request to the file version resource.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, and ends with **/version/version-number**, for example, **/file/2148742318/version/2**.

#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
GET /file/2148742318/version/2
 
StackSync-API: v2
```


### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

{
"id":179,
"parent_id":null,
"filename":"hello.txt",
"is_folder":false,
"status":"NEW",
"modified_at":"2014-06-26 11:52:58.251",
"version":1,
"checksum":310510519,
"size":9,
"mimetype":"text/plain",
"chunks":[
],
"contents":[
]
}

```

## Get file version data

To retrieve data about a file version, an application submits an HTTP GET request to the file version resource.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with */file*, and ends with */version/version-number/data*, for example, */file/2148742318/version/2/data*.


#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
GET /file/2148742318/version/2/data
 
StackSync-API: v2
```


### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
The response body contains the retrieved file data.


#### Response example

```json

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

<File content…. >

```
#Folder
## Create a folder

An application can create a folder by issuing an HTTP POST request to the URL of the containing folder resource. In addition, the application needs to provide as input, JSON that identifies the display name of the folder to be created.

### Request

#### URL structure

**/folder**.

#### Method
POST

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
**Content-Type** | The content type and character encoding of the response. The content type must be **application/json**, and the character encoding must be **UTF-8**.

#### Request Query arguments
JSON input that contains a dictionary with the following keys:

FIELD |  DESCRIPTION | REQUIRED
--- | --- | ---
**name** | The user-visible name of the folder to be created. | Yes
**parent** | ID of the folder where the folder is going to be uploaded. If no ID is passed, it will use the top-level folder. This parameter should **not** point to a file. | No

#### HTTP Request Example

```
POST /folder
 
StackSync-API: v2
Content-Type: application/json

{
     “name”: “clients”,
     “parent”:681465736
}
```


### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.
**Location** | The location of the newly created file.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json

HTTP/1.1 201 Created
Content-Type: application/json; charset=UTF-8
Content-Length: 248
Location: https://domain.ext/stacksync/folder/9873615

{
"id":642,
"parent_id":null,
"filename":"test_folder_for_documtation",
"is_folder":true,
"status":"NEW",
"modified_at":"Tue Apr 28 11:56:53 CEST 2015",
"version":1,
"checksum":0,
"size":0,
"mimetype":"inode/directory""
}

```
## Delete a folder

An application can permanently delete a folder by issuing an HTTP DELETE request to the URL of the folder resource. It's a good idea to precede DELETE requests like this with a caution note in your application's user interface.

### Request

#### URL structure

The URL that represents the file data resource. The URL begins with **/folder**, for example, **/folder/2148742318.**

#### Method
DELETE

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
DELETE /folder/2148742318
 
StackSync-API: v2
```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.

#### Response example

```json

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

{
"id":2022,
"parent_id":null,
"filename":"tmp",
"is_folder":true,
"status":"DELETED",
"modified_at":"Fri May 15 15:11:31 CEST 2015",
"version":2,
"checksum":0,
"size":0,
"mimetype":"inode/directory"
}

```

## Get Folder Metadata

To retrieve information about a folder, an application submits an HTTP GET request to the folder resource that represents the folder. To get information about the root folder, users must set the ID to “0” (i.e. /folder/0).

### Request

#### URL structure

The URL that represents the file data resource. The URL begins with **/folder**, for example, **/folder/2148742318**.

#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### HTTP Request Example

```
GET /folder/2148742318
 
StackSync-API: v2
```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**is_root** | Flag indicating whether it is the root folder or not

#### Response example

```json

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248

{
"id":642,
"parent_id":null,
"filename":"test_folder_for_documtation",
"is_folder":true,
"status":"NEW",
"modified_at":"2015-04-28 11:56:53.205",
"version":1,
"checksum":0,
"size":0,
"mimetype":"inode/directory",
"is_root":false,
"contents":[
]
}

```

## Get Folder Content Metadata

To retrieve information about a folder, an application submits an HTTP GET request to the folder resource that represents the folder. To get information about the root folder, users must set the folder ID to “0” (i.e. /folder/0/contents).

### Request

#### URL structure

The URL that represents the file data resource. The URL begins with **/folder**, followed by **/contents**, for example, **/folder/2148742318/contents**.

#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### Request Query arguments
JSON input that contains a dictionary with the following keys:

FIELD |  VALUE | DECRIPTION
--- | --- | ---
**include_deleted** | true o false | False by default. If this parameter is set to true, then response will include metadata of deleted objects.

#### HTTP Request Example
```json
GET /folder/2148742318/contents
 
StackSync-API: v2
```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
The response body contains a JSON dictionary with the following keys:
ELEMENT |  DESCRIPTION
--- | --- 
**folders** | A list with all the folders.
**files** | A list with all the files.

Each folder metadata is composed by:

ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**is_root** | Flag indicating whether it is the root folder or not

Each file metadata is compounded by:

**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.
**chunks** | Name list of created chunks

#### Response example

```json

{
"id":null,
"parent_id":null,
"filename":"root",
"is_folder":true,
"status":null,
"version":null,
"checksum":null,
"size":null,
"mimetype":null,
"is_root":true,
"contents":[
    {
    "id":628,
    "parent_id":null,
    "filename":"hola",
    "is_folder":true,
    "status":"RENAMED",
    "modified_at":"2015-04-14 11:41:07.65",
    "version":2,
    "checksum":0,
    "size":0,
    "mimetype":"inode/directory",
    "is_root":false
    },
    {
    "id":630,
    "parent_id":null,
    "filename":"datos_reviewers_eyeos",
    "is_folder":false,
    "status":"NEW",
    "modified_at":"2014-11-03 12:51:18.0",
    "version":1,
    "checksum":2082568738,
    "size":349,
    "mimetype":"text/plain",
    "chunks":[
    ]
    }
]
}

```

## Update folder metadata

An application can update various attributes of a folder by issuing an HTTP PUT request to the URL that represents the folder resource. In addition, the app needs to provide as input, JSON that identifies the new attribute values for the folder. Upon receiving the PUT request, the StackSync service examines the input and updates any of the attributes that have been modified.

Here are the file attributes that can be updated:
 * name
 * parent
No other file attributes can be modified using a PUT request.

**Note:** An application can move a file to a different parent folder by changing the value of the parent element.

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/file**, and ends with the file ID, for example, **/file/2148742318**.

#### Method
PUT

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
**Content-Type** | The content type and character encoding of the response. The content type must be **application/json**, and the character encoding must be **UTF-8**.

#### Request Body
JSON input that contains a dictionary with the following keys:

FIELD |  DESCRIPTION | REQUIRED
--- | --- | ---
**name** | The user-visible name of the file to be created. | NO
**parent** | ID of the folder where the file is going to be created. If no ID is passed, it will use the top-level folder. This parameter should **not** point to a file. | No

#### HTTP Request Example

```

POST /folder/2148742318

StackSync-API: v2
Content-Length: 294
Content-Type: application/json

{
     “name”: “clients_2”,
     “parent”:12386548974
}

```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.
**Location** | The location of the newly created file.

#### Response Body
ELEMENT |  DESCRIPTION
--- | --- 
**filename** | The user-visible name of the file to be created.
**id** | A unique identifier for a file or folder.
**parent_id** | ID of the folder’s parent.
**is_folder** | Flag indicating whether it is a folder or not.
**status** | Possible values are “NEW”, “CHANGED”, “DELETED”. Indicating the status of the file in this specific version.
**version** | A unique identifier for the current version of a file. Can be used to detect changes and avoid conflicts.
**checksum** | The file’s checksum.
**size** | The file size in bytes.
**mimetype** | The media type of the file. http://www.iana.org/assignments/media-types
**modified_at** | This is the modification time set by the server at the time of processing the file.

#### Response example

```json

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 248
Location: https://domain.ext/stacksync/file/

{
"id":628,
"parent_id":null,
"filename":"hola",
"is_folder":true,
"status":"RENAMED",
"modified_at":"Tue Apr 14 11:41:07 CEST 2015",
"version":2,
"checksum":0,
"size":0,
"mimetype":"inode/directory"
}

```
## Share a folder

An application can share a folder with other users by issuing an HTTP POST request to the URL that represents the folder resource. The app must provide a JSON object that represents the users that will be invited to the folder.

### Request

#### URL structure

The URL that represents the file data resource. The URL begins with **/folder**, follows with the file ID, and ends with **/share**, for example, **/folder/214874/share**.

#### Method
POST

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
**Content-Type** | The content type and character encoding of the response. The content type must be **application/json**, and the character encoding must be **UTF-8**.

#### Request Body
JSON input that contains a dictionary with the following keys:

FIELD |  DESCRIPTION | REQUIRED
--- | --- | ---
**share_to** |Array of emails representing the users that will be invited to the shared folder. | Yes

#### HTTP Request Example
```json
POST /folder/214874/share

StackSync-API: v2
Content-Length: 294
Content-Type: application/json

["john.doe@yahoo.com", "walter.smith@stacksync.com", "foo@bar.com"]
```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response example

```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 0

{"shared_to":["john.doe@yahoo.com", "walter.smith@stacksync.com", "foo@bar.com"]}
```
## Unshare a folder

An application can unshare a folder with other users by issuing an HTTP POST request to the URL that represents the folder resource. The app must provide a JSON object that represents the users that will be remove to the folder.

### Request

#### URL structure

The URL that represents the file data resource. The URL begins with **/folder**, follows with the file ID, and ends with **/unshare**, for example, **/folder/214874/unshare**.

#### Method
POST

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.
**Content-Length** | The length of the request body.
**Content-Type** | The content type and character encoding of the response. The content type must be **application/json**, and the character encoding must be **UTF-8**.

#### Request Body
JSON input that contains a dictionary with the following keys:

FIELD |  DESCRIPTION | REQUIRED
--- | --- | ---
**unshare_to** |Array of emails representing the users that will be invited to the shared folder. | Yes

#### HTTP Request Example
```json
POST /folder/214874/unshare

StackSync-API: v2
Content-Length: 294
Content-Type: application/json

["john.doe@yahoo.com", "walter.smith@stacksync.com", "foo@bar.com"]
```

#### Errors and Decisions
 * An invited user can’t unshare the folder with its owner. Error response: [{"error":400,"description":"Email a@a.a corresponds with owner of the folder."}] 
 * User can not unshare himself the folder. If the email list contains more emails than his email, his email will be discarded and the other users will be removed from the shared folder. NOT ERROR RESPONSE.
 * If the email list is empty or not contains any valid email. Error response: [{"error":400,"description":"No addressees found"}] 
 * If email list contains some email that not corresponds to any user, this email will be discarded. 

### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response example

```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 0

{"unshared_to":["john.doe@yahoo.com", "walter.smith@stacksync.com", "foo@bar.com"]}
```
## Get folder members

To retrieve information about the users that have access to a folder, an application submits an HTTP GET request to the folder resource that represents the folder. 

### Request

#### URL structure
The URL that represents the file data resource. The URL begins with **/folder**, followed by the ID of the folder, and ending with **/members**, for example, **/folder/2148742/members**.

#### Method
GET

#### Request Headers

The request header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**StackSync-API** | API version. The value must be **v2**.

#### Request Body
JSON input that contains a dictionary with the following keys:

FIELD |  DESCRIPTION | REQUIRED
--- | --- | ---
**name** | The user-visible name of the file to be created. | NO
**parent** | ID of the folder where the file is going to be created. If no ID is passed, it will use the top-level folder. This parameter should **not** point to a file. | No

#### HTTP Request Example

```
GET /folder/2148742/members
 
StackSync-API: v2
```
### Response
#### Response Header

The response header includes the following information:

FIELD |  DESCRIPTION
--- | --- 
**Content-Length** | The length of the retrieved content.
**Content-Type** | The content type and character encoding of the response.

#### Response Body
The response body contains a JSON array enclosing dictionaries with the following keys:

ELEMENT |  DESCRIPTION
--- | --- 
**name** | The name of the user
**email** | The email of the user
**joned_at** | The date the user joined the folder
**is_owner** | Whether the user is the owner of the folder or not. Options are **True** or **False**.

#### Response example

```json

[
	{
		"name":"John Doe",
		"email":"john.doe@yahoo.com",
		"joined_at":"2014-04-11 10:02:33.432",
		"is_owner":true
	},
	{
		"name":"Walter Smith",
		"email":"walter.smith@stacksync.com",
		"joined_at":"2014-05-30 19:39:21.044",
		"is_owner":false
	},
	{
		"name":"Foo Bar",
		"email":"foo@bar.com",
		"joined_at":"2014-06-06 15:42:41.852",
		"is_owner":false
	}
]

```
