#######################################################Sintaksa ITL-a################################################################
import numpy as np
import pandas as pd
import itertools as it

from lark import Lark
from lark import exceptions as lexc

from grrep.report import *
from assesm.fuzzy import *

################################Gramatika ITL domenski specificnog programskog jezika################################################

try:
    input = raw_input
except NameError:
    pass

# Definisemo gramatiku jezika prema prosirenoj Bahus-Naurovoj formi (EBNF) metasintaktičkih opisa
grammar = """
    start: instruction+
    
    instruction: "assessment" STRING code_block -> pocetak_izvestaja
               | "metrics" NAME "{" dict_item* "}" -> skup_metrika
               | "grade" NAME ";" -> oceni_metrike
               | "grade cumulative" NAME "," NAME ("," NAME)* ";" -> oceni_metrike_z
               | "grade comparative" NAME "," NAME";" -> oceni_metrike_u
               | "grade singular" NAME ("," NAME)* ";" -> oceni_metrike_p
               | "print" NAME ("," NAME)* ";" -> ispisi_metrike
               | "make excel report" STRING ";" -> pravi_izvestaj
               | "draw metric" NAME ("," NAME)* "from" set -> nacrtaj_metriku

    code_block: "{" instruction+ "}" -> blok_naredbi
    dict_item: NAME "=" dict_subitem -> naziv_metrike
    dict_subitem: "(" NUMBER "," NUMBER "," NUMBER ")" -> par_mer_lin     
                | "trapezoid(" STRING? ","? NUMBER "," NUMBER "," NUMBER "," NUMBER "," NUMBER ")" -> par_mer_tra
                | "triangle(" STRING? ","? NUMBER "," NUMBER "," NUMBER "," NUMBER ")" -> par_mer_tri
                | "gauss(" STRING? ","? NUMBER "," NUMBER "," NUMBER ")" -> par_mer_gau
                | "gauss2(" STRING? ","? NUMBER "," NUMBER "," NUMBER "," NUMBER "," NUMBER ")" -> par_mer_gau2
                | "sigmoid(" STRING? ","? NUMBER "," NUMBER "," NUMBER ")" -> par_mer_sig
    set: NAME ";" -> from
    COMMENT : /#.*/
    
    %import common.CNAME -> NAME
    %import common.NUMBER -> NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
    %ignore COMMENT
"""

# Definisemo objekat parsera gramatike (citaca) prema Earley algoritmu citanja (parsovanja)
parser = Lark(grammar)

##############################################Fje za obradu parsovnih podataka#######################################################

# obrada naredbe grade, kao izlaz vraca ocenjen skup metrika
def grade(metric, pSkupMtr):
    metricSet = str(metric.children[0]) # smesti naziv skupa metrika
    metricNames = pSkupMtr[metricSet].keys() # smesti nazive metrika unutar skupa
    metrics = pSkupMtr[metricSet] # objekti {} metrika za dato ime skupa metrika

    pFaziSkupMtr = {metricSet:{}}
    avgGrade = ''

    # idi kroz svaku metriku skupa
    for name in metricNames:
        if metrics[name]['type']=='linear':
            # obradi metrike i vrati ih
            pFaziSkupMtr[metricSet][name] = linearFuzz(metrics[name]['data'])
        elif metrics[name]['type']=='trapezoid':
            pFaziSkupMtr[metricSet][name] = trapezoidFuzz(metrics[name]['data'])
        elif metrics[name]['type']=='triangle':
            pFaziSkupMtr[metricSet][name] = triangleFuzz(metrics[name]['data'])
        elif metrics[name]['type']=='sigmoid':
            pFaziSkupMtr[metricSet][name] = sigmoidFuzz(metrics[name]['data'])
        elif metrics[name]['type']=='gauss':
            pFaziSkupMtr[metricSet][name] = gaussFuzz(metrics[name]['data'])
        elif metrics[name]['type']=='gauss2':
            pFaziSkupMtr[metricSet][name] = gauss2Fuzz(metrics[name]['data'])

    avgGrade = averageGrade(pFaziSkupMtr,metricSet,metricNames) 
    print(' Metric set:',pFaziSkupMtr) #napravljen skup sa svim ocenjenim metrikama
    print(' Grade:',str(avgGrade)+'/100 points')
    print(' Grade zone:', gradeZone(avgGrade),'\n')
    return pFaziSkupMtr

