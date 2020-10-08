#######################################################ITL IDE########################################################

import os
import sys
import traceback
import webbrowser

import tkinter
from tkinter.messagebox import *
from tkinter.filedialog import *

import threading
import time

from dsl.language import *

# klasa za preusmeravanje izlaza sa terminala u ITL-ov terminal
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
    
# main ide class
class Itl:
    
    #def threadingColorizer(self):
     #   self.i1 = self.ThreadingColorizer(Itl())
      #  self.i1.run()

    class ThreadingColorizer:
        """ Threading example class
        The run() method will be started and it will run in the background
        until the application exits.
        """

        def __init__(self, itlouter, interval=0.001):
            """ Constructor
            :type interval: int
            :param interval: Check interval, in seconds
            """
            self.itlouter = itlouter
            self.interval = interval

            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution
            
            # TODO: move this to a custom text class
            self.itlouter._Itl__thisTextArea['bg'] = "#2b2b2b"
            self.itlouter._Itl__thisTextArea['fg'] = "#a9b7c6"
            self.itlouter._Itl__thisTextArea['insertbackground']='#a9b7c6'
            self.itlouter._Itl__thisTextArea['undo']=True
            self.itlouter._Itl__thisTextArea['maxundo']=-1
            self.itlouter._Itl__thisTextArea['autoseparators']=True
            self.itlouter._Itl__thisTextArea['font']=("Consolas", 12)
            self.itlouter._Itl__thisTextArea['selectbackground']="DeepSkyBlue4"
            self.itlouter._Itl__thisTextArea['inactiveselectbackground']="gray45"
          
        
            
        def run(self):
            #print("Colorizer thread strated...")
            """ Method that runs forever """
            while True:
                self.itlouter._Itl__thisTextArea.highlight_pattern('#[^\\n]*',"gray") #komentar
                self.itlouter._Itl__thisTextArea.highlight_pattern(r"(?:^|\W)trapezoid|triangle|gauss|gauss2|sigmoid(?:$|\W)","purple")
                self.itlouter._Itl__thisTextArea.highlight_pattern(r"(?:^|\W)cumulative|comparative|singular|excelreport|from(?:$|\W)","blue")
                self.itlouter._Itl__thisTextArea.highlight_pattern(r'"[^"\\\n]*(\\.[^"\\\n]*)*"?',"green") #string
                self.itlouter._Itl__thisTextArea.highlight_pattern(r"(?:^|\W)assessment|grade|print|make|draw|metric(?:$|\W)","orange")
                self.itlouter._Itl__thisTextArea.highlight_pattern('\\mmetrics\\M',"lightorange")
                self.itlouter._Itl__thisTextArea.highlight_pattern('[{}]',"yellow")
                
                time.sleep(self.interval)

    
    class CustomText(Text):
        '''Novi tekst vidžet sa metodom, highlight_pattern()

        primer:
        
        text = CustomText()
        text.tag_configure("red", foreground="#ff0000")
        text.highlight_pattern("this should be red", "red")

        '''
        
        def __init__(self, *args, **kwargs):
            Text.__init__(self, *args, **kwargs)
            #Text(__root, undo=True, autoseparators=True, maxundo=-1, font=("Consolas", 11), fg="#a9b7c6", bg="#2b2b2b", insertbackground='#a9b7c6')

        def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=True):
            '''Primeni dati tag na sav tekst koji odgovara datom paternu
            Ako je 'regexp' True, patern ce biti regularni izraz na osnovu Tcl-ove regex sintakse
            '''

            start = self.index(start)
            end = self.index(end)
            self.mark_set("matchStart", start)
            self.mark_set("matchEnd", start)
            self.mark_set("searchLimit", end)

            count = IntVar()
        
            while True:
                index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.mark_set("matchStart", index)
                self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.tag_add(tag, "matchStart", "matchEnd")
                
    __DEBUG = 'false'
    __DESVER = '1.1.1'
    __ITLVER = '1.1.0'
            
    __root = Tk()
    
    # default window width and height 
    __thisWidth = 300
    __thisHeight = 300

    #__thisTextArea = Text(__root, undo=True, autoseparators=True, maxundo=-1, font=("Consolas", 11), fg="#a9b7c6", bg="#2b2b2b", insertbackground='#a9b7c6') # Tekstualno polje
    __thisTextArea = CustomText() # Tekstualno polje
    __thisDebugArea = Text(__root, state=DISABLED, font=("Consolas", 11), bd = 2, bg="#2b2b2b", fg="#A9B7C6", selectbackground="purple") # Polje za otklanjanje gresaka u kodu
    __thisMenuBar = Menu(__root, background="#2b2b2b", foreground="#A9B7C6") 
    __thisFileMenu = Menu(__thisMenuBar,background="#2b2b2b", foreground="#A9B7C6", activeforeground="white", tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar,background="#2b2b2b", foreground="#A9B7C6", activeforeground="white", tearoff=0) 
    __thisHelpMenu = Menu(__thisMenuBar,background="#2b2b2b", foreground="#A9B7C6", activeforeground="white", tearoff=0)
    __thisRun = Menu(__thisMenuBar, tearoff=0)


    # dodaj boje oznaka za greske
    __thisTextArea.tag_config("stderr", foreground="#b22222")
    __thisTextArea.tag_config("error", background="indian red", foreground="old lace")
    
    # dodaj boje oznaka za sitaksu
    __thisTextArea.tag_configure("red", foreground="#AA4926")
    __thisTextArea.tag_configure("green", foreground="#6A8759")
    __thisTextArea.tag_configure("orange", foreground="#CC7832")
    __thisTextArea.tag_configure("lightorange", foreground="#FFBE5E")
    __thisTextArea.tag_configure("purple", foreground="#94558D")
    __thisTextArea.tag_configure("blue", foreground="#6897BB")
    __thisTextArea.tag_configure("magenta", foreground="#B200B2")
    __thisTextArea.tag_configure("gray", foreground="gray")
    __thisTextArea.tag_configure("yellow", foreground="#A8C023")
    
    sys.stdout = TextRedirector(__thisDebugArea, "stdout")
    sys.stderr = TextRedirector(__thisDebugArea, "stderr")

    # Definisemo klizace (scrollbar)
    __thisScrollBar = Scrollbar(__thisTextArea, cursor="arrow", activebackground="cyan",highlightbackground="purple",highlightcolor="green", bg="yellow")
    __thisDebugScrollBar = Scrollbar(__thisDebugArea, cursor="arrow", activebackground="cyan", bg="yellow",troughcolor="green")
    
    __file = None
  
    def __init__(self,**kwargs):

        print("> ITL Development Studio \n--itl-cor@["+self.__ITLVER+"]\n--itl-des@["+self.__DESVER+"]\n")
  
        # Postavljamo ikonu razvojnog okruzenja (ako postoji) 
        try: 
                self.__root.wm_iconbitmap("logo.ico")  
        except: 
                pass # Ako ne postoji, nastavi dalje
  
        # Podesi velicinu prozora (prepodeseno da bude 700x600) 
  
        try: 
            self.__thisWidth = kwargs['width'] 
        except KeyError: 
            pass
  
        try: 
            self.__thisHeight = kwargs['height'] 
        except KeyError: 
            pass
  
        # Podesi naslov prozora 
        self.__root.title("Untitled - ITL Development Studio") 
  
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
 
        # Dodaj u meni komandu za otvaranje mrezne dokumentacije 
        self.__thisHelpMenu.add_command(label="Online help",
                                        accelerator="F1",
                                        command=self.__onlineDoc)  
        
        # Dodaj u meni komandu za ispis podataka o razvojnom okruzenju 
        self.__thisHelpMenu.add_command(label="About", 
                                        command=self.__showAbout)  
        # Dodaj u meni kaskadni meni Pomoc
        self.__thisMenuBar.add_cascade(label="Help", 
                                       menu=self.__thisHelpMenu) 

        # Dodavanje komande u meniju za izvrsavanje unete sintakse ITL jezika
        #self.labelRun = Label( self.__root,bg="green", text="▶", width=100, height=100)
        self.__thisMenuBar.add_command(label="▶", 
                                        command=self.__runFile,
                                        )
        # Dodavanje komande u meniju za undo
        self.__thisMenuBar.add_command(label="↩", 
                                        command=self.__undo,
                                        )
        
        # Dodavanje komande u meniju za redo
        self.__thisMenuBar.add_command(label="↪", 
                                        command=self.__redo,
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
      
        self.__thisTextArea.insert(END,
"""assessment \"New\" {
    
    # Define your metrics set here
    metrics metric_set_name {
        # Define metrics in the following pattern:
        # metric_name = function(sign,v,a,b,c,d) or
        # metric_name = (v,a,b,c)
    }
    
    # Make the assessment and print out the results
    # Instructions: grade, print, ...
    
    # Save the assessment in the Excel file
    make excel report "New Excel Report"
    
    }                                        
"""
                                   )
        self.__thisTextArea.focus_set()
            
    # Funkcija za iskljucenje aplikacije
    def __quitApplication(self): 
        self.__root.destroy() 
        exit() 
  
    # Funckija za otvaranje dokumentacije na internetu
    def __onlineDoc(self,event=None):
        webbrowser.open("https://matejavulic.github.io/",new=1)
    
    # Funkcija za prikaz informacija o razvojnom okruzenju
    def __showAbout(self,event=None): 
        showinfo(title="About",message="ITL Development Studio\nAuthor: Mateja Vulić\nContact: matejavulic@gmail.com\nITL Core Ver: "+self.__ITLVER+"\nITL DS Ver: "+self.__DESVER) 
    
    # Funkcija za otvaranje novog fajla
    def __openFile(self,event=None):  
        self.__file = askopenfilename(defaultextension=".itl", 
                                      filetypes=[("ITL DS report","*.itl"), 
                                        ("Text document","*.txt"),
                                        ("All files","*.*")
                                       ]
                                      ) 
  
        if self.__file == "": 
              
            # Nema fajla za otvaranje
            self.__file = None
        else: 
              
            # Pokusaj da otvoris fajl i podesis naslov prozora 
            self.__root.title(os.path.basename(self.__file) + " - ITL Development Studio") 
            self.__thisTextArea.delete(1.0,END) 
            
            file = open(self.__file,"r") 
  
            # Upisi sadrzaj oblasti teksta u fajl
            self.__thisTextArea.insert(1.0,file.read()) 
            file.close() 
        
    # Funkcija za pravljenje novog fajla
    def __newFile(self,event=None): 
        self.__root.title("Untitled - ITL Development Studio") 
        self.__file = None
        self.__thisTextArea.delete(1.0,END)
        self.__thisTextArea.insert(END, "assessment \"")
        self.__thisTextArea.focus_set()
  
    # Funkcija za cuvanje trenutnog fajla
    def __saveFile(self,event=None): 
  
        if self.__file == None: 
            # Sacuvaj kao novi fajl
            self.__file = asksaveasfilename(initialfile='Untitled.itl', 
                                            defaultextension=".itl", 
                                            filetypes=[("ITL DS report","*.itl"), 
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
                self.__root.title(os.path.basename(self.__file) + " - ITL Development Studio")          
              
        else:
            file = open(self.__file,"w") 
            file.write(self.__thisTextArea.get(1.0,END)) 
            file.close() 

    def __saveFileAs(self,event=None): 
  
        # Otovri dijalog za cuvanje fajla
        self.__file = asksaveasfilename(initialfile='Untitled.itl', 
                                            defaultextension=".itl", 
                                            filetypes=[("ITL DS report","*.itl"), 
                                                ("Text document","*.txt"),
                                                ("All files","*.*")
                                                  ]
                                                ) 
        # Sacuvaj fajl
        file = open(self.__file,"w") 
        file.write(self.__thisTextArea.get(1.0,END)) 
        file.close()

        # Promeni naslov prozora 
        self.__root.title(os.path.basename(self.__file) + " - ITL Development Studio")
        
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
                print("> Instruction error on line "+str(err.line)+". at the position "+str(err.column)+".")
                #Izvlaciti iz err.args sve sto treba sa sve oznacenim kodom
                self.__thisTextArea.tag_add("error", str(err.line)+".0", str(err.line)+".0+1lines")
                
            except lexc.UnexpectedEOF as err:
                print("> Unexpected end of the file. Did you close all brackets?")
                
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
                print("> An error occured. Please check your code.\nTrace:",e)
                if self.__DEBUG == 'true':
                    traceback.print_exc() # naredba za ispis toka greske
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
        
    # Funkcija za iskakanje menija sa osnovnim alatima
    def __doPopup(self, event): 
        try: 
            self.__thisEditMenu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.__thisEditMenu.grab_release()
        
    # Funkcija za pokretanje glavne aplikacije
    def run(self): 
   
        self.__root.bind_all("<F5>",self.__runFile) # Pridruzujemo kolbek funkciju za precicu za komandu Pokreni (F5)
        self.__root.bind_all("<F1>",self.__onlineDoc)# Precica za ucitavanje online pomoci
        self.__root.bind_all("<Control-d>",self.__deleteAll)# Precica za brisanje teksta
        self.__root.bind_all("<Control-n>",self.__newFile)# Precica za nov fajl
        self.__root.bind_all("<Control-o>",self.__openFile)# Precica za otvaranje fajla
        self.__root.bind_all("<Control-s>",self.__saveFile)# Precica za cuvanje fajla
        self.__root.bind_all("<Control-Alt-s>",self.__saveFileAs)# Precica za cuvanje fajla kao...
        self.__root.bind_all("<Button-3>", self.__doPopup)# Aktiviranje pod-menija 
        
        self.__root.mainloop() 

##########################################################Glavna aplikacija##########################################################  
# Pokretanje glavne aplikacije

if __name__ == "__main__":

    # Napravi objekat tipa Itl u 700x500 prozoru
    itl = Itl(width=700,height=500)

    # Pokreni nit
    example = itl.ThreadingColorizer(itl)
        
    # Pokreni aplikaciju
    itl.run()
