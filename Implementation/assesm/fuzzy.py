import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

faceColor = 'white' #'012a53'
spines = '#e5ecf600'
fill = '#e5ecf6'
fill2 = '#feb377'
fontAxesColor = '#555555'#'whitesmoke'
fontColor = '#555555' #'whitesmoke'

def trapezoidFuzz(data):   
    # pretvori sva polja u float
    if str(data[0]) == '"+"' or str(data[0]) == '"-"':
        data[0] = str(data[0])[1:-1] # skini suvisne navodnike
        for i in range(1,len(data)):
            data[i] = float(data[i])
        # posalji parametre na ocenjivanje
        v = data[1]
        a = data[2]
        b = data[3]
        c = data[4]
        d = data[5]
        s = data[0]
        return trapFu(v,a,b,c,d,s)
    elif str(data[0]) == '+' or str(data[0]) == '-':
        for i in range(1,len(data)):
            data[i] = float(data[i])
        # posalji parametre na ocenjivanje
        v = data[1]
        a = data[2]
        b = data[3]
        c = data[4]
        d = data[5]
        s = data[0]
        return trapFu(v,a,b,c,d,s)
    else:
        for i in range(0,len(data)):
            data[i] = float(data[i])
        v = data[0]
        a = data[1]
        b = data[2]
        c = data[3]
        d = data[4]
        return trapFu(v,a,b,c,d)

# Funkcija koja racuna brojcani stepen pripadnosti trapezoidnoj fazi funkciji pripadnosti
def trapFu(v,a,b,c,d,s='+'):
    x = np.arange(d+2)
    f = fuzz.trapmf(x, [a,b,c,d])
    mf = fuzz.interp_membership(x,f,v)
    if(s=='-'):
        return np.round((1-mf)*100,3)
    else:
        return np.round(mf*100,3)

def triangleFuzz(data):
    # pretvori sva polja u float
    if str(data[0]) == '"+"' or str(data[0]) == '"-"':
        data[0] = str(data[0])[1:-1] # skini suvisne navodnike
        for i in range(1,len(data)):
            data[i] = float(data[i])
        # posalji parametre na ocenjivanje
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        c = data[4]
        return triaFu(v,a,b,c,s)
    elif str(data[0]) == '+' or str(data[0]) == '-':
        for i in range(1,len(data)):
            data[i] = float(data[i])
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        c = data[4]
        return triaFu(v,a,b,c,s)
    else:
        for i in range(0,len(data)):
            data[i] = float(data[i])
        v = data[0]
        a = data[1]
        b = data[2]
        c = data[3]
        return triaFu(v,a,b,c)
    
# Funkcija koja racuna brojcani stepen pripadnosti trougaonoj fazi funkciji pripadnosti
def triaFu(v,a,b,c,s='+'):
    x = np.arange(c+1)
    f = fuzz.trimf(x, [a,b,c])
    mf = fuzz.interp_membership(x,f,v)
    if(s=='-'):
        return np.round((1-mf)*100,3)
    else:
        return np.round(mf*100,3)
    
def sigmoidFuzz(data):
    # pretvori sva polja u float
    if str(data[0]) == '"+"' or str(data[0]) == '"-"':
        data[0] = str(data[0])[1:-1] # skini suvisne navodnike
        for i in range(1,len(data)):
            data[i] = float(data[i])
        # posalji parametre na ocenjivanje
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        return sigmFu(v,a,b,s)
    elif str(data[0]) == '+' or str(data[0]) == '-':
        for i in range(1,len(data)):
            data[i] = float(data[i])
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        return sigmFu(v,a,b,s)
    else:
        for i in range(0,len(data)):
            data[i] = float(data[i])
        v = data[0]
        a = data[1]
        b = data[2]
        return sigmFu(v,a,b)
    
# Funkcija koja racuna brojcani stepen pripadnosti sigmoidnoj Fazi funkciji pripadnosti
def sigmFu(v,a,b,s='+'):
    x = np.arange(b+1)
    f = fuzz.sigmf(x,a,b)
    mf = fuzz.interp_membership(x,f,v)
    if(s=='-'):
        return np.round((1-mf)*100,3)
    else:
        return np.round(mf*100,3)

