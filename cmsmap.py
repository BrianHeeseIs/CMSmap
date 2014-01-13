#!/usr/bin/python

import smtplib, base64, os, sys, getopt, urllib2, urllib, re, socket, time, itertools, urlparse, threading, Queue, multiprocessing, cookielib

  
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
        try:
            htmltext = urllib2.urlopen(self.url).read()
            GenericChecks(self.url).HTTPSCheck()
            
            m = re.search("Wordpress", htmltext,re.IGNORECASE)
            if m: print "[*] CMS Detection: Wordpress"; wordpress = WPScan(self.url)
                
            m = re.search("Joomla", htmltext,re.IGNORECASE)
            if m: print "[*] CMS Detection: Joomla"; joomla = JooScan(self.url)
                
            m = re.search("Drupal", htmltext,re.IGNORECASE);
            if m: print "[*] CMS Detection: Drupal"; drupal = DruScan(self.url)
        except urllib2.URLError, e:
            print "[!] Website Unreachable: "+self.url
            sys.exit()          

class WPScan:
    # Scan WordPress site
    def __init__(self,url):
        self.url = url
        self.queue_num = 5
        self.thread_num = 5
        self.pluginPath = "/wp-content/plugins/"
        self.feed = "/?feed=rss2"
        self.forgottenPsw = "/wp-login.php?action=lostpassword"
        self.weakpsw = ['password', 'admin','123456','abc123','qwerty']
        self.usernames = []
        self.plugins = [line.strip() for line in open('wp_plugins.txt')]
        
        sys.exit()
        self.WPVersion()
        self.WPTheme()
        self.WPConfigFiles()
        self.WPHello()
        self.WPFeed()
        BruteForcer(self.url,self.usernames,self.weakpsw).WPrun()
        self.WPForgottenPassword()
        self.WPplugins()
        ExploitDBSearch(self.url, 'Wordpress', pluginsFound)
        self.WPDirsListing()
        GenericChecks(self.url).AutocompleteOff('/wp-login.php')
        self.WPDefaultFiles()
               
    def WPVersion(self):
        try:
            htmltext = urllib2.urlopen(self.url+'/readme.html').read()
            regex = '<br /> Version[e]* (\d+\.\d+)'
            pattern =  re.compile(regex)
            version = re.findall(pattern,htmltext)
            print "[*] Wordpress Version: "+str(version[0])
        except urllib2.HTTPError, e:
            print e.code
            pass

    def WPTheme(self):
        try:
            htmltext = urllib2.urlopen(self.url).read()
            regex = '/wp-content/themes/(.+?)/'
            pattern =  re.compile(regex)
            version = re.findall(pattern,htmltext)
            print "[*] Wordpress Theme: "+str(version[0])
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
    
    def WPFeed(self):
        usernames = []
        try:
            htmltext = urllib2.urlopen(self.url+self.feed).read()
            print "[*] Enumerating Wordpress Usernames via \"Feed\" ..."
            regex = '<dc:creator><!\[CDATA\[(.+?)\]\]></dc:creator>'
            pattern =  re.compile(regex)
            usernames = re.findall(pattern,htmltext)
            usernames = sorted(set(usernames))
            self.usernames = usernames
            for user in usernames:
                print user
        except urllib2.HTTPError, e:
            #print e.code
            pass
        
    def WPForgottenPassword(self):
        # Username Enumeration via Forgotten Password
        query_args = {"user_login": "N0t3xist!1234"}
        data = urllib.urlencode(query_args)
        # HTTP POST Request
        req = urllib2.Request(self.url+self.forgottenPsw, data)
        try:
            htmltext = urllib2.urlopen(req).read()
            if re.findall(re.compile('Invalid username'),htmltext):
                print "[*] Forgotten Password Allows Username Enumeration: "+self.url+self.forgottenPsw          
        except urllib2.HTTPError, e:
            #print e.code
            pass

    def WPHello(self):
        try:
            htmltext = urllib2.urlopen(self.url+"/wp-content/plugins/hello.php").read()
            fullPath = re.findall(re.compile('Fatal error.*<b>(.+?)hello.php'),htmltext)
            if fullPath[0] :
                print "[*] Wordpress Hello Plugin Full Path Disclosure: "+self.url+"/wp-content/plugins/hello.php -> "+fullPath[0]+"hello.php"
        except urllib2.HTTPError, e:
            #print e.code
            pass

    def WPDirsListing(self):
        GenericChecks(self.url).DirectoryListing('/wp-content/')
        GenericChecks(self.url).DirectoryListing('/wp-includes/')
        GenericChecks(self.url).DirectoryListing('/wp-admin/')
        
        for plugin in pluginsFound:
            GenericChecks(self.url).DirectoryListing('/wp-content/plugins/'+plugin)

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
        self.forgottenPsw = "/?q=user/password"
        self.weakpsw = ['password', 'admin','123456','abc123','qwerty']
        self.plugins = [line.strip() for line in open('drupal_plugins.txt')]
        
        DruScan.DruVersion(self)
        self.DruConfigFiles()
        self.DruViews()
        self.DruBlog()
        BruteForcer(self.url,self.usernames,self.weakpsw).Drurun()
        self.DruForgottenPassword()
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

    def DruViews(self):
        self.views = "/?q=admin/views/ajax/autocomplete/user/"
        self.alphanum = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        usernames = []
        try:
            urllib2.urlopen(self.url+self.views)
            print "[*] Enumerating Drupal Usernames via \"Views\" Module..."
            for letter in self.alphanum:
                htmltext = urllib2.urlopen(self.url+self.views+letter).read()
                regex = '"(.+?)"'
                pattern =  re.compile(regex)
                usernames = usernames + re.findall(pattern,htmltext)
            usernames = sorted(set(usernames))
            for user in usernames:
                print user
        except urllib2.HTTPError, e:
            #print e.code
            pass
        
    def DruBlog(self):
        self.blog = "/?q=blog/"
        usernames = []
        try:
            urllib2.urlopen(self.url+self.blog)
            print "[*] Enumerating Drupal Usernames via \"Blog\" Module..."
            for blognum in range (1,50):
                try:
                    htmltext = urllib2.urlopen(self.url+self.blog+str(blognum)).read()
                    regex = "<title>(.+?)\'s"
                    pattern =  re.compile(regex)
                    user = re.findall(pattern,htmltext)
                    usernames = usernames + user
                    print user[0]
                except urllib2.HTTPError, e:
                    pass
            self.usernames = usernames
        except urllib2.HTTPError, e:
            #print e.code
            pass
        
    def DruForgottenPassword(self):
        # Username Enumeration via Forgotten Password
        query_args = {"name": "N0t3xist!1234" ,"form_id":"user_pass"}
        data = urllib.urlencode(query_args)
        # HTTP POST Request
        req = urllib2.Request(self.url+self.forgottenPsw, data)
        #print "[*] Trying Credentials: "+user+" "+pwd
        try:
            htmltext = urllib2.urlopen(req).read()
            if re.findall(re.compile('Sorry,.*N0t3xist!1234.*is not recognized'),htmltext):
                print "[*] Forgotten Password Allows Username Enumeration: "+self.url+self.forgottenPsw          
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
        print "[*] Searching vulnerable plugins from ExploitDB website ..."
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
            req = urllib2.Request(self.url+self.cmstype+plugin,None,self.headers)
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
        
   
class BruteForcer:
        def __init__(self,url,usrlist,pswlist):
            self.url = url
            self.usrlist = usrlist
            self.pswlist = pswlist
            #self.usrlist = ['test','test2','dfasf','eruru','dsfs','dfasfd']
            #self.pswlist = ['dfafs','dfasfdas','dfadf','dfasfsd','fddeed','dafsfas','test']
            
            #self.FindCMSType()
            
        def FindCMSType(self):
            htmltext = urllib2.urlopen(self.url).read()
            m = re.search("Wordpress", htmltext)
            if m: print "[*] CMS Detection: Wordpress"; print "[*] Wordpress Brute Forcing Attack Started"; self.WPrun()
            m = re.search("Joomla", htmltext)
            if m: print "[*] CMS Detection: Joomla"; print "[*] Joomla Brute Forcing Attack Started"; self.Joorun()
            m = re.search("Drupal", htmltext);
            if m: print "[*] CMS Detection: Drupal"; print "[*] Drupal Brute Forcing Attack Started"; self.Drurun()          
            
        def WPrun(self):
            self.wplogin = "/wp-login.php"
            for user in self.usrlist:
                userFound = False
                userInvalid = False
                cookieJar = cookielib.CookieJar()
                cookieHandler = urllib2.HTTPCookieProcessor(cookieJar)
                opener = urllib2.build_opener(cookieHandler)
                cookieJar.clear()
                for pwd in self.pswlist:
                    query_args = {"log": user ,"pwd": pwd, "wp-submit":"Log+In"}
                    data = urllib.urlencode(query_args)
                    #print "[*] Trying Credentials: "+user+" "+pwd
                    try:
                        # HTTP POST Request
                        htmltext = opener.open(self.url+self.wplogin, data).read()
                        if re.search('<strong>ERROR</strong>: Invalid username',htmltext):
                            userInvalid = True
                        elif re.search('username <strong>(.+?)</strong> is incorrect.',htmltext):
                            userFound = True
                        elif re.search('ERROR.*block.*',htmltext,re.IGNORECASE):
                            print "[*] Account Lockout Enabled: Your IP address has been temporary blocked. Try it later or from a different IP address"
                            return
                        elif re.search('dashboard',htmltext,re.IGNORECASE):
                            print "[*] Valid Credentials: "+user+" "+pwd                           
                    except urllib2.HTTPError, e:
                        #print e.code
                        pass
                
                if verbose:
                    if userInvalid: print "[*] Invalid Username: "+user
                
                #if userInvalid else None if verbose
                
                
                #print "[*] Invalid Username: "+user if verbose: if userInvalid else None
                if userFound: print "[*] Username found: "+user

           
        def Joorun(self):
            # It manages token and Cookies
            self.joologin = "/administrator/index.php";
            for user in self.usrlist:
                cookieJar = cookielib.CookieJar()
                cookieHandler = urllib2.HTTPCookieProcessor(cookieJar)
                opener = urllib2.build_opener(cookieHandler)
                cookieJar.clear()
                
                # Get Token and Session Cookie
                htmltext = opener.open(self.url+self.joologin).read()
                reg = re.compile('<input type="hidden" name="([a-zA-z0-9]{32})" value="1"')
                token = reg.search(htmltext).group(1)
                
                for pwd in self.pswlist:
                    # Send Post With Token and Session Cookie
                    query_args = {"username": user ,"passwd": pwd, "option":"com_login","task":"login",token:"1"}
                    data = urllib.urlencode(query_args)
                    #print "[*] Trying Credentials: "+user+" "+pwd
                    try:
                        htmltext = opener.open(self.url+self.joologin, data).read()
                        if re.findall(re.compile('Joomla - Administration - Control Panel'),htmltext):
                            print "[*] Valid Credentials: "+user+" "+pwd
                    except urllib2.HTTPError, e:
                        #print e.code
                        pass

        def Drurun(self):
            self.drulogin = "/?q=user/login";
            for user in self.usrlist:
                for pwd in self.pswlist:
                    query_args = {"name": user ,"pass": pwd, "form_id":"user_login"}
                    data = urllib.urlencode(query_args)
                    # HTTP POST Request
                    req = urllib2.Request(self.url+self.drulogin, data)
                    #print "[*] Trying Credentials: "+user+" "+pwd
                    try:
                        htmltext = urllib2.urlopen(req).read()
                        if re.findall(re.compile('Sorry, too many failed login attempts from your IP address.'),htmltext):
                            print "[*] Account Lockout Enabled: Your IP address has been temporary blocked. Try it later or from a different IP address"
                            return
                              
                    except urllib2.HTTPError, e:
                        #print e.code
                        if e.code == 403:
                            print "[*] Valid Credentials: "+user+" "+pwd
                
