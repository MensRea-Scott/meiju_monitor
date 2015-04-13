#encoding: utf-8

class meiju(object): #tested on on 2015/4/13
    def __init__(self, series_name):
        self.name = series_name.lower()
        #self.db_path = db_path.lower()
        #self.config_path = config_path.lower()
        #self.update_date = update_date
        self.page = self.get_page()
        self.re_pattern = self.get_pattern()


    def url_operator(self, name):
        #transform series_name into total url address
        from urlparse import urljoin
        tmp_name = name.replace(' ','.') + '.html'
        #return urljoin('http://www.ttmeiju.com/meiju',tmp_name)
        return 'http://www.ttmeiju.com/meiju/'+tmp_name

    def get_page(self):
        #opens webpage, raise exception if page cannot be opened
        import urllib2
        addr = self.url_operator(self.name) #gets series home page
        #print addr
        #raw_input('press to continue')
        try:
            page = urllib2.urlopen(addr).read()
            #page = unicode(page,'gb2312')
        except:
            raise ValueError, 'invalid address'

        return page

    def get_pattern(self):
        #generate RE pattern for the series
        keyword = self.name.lower()
        if '.' in keyword: #like agent of s.h.i.e.l.d
            keyword = keyword.replace('.','\.') #transform to RE pattern, same below
        if ' ' in keyword: #like person of interest
            keyword = keyword.replace(' ','.+')
        
        pattern = r'{0}.*s([0-9]+)e([0-9]+).*720p'.format(keyword)
        return pattern


    pass

class tgt_episode(object): #tested okay on 2015/4/13
    #this is the target episode to be watched.
    def __init__(self, link):
        #self.name = name
        #self.season = season
        #self.episode = episode
        self.addr = link
        #self.update_date = date

    def update_check(self):
        #check whether the episode is updated today
        #NOTE: this method is based on ttmeiju.com's practice that _
        #when an episode hasn't been updated, the page notes it as _
        #大小： M; and as 大小：xxx M after actually updated. But this _
        #may not be a universal solution, and solely bases on current _
        #practice
        import re,datetime

        now = datetime.datetime.now()
        tgt_time = datetime.datetime.isoformat(now).split('T')[1] #gets time at hh:mm:ss.xxx
        print 'Attempt check at {0}'.format(tgt_time)

        page = self.get_page().decode('gb2312')
       
        pattern = r'大小：[\s\S]+>(.+M|.+G)</td>'.decode('utf-8') #!!!THIS IS IMPORTANT FOR PYTHON RE!!!
        #NOTE 150413: some episodes may be noted as x.xxG
        try:
            tmp = re.search(pattern,page).group(1) #finds out whether its _
            #xxx M/G, which means actually updated, or M/G, which means not updated
            if re.search(r'[0-9\.]+',tmp) is None:
                return 0 #means not updated
            else:
                return 1 #means updated
        except:
            raise ValueError, 'RE method failed.'


    def get_page(self):
        #opens webpage, raise exception if page cannot be opened
        import urllib2
        
        try:
            page = urllib2.urlopen(self.addr).read()
            #page = unicode(page,'gb2312')
        except:
            raise ValueError, 'invalid address'

        return page
