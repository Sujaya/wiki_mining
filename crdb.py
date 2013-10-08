import MySQLdb as mdb
import datetime
import matplotlib.pyplot as plt
from pylab import *

def Datastore(search):
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS SARGAM")
    cursor.execute("CREATE TABLE SARGAM(WORD VARCHAR(200) NOT NULL, BIRTH_UN VARCHAR(60), DEATH_UN VARCHAR(60), BIRTH VARCHAR(60), DEATH VARCHAR(60), SCORE REAL(8,2))")
    
    f=open('/home/sujaya/csa_internship/'+search+'/Add_Delete.txt',"r")
    text=f.read().split('\n')
    count=0
    birth_un = []
    birth_time = []

    for lines in text:
        l1=lines.split('\t')
        if(l1[0]=="Added"):
            try:
                cursor.execute("""INSERT INTO SARGAM(WORD, BIRTH_UN, BIRTH) VALUES(%s, %s, %s)""",(l1[1], l1[2], l1[3]))
            except Exception, e:
                print e , l1[1]
        elif(l1[0]=="Deleted"):
            cursor.execute("""SELECT * FROM SARGAM WHERE WORD=%s""",(l1[1]))
            results = cursor.fetchall()
            if results:
                for row in results:
                    word=row[0]
                    birth_un.append(row[1])
                    birth_time.append(row[3])

                last_birth = birth_time[len(birth_time)-1]
                #death_un = birth_un[len(birth_un)-1]
                #print l1[2]  , word, last_birth , l1[3]
                if len(l1)>3:
                    cursor.execute("""UPDATE SARGAM SET DEATH_UN = %s WHERE WORD = %s AND BIRTH = %s""",(l1[2], word , last_birth))
                    cursor.execute("""UPDATE SARGAM SET DEATH = %s WHERE WORD = %s AND BIRTH = %s""",(l1[3], word , last_birth))
                #print "word = "+word+" username = "+user_name+" birth = "

                
    db.commit()
    db.close()


def Score():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute('SELECT * FROM SARGAM')
    results = cursor.fetchall()
    for row in results:
        #print row[3], row[4]
        birth = datetime.datetime.strptime(row[3],'%H:%M, %d %B %Y')
        if row[4] != None:
            death = datetime.datetime.strptime(row[4],'%H:%M, %d %B %Y') 
            score = (death - birth).days
            cursor.execute("""UPDATE SARGAM SET SCORE = %s WHERE DEATH = %s AND BIRTH = %s AND WORD = %s""",(score, row[4], row[3], row[0]))
            
        else:
            death = datetime.datetime.now()
            score = (death - birth).days
            cursor.execute("""UPDATE SARGAM SET SCORE = %s WHERE BIRTH = %s AND WORD = %s""",(score,row[3],row[0]))
            
    db.commit()
    db.close()


def Extractscore():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM SARGAM WHERE DEATH IS NULL""")
    results = cursor.fetchall()
    alive_score = []
    alive_words = []
    dead_score = []
    alive_count = []
    dead_count = []
    arr2 = []

    if results:
        for row in results:
            alive_score.append(row[5])
        print sum(alive_score)/len(results) , max(alive_score), len(results)

    cursor.execute("""SELECT * FROM SARGAM WHERE DEATH IS NOT NULL""")
    results = cursor.fetchall()
    if results:
        for row in results:
            dead_score.append(row[5])
        print sum(dead_score)/len(results) , max(dead_score)

    uniq_alive = list(set(alive_score))
    uniq_dead = list(set(dead_score))
    uniq_alive.sort()
    print uniq_alive
    print
    uniq_dead.sort()
    print uniq_dead
    print

    for i in uniq_alive:
        alive_count.append(alive_score.count(i))
    for i in uniq_dead:
        dead_count.append(dead_score.count(i))

    print alive_count
    print
    print dead_count
    print sum(alive_count) , sum(dead_count)

    i = alive_count.index(max(alive_count))
    print uniq_alive[i]

    arr =[0]*int(max(alive_score)/100+1)
    for i in alive_score:
        arr[int(i/100)] = arr[int(i/100)] + 1     
    print "------------" + str(arr)
    for i in range( 0 , int(max(alive_score)) , 100):
        arr2.append(i)
    print arr2, len(arr2), len(arr)
    bar( arr2, arr, 100)
    title('ALIVE')
    show()

    arr =[0]*int(max(dead_score)/100+1)
    for i in dead_score:
        arr[int(i/100)] = arr[int(i/100)] + 1    
    print "------------" + str(arr)
    arr2 = []
    for i in range( 0 , int(max(dead_score)) , 100):
        arr2.append(i)
    print arr2, len(arr2), len(arr)
    bar( arr2, arr, 100)
    title('DEAD')
    show()

def Userscore():
    db = mdb.connect("localhost","root","wrongpassword","WORDS" )
    cursor = db.cursor()
    user_name = raw_input("Enter username to find his score: ")
    cursor.execute("""SELECT * FROM SARGAM WHERE BIRTH_UN = %s""",(user_name))
    results = cursor.fetchall()
    u_score = 0
    if results:
        for row in results:
            u_score = u_score + row[5]
        print u_score


#Datastore('SARGAM')
#Score()
#Extractscore()
#Userscore()
