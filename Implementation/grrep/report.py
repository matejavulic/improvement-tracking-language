import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from tkinter import PhotoImage
# Funkcija za crtanje radarskog grafika

faceColor = 'white' #'012a53'
spines = '#e5ecf600'
fill = '#e5ecf6'
fill2 = '#feb377'
fontAxesColor = '#555555'#'whitesmoke'
fontColor = '#555555' #'whitesmoke'

def nacrtajRadGraf(df, nazivSkupaMtr, nazivIzv):

    # Broj promenljivih
    categories=list(df)[1:]
    N = len(categories)
 
    # Crtamo samo prvi parametar dejta frejma
    # Ponavljamo prvu vrednost kako bismo zatvorili polarni koord. sistem:
    values=df.loc[0].drop('Vrsta').values.flatten().tolist() # Ovde uzimamo samo prvi parametar
    values += values[:1]

    # Vrednosti za opsege ocene kvaliteta parametra
    valuesGreen = 100*np.ones(len(values))
    valuesOrange = 70*np.ones(len(values))
    valuesRed = 40*np.ones(len(values))
 
    # Definisemo uglove za svaku osu (delimo grafik / sa brojem promenljivih)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
 
    # Inicijalizujemo grafik
    fig = plt.figure(figsize=(7, 6), facecolor=faceColor)

    # Definisemo fontove
    font = {'fontname':'Calibri', 'fontsize':16, 'color':fontColor, 'weight':'bold'}
    fontAxes = {'fontname':'Calibri', 'fontsize':12, 'color':fontAxesColor}

    # Inicijalizujemo podgrafik
    ax = plt.subplot(111, polar=True)
    
    # Nacraj jednu osu po promenljivoj i dodaj labele
    plt.xticks(angles[:-1], categories, **fontAxes)

    # Nacrtaj labele
    ax.set_rlabel_position(0)
   
    plt.yticks([10,20,30,40,50,60,70,80,90,100],
               ["10","20","30","40","50","60","70","80","90","100"],
               color="grey", size=7)
    plt.ylim(0,110)
 
    # Nacrtaj podatke
    ax.plot(angles, values, linewidth=1.2, linestyle='solid', color='blue', label= nazivSkupaMtr)

    # Nacrtaj intervale prihvatljivosti
    ax.plot(angles, valuesGreen, linewidth=1.2, linestyle='dashed',alpha=0.8, color='green')
    ax.plot(angles, valuesOrange, linewidth=1.2, linestyle='dashed',alpha=0.5, color='orange')
    ax.plot(angles, valuesRed, linewidth=1.2, linestyle='dashed',alpha=0.4, color='red')

    # Oznaci vrednosti metrika
    oznaciOcene(values,angles,'o')
        
    ax.set_facecolor(faceColor)

    # Popuni oblast
    ax.fill(angles, values, 'b', alpha=0.9, color=fill)

    # Dodaj legendu
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Boja y ose
    ax.spines["polar"].set_color(spines)

    plt.title(nazivIzv, pad='0', **font)

# Funkcija koja pravi dejta frejm od skupa metrika i poziva funkciju za crtanje grafika     
def grafickiPrikaz(pFaziSkupMtr,nazivSkupaMtr, nazivIzv):

    # Napravi dejta frejm
    df = pd.DataFrame({
        'Vrsta': ['Izmereno','Prag','Savrseno'], # Ovde definisemo broj parametara
        }) 

    # Za vrednosti kljuceva iz skupa ocenjenih metrika uzimaj vrednost i postavljaj i prvi parametar dejta frejma
    for key1 in pFaziSkupMtr.keys():
        for key2 in pFaziSkupMtr[key1].keys():
            df[key2] = [pFaziSkupMtr[key1][key2],0,0]   
    nacrtajRadGraf(df,nazivSkupaMtr ,nazivIzv[1:-1]+'\n')

    plt.show(block=False)

