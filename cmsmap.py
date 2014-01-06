#!/usr/bin/python

import smtplib, base64, os, sys, getopt, urllib2, urllib, re, socket, time, itertools, urlparse, threading, Queue, multiprocessing
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
SHODAN_API_KEY = "AEzTfpDGdjHukHq48105386CHnunaTXB"
 
    
class Initialize:
    # Save Wordpress, Joomla and Drupal plugins in a local file
    # Set default parameters 
    def __init__(self):
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}
    
    def GetWordPressPlugins(self):
        print "[*] Downloading WordPress plugins"
        f = open("plugins.txt", "a")
        htmltext = urllib2.urlopen("http://plugins.svn.wordpress.org").read()
        regex = '">(.+?)/</a></li>'
        pattern =  re.compile(regex)
        plugins = re.findall(pattern,htmltext)
        for plugin in plugins: f.write("%s\n" % plugin)
        
        for n in range(1,1844):
            while True:
                try:
                    htmltext = urllib2.urlopen("http://wordpress.org/extend/plugins/browse/popular/page/"+str(n)+"/").read()
                    regex = '<h3><a href="http://wordpress.org/plugins/(.+?)/">'
                    pattern =  re.compile(regex)
                    plugins_per_page = re.findall(pattern,htmltext) 
                    #plugins.append(plugins_in_page)
                    for plugin in plugins_per_page: f.write("%s\n" % plugin) 
                    #sys.stdout.write("\r%d%%" %((100*(n+1))/1844))
                    #sys.stdout.flush()
                    sys.stdout.write('\r')
                    sys.stdout.write("[%-100s] %d%%" % ('='*((100*(n+1))/1844), (100*(n+1))/1844))
                    sys.stdout.flush()
                except:
                    time.sleep(4)
                    continue
                break
            
        # sort unique
        #oldplugins = [line.strip() for line in open('plugins.txt')]
        #plugins = plugins + oldplugins
        #plugins = sorted(set(plugins))
        
        # write to file
        f.close()
        #for plugin in plugins: f.write("%s\n" % plugin, "a")  
        print "[*] Writing file: %s" % ('plugins.txt')
        

    def GetJoomlaPlugins(self):
        pass
    
    def GetDrupalPlugins(self):
        print "[*] Downloading Drupal plugins"
        f = open("drupal_plugins.txt", "a")
        for n in range(0,969):
            htmltext = urllib2.urlopen("https://drupal.org/project/modules?page="+str(n)+"+&solrsort=iss_project_release_usage desc&f[0]=bundle:project_project&f[1]=im_vid_3:14&f[2]=bundle:project_project").read()
            regex = '<a href="/project/(\w*?)">'
            pattern =  re.compile(regex)
            plugins_per_page = re.findall(pattern,htmltext)
            for plugin in plugins_per_page: f.write("%s\n" % plugin) 
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*((100*(n+1))/969), (100*(n+1))/969))
            sys.stdout.flush()
        print "[*] Writing file: %s" % ('drupal_plugins.txt')
        sys.exit() 

    def ExploitDBSearch(self,query,file):
        f = open(file, "a")
        print "[*] Downloading "+query+" plugins"
        
        htmltext = urllib2.urlopen("http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description="+query).read()
        regex ='filter_page=(.+?)\t\t\t.*>&gt;&gt;</a>'
        pattern =  re.compile(regex)
        pages = re.findall(pattern,htmltext)
        for page in range(1,int(pages[0])):
            print "page "+str(page)
            time.sleep(2)
            request = urllib2.Request("http://www.exploit-db.com/search/?action=search&filter_page="+str(page)+"&filter_description="+query,None,self.headers)
            htmltext = urllib2.urlopen(request).read()
            regex = '<a href="http://www.exploit-db.com/download/(.+?)">'
            pattern =  re.compile(regex)
            ExploitID = re.findall(pattern,htmltext)
            for Eid in ExploitID:
                htmltext = urllib2.urlopen("http://www.exploit-db.com/exploits/"+str(Eid)+"/").read()
                regex = '\?option=(.+?)\&'
                pattern =  re.compile(regex)
                JoomlaComponent = re.findall(pattern,htmltext)
                print JoomlaComponent
                try:
                    f.write("%s\n" % JoomlaComponent[0])
                except IndexError:
                    pass