def gaussFuzz(data):
    # pretvori sva polja u float
    if str(data[0]) == '"+"' or str(data[0]) == '"-"':
        data[0] = str(data[0])[1:-1] # skini suvisne navodnike
        for i in range(1,len(data)):
            data[i] = float(data[i])
        # posalji parametre na ocenjivanje
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        return gausFu(v,a,b,s)

    elif str(data[0]) == '+' or str(data[0]) == '-':
        for i in range(1,len(data)):
            data[i] = float(data[i])
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        return gausFu(v,a,b,s)
    else:
        for i in range(0,len(data)):
            data[i] = float(data[i])
        v = data[0]
        a = data[1]
        b = data[2]
        return gausFu(v,a,b)
    
# Funkcija koja racuna brojcani stepen pripadnosti gausovoj Fazi funkciji pripadnosti
def gausFu(v,a,b,s='+'):
    x = np.arange(3*b)
    f = fuzz.gaussmf(x,a,b)
    mf = fuzz.interp_membership(x,f,v)
    if(s=='-'):
        return np.round((1-mf)*100,3)
    else:
        return np.round(mf*100,3)

def gauss2Fuzz(data):
    # pretvori sva polja u float
    if str(data[0]) == '"+"' or str(data[0]) == '"-"':
        data[0] = str(data[0])[1:-1] # skini suvisne navodnike
        for i in range(1,len(data)):
            data[i] = float(data[i])
        # posalji parametre na ocenjivanje
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        c = data[4]
        d = data[5]
        return gau2Fu(v,a,b,c,d,s)

    elif str(data[0]) == '+' or str(data[0]) == '-':
        for i in range(1,len(data)):
            data[i] = float(data[i])
        s = data[0]
        v = data[1]
        a = data[2]
        b = data[3]
        c = data[4]
        d = data[5]
        return gau2Fu(v,a,b,c,d,s)

    else:
        for i in range(0,len(data)):
            data[i] = float(data[i])
        v = data[0]
        a = data[1]
        b = data[2]
        c = data[3]
        d = data[4]
        return gau2Fu(v,a,b,c,d)
    
# Funkcija koja racuna brojcani stepen pripadnosti gausovoj Fazi funkciji pripadnosti
def gau2Fu(v,a,b,c,d,s='+'):
    x = np.arange(3*d)
    f = fuzz.gauss2mf(x,a,b,c,d)
    mf = fuzz.interp_membership(x,f,v)
    if(s=='-'):
        return np.round((1-mf)*100,3)
    else:
        return np.round(mf*100,3)

# Fja za racunanje prosecne vrednosti ocena metrika unutar skupa metrika
def averageGrade(pFaziSkupMtr,metricSet,metricNames):
    num = 0
    summ = 0.0

    for name in metricNames:
       summ = summ + pFaziSkupMtr[metricSet][name]
       num = num + 1

    return int(round(summ/num))

# Fja za racunanje proseka vise skupova metrika
def averageGradeMult(pFaziSkupMtr,metricSet,metricNames, compare="none"):
    num = 0
    summ = 0.0
    if compare == "compare":
        avgDict = {}
        for metricSet in pFaziSkupMtr:
            keysMetricNames = list(pFaziSkupMtr[metricSet].keys())
            avgDict[metricSet] = averageGrade(pFaziSkupMtr,metricSet,keysMetricNames)
 
        return avgDict
    else:
        for metricSet in pFaziSkupMtr:
            for key in pFaziSkupMtr[metricSet]:
                summ = summ + pFaziSkupMtr[metricSet][key]
                num = num + 1
        
        return int(round(summ/num))

# Fja koja racuna linearnu fazi fju
def linearFuzz(data):
    # pretvori sva polja u float
    for i in range(0,len(data)):
        data[i] = float(data[i])
        
    # U ako je prvi parametar manji od drugog -> pravi rastucu Fazi funkciju
    if (data[1]<=data[2]):
        pfMtr = faziRastuci(data[0],data[1],data[2])
    else:
        pfMtr = faziOpadajuci(data[0],data[1],data[2])

    return pfMtr

# Funkcija koja racuna brojcani stepen pripadnosti linearnoj opadajucoj fazi fji pripadnosti
def faziOpadajuci(v1,a1,b1):
    x = np.arange(a1+1)
    f1 = fuzz.trimf(x, [0, 0, b1]) # Izmenjena trougaona Fazi funkcija
    m1f1 = fuzz.interp_membership(x,f1,v1)
    return np.round(m1f1*100,3)