# Funkcija koja vizuelno (zelena, zuta, crvena) oznacava kvalitet ocenjenog parametra u odnosu na njegovu vrednost
def oznaciOcene(values,angles,znak):

    for i in range (0,len(values)):
        if values[i]<=40:
            plt.plot(angles[i], values[i], color='black', linestyle='dashed', linewidth = 3, 
                     marker=znak, markerfacecolor='red', markersize=6)
        elif values[i]>40 and values[i]<=70:
            plt.plot(angles[i], values[i], color='black', linestyle='dashed', linewidth = 3, 
                     marker=znak, markerfacecolor='orange', markersize=6)
        elif values[i]>70 and values[i]<=100:
            plt.plot(angles[i], values[i], color='black', linestyle='dashed', linewidth = 3, 
                     marker=znak, markerfacecolor='green', markersize=6)

# Funkcija koja crta dva uporedna radarska grafika
def nacrtajRadGrafUporedno(df,nazivSkupaMtr1,nazivSkupaMtr2,nazivIzv):

    categories=list(df)[1:]
    N = len(categories)
  
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
  
    fig = plt.figure(figsize=(7, 6), facecolor=faceColor)

    font = {'fontname':'Calibri', 'fontsize':16, 'color':fontColor, 'weight':'bold'}
    fontAxes = {'fontname':'Calibri', 'fontsize':12, 'color':fontAxesColor}

    ax = plt.subplot(111, polar=True)
    
    plt.xticks(angles[:-1], categories, **fontAxes)

    ax.set_rlabel_position(0)
   
    plt.yticks([10,20,30,40,50,60,70,80,90,100],
               ["10","20","30","40","50","60","70","80","90","100"],
               color="grey", size=7)
    plt.ylim(0,110)
 
    # Crtanje metrika iz prvog skupa
    values=df.loc[0].drop('Vrsta').values.flatten().tolist() #ovde uzimamo samo prvi parametar
    values += values[:1]
    ax.plot(angles, values, linewidth=1.2, linestyle='solid', color='blue', label= nazivSkupaMtr1)
    ax.fill(angles, values, 'b', alpha=0.9, color=fill)

    # Crtanje metrika iz drugog skupa
    values=df.loc[1].drop('Vrsta').values.flatten().tolist() #ovde uzimamo samo prvi parametar
    values += values[:1]
    ax.plot(angles, values, linewidth=1.2, linestyle='solid', color='red',label= nazivSkupaMtr2)
    ax.fill(angles, values, 'b', alpha=0.9, color=fill2)

    valuesGreen = 100*np.ones(len(values))
    valuesOrange = 70*np.ones(len(values))
    valuesRed = 40*np.ones(len(values))
    
    ax.plot(angles, valuesGreen, linewidth=1.2, linestyle='dashed',alpha=0.8, color='green')
    ax.plot(angles, valuesOrange, linewidth=1.2, linestyle='dashed',alpha=0.5, color='orange')
    ax.plot(angles, valuesRed, linewidth=1.2, linestyle='dashed',alpha=0.4, color='red')

    # Oceni vrednosti metrika
    # Vrednosti loc[1] su vec u memoriji
    oznaciOcene(values,angles,'D')

    # Ucitaj vrednosti loc[0] pa ih oceni
    values=df.loc[0].drop('Vrsta').values.flatten().tolist() #ovde uzimamo samo prvi parametar
    values += values[:1]
    oznaciOcene(values,angles,'o')
    
    ax.set_facecolor(faceColor)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    ax.spines["polar"].set_color(spines)

    plt.title(nazivIzv, pad='0', **font)

# Funkcija koja poziva funkciju za crtanje dva grafa i priprema podatke za nju    
def grafickiPrikazUporedno(pFaziSkupMtr1,pFaziSkupMtr2,nazivSkupaMtr1,nazivSkupaMtr2,nazivIzv):

    df = pd.DataFrame({
        'Vrsta': ['Izmereno','Prag','Savrseno'],
        }) 

    # Popunjavaj prvi i drugi red dejta frejma podacima prvog i drugog parametra
    for key in pFaziSkupMtr1.keys():
            df[key] = [pFaziSkupMtr1[key],pFaziSkupMtr2[key],0]    
    nacrtajRadGrafUporedno(df,nazivSkupaMtr1,nazivSkupaMtr2,nazivIzv[1:-1]+'\n')

    plt.show(block=False)
