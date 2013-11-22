Welcome to StackSync!
=====================

> **NOTE:** This is BETA quality code!

**Table of Contents**

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Swift REST API](#swift-rest-api)
    - [Differences between V1 and V2](#differences-between-v1-and-v2)
- [Requirements](#requirements)
- [Installation instructions](#installation-instructions)
- [Uninstallation intructions](#uninstallation-instructions)
- [Issue Tracking](#issue-tracking)
- [Licensing](#licensing)
- [Contact](#contact)

# Introduction

StackSync (<http://stacksync.com>) is a scalable open source Personal Cloud
that implements the basic components to create a synchronization tool.


# Architecture

In general terms, StackSync can be divided into three main blocks: clients
(desktop and mobile), synchronization service (SyncService) and storage
service (Swift, Amazon S3, FTP...). An overview of the architecture
with the main components and their interaction is shown in the following image.

<p align="center">
  <img width="500" src="https://raw.github.com/stacksync/desktop/master/res/stacksync-architecture.png">
</p>

The StackSync client and the SyncService interact through the communication
middleware called ObjectMQ. The sync service interacts with the metadata
database. The StackSync client directly interacts with the storage back-end
to upload and download files.

As storage back-end we are using OpenStack Swift, an open source cloud storage
software where you can store and retrieve lots of data in virtual containers.
It's based on the Cloud Files offering from Rackspace. But it is also possible
to use other storage back-ends, such as a FTP server or S3.

# Swift REST API

This is a module for OpenStack Swift. It's aim is to simulate StackSync behaviour
with a simple REST API for mobile and web applications.

In the [docs folder](docs) there is the API specification. There are two different
APIs documents. This code implements V1 since V2 is not developed yet, but we
have ready the specification.

## Differences between V1 and V2

Main differences are:
- V1 code is hard to follow and it is bad structured. We started with some simple
features but then we stated adding new functionalities until we finally get a huge
file with horrible code.
- V1 is too inefficient since it has to create chunks and communicate with SyncService.
- Besides V2, V1 is not a real REST API!

With API v2 we want to solve all these problems.

# Requirements

- [Python-magic](https://github.com/ahupp/python-magic) library to obtain files mimetype:
        
        $ sudo apt-get install pip
        $ sudo pip install python-magic

# Installation instructions

1) Install StackSync REST API with:
        
        $ sudo python setup.py install


2) Alter your proxy-server.conf pipeline to enable apiweb:

From:

        [pipeline:main]
        pipeline = healthcheck cache authtoken keystone proxy-server

To:

        [pipeline:main]
        pipeline = healthcheck cache authtoken keystone apiweb proxy-server

3) Add to your proxy-server.conf the section for the StackSync WSGI filter::

        [filter:apiweb] 
        use = egg:apiweb#apiweb
        rpc_server_ip = SERVER_IP
        rpc_server_port = SERVER_PORT
        
If rpc_server_ip and rpc_server_port are not defined the default values will be 127.0.0.1 and 61234.


4) Restart the proxy:
    
        $ sudo swift-init proxy restart


# Uninstallation instructions

1) Change the pipeline of the proxy-server.conf again to disable the stacksync module.
    
From:

        [pipeline:main] 
        pipeline = healthcheck cache authtoken keystone apiweb proxy-server 
    
To:

        [pipeline:main] 
        pipeline = healthcheck cache authtoken keystone proxy-server 

2) Restart the proxy:
    
        $ sudo swift-init proxy restart
        
# Issue Tracking
For the moment, we are going to use the github issue tracking.

# Licensing
StackSync is licensed under the GPLv3. Check [license.txt](license.txt) for the latest
licensing information.

# Contact
Visit www.stacksync.com to contact information.
