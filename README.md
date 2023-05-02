# WP-LogCrack

### Combine wpbiff and delorean

Requirements
------------

This utility runs on Python 3 and requires administrator privileges

```
sudo python3 WPLogCrack.py  --server http://192.168.43.167/wordpress/wp-login.php --username admin --password ubuntu --dns-spoof


```
Instructions for Use
==================

To successfully carry out an attack against a two-factor protected Wordpress blog, you must meet the following prerequisite.

Prerequisites
--------------

You need to have the login username and password for the Wordpress dashboard at ``/wp-admin``. Credentials can be acquired through phishing, key logging, or password reuse.

Options
-------
```
The following section explains the basic usage of WP-LogCrack. You can also use the ``--help`` switch at any time to get help.

--server SERVER vulnerable WordPress server [required]
--username USER Wordpress username [required]
--password PASS Wordpress password [required]
--dns-spoof or --no-dns-spoof The first one to use DNS-Spoofing with ettercap, the second one not to use it and autonomously choose a MITM type attack.[Boolean]
```