class PostExploit:
    def __init__(self,url):
        self.url = url
        self.WPTheme = "twentythirteen"
        
    def WPShell(self):
        print "[*] Uploading a shell on the target website ..."
        
        try:
            htmltext = urllib.urlopen(self.url+"/wp-content/themes/"+self.WPTheme+"/404.php?c=id").read()
            print "[*] Web shell Found: " + self.url+"/wp-content/themes/"+self.WPTheme+"/404.php?c=id"
            print "[*] $ id"
            print htmltext
            
        except urllib2.HTTPError, e:
            #print e.code
            pass
    
class JobQue:
        pass
    
class GenericChecks:
    def __init__(self,url):
            self.url = url
        # autocompletation
        # clear text : http or https
        # directory listing 
        
    def DirectoryListing(self,relPath):
        self.relPath = relPath
        htmltext = urllib2.urlopen(self.url+self.relPath).read()
        dirList = re.search("<title>Index of", htmltext,re.IGNORECASE)
        if dirList: print "[*] Directory Listing Enabled: "+self.url+self.relPath
        
    def HTTPSCheck(self):
        pUrl = urlparse.urlparse(self.url)
        #clean up supplied URLs
        scheme = pUrl.scheme.lower()
        if scheme == 'http' : print "[*] Website Not in HTTPS: "+self.url

    def AutocompleteOff(self,relPath):
        self.relPath = relPath
        htmltext = urllib2.urlopen(self.url+self.relPath).read()
        autoComp = re.search("autocomplete=\"off\"", htmltext,re.IGNORECASE)
        if not autoComp : print "[*] Autocomplete Off Not Found: "+self.url+self.relPath

# Global Variables 

pluginsFound = []
version=0.1
verbose = False

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
    Scanner(url).FindCMSType()
    #BruteForcer(url).FindCMSType()
    #BruteForcer(url,'/administrator/index.php',['admin1','admin2','admin3fd'],['dfafs','dfasfdas','dfadf','dfasfsd','fddeed','adfasss','test']).Joorun()
    #BruteForcer(url,'/?q=user/login',['admin1','admin2','admdfasin','admin3fd'],['dfafs','dfasfdas','dfadf','adfasa']).Drurun()
    #TestCommit
    
    #PostExploit(url).WPShell()
    end = time.time()
    print "End: ", end
    print end - start, "seconds"

        
        
                

