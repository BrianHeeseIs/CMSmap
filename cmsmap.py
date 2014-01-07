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
    def __init__(self,url):
        self.url = url
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}
        htmltext = urllib2.urlopen(self.url).read()
        m = re.search("Wordpress", htmltext)
        if m: print "[*] CMS Detection: Wordpress"; wordpress = WPScan(self.url)
        m = re.search("Joomla", htmltext)
        if m: print "[*] CMS Detection: Joomla"; joomla = JooScan(self.url)
        m = re.search("Drupal", htmltext)
        if m: print "[*] CMS Detection: Drupal"; drupal = DruScan(self.url)
       

class WPScan:
    # Scan WordPress site
    def __init__(self,url):
        self.url = url
        WPScan.WPVersion(self)
        WPScan.WPConfigFiles(self)
        WPScan.DefaultFiles(self)
        
    def WPVersion(self):
        try:
            htmltext = urllib2.urlopen(self.url+'/readme.html').read()
            regex = '<br /> Version (\d+\.\d+)'
            pattern =  re.compile(regex)
            version = re.findall(pattern,htmltext)
            print "[*] Wordpress Version: "+str(version[0])
        except urllib2.HTTPError, e:
            print e.code
            pass
    def WPConfigFiles(self):
        confFiles=['/wp-config.php.txt','/wp-config.old','/wp-config.php~','/wp-config.txt','/wp-config']
        for file in confFiles:
            req = urllib2.Request(self.url+file)
            try:
                urllib2.urlopen(req)
                print "[*] Configuration File Found: " +self.url+file
            except urllib2.HTTPError, e:
                #print e.code
                pass

    def DefaultFiles(self):
        # Check for default files
        defFiles=['/readme.html',
                  '/license.txt',
                  '/wp-config-sample.php',
                  '/wp-includes/images/crystal/license.txt',
                  '/wp-includes/images/crystal/license.txt',
                  '/wp-includes/js/plupload/license.txt',
                  '/wp-includes/js/plupload/changelog.txt',
                  '/wp-includes/js/tinymce/license.txt',
                  '/wp-includes/js/tinymce/plugins/spellchecker/changelog.txt',
                  '/wp-includes/js/swfupload/license.txt',
                  '/wp-includes/ID3/license.txt',
                  '/wp-includes/ID3/readme.txt',
                  '/wp-includes/ID3/license.commercial.txt',
                  '/wp-content/themes/twentythirteen/fonts/COPYING.txt',
                  '/wp-content/themes/twentythirteen/fonts/LICENSE.txt'
                  ]
        for file in defFiles:
            req = urllib2.Request(self.url+file)
            try:
                urllib2.urlopen(req)
                print "[*] Info Disclosure: " +self.url+file
            except urllib2.HTTPError, e:
                #print e.code
                pass
            
        # Check for default files in plugins directory such as README.txt, readme.txt, licences.txt, changelog.txt

class JooScan:
    # Scan Joomla site
    def __init__(self,url):
        self.url = url
        JooScan.JooVersion(self)
        JooScan.JooConfigFiles(self)
        JooScan.DefaultFiles(self)
        
    def JooVersion(self):
        try:
            htmltext = urllib2.urlopen(self.url+'/joomla.xml').read()
            regex = '<version>(.+?)</version>'
            pattern =  re.compile(regex)
            version = re.findall(pattern,htmltext)
            print "[*] Joomla Version: "+str(version[0])
        except urllib2.HTTPError, e:
            #print e.code
            pass
        
    def JooConfigFiles(self):
        confFiles=['/configuration.php.txt','/configuration.old','/configuration.php~','/configuration.txt','/configuration']
        for file in confFiles:
            req = urllib2.Request(self.url+file)
            try:
                urllib2.urlopen(req)
                print "[*] Configuration File Found: " +self.url+file
            except urllib2.HTTPError, e:
                #print e.code
                pass        
    
    def DefaultFiles(self):
        # Check for default files
        defFiles=['/README.txt',
                  '/htaccess.txt',
                  '/administrator/templates/hathor/LICENSE.txt',
                  '/web.config.txt',
                  '/joomla.xml',
                  '/robots.txt.dist',
                  '/LICENSE.txt',
                  '/media/jui/fonts/icomoon-license.txt',
                  '/media/editors/tinymce/jscripts/tiny_mce/license.txt',
                  '/media/editors/tinymce/jscripts/tiny_mce/plugins/style/readme.txt',
                  '/libraries/idna_convert/ReadMe.txt',
                  '/libraries/simplepie/README.txt',
                  '/libraries/simplepie/LICENSE.txt',
                  '/libraries/simplepie/idn/ReadMe.txt',
                  ]
        
        for file in defFiles:
            req = urllib2.Request(self.url+file)
            try:
                urllib2.urlopen(req)
                print "[*] Info Disclosure: " +self.url+file
            except urllib2.HTTPError, e:
                #print e.code
                pass

