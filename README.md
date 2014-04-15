CMSmap
======

CMSmap is a python open source CMS (Content Management System) scanner that automates the process 
of detecting security flaws of the most popular CMSs. The main purpose of CMSmap is to integrate common vulnerabilities 
for different types of CMSs in a single tool. 

At the moment, CMSs supported by CMSmap are WordPress, Joomla and Drupal.

Please note that this project is an early state. As such, you might find bugs, flaws or mulfunctions.
Use it at your own risk!


Installation
=====
You can download the latest version of CMSmap by cloning the GitHub repository:

	git clone https://github.com/Dionach/CMSmap.git


Usage
=====
	CMSmap tool v0.3 - Simple CMS Scanner
	Author: Mike Manzotti mike.manzotti@dionach.com
	Usage: cmsmap.py -t <URL>
	          -t, --target    target URL (e.g. 'https://abc.test.com:8080/')
	          -v, --verbose   verbose mode (Default: false)
	          -T, --threads   number of threads (Default: 5)
	          -u, --usr       username or file 
	          -p, --psw       password or file
	          -o, --output    save output in a file
	          -k, --crack     password hashes file
	          -w, --wordlist  wordlist file (Default: rockyou.txt - WordPress only)
	          -U, --update    update CMSmap to the latest version
	          -h, --help      show this help
	          
	Example: cmsmap.py -t https://example.com
	         cmsmap.py -t https://example.com -u admin -p passwords.txt
	         cmsmap.py -k hashes.txt


Disclaimer
=====
Usage of CMSmap for attacking targets without prior mutual consent is illegal. 
It is the end user's responsibility to obey all applicable local, state and federal laws. 
Developers assume NO liability and are NOT responsible for any misuse or damage caused by this program.