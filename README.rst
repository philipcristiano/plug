Plug
====

Plug is a tool to automate packaging and installation of Python daemons
including Python dependencies in the package. It grew out of my use of
Supervisor and the problems of managing large numbers of processe.

Installing
==========

Use pip!

    pip install plug


Creating a Plug
===============

To create a plug you create a config file with minimal information then run

    plug create {package_name}

The config file looks something like:

    [server1]
    command=bin/python -m SimpleHTTPServer 8001
    user=plug_user

You will be left with a plug:

    {package_name}.server1.plug

Installing a Plug
=================

Once you put this on your system you can run

    plug install {package_name}.server1.plug

This will create a new virtualenv in /srv/plug ready to be setup as a daemon.
To have runit start the process you run:

    plug setup {package_name}.server1.plug

Optionally with the argument --number to setup multiple daemons from that
package. The number causes multiple links to be created in /etc/sv and
/etc/srv.

Uninstalling a Plug
===================

To uninstall the plug use the ``uninstall`` command

    plug uninstall {package_name}.server1.plug

This will also remove the links for runit.

Other Commands
==============

Other commands included are ``list`` and ``status`` which will list all plugs
installed and the runit status of each daemon instance.