# Funkcija koja racuna brojcani stepen pripadnosti linearnoj rastucoj fazi fji pripadnosti
def faziRastuci(v2,a2,b2):
    x = np.arange(b2+1)
    f2 = fuzz.piecemf(x,[a2,b2,b2])
    m1f2 = fuzz.interp_membership(x,f2,v2)
    return np.round(m1f2*100,3)

##############################################Fje koje treba preseliti u nov modul##################################################

# Funkcija koja zeljene metrike iz skupa metrika crta odgovarajucu fazi funkciju
def crtajMetrike(nazivSkupaMtrCrtanje,pMetrikeKCrtanje,pFaziSkupMtr,pSkupMtr):

    # Inicijalizujemo niz cije cemo clanove koristiti kao parametre za prosledjivanje Fazi fjama crtanja
    niz = [0,0,0]
    print('Drawing metrics:',nazivSkupaMtrCrtanje,'\n')

    # Izdvoj iz skupa svih ocenjenih metrika pFaziSkupMtr
    # one izracunate vrednosti metrika prema imenima navedenim u nazivSkupaMtrCrtanje
    for i in range(0,len(pMetrikeKCrtanje[nazivSkupaMtrCrtanje])):
        print(
            pMetrikeKCrtanje[nazivSkupaMtrCrtanje][i],
            pFaziSkupMtr[nazivSkupaMtrCrtanje][pMetrikeKCrtanje[nazivSkupaMtrCrtanje][i]]
          ,'\n')
    # Izdvoji zeljene vrednosti metrika iz skupa metrika pSkupMtr i smesti za svaki parametar
    # sve tri vrednosti (izmerena vrednost, a, b)
    metricsDraw = list(pMetrikeKCrtanje[nazivSkupaMtrCrtanje].values())
    
    for key in metricsDraw:
        niz = list(pSkupMtr[nazivSkupaMtrCrtanje][key]['data'].values()) # uzmi podatke sirove metrike

        # na osnovu vrste metrike zovi odgovarajucu fju za njeno crtanje
        if (pSkupMtr[nazivSkupaMtrCrtanje][key]['type']) == 'linear':
            # Ako je prvi parametar manji od drugog -> crtaj i racunaj rastucu Fazi funkciju
            if (niz[1]<=niz[2]):
               faziRastuciCrtaj(niz[0],niz[1],niz[2],key,nazivSkupaMtrCrtanje)
            # U suprotnom -> crtaj i racunaj opadajucu Fazi funkciju
            else:
               faziOpadajuciCrtaj(niz[0],niz[1],niz[2],key,nazivSkupaMtrCrtanje)
        else:
            raise SyntaxError("Unsuported function type for drawing.")

# Funkcija koja crta grafik Fazi funkcije za metriku koja ima rastucu Fazi funkciju pripadnosti
def faziRastuciCrtaj(v2,a2,b2,nazivMetrike,nazivSkupaMtrCrtanje):

    # Napravi oblast vrednosti, Fazi fju pripadnosti i izracunaj stepen pripadnosti v2 fji f2
    x = np.arange(b2+1)
    f2 = fuzz.piecemf(x,[a2,b2,b2])
    m1f2 = fuzz.interp_membership(x,f2,v2)

    fig = plt.figure(figsize=(7, 6), facecolor=faceColor)
    
    # Podesavanje izgleda grafika
    ax = plt.gca()
    ax.set_facecolor(faceColor) #'#012a53'
    ax.spines["right"].set_color(spines)
    ax.spines["top"].set_color(spines)
    ax.spines["left"].set_color('gray')
    ax.spines["bottom"].set_color('gray')

    font = {'fontname':'Calibri', 'fontsize':16, 'color':fontColor, 'weight':'bold'}
    fontAxes = {'fontname':'Calibri', 'fontsize':12, 'color':fontAxesColor}
    plt.xticks(**fontAxes)
    plt.yticks(**fontAxes)

    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')

    ax.yaxis.label.set_color('grey')
    ax.xaxis.label.set_color('grey')
    
    ax.set_xlabel('Value')
    ax.set_ylabel('Grade')
   
    plt.title('Metric '+nazivMetrike+' - '+nazivSkupaMtrCrtanje, **font)
    plt.plot(x,f2, color='grey')

    # Nacrtaj uspravnu i vodoravnu projekciju vrednosti v2
    plt.axhline(y=m1f2, xmin=0, xmax=v2/b2, color='blue', alpha=0.8, linewidth=1.2, linestyle='dashed')
    plt.axvline(x=v2, ymin=0, ymax=m1f2, color='blue', alpha=0.8, linewidth=1.2, linestyle='dashed')

    plt.axhline(y=1, linewidth=1.2, linestyle='dashed',alpha=0.8, color='green')
    plt.axhline(y=0.7, linewidth=1.2, linestyle='dashed',alpha=0.5, color='orange')
    plt.axhline(y=0.4, linewidth=1.2, linestyle='dashed',alpha=0.4, color='red')


    # Iznad oznacene tacke na grafi
    plt.annotate(str(round(m1f2,2))+'; '+str(v2),
                 (v2,m1f2),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center', bbox=dict(boxstyle="round",
                    facecolor='wheat', alpha=1
                   ))
    
    # Oznaci gde se nalazi tacka na funkciji pripadnosti za v2 i oboj je prema vrednosti m1f2
    if 100*m1f2<=40:
        plt.plot(v2, m1f2, color='black', linestyle='dashed', linewidth = 3, 
                     marker='o', markerfacecolor='red', markersize=6)
    elif 100*m1f2>40 and 100*m1f2<=70:
        plt.plot(v2, m1f2, color='black', linestyle='dashed', linewidth = 3, 
                     marker='o', markerfacecolor='orange', markersize=6)
    elif 100*m1f2>70 and 100*m1f2<=100:
        plt.plot(v2, m1f2, color='black', linestyle='dashed', linewidth = 3, 
                     marker='o', markerfacecolor='green', markersize=6)
    
    plt.show(block=False)