class DruScan:
    # Scan Drupal site
    def __init__(self,url):
        self.url = url
        DruScan.DruVersion(self)
        DruScan.DruConfigFiles(self)
        DruScan.DefaultFiles(self)
        
    def DruVersion(self):
        try:
            htmltext = urllib2.urlopen(self.url+'/CHANGELOG.txt').read()
            regex = 'Drupal (\d+\.\d+),'
            pattern =  re.compile(regex)
            version = re.findall(pattern,htmltext)
            print "[*] Drupal Version: "+str(version[0])
        except urllib2.HTTPError, e:
            #print e.code
            pass   

    def DruConfigFiles(self):
        confFiles=['/sites/default/settings.php.txt','/sites/default/settings.old','/sites/default/settings.php~','/sites/default/settings.txt','/sites/default/settings']
        for file in confFiles:
            req = urllib2.Request(self.url+file)
            try:
                urllib2.urlopen(req)
                print "[*] Configuration File Found: " +self.url+file
            except urllib2.HTTPError, e:
                #print e.code
                pass   
           
    def DefaultFiles(self):
        defFiles=['/README.txt',
                  '/robots.txt',
                  '/INSTALL.mysql.txt',
                  '/MAINTAINERS.txt',
                  '/profiles/standard/translations/README.txt',
                  '/profiles/minimal/translations/README.txt',
                  '/INSTALL.pgsql.txt',
                  '/UPGRADE.txt',
                  '/CHANGELOG.txt',
                  '/INSTALL.sqlite.txt',
                  '/LICENSE.txt',
                  '/INSTALL.txt',
                  '/COPYRIGHT.txt',
                  '/web.config',
                  '/modules/README.txt',
                  '/modules/simpletest/files/README.txt'
                  '/modules/simpletest/files/javascript-1.txt',
                  '/modules/simpletest/files/php-1.txt',
                  '/modules/simpletest/files/sql-1.txt',
                  '/modules/simpletest/files/html-1.txt',
                  '/modules/simpletest/tests/common_test_info.txt',
                  '/modules/filter/tests/filter.url-output.txt',
                  '/modules/filter/tests/filter.url-input.txt',
                  '/modules/search/tests/UnicodeTest.txt',
                  '/themes/README.txt',
                  '/themes/stark/README.txt',
                  '/sites/README.txt',
                  '/sites/all/modules/README.txt',
                  '/sites/all/themes/README.txt',
                  '/modules/simpletest/files/html-2.html',
                  '/modules/color/preview.html',
                  '/themes/bartik/color/preview.html'
                  ]
        
        for file in defFiles:
            req = urllib2.Request(self.url+file)
            try:
                urllib2.urlopen(req)
                print "[*] Info Disclosure: " +self.url+file
            except urllib2.HTTPError, e:
                #print e.code
                pass


class OutputReport:

    #def TXT:
        pass
    
    #def HTML:
        pass
    
    #def XML:
        pass
    
class Scanner(threading.Thread):
    # Multi-threading Scan Class (just for Wordpress for now) 
    def __init__(self,url,q):
        threading.Thread.__init__ (self)
        self.url = url
        self.q = q
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}

    def run(self):
        while True:
            # Get plugin from plugin queue
            plugin = self.q.get()
            req = urllib2.Request(self.url+'/wp-content/plugins/'+plugin)
            try:
                urllib2.urlopen(req)
                print plugin
            except urllib2.HTTPError, e:
                #print e.code
                pass
            self.q.task_done()

    def GetPlugins(self):
        #Old Method === No thread Method =============
        for plugin in self.plugins:
            req = urllib2.Request('http://192.168.71.133/wp/wp-content/plugins/'+plugin+'/')
            try:
                urllib2.urlopen(req)
                print plugin
            except urllib2.HTTPError, e:
                #print e.code
                pass
        #==============================
        
   
class ScanWordpressPlugins:
    def __init__(self, url):
        self.queue_num = 5
        self.thread_num = 10
        self.plugins = [line.strip() for line in open('wp_plugins.txt')]
        
        # Create Code
        q = Queue.Queue(self.queue_num)
        
        # Spawn all threads into code
        for u in range(self.thread_num):
            t = Scanner(url,q)
            t.daemon = True
            t.start()
        
        # Add all plugins to the queue
        for i in self.plugins:
            q.put(i)
        
        q.join()
        
        
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
    
    # if plugins don't exist (first time of running) then initialize
    if not os.path.exists('wp_plugins.txt' or 'joomla_plugins.txt' or 'drupal_plugins.txt'):
        initializer = Initialize()
        
        #initializer.GetWordPressPlugins()
        #initializer.GetDrupalPlugins()
        #initializer.WordPressPlugins()
        #initializer.ExploitDBSearch("Joomla","joomla_plugins.txt")
        #initializer.ExploitDBSearch("Wordpress","wp_plugins.txt")
        #initializer.ExploitDBSearch("Drupal","drupal_plugins.txt")
        

    start = time.time()
    print "Start: ", start
    #scanner = ScanWordpressPlugins(url)
    finder = CMStype(url)
    end = time.time()
    print "End: ", end
    print end - start, "seconds"

        
        
                

