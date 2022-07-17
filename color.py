while True:
    x=input('Enter color: ')
    y=x.split(',')
    for i in range(len(y)):
        y[i]=round(int(y[i])/255,2)
    y.append(1)
    print(y)
#013c44	(1,60,68)
#0d496e	(13,73,110)
#366092	(54,96,146)
#bdd7ee	(189,215,238)
#a5aaad	(165,170,173)