class CMStype:
    # Detect type of CMS
    pass

class WPScan:
    # Scan WordPress site
    pass

class JooScan:
    # Scan Joomla site
    pass

class DruScan:
    # Scan Drupal site
    pass

class OutputReport:

    #def TXT:
        pass
    
    #def HTML:
        pass
    
    #def XML:
        pass
    
class Scanner:
    def __init__(self):
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}

                
    def GetPlugins(self):
        #No thread Method =============
        plugins = open('wp_plugins.txt')
        for plugin in plugins:
            req = urllib2.Request('http://192.168.71.133/wp/plugins/'+plugin[0]+'/',None,self.headers)
            try:
                urllib2.urlopen(req)
                print plugin[0]
            except urllib2.HTTPError, e:
                #print e.code
                pass
        #==============================
        
        # called by each thread
    def GetPluginsTread(self,plugin):
        url = 'http://192.168.71.133/wp/wp-content/plugins/'+plugin
        #print url
        req = urllib2.Request(url)
        try:
            urllib2.urlopen(req)
            print plugin
        except urllib2.HTTPError, e:
            #print e.code
            pass
        
    
    plugins = [line.strip() for line in open('wp_plugins.txt')]
    
    threadlist = []
    q = Queue.Queue()
    
    for u in plugins:
        t = threading.Thread(target=GetPluginsTread, args=(u,u))
        t.daemon = True
        t.start()
        threadlist.append(t)
    
    for i in threadlist:
        i.join()

                
                
        
    
class BruteForce:
        pass
    
class PostExploit:
        pass
    
class JobQue:
        pass

#=======================
        '''
        def th(ur):
            base = "http://finance.yahoo.com/q?="
            regex = "<title>(.+?)</title>"
            pattern =  re.compile(regex)
            htmltext = urllib.urlopen(url).read()
            results = re.findall(pattern,htmltext)
            print results
        
        symbolslist = open("symbols.txt").read()
        symbolslist = symbolslist.replace(" ","").split()
        
#=======================
        # called by each thread
        def get_url(q, url):
            q.put(urllib2.urlopen(url).read())
        
        theurls = 'http://google.com http://yahoo.com'.split()
        
        q = Queue.Queue()
        
        for u in theurls:
            t = threading.Thread(target=get_url, args = (q,u))
            t.daemon = True
            t.start()
        
        s = q.get()
        print s
        '''
#======================


# Global Methos

def WriteTextFile(fn,s):
    f = open(fn,"w")
    f.write(s)
    f.close()
    
def usage(version):
    print "cmsmap tool v"+str(version)+" - Automatic CMS Scanner\nUsage: " + os.path.basename(sys.argv[0]) + """ -u <URL>
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
    
    # if plugins don't exist (first time of running) then initiliaze
    if not os.path.exists('wp_plugins.txt' or 'joomla_plugins.txt' or 'drupal_plugins.txt'):
        initializer = Initialize()
        
        #initializer.GetWordPressPlugins()
        #initializer.GetDrupalPlugins()
        #initializer.WordPressPlugins()
        #initializer.ExploitDBSearch("Joomla","joomla_plugins.txt")
        #initializer.ExploitDBSearch("Wordpress","wp_plugins.txt")
        #initializer.ExploitDBSearch("Drupal","drupal_plugins.txt")
        
    #scanner = Scanner()
  
    #scanner.GetPluginsTread

    start = time.time()
    print "Start: ", start
    end = time.time()
    print "End: ", end
    print end - start, "seconds"

        
        
                