# obrada naredbe grade cumulative, kao izlaz vraca zbirno ocenjene skupove metrika
def gradeCumul(metric, pSkupMtr):
    metricSet = {}

    for index in range(0,len(metric.children)): 
        metricSet[index] = str(metric.children[index]) # izlaz {0: 'E_banka_1', 1: 'E_banka_2'}

    metricNames = metricSet.keys() # smesti nazive metrika unutar skupa

    pFaziSkupMtr = {}
    avgGrade = ''

    for name in metricNames:

       pFaziSkupMtr[metricSet[name]] = {}

       for key in pSkupMtr[metricSet[name]].keys():
           data = pSkupMtr[metricSet[name]][key]['data']

           if pSkupMtr[metricSet[name]][key]['type']=='linear':
               pFaziSkupMtr[metricSet[name]][key] = linearFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='trapezoid':
               pFaziSkupMtr[metricSet[name]][key] = trapezoidFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='triangle':
               pFaziSkupMtr[metricSet[name]][key] = triangleFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='sigmoid':
               pFaziSkupMtr[metricSet[name]][key] = sigmoidFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='gauss':
               pFaziSkupMtr[metricSet[name]][key] = gaussFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='gauss2':
               pFaziSkupMtr[metricSet[name]][key] = gauss2Fuzz(data)

    avgGrade = averageGradeMult(pFaziSkupMtr,metricSet,metricNames)
    
    print(' Metric sets:',pFaziSkupMtr) #napravljen skup sa svim ocenjenim metrikama
    print(' Grade:',str(avgGrade)+'/100 points')
    print(' Grade zone:', gradeZone(avgGrade),'\n')
    return pFaziSkupMtr,avgGrade

# obrada naredbe grade comparative, kao izlaz vraca dva ocenjena skupa metrika i ispisuje koji ima bolju ocenu i za koliko %
def gradeComp(metric, pSkupMtr):
    metricSet = {}

    for index in range(0,len(metric.children)): 
        metricSet[index] = str(metric.children[index]) # izlaz {0: 'E_banka_1', 1: 'E_banka_2'}

    metricNames = metricSet.keys() # smesti nazive metrika unutar skupa

    pFaziSkupMtr = {}
    avgGrade = ''

    for name in metricNames:

       pFaziSkupMtr[metricSet[name]] = {}

       for key in pSkupMtr[metricSet[name]].keys():
           data = pSkupMtr[metricSet[name]][key]['data']

           if pSkupMtr[metricSet[name]][key]['type']=='linear':
               pFaziSkupMtr[metricSet[name]][key] = linearFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='trapezoid':
               pFaziSkupMtr[metricSet[name]][key] = trapezoidFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='triangle':
               pFaziSkupMtr[metricSet[name]][key] = triangleFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='sigmoid':
               pFaziSkupMtr[metricSet[name]][key] = sigmoidFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='gauss':
               pFaziSkupMtr[metricSet[name]][key] = gaussFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='gauss2':
               pFaziSkupMtr[metricSet[name]][key] = gauss2Fuzz(data)

    avgGrade = averageGradeMult(pFaziSkupMtr,metricSet,metricNames,"compare")
    
    print(' Metric sets:',pFaziSkupMtr,'\n') #napravljen skup sa svim ocenjenim metrikama

    # odredjivanje vece vrednosti metrike
    avgGrade1 = list(avgGrade.values())[0]
    avgGradeName1 = list(avgGrade)[0]
    avgGrade2 = list(avgGrade.values())[1]
    avgGradeName2 = list(avgGrade)[1]

    if avgGrade1>avgGrade2:
        grade = str(round((avgGrade1/avgGrade2-1)*100))
        print("> Result:\n The metric",avgGradeName1,"has", grade+"% higer grade than the metric",avgGradeName2+'.')
    elif avgGrade2>avgGrade1:
        grade = str(round((avgGrade2/avgGrade1-1)*100))
        print(" The metric",avgGradeName2,"has", grade+"% higer grade than the metric",avgGradeName1+'.')
    else:
        print(' The both metrics have equal grades.')

    print(' Grades:',avgGrade,'\n')

    return pFaziSkupMtr,avgGrade

