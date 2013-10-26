#!/usr/bin/python

import smtplib, base64, os, sys, getopt, urllib2, urllib, re, socket, time, itertools, urlparse, multiprocessing
try:
    #from BeautifulSoup import BeautifulSoup
    from bs4 import BeautifulSoup
except:
    print "No BeautifulSoup installed"
    print "See: http://www.crummy.com/software/BeautifulSoup/#Download"
    sys.exit()
try:
    import DNS
except:
    print "No pyDNS installed"

version=0.1
 
    


def usage(version):
    print "CMScan tool v"+str(version)+" - Automatic CMS Scanner\nUsage: " + os.path.basename(sys.argv[0]) + """ -u <URL>
          -u, --url      target URL (e.g. 'https://abc.test.com:8080/')
          -v, --verbose  verbose mode (Default: false)
          -h, --help 
          """
    print "Example: "+ os.path.basename(sys.argv[0]) +" -u https://wordpress.com"
    
if __name__ == "__main__":
    # command line arguments
    if sys.argv[1:]:
        try:
            optlist, args = getopt.getopt(sys.argv[1:], 'u:vh', ["url=", "version", "help"])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err) # print something like "option -a not recognized"
            usage(version)
            sys.exit(2)  
        for o, a in optlist:
            if o == "-h":
                usage(version)
                sys.exit()
            elif o in ("-u", "--url"):
                url = a
                pUrl = urlparse.urlparse(url)
                #clean up supplied URLs
                netloc = pUrl.netloc.lower()
                scheme = pUrl.scheme.lower()
                path = pUrl.path.lower()
                if not scheme:
                    print 'VALIDATION ERROR: http(s):// prefix required'
                    exit(1)
            elif o == "-v":
                verbose = True
            else:
                usage(version)
                sys.exit()
                

