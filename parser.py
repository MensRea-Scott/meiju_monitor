#encoding: utf-8

def page_parser(objPage):
    #parse page and get key information
    from bs4 import BeautifulSoup
    import re

    soup = BeautifulSoup(objPage.page)
    tgt_sections = soup.find_all('tr') #find out all <tr>...</tr> sections

    pattern = objPage.re_pattern
    #print pattern,len(tgt_sections)
    #raw_input('abcd')
    result = {}

    for i in tgt_sections:
        if i.has_attr('class') and i['class'] == ['Scontent']: #['Scontent'] is a list _
            # _ due to ttmeiju.com's special page structure
            tmp = i.get_text().lower()
 
            n = re.search(pattern,tmp) #filter-> person of interest sxxexx 720p
            if n is not None:
                season, episode = n.group(1), n.group(2)
                #print season
                #raw_input('continue')
            else:
                continue #if it's not target, there is no need to continue the loop
            #result.append((season,episode))
            tmp_links = i.find_all('a') #finds out all <a> tags
            #notice if codes run to here, there is already a "720P" in the text
            for i1 in tmp_links:
                t1=re.search(r'http://www.ttmeiju.com/seed/.+\.html',i1['href'])
                if t1 is not None:
                    link=t1.group()
                    #print link, '*'*10
                    #result.append([season,episode,link])
                    result["{0}-{1}".format(season,episode)] = link
        #    continue
    return result