# obrada naredbe grade singular, kao izlaz vraca pojedinacno ocenjene skupove metrika i ispisuje rang listu
def gradeSing(metric, pSkupMtr, leaderboard="hide"):
    metricSet = {}

    for index in range(0,len(metric.children)): 
        metricSet[index] = str(metric.children[index]) # izlaz {0: 'E_banka_1', 1: 'E_banka_2'}

    metricNames = metricSet.keys() # smesti nazive metrika unutar skupa

    pFaziSkupMtr = {}
    avgGrade = ''

    for name in metricNames:
        
       for key in pSkupMtr[metricSet[name]].keys():
           data = pSkupMtr[metricSet[name]][key]['data']

           if pSkupMtr[metricSet[name]][key]['type']=='linear':
               pFaziSkupMtr[metricSet[name]] = linearFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='trapezoid':
               pFaziSkupMtr[metricSet[name]] = trapezoidFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='triangle':
               pFaziSkupMtr[metricSet[name]] = triangleFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='sigmoid':
               pFaziSkupMtr[metricSet[name]] = sigmoidFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='gauss':
               pFaziSkupMtr[metricSet[name]] = gaussFuzz(data)

           elif pSkupMtr[metricSet[name]][key]['type']=='gauss2':
               pFaziSkupMtr[metricSet[name]] = gauss2Fuzz(data)

    
    for setName in pFaziSkupMtr:
        print(' Metric set:',setName)
        grade = str(int(round(pFaziSkupMtr[setName])))
        print(' Grade:',grade+'/100 points')
        print(' Grade zone:', gradeZone(pFaziSkupMtr[setName]),'\n')

    if leaderboard=="show":
        sortedPFaz = sorted(pFaziSkupMtr.items(), key=lambda x: x[1], reverse=True)
        print("> Leaderboard:")
        print("____________________________________")
        num = 1
        for setName in sortedPFaz:
            print(str(num)+'. Metric set:',setName)
            num = num + 1
        print('\n')
    return pFaziSkupMtr

#####################################################Parsovanje unetih naredbi########################################################

