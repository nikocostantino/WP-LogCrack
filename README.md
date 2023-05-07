# WP-LogCrack

### Tool to combine `Wpbiff` and `Deloran`

`WPbiff`: https://github.com/gszathmari/wpbiff

`Delorean`: https://github.com/jselvi/Delorean

Requirements
------------

This utility runs on Python 3 and requires administrator privileges.

Instructions for Use
==================

To successfully carry out an attack against a two-factor protected Wordpress blog, you must meet the following prerequisites.

Prerequisites
--------------

1. You need to have the login username and password for the Wordpress dashboard at ``/wp-admin``. Credentials can be acquired through phishing, key logging, or password reuse.
2. You must have **WPbiff** and **ettercap** installed on your machine.
3. **Delorean** is already present in a project folder

Options
-------
```
The following section explains the basic usage of WP-LogCrack. You can also use the ``--help`` switch at any time to get help.

--server SERVER vulnerable WordPress server [required]
--username USER Wordpress username [required]
--password PASS Wordpress password [required]
--dns-spoof or --no-dns-spoof, the first one to use DNS-Spoofing with ettercap, the second one not to use it and autonomously choose a MITM type attack.[Boolean]
```
Example of use
-------
Where server is **http://192.168.43.167/wordpress/wp-login.php** , username **admin**, password **ubuntu**, and you are chosen to use DNS spoofing ``--dns-spoof``

```
sudo python3 WPLogCrack.py  --server http://192.168.43.167/wordpress/wp-login.php --username admin --password ubuntu --dns-spoof

```