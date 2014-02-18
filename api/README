StackSync REST API
------------------

Module for OpenStack to simulate StackSync behavior with a simple REST API.

First steps
    Extract StackAuth.tar:
        $ tar xvf StackAuth.tar

Install
-------

1) Install StackSync REST API with `sudo python setup.py install`.


2) Alter your proxy-server.conf pipeline to enable apiweb:

    Was::

        [pipeline:main]
        pipeline = healthcheck cache authtoken keystone proxy-server

    Change To::

        [pipeline:main]
        pipeline = healthcheck cache authtoken keystone apiweb proxy-server

3) Add to your proxy-server.conf the section for the StackSync WSGI filter::

   [filter:apiweb] 
   use = egg:apiweb#apiweb


4) Restart the proxy:
    $ sudo swift-init proxy restart


Uninstall
---------

1) Change the pipeline of the proxy-server.conf again to disable the stacksync module.
    
    Was::
        [pipeline:main] 
        pipeline = healthcheck cache authtoken keystone apiweb proxy-server 
    
    Change To::
        [pipeline:main] 
        pipeline = healthcheck cache authtoken keystone proxy-server 

2) Restart the proxy:
    $ sudo swift-init proxy restart