# Glavna funkcija koja izvrsava naredbe ITL jezika
def run_instruction(t):
    pSkupMtr = {}
    pMtr = {}
    pfMtr = {}

    pFaziSkupMtr = {}
    pFaziSkupMtrCumul = {}
    pFaziSkuMtrComp = {}
    pFaziSkupMtrSing = {}

    nazivIzv = ""

    # Sledi deo koda koji procitanu (parsovanu) sintaksu koju
    # je uneo korisnik razlaze iz drveta gramatike (koje je
    # napravio Earley citac (parser) i na osnovu naredbe i
    # njenih parametara poziva odredjenu funkciju
    
    # Ako je koren drveta tj. naredba "izvestaj"
    if t.data == 'pocetak_izvestaja':
        # Inicijalizuj objekat za ispis metrika u Eksel
        pdPrintMetrics = []
        pdCumulativeGrades = []
        pdIndividualGrades = []
        pdComparativeGrades = []

        # Izdvoj naziv izvestaja
        nazivIzv = t.children[0]

        # A za grane njegovog drveta
        for i in t.children[1].iter_subtrees():

            # Ako je grana skup_metrika
            if i.data == 'skup_metrika':
                # Uzmi njegov naziv
                nazivSkupaMtr = str(i.children[0]) #naziv skupa metrika
                # Inicijalizuj niz u kome cemo da cuvamo privremeno metriku
                pSkupMtr[nazivSkupaMtr] = {}

                # Prodji kroz grane metrike
                for j in i.iter_subtrees():
                    # Za svaku metriku napravi privremeni prazan recnik
                    priv = {}
                    # Kad naidjes na naziv metrike
                    if j.data == "naziv_metrike":
                        nazivMtr = str(j.children[0]) # Smesti naziv metrike

                        if j.children[1].data =="par_mer_lin":
                            # Unesi vrstu metrike u polje 'type'
                            priv = {"type":"linear","data":{}}

                        elif j.children[1].data =="par_mer_tra":
                            priv = {"type":"trapezoid","data":{}}
                     
                        elif j.children[1].data =="par_mer_gau":
                            priv = {"type":"gauss","data":{}}

                        elif j.children[1].data =="par_mer_gau2":
                            priv = {"type":"gauss2","data":{}}
        
                        elif j.children[1].data =="par_mer_tri":
                            priv = {"type":"triangle","data":{}}

                        elif j.children[1].data =="par_mer_sig":
                            priv = {"type":"sigmoid","data":{}}

                        # Unesi podatke metrike u polje 'data'
                        for k in range(0,len(j.children[1].children)): 
                            try:
                                item =float(j.children[1].children[k])   
                            except:
                                try:
                                    item =str(j.children[1].children[k])
                                except:
                                    pass
                            priv["data"][k] = item 
                        
                        # Smesti recnik sa vrednostima metrike u privremeni niz metrika
                        pMtr[nazivMtr] = priv
                        
                # Na kraju smesti recnik koji sadrzi
                # {Naziv metrike: {'Metrika 1': vrednost 1,'Metrika 2': vrednost 2,'Metrika 3': vrednost 3},...}
                pSkupMtr[nazivSkupaMtr] = pMtr
                # Isprazni recnik za sledecu metriku
                pMtr = {}

            # Deo koda zaduzen za ocenjivanje jedne metrike
            # Kao izlaz dobija se radarski grafik zeljenog skupa metrika
            # i izracunata ocena skupa metrika (srednja vrednost ocena pojedinacnih metr.) 
            # Ako je naredba "grade"
            elif i.data == 'oceni_metrike':
                print("> Metric grade:")
                print("______________\n")
                # Inicijaluzuj recnik u koji smestamo ocenjene metrike u njihovim skupovima metrika
                pFaziSkupMtr = {}

                # Izdvoj vrednosti metrika iz trenutnog skupa metrike i izracunaj njenu vrednost
                pFaziSkupMtr = grade(i, pSkupMtr)           
                    
                # Spremi podatke za crtanje i posalji ih
                nazivSkupaMtrGrafik = ''
                for key in pFaziSkupMtr:
                    nazivSkupaMtrGrafik = key
                grafickiPrikaz(pFaziSkupMtr, nazivSkupaMtrGrafik, nazivIzv)
               

            # Deo koda zaduzen za zbirno ocenjivanje vise metrika
            # Kao izlaz dobija se prosecna ocena za unete metrike
            # Ako je naredba "grade cumulative"
            elif i.data == 'oceni_metrike_z':
                print("> Cumulative grade:")
                print("__________________\n")
                pFaziSkuMtrCumul = {}
                pFaziSkupMtrCumul = gradeCumul(i, pSkupMtr)

                # uzmi vracen objekat od gradeCumul i unesi u Eksel objekat
                for setName in pFaziSkupMtrCumul[0]:
                    pdCumulativeGrades.append({'Metric': setName, 'Grade':'','Max grade':''})

                gradeCumulative = pFaziSkupMtrCumul[1]
                pdCumulativeGrades.append({'Metric': '', 'Grade':gradeCumulative,'Max grade':100})
    
                
            # Deo koda zaduzen za uporedno ocenjivanje i prikaz dva skupa metrika sa istim nazivima metrika
            # Kao izlaz dobija se prosecna ocena za dve unete metrike i njihv prikaz na radarskom grafiku
            # Ako je naredba "oceni uporedno"
            elif i.data == 'oceni_metrike_u':
                print("> Comparative grade:")
                print("___________________\n")
                pFaziSkuMtrComp = {}
                pFaziSkupMtrComp = gradeComp(i, pSkupMtr)

                # Spremi podatke za crtanje
                nazivSkupaMtrGraf = []
                for key in pFaziSkupMtrComp[0]:
                    nazivSkupaMtrGraf.append(key)
               # Pozovi fju za crtenje dva radaska grafika na jednoj slici
                grafickiPrikazUporedno(
                    pFaziSkupMtrComp[0][nazivSkupaMtrGraf[0]],
                    pFaziSkupMtrComp[0][nazivSkupaMtrGraf[1]],
                    nazivSkupaMtrGraf[0],
                    nazivSkupaMtrGraf[1],
                    nazivIzv
                    )

                # uzmi vracen objekat od gradeComp i unesi u Eksel objekat
                for setName in pFaziSkupMtrComp[1]:
                    gradeComparative = int(round(pFaziSkupMtrComp[1][setName]))
                    pdComparativeGrades.append({'Metric': setName, 'Grade':gradeComparative,'Max grade':100})

            # Deo koda zaduzen za pojedinacno ocenjivanje vise metrika
            # Kao izlaz dobija pojedinacna se prosecna ocena za unete metrike
            # Ako je naredba "grade singular"
            elif i.data == 'oceni_metrike_p':
                print('> Individual grades:')
                print("___________________\n")
                pFaziSkupMtrSing = {}           
                pFaziSkupMtrSing = gradeSing(i, pSkupMtr, leaderboard="show")

                # uzmi vracen objekat od gradeSing i unesi u Eksel objekat
                for setName in pFaziSkupMtrSing:
                    gradeIndi = int(round(pFaziSkupMtrSing[setName]))
                    pdIndividualGrades.append({'Metric': setName, 'Grade':gradeIndi,'Max grade':100})               
            
            # Deo koda zaduzen za ispis unetih parametara jedne ili vise metrika
            # Kao izlaz dobija se spisak metrika sa parametrima
            # Ako je naredba "ispisi"
            elif i.data == 'ispisi_metrike':
                print("> Metric sets values:")
                print("____________________\n")
                for j in range(0,len(i.children)):
                    print(' Metric:',i.children[j])
                    print(' Values:',pSkupMtr[i.children[j]],'\n')

                    # Pripremi df za upis u Eksel
                    for key in pSkupMtr[i.children[j]]:

                        tempType = pSkupMtr[i.children[j]][key]['type'];
                        temp = pSkupMtr[i.children[j]][key]['data'];
                        sign = '+'
                    
                        # proveri znak fje i pretvori objekat u listu, izbaci ga iz liste,
                        # vrati u dict i prekoprija elemente kako bi index krenuo od 0
                        if str(temp[0]) == '"-"' or str(temp[0]) =='-':
                            sign = '-'
                            tempList = list(temp.values())
                            tempList.pop(0)
                            for num in range(0,len(tempList)):
                                tempList[num]= float(tempList[num])
                            tempDict = {}
                            for num in range(0,len(tempList)):
                                tempDict[str(num)] = tempList[num]

                        elif str(temp[0]) == '"+"' or str(temp[0]) =='+':
                            sign = '+'
                            tempList = list(temp.values())
                            tempList.pop(0)
                            for num in range(0,len(tempList)):
                                tempList[num]= float(tempList[num])
                            tempDict = {}
                            for num in range(0,len(tempList)):
                                tempDict[str(num)] = tempList[num]
                        else:
                            tempDict = temp
 
                        excelObject = {'Set':i.children[j][0:],
                                                   'Name': key,
                                                   'Type': '/',
                                                   'Sign': sign,
                                                   'Param v':'/',
                                                   'Param a':'/',
                                                   'Param b':'/',
                                                   'Param c':'/',
                                                   'Param d':'/',
                                                   }
                        if tempType == 'linear':
                            excelObject['Type'] = 'Linear'
                        
                        elif tempType == 'trapezoid':
                            excelObject['Type'] = 'Trapezoidal'
                            
                        elif tempType == 'triangle':
                            excelObject['Type'] = 'Triangular'
                            
                        elif tempType == 'gauss':
                            excelObject['Type'] = 'Gaussian type 1'

                        elif tempType == 'gauss2':
                           excelObject['Type'] = 'Gaussian type 2'
                           
                        elif tempType == 'sigmoid':
                            excelObject['Type'] = 'Sigmoidal'
                            
                        else:
                            raise ValueError("Unknown metric type for Excel writing")

             
                        for excelKey,iterator in zip(('Param v','Param a','Param b','Param c','Param d'),tempDict):
                            excelObject[excelKey] = float(tempDict[iterator])

