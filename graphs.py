import MySQLdb as mdb
import datetime
import matplotlib.pyplot as plt
from pylab import *
import datetime, time
import json
from nvd3 import lineChart
'''
1. Number of Words vs Range (All Words)
2. Number of Words vs Range (Alive)
3. Number of Words vs Range (Dead)
4. Number of Users vs Score Range 
5. Ratio of alive/dead words vs Time
6. No of distinct users vs Time
7. Score vs Time for many users in the same graph
8. Ratio of alive/dead words vs Time for many users in the same graph
'''

def convert(date):
    dt = datetime.datetime.strptime(date,'%H:%M, %d %B %Y')
    return dt

def graph2():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("""SELECT SCORE,DEATH FROM SARGAM WHERE DEATH IS NULL""")
    results = cursor.fetchall()
    score = []
    scorerange = []
    startscore = 0
    
    for i in results:
        score.append(i[0])

    maxscore = max(score)
   
    while 1:
        scorerange.append(startscore)
        startscore = startscore+100
        if startscore>maxscore:
            break
        
    wordcount = [0]*len(scorerange)
    for i in score:
        index = int(i/100)
        wordcount[index] = wordcount[index]+1

    #print scorerange,wordcount    
    bar(scorerange,wordcount,100)
    title('ALIVE WORDS')
    show()
    db.close()


def graph3():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("""SELECT SCORE,DEATH FROM SARGAM WHERE DEATH IS NOT NULL""")
    results = cursor.fetchall()
    score = []
    scorerange = []
    startscore = 0
    
    for i in results:
        score.append(i[0])

    maxscore = max(score)
    
    while 1:
        scorerange.append(startscore)
        startscore = startscore+100
        if startscore>maxscore:
            break
        
    wordcount = [0]*len(scorerange)
    for i in score:
        index = int(i/100)
        wordcount[index] = wordcount[index]+1

    #print scorerange,wordcount
    #print maxscore
    bar(scorerange,wordcount,100)
    title('DEAD WORDS')
    show()
    db.close()



def graph4():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("SELECT BIRTH_UN,SUM(SCORE) as TOTAL from SARGAM group by BIRTH_UN ORDER BY TOTAL DESC")
    results = cursor.fetchall()
    maxscore = results[0][1]
    scorerange=[]
    leastscore=0
    
    nob = int(maxscore/200000);
    
    for i in range(nob+1):
        scorerange.append(leastscore)
        leastscore = leastscore + 200000
        
    countuser=[0]*(nob+1)
    
    for i in results:
        print i[1]
        index = int(i[1]/200000)
        countuser[index]=countuser[index]+1
        
    #print leastscore,maxscore
    #print scorerange,countuser
    bar(scorerange,countuser,200000)
    title('NUMBER OF USERS VS SCORE RANGE')
    show()
    db.close()


def graph5():    
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("SELECT BIRTH,DEATH FROM SARGAM")
    results = cursor.fetchall()

    startdate = results[0][0]
    startdate = convert(startdate)
    articledeath = datetime.datetime.now()
    daterange = (articledeath-startdate)/10

    dates = []
    for i in range(11):
        dates.append(startdate)
        startdate = startdate + daterange
    print dates,len(dates)

    alive = 0
    dead = 0
    dd=[]
    fract = [0.0]*(len(dates)-1)
    
    for i in results:
        if(i[1]==None):
            dd.append("NULL")
        else:
            dd.append(convert(i[0]))
        
    count = 0
    z = 1
    
    for i in results:
        if(i[1]==None):
            alive = alive+1
        else:
            dead = dead+1
        if(dd[count]!="NULL") :
            if(dd[count]<dates[z]):
                fract[z-1] = float(float(alive)/(float(dead)+float(alive)))
            else:
                z=z+1
        count=count+1
        
    fract.reverse()
    fract.append(0.0)
    fract.reverse()
    
    plot(dates,fract)
    title('ALIVE/TOTAL WORDS VS TIME')
    show()   
    db.close()
    
