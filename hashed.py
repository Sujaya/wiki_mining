import hashlib
import os
import sys
import codecs



def Hashed(search, cnt):
    d = '/home/sujaya/csa_internship/'+search +'/'
    hashlist=[]
    
    tobedel=[]    

    for i in range(0,cnt):
        fn = d + search+str(i)+".txt"
        text=open(fn,"r").read()
        hashlist.append(hashlib.sha256(text))

    for i in range(0,cnt-7):
        for k in range(i+1,i+7):
            if(hashlist[k].digest() == hashlist[i].digest()):
                tobedel.append(k)

    tobedel=list(set(tobedel))
    count = Deletion(search, tobedel, cnt)
    return count


def Deletion(search,tobedel, cnt):
    d = '/home/sujaya/csa_internship/'+search +'/'

    user_names=[]
    try:
        uname=open(d + "un1.txt","r")
    except Exception,e:
        uname=open(d + "un.txt","r")
    user_names=uname.read().split("\n")
    uname.close()

    newuname=[]
    for i in range(cnt):
        if i not in tobedel:
            newuname.append(user_names[i])
        else:
            print user_names[i]    


    for i in tobedel:
        myfile = d + search + str(i)+".txt"
        if os.path.isfile(myfile):
            os.remove(myfile)
        else:
            print("Error: %s file not found" % myfile)


    count=-1
    for i in range(cnt):
        myfile= d + search+str(i)+".txt"
        if os.path.isfile(myfile):
            count=count+1
            newname = d + search+str(count)+".txt"
            os.renames(myfile,newname)
               
 
    uname=codecs.open(d + "un1.txt","w",encoding = "utf-8")
    text=''
    j = 0
    for i in newuname:
        try:
            uname.writelines(i + '\n')
        except UnicodeDecodeError:
            dt = i.partition('\t')
            uname.writelines("user" + str(j) +" "+ str(dt[2]) + '\n')
            j = j + 1
            
    uname.close()

    return count
#Hashed('sargam', 41)



