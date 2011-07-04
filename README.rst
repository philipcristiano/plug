Plug
====

Plug is a tool to automate packaging and installation of Python daemons
including Python dependencies in the package. It grew out of my use of
Supervisor and the problems of managing large numbers of processe.

Installing
==========

Since many parts of Plug are still in flux you should clone the repo and run

    python setup.py install

to install Plug.


Creating a Plug
===============

To create a plug you create a config file with minimal information then run

    plug create --package={package_name}

The config file looks something like:

    [server1]
    command=bin/python -m SimpleHTTPServer 8001
    user=plug_user

You will be left with a plug:

    {package_name}.server1.plug

Installing a Plug
=================

Once you put this on your system you can run

    plug install --plug={package_name}.server1.plug

This will create a new virtualenv in /srv/plug ready to be setup as a daemon.
To have runit start the process you run:

    plug setup --plug={package_name}.server1.plug

Optionally with the argument --number to setup multiple daemons from that
package. The number causes multiple links to be created in /etc/sv and
/etc/srv.

Other Commands
==============

Other commands included are ``list`` and ``status`` which will list all plugs
installed and the runit status of each daemon instance.
