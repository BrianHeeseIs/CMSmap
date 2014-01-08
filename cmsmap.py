#!/usr/bin/python

import smtplib, base64, os, sys, getopt, urllib2, urllib, re, socket, time, itertools, urlparse, threading, Queue, multiprocessing

  
class Initialize:
    # Save Wordpress, Joomla and Drupal plugins in a local file
    # Set default parameters 
    def __init__(self):
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}
    
    def GetWordPressPlugins(self):
        # Download Wordpress Plugins from Wordpress SVN website and popular Wordpress plugins page
        print "[*] Downloading WordPress plugins"
        f = open("wp_plugins.txt", "a")
        
        # from SVN Website
        htmltext = urllib2.urlopen("http://plugins.svn.wordpress.org").read()
        regex = '">(.+?)/</a></li>'
        pattern =  re.compile(regex)
        plugins = re.findall(pattern,htmltext)
        for plugin in plugins: f.write("%s\n" % plugin)
        
        # from popular Wordpress plugins page
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
        #oldplugins = [line.strip() for line in open('wp_plugins.txt')]
        #plugins = plugins + oldplugins
        #plugins = sorted(set(plugins))        
        # write to file
        #for plugin in plugins: f.write("%s\n" % plugin, "a")
        
        f.close()
         
        print "[*] Wordpress Plugin File: %s" % ('wp_plugins.txt')
   
    def GetWordpressPluginsExploitDB(self):
        # Download Wordpress Plugins from ExploitDB website
        f = open("wp_plugins.txt", "a")
        print "[*] Downloading Wordpress plugins from ExploitDB website"
        
        htmltext = urllib2.urlopen("http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description=Wordpress").read()
        regex ='filter_page=(.+?)\t\t\t.*>&gt;&gt;</a>'
        pattern =  re.compile(regex)
        pages = re.findall(pattern,htmltext)
        for page in range(1,int(pages[0])):
            time.sleep(2)
            request = urllib2.Request("http://www.exploit-db.com/search/?action=search&filter_page="+str(page)+"&filter_description=Wordpress",None,self.headers)
            htmltext = urllib2.urlopen(request).read()
            regex = '<a href="http://www.exploit-db.com/download/(.+?)">'
            pattern =  re.compile(regex)
            ExploitID = re.findall(pattern,htmltext)
            print page
            for Eid in ExploitID:
                htmltext = urllib2.urlopen("http://www.exploit-db.com/download/"+str(Eid)+"/").read()
                regex = '/plugins/(.+?)/'
                pattern =  re.compile(regex)
                WPplugins = re.findall(pattern,htmltext)
                print Eid
                print WPplugins
                for plugin in WPplugins:
                    try:
                        f.write("%s\n" % plugin)
                    except IndexError:
                        pass
        f.close()
        print "[*] Wordpress Plugin File: %s" % ('wp_plugins.txt')     

    def GetJoomlaPlugins(self):
        # Not Implemented yet
        pass
    
    def GetJoomlaPluginsExploitDB(self):
        # Download Joomla Plugins from ExploitDB website
        f = open("joomla_plugins.txt", "a")
        print "[*] Downloading Joomla plugins from ExploitDB website"
        htmltext = urllib2.urlopen("http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description=Joomla").read()
        regex ='filter_page=(.+?)\t\t\t.*>&gt;&gt;</a>'
        pattern =  re.compile(regex)
        pages = re.findall(pattern,htmltext)
        for page in range(1,int(pages[0])):
            time.sleep(2)
            request = urllib2.Request("http://www.exploit-db.com/search/?action=search&filter_page="+str(page)+"&filter_description=Joomla",None,self.headers)
            htmltext = urllib2.urlopen(request).read()
            regex = '<a href="http://www.exploit-db.com/download/(.+?)">'
            pattern =  re.compile(regex)
            ExploitID = re.findall(pattern,htmltext)
            for Eid in ExploitID:
                htmltext = urllib2.urlopen("http://www.exploit-db.com/exploits/"+str(Eid)+"/").read()
                regex = '\?option=(.+?)\&'
                pattern =  re.compile(regex)
                JoomlaComponent = re.findall(pattern,htmltext)
                try:
                    f.write("%s\n" % JoomlaComponent[0])
                except IndexError:
                    pass
        f.close()
        print "[*] Joomla Plugin File: %s" % ('joomla_plugins.txt')

    def GetDrupalPlugins(self):
        # Download Drupal Plugins from Drupal website
        print "[*] Downloading Drupal plugins"
        f = open("drupal_plugins.txt", "a")
        for n in range(0,969):
            htmltext = urllib2.urlopen("https://drupal.org/project/project_module?page="+str(n)+"&solrsort=iss_project_release_usage%20desc&").read()
            regex = '<a href="/project/(\w*?)">'
            pattern =  re.compile(regex)
            plugins_per_page = re.findall(pattern,htmltext)
            for plugin in plugins_per_page: f.write("%s\n" % plugin) 
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*((100*(n+1))/969), (100*(n+1))/969))
            sys.stdout.flush()            
        print "[*] Drupal Plugin File: %s" % ('drupal_plugins.txt') 





class Scanner:
    # Detect type of CMS -> Maybe add it to the main after Initialiazer 
    def __init__(self,url):
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}
        self.url = url 

    def FindCMSType(self):
        htmltext = urllib2.urlopen(self.url).read()
        m = re.search("Wordpress", htmltext)
        if m: print "[*] CMS Detection: Wordpress"; wordpress = WPScan(self.url)
            
        m = re.search("Joomla", htmltext)
        if m: print "[*] CMS Detection: Joomla"; joomla = JooScan(self.url)
            
        m = re.search("Drupal", htmltext);
        if m: print "[*] CMS Detection: Drupal"; drupal = DruScan(self.url)
            

