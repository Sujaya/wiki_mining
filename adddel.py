import os
import codecs

def Adddel(search, count):
    #count  = Vand(search, cnt)
    d = '/home/sujaya/csa_internship/'+search
    
    mod=open(d+ "/Add_Delete.txt","w")
    text=open(d+'/'+search+'0.txt',"r").read().split()
    un=open(d+'/un1.txt',"r")

    user_names=un.read().split("\n")
    mod.writelines('\n\nUser0 : '+user_names[0]+'\n\n')
    for x in text:
        mod.writelines('Added\t'+x+'\t'+user_names[0]+'\n')
    un.close()
    for i in range(1,count+1):
        deleted=[]
        added=[]
        word1=[]
        word2=[]
        fn1 = d+'/'+search+str(i-1)+".txt"
        fn2 = d+'/'+search+str(i)+".txt"
        word1=open(fn1,"r").read().split()
        word2=open(fn2,"r").read().split()
        

        cun = user_names[i]
        deleted = [x for x in word1 if x not in word2]
        added = [x for x in word2 if x not in word1]
        mod.writelines('\n\nUser'+str(i)+' : '+cun+'\n\n')
        for x in deleted:
            mod.writelines('Deleted\t'+x+'\t'+cun+'\n')
        for x in added:
            mod.writelines('Added\t'+x+'\t'+cun+'\n')
            #print deleted
            #print added
    mod.close()
    print 'Done'

    

#Adddel('glide', 65)