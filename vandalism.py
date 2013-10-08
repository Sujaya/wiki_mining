from bs4 import BeautifulSoup
import urllib2
import pdb

def Linkstopage(url):
    
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	infile = opener.open(url) 
	#We are using Beautifl soup to parse the obtained html page and access the required fields in the html page
	page = infile.read()
	soup = BeautifulSoup(page)
	
	return soup


def Vandetect(search):
	url = 'http://en.wikipedia.org/w/index.php?title='+ search + '&offset=&limit=500&action=history'
	count=0
	soup = Linkstopage(url) 	
	
		
	current = []
	while True:#(new_url != '') or (count==0):

		
		para = soup.body.find(id="pagehistory")
		k = para.findAll("li")
		for i in range(len(k)):
			count = count + 1
			curr_edit = k[i].findAll('span','mw-plusminus-neg')

			if curr_edit:
					bdstr=str(curr_edit[0].get_text())		
					bdstr=bdstr[1:-1]	

			if not curr_edit:
				curr_edit = k[i].findAll('span','mw-plusminus-pos')
				if curr_edit:
					bdstr=str(curr_edit[0].get_text())		
					bdstr=bdstr[1:-1]					

			if not curr_edit:
				curr_edit = k[i].findAll('span','mw-plusminus-null')
				if curr_edit:
					bdstr=str(curr_edit[0].get_text())		
					bdstr=bdstr[1:-1]

			if not curr_edit:
				curr_edit = k[i].findAll('strong','mw-plusminus-neg')
				if curr_edit:
					bdstr=str(curr_edit[0].get_text())		
					bdstr=bdstr[1:-1]
				if not curr_edit:
					curr_edit = k[i].findAll('strong','mw-plusminus-pos')
				if curr_edit:
					bdstr=str(curr_edit[0].get_text())		
					bdstr=bdstr[1:-1]	

			tmp = ''
			q = bdstr.split(',')
			for x in q:
				tmp = tmp+x
			current.append(int(tmp))

		newer = soup.body.find('a','mw-nextlink')
		# We obtain the URL to next 500 entries from the current page and save it in new_url
		if newer == None:
			new_url = ''
			break
		else:
			new_url = 'http://en.wikipedia.org' +newer.get('href')


		#pdb.set_trace()
		soup = Linkstopage(new_url)
		

	current.reverse()
	print current

	return current


def Deletelist(search, lt):

	#lt = Vandetect(search)

	listlength=len(lt)
	tobedel=[]

	for i in range(listlength-2):
	    if(lt[i]+lt[i+1]+lt[i+2]==0):
	        tobedel.append(i)
	        tobedel.append(i+1)
	        tobedel.append(i+2)

	    if(lt[i] + lt[i+2] == 0):
	        tobedel.append(i)
	        tobedel.append(i+2)

	

	for i in range(listlength-1):
	    if(lt[i]+lt[i+1]==0):
	        tobedel.append(i)
	        tobedel.append(i+1)
	    elif(lt[i] == 61558):
	    	tobedel.append(i)
	    	tobedel.append(i-1)
	    	tobedel.append(i-2)
	    	tobedel.append(i-3)
	    	tobedel.append(i-4)
	    	tobedel.append(i-5)
	    	tobedel.append(i-6)
	    	tobedel.append(i-7)
	tobedel=list(set(tobedel))

	print tobedel
	return tobedel


#Deletelist('alpha')
