#encoding: utf-8

import web_utils, page_parser

config_path = r'.\config'
db_path = r'.\db'

def main():
    import os.path,time
    ###read config files and load up target series
    tgt_series = load_config() #tested okay on 2015/4/13
    ###complete


    #dispatch major functions
    while True:
    #TODO 150410: re-write this part using multi-threading
        sleep = False
        for i in tgt_series:
            ###inits data for detect_new()
            tgt = web_utils.meiju(i.lower()) #an object
            db = db_init(i.lower(),db_path) #in the format of "xx-xx" (string) -> season-episode
            ###all data initiated

            n=detect_new(tgt,db)

            if n: #means has new episodes, a list of [season, episode, link]
                for j in n:
                    new_episode = web_utils.tgt_episode(j[2])
                    if new_episode.update_check():
                        invoke_notify(i) #notify on locating new episode with exact links updated
                        update_log(j,os.path.join(db_path,i+'.txt'))
                    else:
                        sleep = True #means new upisode have not been updated with links, and _
                        #should sleep for another round of check
        if sleep: #means at least 1 episode needs sleep and recheck
            time.sleep(3600)
            continue
        else:
            break

def load_config():
    #load config files for each day
    import os.path
    weekday = get_weekday()
    config_file = open(os.path.join(config_path,weekday+'.txt'))
    tgt_series = [] #loads all target series
    for line in config_file:
        tgt_series.append(line.replace('\n',''))
    return tgt_series

def db_init(series_name, path = db_path):
    #initiates database for each series
    import os.path
    db=[]
    #db_file = open(os.path.join(path, series_name+'.txt'),'r+')
    db_file_path = os.path.join(path, series_name+'.txt')
    if os.path.lexists(db_file_path):
        db_file = open(db_file_path,'r')
        for line in db_file: #NOTE: line read from a file ends with \n in default
            try:    
                tmp = line.replace('\n','').split(';;;')
                db.append("{0}-{1}".format(tmp[0],tmp[1]))
            except: #if the file is empty, codes goes here and db=[]
                continue
        db_file.close()
    else:
        f=open(db_file_path,'a')
        f.close()
        db = []

    return db


def detect_new(objTgt, lstDB):
    #determines if there is a new episode on given day
    import page_parser
    results = page_parser.page_parser(objTgt) #parsed result from page
    new = 0
    new_episode=[] 
    for i in results: #each result is in the form of {'season-episode':link}
        if i in lstDB: #means already have information of this episode
            continue
        else: #got a new episode
            new = 1
            temp = i.split('-')
            new_episode.append([temp[0],temp[1],results[i]]) #[season, episode, link]
    if new:
        return new_episode
    else:
        return 0

def invoke_notify(name):
    import win32com.client, datetime

    now = datetime.datetime.now()
    tgt_time = datetime.datetime.isoformat(now).split('T')[1].split('.')[0] #gets time at hh:mm:ss.xxx

    wsh=win32com.client.DispatchEx('WScript.Shell')
    wsh.popup('new {0} episode found at {1}'.format(name.upper(),tgt_time))

def update_log(log, db_file):
    #update the log
    f = open(db_file,'a')
    #formats the log from [season,episode,link]
    content = ';;;'.join(log)
    f.write(content+'\n')
    f.close()
    


def get_weekday():
    import datetime
    tmp_today = datetime.date.today()
    today = datetime.date.isoweekday(tmp_today)
    if today==1:
        return 'monday'
    elif today==2:
        return 'tuesday'
    elif today==3:
        return 'wednesday'
    elif today==4:
        return 'thursday'
    elif today==5:
        return 'friday'
    elif today==6:
        return 'saturday'
    elif today==7:
        return 'sunday'
    else:
        raise ValueError, 'Weekday Error, result={0}'.format(today)

#def output(parse_result, output_file):
#    #output results from page_parser to local file
#    #import os.path,os
#    n=parse_result
#    f=open(output_file,'a')
#    f.write("season:{0},episode:{1},link:{2}\n".format(n[0],n[1],n[2]))
#    f.close()


if __name__=="__main__":
    main()