class WPScan:
    # Scan WordPress site
    def __init__(self,url):
        self.url = url
        self.queue_num = 5
        self.thread_num = 10
        self.pluginPath = "/wp-content/plugins/"
        self.plugins = [line.strip() for line in open('wp_plugins.txt')]
        
        self.WPVersion()
        self.WPConfigFiles()
        self.WPplugins()
        ExploitDBSearch(self.url, 'Wordpress', pluginsFound)
        self.WPDefaultFiles()
               
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

    def WPDefaultFiles(self):
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

    def WPplugins(self):
        print "[*] Searching Wordpress plugins ..."
        # Create Code
        q = Queue.Queue(self.queue_num)
        
        # Spawn all threads into code
        for u in range(self.thread_num):
            t = ThreadScanner(self.url,self.pluginPath,q)
            t.daemon = True
            t.start()
        
        # Add all plugins to the queue
        for i in self.plugins:
            q.put(i)  
        q.join()

class JooScan:
    # Scan Joomla site
    def __init__(self,url):
        self.url = url
        self.queue_num = 5
        self.thread_num = 10
        #self.cmstype = "?option="
        self.pluginPath = "/components/"
        self.plugins = [line.strip() for line in open('joomla_plugins.txt')]
        
        self.JooVersion()
        self.JooConfigFiles()
        self.JooComponents()
        ExploitDBSearch(self.url, "Joomla", pluginsFound)
        self.JooDefaultFiles()
        
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
    
    def JooDefaultFiles(self):
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

    def JooComponents(self):
        print "[*] Searching Joomla Components ..."
        # Create Code
        q = Queue.Queue(self.queue_num)
        
        # Spawn all threads into code
        for u in range(self.thread_num):
            t = ThreadScanner(self.url,self.pluginPath,q)
            t.daemon = True
            t.start()
        
        # Add all plugins to the queue
        for i in self.plugins:
            q.put(i)  
        q.join()
        
class DruScan:
    # Scan Drupal site
    def __init__(self,url):
        self.url = url
        self.queue_num = 5
        self.thread_num = 10
        self.pluginPath = "/modules/"
        self.plugins = [line.strip() for line in open('drupal_plugins.txt')]
        
        DruScan.DruVersion(self)
        self.DruConfigFiles()
        self.DruModules()
        ExploitDBSearch(self.url, "Drupal", pluginsFound)
        self.DefaultFiles()
        
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

    def DruModules(self):
        print "[*] Searching Drupal Modules ..."
        # Create Code
        q = Queue.Queue(self.queue_num)
        
        # Spawn all threads into code
        for u in range(self.thread_num):
            t = ThreadScanner(self.url,self.pluginPath,q)
            t.daemon = True
            t.start()
        
        # Add all plugins to the queue
        for i in self.plugins:
            q.put(i)  
        q.join()

class OutputReport:

    #def TXT:
        pass
    
    #def HTML:
        pass
    
    #def XML:
        pass
    
class ExploitDBSearch:
    def __init__(self,url,cmstype,pluginList):
        self.url = url
        self.pluginList = pluginList
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}
        print "[*] Searching vulnerable plugins from ExploitDB website"
        for plugin in self.pluginList:
            htmltext = urllib2.urlopen("http://www.exploit-db.com/search/?action=search&filter_description="+cmstype+"&filter_exploit_text="+plugin).read()
            regex = '/download/(.+?)">'
            pattern =  re.compile(regex)
            ExploitID = re.findall(pattern,htmltext)
            print plugin
            for Eid in ExploitID:
                print "\t[*] Vulnerable Plugin: http://www.exploit-db.com/exploits/"+Eid
                

    
class ThreadScanner(threading.Thread):
    # Multi-threading Scan Class (just for Wordpress for now) 
    def __init__(self,url,cmstype,q):
        threading.Thread.__init__ (self)
        self.url = url
        self.q = q
        self.cmstype = cmstype
        self.agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers={'User-Agent':self.agent,}
        
    def run(self):
        while True:
            # Get plugin from plugin queue
            plugin = self.q.get()
            req = urllib2.Request(self.url+self.cmstype+plugin)
            try:
                urllib2.urlopen(req)
                print plugin; pluginsFound.append(plugin)
            except urllib2.HTTPError, e:
                #print e.code
                if e.code != 404: print plugin; pluginsFound.append(plugin)
            self.q.task_done()


    def GetPlugins(self):
        #=== No thread Method =============
        for plugin in self.plugins:
            req = urllib2.Request('http://192.168.71.133/wp/wp-content/plugins/'+plugin+'/')
            try:
                urllib2.urlopen(req)
                print plugin
            except urllib2.HTTPError, e:
                #print e.code
                pass
        #==================================
        
   



        
        
class BruteForce:
        pass
    
class PostExploit:
        pass
    
class JobQue:
        pass

# Global Variables 

pluginsFound = []
version=0.1

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
        #initializer.GetJoomlaPluginsExploitDB()
        #initializer.GetWordpressPluginsExploitDB()
        #initializer.GetDrupalPlugins()

    start = time.time()
    print "Start: ", start
    #scanner = CMStype(url)
    #scanner.FindCMS()
    
    scanner = Scanner(url).FindCMSType()
    end = time.time()
    print "End: ", end
    print end - start, "seconds"

        
        
                