##                        for key in tempDict:
##                            excelObject[list(excelObject.keys())[int(key)+4]] = float(tempDict[key])

                        pdPrintMetrics.append(excelObject)
                                             
            # Deo koda zaduzen za pravljenje Eksel izvestaja
            # Kao izlaz dobija se Eskel fajl sa svim podacima
            # Ako je naredba "make report"
            elif i.data == 'pravi_izvestaj':
                try:
                    path = 'reports/'+(i.children[0][0:])[1:-1]+'.xlsx'
                    writer = pd.ExcelWriter(path, engine = 'xlsxwriter')

                    if(len(pdPrintMetrics)!=0):
                        df = pd.DataFrame.from_dict(pdPrintMetrics)
                        df.to_excel(writer, sheet_name = "Assessment metrics")

                    if(len(pdIndividualGrades)!=0):
                        df = pd.DataFrame.from_dict(pdIndividualGrades)
                        df.to_excel(writer, sheet_name = 'Individual grades')

                    if(len(pdCumulativeGrades)!=0):
                        df = pd.DataFrame.from_dict(pdCumulativeGrades)
                        df.to_excel(writer, sheet_name = 'Cumulative grade')

                    if(len(pdComparativeGrades)!=0):
                        df = pd.DataFrame.from_dict(pdComparativeGrades)
                        df.to_excel(writer, sheet_name = 'Comparative grades')
                    
                    writer.save()
                    #writer.close()
                except:
                    raise IOError("> File read/write error. Please try again.")
                
            # Deo koda zaduzen za pojedinacno crtanje oblika Fazi funkcija jedne ili vise metrika iz skupa metrika
            # Kao izlaz dobija se grafik svake navedene metrike iz skupa metrika
            # Ako je naredba "nacrtaj metriku metr1,metr2,...metrn iz Naziv_skupa_metrika"
            # Ovde napominjemo da pre ove naredbe mora da se izvrsi naredba "oceni Naziv_skupa_metrika"
            elif i.data == 'nacrtaj_metriku':
                pMetrikeCrtanje = {}
                pMetrikeKCrtanje = {}
                nazivSkupaMtrCrtanje = ''

                for j in range(0,len(i.children)-1):
                    pMetrikeCrtanje[j] = str(i.children[j]) # Uzmi nazive metrika

                nazivSkupaMtrCrtanje = str(i.children[j+1].children[0]) # Uzmi naziv skupa metrika

                # Smesti sve u skup za crtanje metrika -> {Naziv_skupa_mtr_za_crtanje: {Metr1, Metr2,...Metrn}}
                pMetrikeKCrtanje[nazivSkupaMtrCrtanje] = pMetrikeCrtanje 
                
                # Nacrtaj zeljene metrike iz zeljenog skupa materika, i prikazi njihove ocene na grafiku
                crtajMetrike(nazivSkupaMtrCrtanje,pMetrikeKCrtanje,pFaziSkupMtr,pSkupMtr)
                
            
    # Ako ne prepoznas naredbu
    else:
        raise SyntaxError('> Unknown instruction: %s' % t.data)

