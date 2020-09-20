#######################################################ITL IDE########################################################
import tkinter
import os
import sys

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from dsl.language import *

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
  
class Itl: 
  
    __root = Tk() 
  
    # default window width and height 
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root, undo=True, autoseparators=True, maxundo=-1,font=("Consolas", 11)) # Tekstualno polje
    __thisDebugArea = Text(__root, state=DISABLED, bd = 2) # Polje za otklanjanje gresaka u kodu
    __thisMenuBar = Menu(__root) 
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0) 
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0) 
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    __thisRun = Menu(__thisMenuBar, tearoff=0) 

    __thisTextArea.tag_config("stderr", foreground="#b22222")
    __thisTextArea.tag_config("error", background="yellow", foreground="red")
    
    sys.stdout = TextRedirector(__thisDebugArea, "stdout")
    sys.stderr = TextRedirector(__thisDebugArea, "stderr")

    # Definisemo klizace (scrollbar)
    __thisScrollBar = Scrollbar(__thisTextArea)
    __thisDebugScrollBar = Scrollbar(__thisDebugArea)
    
    __file = None
  
    def __init__(self,**kwargs): 
  
        # Postavljamo ikonu razvojnog okruzenja (ako postoji) 
        try: 
                self.__root.wm_iconbitmap("ITL.ico")  
        except: 
                pass # Ako ne postoji, nastavi dalje
  
        # Podesi velicinu prozora (prepodeseno da bude 300x300) 
  
        try: 
            self.__thisWidth = kwargs['width'] 
        except KeyError: 
            pass
  
        try: 
            self.__thisHeight = kwargs['height'] 
        except KeyError: 
            pass
  
        # Podesi naslov prozora 
        self.__root.title("Untitled - ITL") 
  
        # Centriraj prozor 
        screenWidth = self.__root.winfo_screenwidth() 
        screenHeight = self.__root.winfo_screenheight() 
      
        # Alajning levo 
        left = (screenWidth / 2) - (self.__thisWidth / 2)  
          
        # Al. desno 
        top = (screenHeight / 2) - (self.__thisHeight /2)  
          
        # Za vrh i dno 
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, 
                                              self.__thisHeight, 
                                              left, top))  
  
        # Podesi oblast teksta da bude automatski prosiriva 
        self.__root.grid_rowconfigure(0, weight=5)
        self.__root.grid_columnconfigure(0, weight=5)

        self.__root.grid_rowconfigure(1, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
  
        # Dodaj kontrole i oblasti teksta (gore i dole)
        self.__thisTextArea.grid(sticky = N + E + S + W) 
        self.__thisDebugArea.grid(sticky = N + E + S + W)
        
        # Dodaj u meni komandu za otvaranje novog fajla 
        self.__thisFileMenu.add_command(label="New",
                                        accelerator="Ctrl+N",
                                        command=self.__newFile)     
          
        # Dodaj u meni komandu za otvaranje postojeceg fajla 
        self.__thisFileMenu.add_command(label="Open",
                                        accelerator="Ctrl+O",
                                        command=self.__openFile) 

        self.__thisFileMenu.add_separator()
        
        # Dodaj u meni komandu za cuvanje postojeceg fajla
        self.__thisFileMenu.add_command(label="Save",
                                        accelerator="Ctrl+S",
                                        command=self.__saveFile)

        # Dodaj u meni komandu za cuvanje postojeceg fajla kao novog fajla
        self.__thisFileMenu.add_command(label="Save as", 
                                        accelerator="Ctrl+Alt+S",
                                        command=self.__saveFileAs)
        self.__thisFileMenu.add_separator()

        # Dodaj u meni komandu za izvrsavanje unete sintakse JePU jezika 
        self.__thisFileMenu.add_command(label="Run",
                                        accelerator="F5",
                                        command=self.__runFile)
        
        # Napravi liniju razdvajanja u meniju         
        self.__thisFileMenu.add_separator()                                          
        self.__thisFileMenu.add_command(label="Exit", 
                                        accelerator="Alt+F4",
                                        command=self.__quitApplication) 

        #Dodaj u meni komandu za rukovanje fajlom
        self.__thisMenuBar.add_cascade(label="File", 
                                       menu=self.__thisFileMenu)      
          
        # Dodaj u meni komandu za korak nazad
        self.__thisEditMenu.add_command(label="Undo", 
                                        accelerator="Ctrl+Z",
                                        command=self.__undo)
        
        # Dodaj u meni komandu za korak napred
        self.__thisEditMenu.add_command(label="Redo", 
                                        accelerator="Ctrl+Y",
                                        command=self.__redo)

        self.__thisEditMenu.add_separator()
        
        # Dodaj u meni komandu zasecenje teksta
        self.__thisEditMenu.add_command(label="Cut", 
                                        accelerator="Ctrl+X",
                                        command=self.__cut)              
      
        # Dodaj u meni komandu za umnozavanje teksta     
        self.__thisEditMenu.add_command(label="Copy", 
                                        accelerator="Ctrl+C",
                                        command=self.__copy)          
          
        # Dodaj u meni komandu za lepljenje teksta 
        self.__thisEditMenu.add_command(label="Paste", 
                                        accelerator="Ctrl+V",
                                        command=self.__paste)
        
        # Dodaj u meni komandu za lepljenje teksta 
        self.__thisEditMenu.add_command(label="Clear all",
                                        accelerator="Ctrl+D",
                                        command=self.__deleteAll) 
          
        # Dodaj u meni kaskadnog menija za izmenu 
        self.__thisMenuBar.add_cascade(label="Edit", 
                                       menu=self.__thisEditMenu)      
 

        # Dodaj u meni komandu za ispis podataka o razvojnom okruzenju 
        self.__thisHelpMenu.add_command(label="About ITL", 
                                        accelerator="F1",
                                        command=self.__showAbout)  
        # Dodaj u meni kaskadni meni Pomoc
        self.__thisMenuBar.add_cascade(label="Help", 
                                       menu=self.__thisHelpMenu) 

        # Dodavanje komande u meniju za izvrsavanje unete sintakse JePU jezika
        #self.labelRun = Label( self.__root,bg="green", text="▶", width=100, height=100)
        self.__thisMenuBar.add_command(label="▶", 
                                        command=self.__runFile,
                                        )
        
        self.__root.config(menu=self.__thisMenuBar) 
  
        # Postavi klizac na desnu stranu ekrana
        self.__thisScrollBar.pack(side=RIGHT,fill=Y)
        self.__thisDebugScrollBar.pack(side=RIGHT,fill=Y)
          
        # Klizac ce se automatski prilagoditi sadrzaju         
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)      
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
        self.__thisDebugScrollBar.config(command=self.__thisDebugArea.yview)      
        self.__thisDebugArea.config(yscrollcommand=self.__thisDebugScrollBar.set) 
      
        self.__thisTextArea.insert(END, "izvestaj \"New report\"\n{\n #Insert your code here\n ")
        self.__thisTextArea.focus_set()
        
    # Funkcija za iskljucenje aplikacije
    def __quitApplication(self): 
        self.__root.destroy() 
        exit() 
  
    # Funkcija za prikaz informacija o razvojnom okruzenju
    def __showAbout(self,event=None): 
        showinfo("ITL","Improvement Tracking Language\nAuthor: Mateja Vulić\nVer: 1.0") 
  
    # Funkcija za otvaranje novog fajla
    def __openFile(self,event=None):  
        self.__file = askopenfilename(defaultextension=".jepu", 
                                      filetypes=[("ITL report","*.jepu"), 
                                        ("Text document","*.txt"),
                                        ("All files","*.*")
                                       ]
                                      ) 
  
        if self.__file == "": 
              
            # Nema fajla za otvaranje
            self.__file = None
        else: 
              
            # Pokusaj da otvoris fajl i podesis naslov prozora 
            self.__root.title(os.path.basename(self.__file) + " - ITL") 
            self.__thisTextArea.delete(1.0,END) 
            
            file = open(self.__file,"r") 
  
            # Upisi sadrzaj oblasti teksta u fajl
            self.__thisTextArea.insert(1.0,file.read()) 
            file.close() 
        
    # Funkcija za pravljenje novog fajla
    def __newFile(self,event=None): 
        self.__root.title("Untitled - ITL") 
        self.__file = None
        self.__thisTextArea.delete(1.0,END)
        self.__thisTextArea.insert(END, "izvestaj \"New report\"\n{\n #Insert your code here\n ")
        self.__thisTextArea.focus_set()
  
    # Funkcija za cuvanje trenutnog fajla
    def __saveFile(self,event=None): 
  
        if self.__file == None: 
            # Sacuvaj kao novi fajl
            self.__file = asksaveasfilename(initialfile='Untitled.jepu', 
                                            defaultextension=".jepu", 
                                            filetypes=[("ITL report","*.jepu"), 
                                                ("Text document","*.txt"),
                                                ("All files","*.*")
                                             ]
                                            ) 
  
            if self.__file == "": 
                self.__file = None
            else:  
                # Pokusaj da sacuvas fajl
                file = open(self.__file,"w") 
                file.write(self.__thisTextArea.get(1.0,END)) 
                file.close() 
                  
                # Promeni naslov prozora
                self.__root.title(os.path.basename(self.__file) + " - ITL")          
              
        else:
            file = open(self.__file,"w") 
            file.write(self.__thisTextArea.get(1.0,END)) 
            file.close() 

    def __saveFileAs(self,event=None): 
  
        # Otovri dijalog za cuvanje fajla
        self.__file = asksaveasfilename(initialfile='Untitled.jepu', 
                                            defaultextension=".jepu", 
                                            filetypes=[("ITL report","*.jepu"), 
                                                ("Text document","*.txt"),
                                                ("All files","*.*")
                                                  ]
                                                ) 
        # Sacuvaj fajl
        file = open(self.__file,"w") 
        file.write(self.__thisTextArea.get(1.0,END)) 
        file.close()

        # Promeni naslov prozora 
        self.__root.title(os.path.basename(self.__file) + " - ITL")
        
    def pronadji(self,rec,string):
        br=0
        baf = ''
        poz = string.rfind(rec)
        red = 0
        for i in string:
           baf = baf+i;
           if i=="\n":
               br = br + 1
               if baf.find(rec)!=-1:
                   red = br
                   baf = ''
        return str(red)+'.0'

    # Funkcija kojom izvrsavamo uneti ITL kod
    def __runFile(self,event=None): 
        self.__thisTextArea.tag_remove("error",1.0,END)

        if not len(str(self.__thisTextArea.get(1.0,END)))==1:
            try:
                self.__thisDebugArea.config(state=NORMAL) 
                self.__thisDebugArea.delete('1.0', END)
                self.__thisDebugArea.config(state=DISABLED)
                runn(self.__thisTextArea.get(1.0,END))

            except lexc.UnexpectedCharacters as err:
                print("> Instruction error on line "+str(err.line)+". at position "+str(err.column)+".")
                #Izvlaciti iz err.args sve sto treba sa sve oznacenim kodom
                self.__thisTextArea.tag_add("error", str(err.line)+".0", str(err.line)+".0+1lines")
                
            except lexc.UnexpectedEOF as err:
                #print(err)
                print("Unexpected end of file. Did you close all brackets?")
                
            except KeyError as err:
                print("\n> Syntax error:")
                print("> Unknown variable:",err.args[0])
                gre = self.__thisTextArea.get("1.0",END)
                lin = self.pronadji(err.args[0],gre)
                self.__thisTextArea.tag_add("error",str(lin),str(lin)+"+1lines")
                self.__thisDebugArea.config(state=NORMAL) 
                self.__thisDebugArea.see(END)
                self.__thisDebugArea.config(state=DISABLED)    

            except Exception as e:
                print("> Unknown error occured. Please check your code.\nTrace:",e)

            else:
                print("> Code successufully executed.")
        else:
            showinfo("Please try again",
                     "There are no instructions to execute.\nTo execute instruction please load new file or insert instructions in code editor.")
         
    # Funkcija za korak napred (pravljenje dogadjaja) 
    def __undo(self): 
        self.__thisTextArea.event_generate("<<Undo>>")

    # Funkcija za korak nazad (pravljenje dogadjaja) 
    def __redo(self): 
        self.__thisTextArea.event_generate("<<Redo>>")
        
    # Funkcija za secenje teksta (pravljenje dogadjaja) 
    def __cut(self): 
        self.__thisTextArea.event_generate("<<Cut>>") 
  
    # Funkcija za kopiranje teksta (pravljenje dogadjaja) 
    def __copy(self): 
        self.__thisTextArea.event_generate("<<Copy>>") 
  
    # Funkcija za lepljenje teksta (pravljenje dogadjaja) 
    def __paste(self): 
        self.__thisTextArea.event_generate("<<Paste>>") 

    # Funkcija za brisanje celog teksta 
    def __deleteAll(self, event=None): 
        self.__thisTextArea.delete(1.0,END)
        
    # Funkcija za pokretanje glavne aplikacije
    def run(self): 
   
        self.__root.bind_all("<F5>",self.__runFile) # Pridruzujemo kolbek funkciju za precicu za komandu Pokreni (F5)
        self.__root.bind_all("<F1>",self.__showAbout)# Precica za prikaz pomoci
        self.__root.bind_all("<Control-d>",self.__deleteAll)# Precica za brisanje teksta
        self.__root.bind_all("<Control-n>",self.__newFile)# Precica za nov fajl
        self.__root.bind_all("<Control-o>",self.__openFile)# Precica za otvaranje fajla
        self.__root.bind_all("<Control-s>",self.__saveFile)# Precica za cuvanje fajla
        self.__root.bind_all("<Control-Alt-s>",self.__saveFileAs)# Precica za cuvanje fajla kao...
        
        self.__root.mainloop() 

#########################################################Glavna aplikacija##########################################################  
# Pokretanje glavne aplikacije

# Napravi objekat tipa Itl u 600x400 prozoru
itl = Itl(width=600,height=400)

# Pokreni aplikaciju
itl.run()
