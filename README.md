StackSync API module
--------------------


1) Install StackSync REST API.

    $ sudo python setup.py install


2) Edit your proxy-server.conf pipeline to enable the StackSync API module.

    [pipeline:main]
    pipeline = healthcheck cache authtoken keystone __stacksync-api__ proxy-server

3) And add the WSGI filter below:

    [filter:stacksync-api]
    use = egg:stacksync-api-swift#stacksync_api
    stacksync_host = 127.0.0.1
    stacksync_port = 61234

4) Restart the proxy:

    $ swift-init proxy restart

