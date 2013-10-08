for i in range(919):
    f = open(d + str(c) +".txt", "r")
    text = f.read()
    text = stop1.Removestopwords(text)
    f.close()
    f = codecs.open(d + str(c) +".txt","w", "utf-8")
    if f:
        if text != ' ':
            try:
                f.writelines(text)
            except Exception, e:
                text = unicode(text , errors='ignore')
                f.writelines(text)
    f.close()
    c = c+1