def graph6():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("select DISTINCT BIRTH_UN,BIRTH FROM SARGAM")
    results = cursor.fetchall()
    uniquename = []
    uniquedate = []
    convertdate = []
    
    for i in results:
        if i[0] not in uniquename:
            uniquename.append(i[0])
            uniquedate.append(i[1])
            
    for i in uniquedate:
        convertdate.append(convert(i))
       
    startdate = convertdate[0]
    enddate = datetime.datetime.now()
    #print enddate,startdate
    daterange = (enddate - startdate)/10
    #print daterange
    dates = []
    for i in range(11):
        dates.append(startdate)
        startdate = startdate + daterange
    usercount = [0]*11
    usercount[0]=0
    cumusercount = [0]*11
    for date in convertdate:
        if date<dates[1]:
            usercount[1] = usercount[1]+1
        elif date<dates[2]:
            usercount[2] = usercount[2]+1
        elif date<dates[3]:
            usercount[3] = usercount[3]+1
        elif date<dates[4]:
            usercount[4] = usercount[4]+1
        elif date<dates[5]:
            usercount[5] = usercount[5]+1
        elif date<dates[6]:
            usercount[6] = usercount[6]+1
        elif date<dates[7]:
            usercount[7] = usercount[7]+1
        elif date<dates[8]:
            usercount[8] = usercount[8]+1
        elif date<dates[9]:
            usercount[9] = usercount[9]+1
        else:
            usercount[10] = usercount[10]+1

    
    cumusercount[0] = usercount[0]
    for i in range(1,len(usercount)):
        print i
        cumusercount[i] = usercount[i]+cumusercount[i-1]
        
    #print cumusercount
    print dates,cumusercount
        
    plot(dates,cumusercount)
    title('CUMULATIVE NUMBER OF USERS VS TIME')
    show()
    db.close()

def graph7():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("SELECT BIRTH_UN, SUM(score) as TOTAL from SARGAM group by BIRTH_UN ORDER BY TOTAL DESC LIMIT 5")
    results = cursor.fetchall()
    usernames = []
    for i in results:
        usernames.append(i[0])

    x_array = []
    y_array = []
    
    for nms in usernames:
        score = []
        d_str = []
        deathdate = []
        clubbed = []
        cursor.execute("""SELECT DEATH,SCORE from SARGAM where BIRTH_UN=%s""",(nms))
        results = cursor.fetchall()

        for i in results:
            if(i[0]!=None):
                ddate = convert(i[0])
            else:
                ddate = datetime.datetime.now()
            clubbed.append([ddate,i[1]])
        clubbed.sort()
        
        for i in clubbed:
            deathdate.append(i[0])
            t1 = i[0].timetuple()
            d_str.append(time.mktime(t1))
            score.append(i[1])
            
        cumscore = [0]*len(deathdate)
        cumscore[0] = score[0]
        
        for i in range(1,len(score)):
            cumscore[i] = score[i]+cumscore[i-1]
            
        print cumscore[i]       
        
        x_array.append(deathdate)
        y_array.append(cumscore)
    '''
    chart = lineChart(name='lineChart', height=500, width=1000, date=True)
    extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " calls"}}
    chart.add_serie(name="user 1", y=y_array[0], x=x_array[0] , extra=extra_serie)
    extra_serie = {"tooltip": {"y_start": "", "y_end": " mins"}}
    chart.add_serie(name="user 2", y=y_array[1], x=x_array[1], extra=extra_serie)
    chart.add_serie(name="user 3", y=y_array[2], x=x_array[2] , extra=extra_serie)
    chart.add_serie(name="user 4", y=y_array[3], x=x_array[3], extra=extra_serie)
    chart.add_serie(name="user 5", y=y_array[4], x=x_array[4], extra=extra_serie)
    chart.buildhtml()
    output_file = open('users.html', 'w')
    output_file.write(chart.htmlcontent)

    #close Html file
    output_file.close()
    '''
    plot(x_array[0],y_array[0], x_array[1],y_array[1],x_array[2],y_array[2],x_array[3],y_array[3],x_array[4],y_array[4])
    show()
    db.close()
    
        
    
    
'''    
graph2()
graph3()
graph4()
graph5()
graph6()
graph7()
'''

    
