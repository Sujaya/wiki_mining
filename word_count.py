from bs4 import BeautifulSoup
import urllib2
from datetime import datetime
import stop1
import os
import adddel
import crdb
import hashed
import codecs
import vandalism
import pdb
import graphs

def Linkstopage(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    infile = opener.open(url) 
    #We are using Beautifl soup to parse the obtained html page and access the required fields in the html page
    page = infile.read()
    soup = BeautifulSoup(page)
    print url
    return soup

def Lists(url):
	soup = Linkstopage(url)

	newer = soup.body.find('a','mw-nextlink')
	if newer == None:
		new_url = ''
	else:
		new_url = newer.get('href')

	para = soup.body.find(id="pagehistory")
	k = para.findAll("li")
	date = []
	names = []
	bytes = []
	url_list = []
	curr_edit=[]
	#this loop is to traverse the list items and obtain name, date and size of each edit
	try:
		for i in range(len(k)):
			tmp = ''
			bdstr = ''
			#dt, nm, sz are temporary variables
			dt = k[i].findAll('a','mw-changeslist-date')
			nm = k[i].findAll('a','mw-userlink')
			sz = k[i].findAll('span','history-size')
			curr_edit_1 = k[i].findAll('span','mw-plusminus-neg')
			if curr_edit_1:
					bdstr=str(curr_edit_1[0].get_text())		
					bdstr=bdstr[1:-1]	

			if not curr_edit_1:
				curr_edit_1 = k[i].findAll('span','mw-plusminus-pos')
				if curr_edit_1:
					bdstr=str(curr_edit_1[0].get_text())		
					bdstr=bdstr[1:-1]					

			if not curr_edit_1:
				curr_edit_1 = k[i].findAll('span','mw-plusminus-null')
				if curr_edit_1:
					bdstr=str(curr_edit_1[0].get_text())		
					bdstr=bdstr[1:-1]

			if not curr_edit_1:
				curr_edit_1 = k[i].findAll('strong','mw-plusminus-neg')
				if curr_edit_1:
					bdstr=str(curr_edit_1[0].get_text())		
					bdstr=bdstr[1:-1]

			if not curr_edit_1:
				curr_edit_1 = k[i].findAll('strong','mw-plusminus-pos')
				if curr_edit_1:
					bdstr=str(curr_edit_1[0].get_text())		
					bdstr=bdstr[1:-1]
			tmp = ''
			q = bdstr.split(',')
			for x in q:
				tmp = tmp+x
			curr_edit.append(int(tmp))


			#convert unicode to string and then string to Date type
			dt1 = str(dt[0].get_text())
			#date_object = datetime.strptime(dt1, '%H:%M, %d %B %Y')
			date.append(dt1)

			tmp_url = 'http://en.wikipedia.org' + dt[0].get('href')
			url_list.append(tmp_url)

			names.append((nm[0].get_text()))

			#convert unicode to string and then string to float type
			bt = str(sz[0].get_text())
			if bt == '(empty)':
				bt = '0'
			else:
			    bt = bt[1:]
			    bt = bt.split(" ")
			    bt = bt[0].split(',')
			for i in bt:
				tmp = tmp+i
			bytes.append(int(tmp))
		
	except Exception, e:
		print e

	return date, names, bytes, curr_edit, url_list, new_url

 
def CreateFiles(url,fn):
    soup=Linkstopage(url)
    
    para = soup.body.find(id="content").find(id="bodyContent").find(id="mw-content-text")
    p = para.findAll('p')
    li = para.findAll('li')
    text = ''
    for i in p:
        text = text + i.get_text()
    for t in li:
        text = text +' ' + t.get_text() 
 
    text = stop1.Removestopwords(text)
    
    f=codecs.open(fn, "w", "utf-8")
    if f:
        print 'File Successfully Opened'
        if text!= ' ':
            try :
                f.writelines(text)   
            except Exception, e:
                text = unicode(text , errors='ignore')
                f.writelines(text)
    else:
        print 'Cannot Open file'
    f.close()

def Dataextract(search):
	date = []
	names = []
	bytes = []
	url_list = []
	curr_edit=[]
 	
 	url = 'http://en.wikipedia.org/w/index.php?title=' + search + '&limit=500&action=history'
 	dts, nms, byts, cur_ed, urls, new_url = Lists(url)
	date.extend(dts)
	names.extend(nms)
	bytes.extend(byts)
	curr_edit.extend(cur_ed)
	url_list.extend(urls)

	while new_url != '':	
		new_url = 'http://en.wikipedia.org/' + new_url
		dts, nms, byts, cur_ed ,urls,new_url = Lists(new_url)
		date.extend(dts)
		names.extend(nms)
		bytes.extend(byts)
		curr_edit.extend(cur_ed)
		url_list.extend(urls)
	
	names.reverse()
	date.reverse()
	bytes.reverse()
	curr_edit.reverse()
	url_list.reverse()

	d = '/home/sujaya/csa_internship/'+search
	if not os.path.exists(d):
	    os.makedirs(d)

	count =  0    
	for i in url_list:
		fn = d+'/'+search+str(count)+'.txt'
		print 'New Url : ', i ,fn
		CreateFiles(i,fn)
		count = count +1

	f1=codecs.open(d+'/un.txt',"w", "utf-8")
    
	if f1:
		for j in range(len(names)):
		    f1.writelines(names[j]+'\t')
		    f1.writelines(str(date[j])+'\n')
	f1.close()
	return count




def Textprocess(search, count):

	tobedel = vandalism.Vandetect(search)
	vand_list = vandalism.Deletelist(search, tobedel)
	count = hashed.Deletion(search,vand_list, count)
	cnt = hashed.Hashed(search,count+1)
	adddel.Adddel(search,cnt)
	crdb.Datastore(search)
	crdb.Score()
	

search = raw_input("Enter the Search Query :")
#pdb.set_trace()
count = Dataextract(search)

Textprocess(search, 8442)
graphs.graph2()
graphs.graph3()
graphs.graph5()
graphs.graph6()
graphs.graph7()
