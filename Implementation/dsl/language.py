#######################################################Sintaksa JePU########################################################
import numpy as np

from lark import Lark
from lark import exceptions as lexc

from grrep.report import *
from assesm.fuzzy import *

#################Gramatika JePU domenski specificnog programskog jezika###########################

try:
    input = raw_input
except NameError:
    pass

# Definisemo gramatiku jezika prema prosirenoj Bahus-Naurovoj fromi (EBNF) metasintaksnih opisa
grammar = """
    start: instruction+
    
    instruction: "izvestaj" STRING code_block -> pocetak_izvestaja
               | "metrike" NAME "{" dict_item* "}" -> skup_metrika
               | "oceni" NAME ";" -> oceni_metrike
               | "oceni zbirno" NAME ("," NAME)* ";" -> oceni_metrike_z
               | "oceni uporedno" NAME "," NAME";" -> oceni_metrike_u
               | "oceni pojedinacno" NAME ("," NAME)* ";" -> oceni_metrike_p
               | "ispisi" NAME ("," NAME)* ";" -> ispisi_metrike
               | "nacrtaj metriku" NAME ("," NAME)* "iz" set -> nacrtaj_metriku

    code_block: "{" instruction+ "}" -> blok_naredbi
    dict_item: NAME "=" dict_subitem -> naziv_metrike
    dict_subitem: "(" NUMBER "," NUMBER "," NUMBER ")" -> parametri_metrike
    set: NAME ";" -> iz
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

# Glavna funkcija koja izvrsava naredbe JePU jezika
def run_instruction(t):
    pSkupMtr = {}
    pMtr = {}
    pfMtr = {}
    pFaziSkupMtr = {}
    pFaziSkupMtrZ = {}
    pFaziSkupMtrU = {}
    pFaziSkupMtrP = {}
    nazivIzv = ""

    # Sledi deo koda koji procitanu (parsovanu) sintaksu koju
    # je uneo korisnik razlaze iz drveta gramatike (koje je
    # napravio Earley citac (parser) i na osnovu naredbe i
    # njenih parametara poziva odredjenu funkciju
    
    # Ako je koren drveta tj. naredba "izvestaj"
    if t.data == 'pocetak_izvestaja':
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
                        # Prodji kroz sva tri parametra metrike
                        for k in range(0,3):
                            priv[k] = float(j.children[1].children[k]) # Unesi j-tu metriku
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
            # Ako je naredba "oceni Metr1"
            elif i.data == 'oceni_metrike':
                print("Ocena metrike:\n")
                # Inicijalizuj promenljive za racunanje ocene
                br = 0
                ocenaP = 0
                ocenaK = 0
                # Inicijaluzuj recnik u koji smestamo ocenjene metrike u njihovim skupovima metrika
                # {'Skup metrika 1': ocena 1,'Skup metrika 2': ocena 2,...}
                pFaziSkupMtr = {}

                # Izdvoj vrednosti metrika iz trenutnog skupa metrike
                for m in range(0,np.size(i.children)):
                    for key in pSkupMtr[i.children[m]].keys():
                        niz = {}
                        for val in range (0,3):
                            # kada to obavis
                            niz[val] = pSkupMtr[i.children[m]][key][val]
                        # U ako je prvi parametar manji od drugog -> pravi rastucu Fazi funkciju
                        if (niz[1]<=niz[2]):
                            pfMtr[key] = faziRastuci(niz[0],niz[1],niz[2])
                            #Sracunaj trenutnu vrednost ocene za ukupan prosek svih metrika unutar jednog skupa metrika
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1

                        # U suprotnom -> pravi opadajucu Fazi funkciju
                        else:
                            pfMtr[key] = faziOpadajuci(niz[0],niz[1],niz[2])
                            #Sracunaj trenutnu vrednost ocene za ukupan prosek svih metrika unutar jednog skupa metrika
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1
                            
                    # Ubaci skup ocenjenuh metrika u skup svih ocenjenih skupova metrika
                    pFaziSkupMtr[i.children[m][0:]] = pfMtr
                    pfMtr = {}
                    # Oceni trenutni skup metrika (pronadji srednju vrednost ocene)
                    ocenaK = ocenaP/br
                    print('Metrika:',pFaziSkupMtr) #napravljen skup sa svim ocenjenim metrikama
                    print('Ocena:', str(int(round(ocenaK)))+'/100 bodova\n')
                # Spremi podatke za crtanje i posalji ih
                nazivSkupaMtrGrafik = ''
                for key in pFaziSkupMtr:
                    nazivSkupaMtrGrafik = key
                grafickiPrikaz(pFaziSkupMtr, nazivSkupaMtrGrafik, nazivIzv)
               

            # Deo koda zaduzen za zbirno ocenjivanje vise metrika
            # Kao izlaz dobija se prosecna ocena za unete metrike
            # Ako je naredba "oceni zbirno"
            elif i.data == 'oceni_metrike_z':
                print("Zbirne ocene:\n")
                br = 0
                ocenaP = 0
                ocenaK = 0
                pFaziSkupMtrZ = {}
                for m in range(0,np.size(i.children)):
                    for key in pSkupMtr[i.children[m]].keys():
                        niz = {}
                        for val in range (0,3):
                            niz[val] = pSkupMtr[i.children[m]][key][val]
                        if (niz[1]<=niz[2]):
                            pfMtr[key] = faziRastuci(niz[0],niz[1],niz[2])
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1
                        else:
                            pfMtr[key] = faziOpadajuci(niz[0],niz[1],niz[2])
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1
                            
                    pFaziSkupMtrZ[i.children[m][0:]] = pfMtr
                    pfMtr = {}
                    ocenaK = ocenaP/br
                print('Metrika:',pFaziSkupMtrZ) #napravljen skup sa svim ocenjenim metrikama
                print('Ocena:', str(int(round(ocenaK)))+'/100 bodova\n')
                
            # Deo koda zaduzen za uporedno ocenjivanje i prikaz dva skupa metrika sa istim nazivima metrika
            # Kao izlaz dobija se prosecna ocena za dve unete metrike i njihv prikaz na radarskom grafiku
            # Ako je naredba "oceni uporedno"
            elif i.data == 'oceni_metrike_u':
                print("Uporedne ocene:\n")
                br = 0
                ocenaP = 0
                ocenaK = 0
                pFaziSkupMtrU = {}

                for m in range(0,np.size(i.children)):
                    for key in pSkupMtr[i.children[m]].keys():
                        niz = {}
                        for val in range (0,3):
                            niz[val] = pSkupMtr[i.children[m]][key][val]
                        if (niz[1]<=niz[2]):
                            pfMtr[key] = faziRastuci(niz[0],niz[1],niz[2])
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1
                        else:
                            pfMtr[key] = faziOpadajuci(niz[0],niz[1],niz[2])
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1
                            
                    pFaziSkupMtrU[i.children[m][0:]] = pfMtr
                    pfMtr = {}
                    ocenaK = ocenaP/br
                print('Metrika:',pFaziSkupMtrU) #napravljen skup sa svim ocenjenim metrikama
                print('Ocena:', str(int(round(ocenaK)))+'/100 bodova\n')

                # Spremi podatke za crtanje
                nazivSkupaMtrGraf = []
                for key in pFaziSkupMtrU:
                    nazivSkupaMtrGraf.append(key)
               # Pozovi fju za crtenje dva radaska grafika na jednoj slici
                grafickiPrikazUporedno(
                    pFaziSkupMtrU[nazivSkupaMtrGraf[0]],
                    pFaziSkupMtrU[nazivSkupaMtrGraf[1]],
                    nazivSkupaMtrGraf[0],
                    nazivSkupaMtrGraf[1],
                    nazivIzv
                    )

            # Deo koda zaduzen za pojedinacno ocenjivanje vise metrika
            # Kao izlaz dobija pojedinacna se prosecna ocena za unete metrike
            # Ako je naredba "oceni pojedinacno"
            elif i.data == 'oceni_metrike_p':
                print('Pojedinacne ocene:\n')                
                pFaziSkupMtrP = {}
                for m in range(0,np.size(i.children)):
                    br = 0
                    ocenaP = 0
                    ocenaK = 0
                    for key in pSkupMtr[i.children[m]].keys():
                        niz = {}
                        for val in range (0,3):

                            niz[val] = pSkupMtr[i.children[m]][key][val]
                        if (niz[1]<=niz[2]):
                            pfMtr[key] = faziRastuci(niz[0],niz[1],niz[2])
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1
                        else:
                            pfMtr[key] = faziOpadajuci(niz[0],niz[1],niz[2])
                            ocenaP = ocenaP + pfMtr[key]
                            br = br + 1
 
                    pFaziSkupMtrP[i.children[m][0:]] = pfMtr
                    pfMtr = {}
                    ocenaK = ocenaP/br
                    print('Metrika:',pFaziSkupMtrP) # Napravljen skup sa svim ocenjenim metrikama
                    print('Ocena:', str(int(round(ocenaK)))+'/100 bodova\n')
                    pFaziSkupMtrP = {}
            
            # Deo koda zaduzen za ispis unetih parametara jedne ili vise metrika
            # Kao izlaz dobija se spisak metrika sa parametrima
            # Ako je naredba "ispisi"
            elif i.data == 'ispisi_metrike':
                print("Ispis metrika:\n")
                for j in range(0,len(i.children)):
                    print('Metrika:',i.children[j])
                    print('Sadrzaj:',pSkupMtr[i.children[j]],'\n')

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
        raise SyntaxError('Nepoznata naredba: %s' % t.data)

# Funkcija koja ubacuje nisku sa unetom sintaksom u citac (parser)
# i zatim izvrsava instrukciju po instrukciju iz drveta
def runn(program): 
    parse_tree = parser.parse(program)
    for inst in parse_tree.children:
        run_instruction(inst)
    
# Funkcija za testiranje gramatike, citaca i ostalih funkcija
def test():
    text = """

