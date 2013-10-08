import nltk
import re

def Removestopwords(textwords):
    stopwords=open('stopwords.txt','r').read().split()

    textwords=textwords.replace('.',' ')
    textwords=textwords.replace(',',' ')
    textwords=textwords.replace(':',' ')
    textwords=textwords.replace('(',' ')
    textwords=textwords.replace(')',' ')
    textwords=textwords.replace(']',' ')
    textwords=textwords.replace('[',' ')    
    textwords=textwords.replace('/',' ')
    textwords=textwords.replace('"',' ')
    textwords=textwords.replace("'",' ')
    textwords=textwords.split(' ')
    new = []
    text=''
    
    #stp = ["bangalore","india", "institute","institution", "science", "research", "student" ,"indian", "iisc", "tata"]
    #stp = ["concepts", "conception", "liberty", "free", "freedom", "rights", "state", "liberalism"]
    #stp = ["alpha","alphabet","greek","letter","first"]
    #stp = ["quilt","fabric","quilts", "sewing", "sewn", "stitches","large", "piece", "pieces"]
    #stp = ["sweet", "sweetness","taste", "sugar","sugars", "substances","chemical", "bitter","bitterness","sour","sourness","detect","sensation","sence","substance","food","foods"]
    stp = ["sargam","film"]
    #stp = ["bangalore", "city","karnataka", "region", "bengaluru","south", "indian", "india", "area","areas","capital","mysore","government", "technology","state","states","public"]
    textwords = re.sub(" \d+", "", textwords )
    for words in textwords:
        if words.lower() not in stopwords and words.lower() not in stp:
            new.append(words)

    for words in new:
        text=text+' '+words
        
    return text