# Funkcija koja crta grafik Fazi funkcije za metriku koja ima opadajucu Fazi funkciju pripadnosti
def faziOpadajuciCrtaj(v2,a2,b2,nazivMetrike,nazivSkupaMtrCrtanje):
    x = np.arange(a2+1)
    f2 = fuzz.trimf(x,[0,0,b2])
    m1f2 = fuzz.interp_membership(x,f2,v2)

    fig = plt.figure(figsize=(7, 6), facecolor=faceColor)
    ax = plt.gca()
    ax.set_facecolor(faceColor)
    ax.spines["right"].set_color("white")
    ax.spines["top"].set_color("white")
    ax.spines["left"].set_color(fontColor)
    ax.spines["bottom"].set_color(fontColor)

    font = {'fontname':'Calibri', 'fontsize':16, 'color':fontColor, 'weight':'bold'}
    fontAxes = {'fontname':'Calibri', 'fontsize':12, 'color':"black"}
    plt.xticks(**fontAxes)
    plt.yticks(**fontAxes)

    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')
    
    ax.yaxis.label.set_color('grey')
    ax.xaxis.label.set_color('grey')
    
    ax.set_xlabel('Value')
    ax.set_ylabel('Grade')
   
    plt.title('Metric '+nazivMetrike+' - '+nazivSkupaMtrCrtanje, **font)

    plt.plot(x,f2, color="grey")
    plt.axhline(y=m1f2, xmin=0, xmax=v2/a2, color='blue', alpha=0.8, linewidth=1.2, linestyle='dashed')
    plt.axvline(x=v2, ymin=0, ymax=m1f2, color='blue', alpha=0.8, linewidth=1.2, linestyle='dashed')

    plt.axhline(y=1, linewidth=1.2, linestyle='dashed',alpha=0.8, color='green')
    plt.axhline(y=0.7, linewidth=1.2, linestyle='dashed',alpha=0.5, color='orange')
    plt.axhline(y=0.4, linewidth=1.2, linestyle='dashed',alpha=0.4, color='red')

    plt.annotate(str(round(m1f2,2))+'; '+str(v2),
                (v2,m1f2),
                textcoords="offset points",
                xytext=(0,11),
                ha='center', bbox=dict(boxstyle="round",
                facecolor='wheat', alpha=1
                ))
    
    if 100*m1f2<=40:
        plt.plot(v2, m1f2, color='black', linestyle='dashed', linewidth = 3, 
                     marker='o', markerfacecolor='red', markersize=6)
    elif 100*m1f2>40 and 100*m1f2<=70:
        plt.plot(v2, m1f2, color='black', linestyle='dashed', linewidth = 3, 
                     marker='o', markerfacecolor='orange', markersize=6)
    elif 100*m1f2>70 and 100*m1f2<=100:
        plt.plot(v2, m1f2, color='black', linestyle='dashed', linewidth = 3, 
                     marker='o', markerfacecolor='green', markersize=6)
    
    plt.show(block=False)