# Funkcija koja ubacuje nisku sa unetom sintaksom u citac (parser)
# i zatim izvrsava instrukciju po instrukciju iz drveta
def runn(program): 
    parse_tree = parser.parse(program)
    for inst in parse_tree.children:
        run_instruction(inst)
    
# Funkcija za testiranje gramatike, citaca i ostalih funkcija
def test():
    text = """

assessment "Test"
{    
  metrics Test_1
    {
	trap1 = trapezoid(3,1,6,9,11)
	trap2 = trapezoid("-",4,1,5,10,14)

        sig1 = sigmoid(7.3,6.2,8.4)
        sig2 = sigmoid("-",7.3,6.2,8.4)

        tri1 = triangle(3.45,0,5,10)
        tri2 = triangle("-",3.45,0,5,10)

        gau1 = gauss(3,6,3)
        gau2 = gauss("-",3,6,3)

        gss1 = gauss2(4,6,3,8,3)
        gss2 = gauss2("-",4,6,3,8,3)

        lin1 = (20,60,30)
        lin2 = (50,0,200)
    }
 
  metrics Test_2
  {
        trap1 = trapezoid(1,1,6,9,11)
	trap2 = trapezoid("-",4,1,5,10,14)

        sig1 = sigmoid(7.3,6.2,8.4)
        sig2 = sigmoid("-",7.3,6.2,8.4)

        tri1 = triangle(0,0,5,10)
        tri2 = triangle("+",1.45,0,5,10)

        gau1 = gauss(0,6,3)
        gau2 = gauss("-",3,6,3)

        gss1 = gauss2(0,6,3,8,3)
        gss2 = gauss2("-",0,6,3,8,3)

        lin1 = (50,60,30)
        lin2 = (0,0,200) 
  }

   metrics Test_5
  {
        da1 = sigmoid(2.3,4.2,8.4)
        da2 = sigmoid("-",2.3,6.2,8.4)

        da3 = trapezoid(9.5,1,6,9,11)
	da4 = trapezoid("-",4.5,1,6,9,11) 
  }

   metrics Test_3
   {
        ne1 = (6,20,5)
        ne2 = (158,100,400)
        ne3 = (3.5,1,15)
        ne4 = (166,30,500)
        ne5 = (9.52,30,15) 
   }

   metrics Test_4
   {
        ne15 = (6,20,5)
        ne25 = (158, 100, 400)
        ne35 = (3.5,1,15)
        ne45 = (166,30,500)
        ne55 = (9.52,30,15) 
   }
    #grade cumulative Test_4, Test_3, Test_2;
    
    #grade singular Test_1, Test_2, Test_3;

    #grade E_banka_1;
    #grade cumulative Test_1, Test_3, Test_5;

    #grade Test_5;
    #grade Test_3;
    
    #draw metric ne1, ne2 from Test_3; 

    #grade comparative Test_1, Test_2;

    #print Test_1, Test_2, Test_3;
    #print Test_1;
}

"""
    # Procitaj i izvrsi unetu sintaksu
    runn(text)