izvestaj "Nedeljni izvestaj - Grupa E-banka"
{    
   
  # Prvo definisemo skupove metrika za sve tri banke
  metrike E_banka_1
    {
        # Deifnisanje metrike Zalbe
	Zalbe = (3,20,5)
        NoveKredKartice = (218, 100, 400)
	ProvedenoVreme = (7.4, 1, 15)
	NovKredit = (305,30,500)
	VremeOdobrenjaKredita = (4.43,30,15) 
        }
 
  metrike E_banka_2
    {
        Zalbe = (1,20,5)
        NoveKredKartice = (295, 100, 400)
	ProvedenoVreme = (4.9, 1, 15)
	NovKredit = (352,30,500)
	VremeOdobrenjaKredita = (8.82,30,15)
        } 
 
  metrike E_banka_3
    {
        Zalbe = (4,20,5)
        NoveKredKartice = (191, 100, 400)
	ProvedenoVreme = (9.5, 1, 15)
	NovKredit = (254,30,500)
	VremeOdobrenjaKredita = (2.52,30,15) 
        }
  
    
    # Prvo zelimo da vidimo ukupnu ocenu sve tri banke
    oceni zbirno E_banka_1,E_banka_2,E_banka_3;
    
    # Nakon toga proveravamo pojedinacnu ocenu svake banke
    oceni pojedinacno E_banka_1, E_banka_2, E_banka_3;
    
    # Vidimo da je treca banka dobila najlosiju ocenu zato detaljnije
    # ispitujemo njen grafik:
    oceni E_banka_3;

   # Banka je ostvarila najlosiji rezultat za metrike Zalbe i 
   # NoveKredKartice. Crtamo ih da bismo ih bolje proucili:
   nacrtaj metriku Zalbe, NoveKredKartice iz E_banka_3; 

   # Na kraju, poredimo uspesnost prve i druge banke:
   oceni uporedno E_banka_1, E_banka_2;

  # Ispis svih unetih metrika vrsimo naredbom:
  ispisi E_banka_1, E_banka_2, E_banka_3;
}

"""
    # Procitaj i izvrsi unetu sintaksu
    runn(text)
    
