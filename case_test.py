#encolding: utf-8

import web_utils
db_path = r'./db'

def load_config(weekday):
    #load configuration files
    import os, os.path

    config_path = r'./config'

    f = open(os.path.join(config_path,weekday+'.txt'))
    result = []
    for line in f:
        result.append(line.replace('\n',''))
    return result



def TEST_web_utils():
    #test case for web_utils modules
    import web_utils, urllib2, main
    import os
    series_names = load_config('monday')

    for i in series_names:
        case1 = web_utils.meiju(i.lower())
        print "Now start web_utils test for Subject: {0}".format(i)

        #test meiju class
        test_url_operator(case1, i.lower()) #test whether generates right URL
        test_get_page(case1) #test whether get the same page
        test_get_pattern(case1) #test whether generates the right RE pattern

        #test tgt_episode class
        tgt_links = get_links(case1)
        for i in tgt_links:
            sub_case_1 = web_utils.tgt_episode(i)
            if sub_case_1.update_check():
                print 'For link {0}: FOUND update'.format(i)
            else:
                print 'For link {0}: NOT FOUND update'.format(i)
            #os.system('powershell chrome {0}'.format(i))




def test_get_page(subject):
    #test whether gets the right page
    import urllib2

    tmp = subject.get_page()
    if len(tmp) < 10000:
        print 'GET_PAGE TEST: ERROR, length of page not match'
    else:
        print 'GET_PAGE TEST: SUCCESSFUL'

def test_url_operator(subject, name):
    import web_utils, urllib2, os
    
    #test for url generating
    url = subject.url_operator(name.lower())
    print "URL TEST: the URL generated is {0}".format(url)
    try:
        test_web = urllib2.urlopen(url)
        print "URL TEST: SUCCESSFUL"
        #os.system('powershell chrome {0}'.format(url))
        #result = 1
    except:
        print "URL TEST: connectivity error!"
        #result = 0

    #return result

def test_get_pattern(subject):
    print "GET_PATTERN TEST: generated RE pattern is {0}\n".format(subject.get_pattern())

def get_links(subject):
    #get episode links using page_parser module
    import page_parser
    links=[]

    res = page_parser.page_parser(subject)
    print "Test for following links:\n"
    for i in res:
        print '\t'+res[i]
        links.append(res[i])
    
    return links



def TEST_parser():
    #test case for parser module
    import page_parser, web_utils
    series_names = load_config('monday')
    #links=[]

    for i in series_names:
        case1 = web_utils.meiju(i.lower())
        print 'Now start page_parser test for subject: {0}'.format(i)

        res = page_parser.page_parser(case1)
        for i in res:
            print "{0}: {1}".format(i,res[i])
            #links.append(res[i])

        print '\n'*2
    #return links






