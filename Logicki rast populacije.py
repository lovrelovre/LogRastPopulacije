import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt 
                                
                                
import time

class Aplikacija:  #klasa koja nam crta tockice
    def __init__(self, root):
        self.root = root
        self.root.title("Crtanje točkica")
        self.sirina = self.visina = 600
        self.razmak = 2
        self.canvas = tk.Canvas(root, width=self.sirina, height=self.visina)
        self.canvas.pack()
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        self.canvas.bind("<B1-Motion>", self.pomicanje) #ovo tu je konstruktor klase (kak da se pozove i objasni programu sta je sta)

    def nacrtaj_tockice(self, broj_tockica, i=0):
        if i < broj_tockica:
            x = self.razmak + (i % (self.sirina // self.razmak)) * self.razmak
            y = self.razmak + (i // (self.sirina // self.razmak)) * self.razmak
            self.canvas.create_oval(x, y, x+2, y+2, fill="blue") 
            self.root.after(1, self.nacrtaj_tockice, broj_tockica, i+1)

    def pomicanje(self, event):
        x, y = event.x, event.y
        if 0 <= x <= self.sirina and 0 <= y <= self.visina:
            self.canvas.scan_dragto(x, y, gain=1)
    #do tu sve funkcije same kazu po imenu sta rade tako da mislim da ne treba nesto dodatno objasnjavat

fig = None
canvas = None #moramo inicijalizirat globalne varijable kako bi ih mogli koristit prije neg sta kazemo sta su zapravo


def update_values():
    global fig, canvas #radim ih globalnima da bi on skuzio da to nisu privatne varijable funkcije neg one gore sta smo stavili
    natalitet = int_slider_1.get()  # Dobivanje vrijednosti nataliteta
    mortalitet = int_slider_2.get()  # Dobivanje vrijednosti mortaliteta
    pocetna_populacija = int_slider_3.get()  # Dobivanje pocetne populacije
    vrijeme = int_slider_4.get() # Dobivanje vremena
    rast = (natalitet - mortalitet) / pocetna_populacija # inicijaliziram si tu varijablu da se updatea odma live

    # print("Natalitet:", natalitet)
    # print("Mortalitet:", mortalitet)
    # print("Pocetna populacija:", pocetna_populacija)
    # print("Provedeno vrijeme:", vrijeme)
    # print("Rast:", rast)                                                    ovo sve mi je trebalo da provjerim ak radi al ostavio sam za debugganje tijekom projekta
    populations = [] #buduci da moramo prikazat u odnosu na vrijeme populaciju, trebat cemo listu u koju cemo svake godine spremat trenutnu populaciju
    for i in range(vrijeme):
        trenutna_populacija = pocetna_populacija + pocetna_populacija * rast
        populations.append(trenutna_populacija)
        pocetna_populacija = trenutna_populacija # ovo nema smisla logicki al necemo vise koristit pocetnu populaciju pa cemo 
                                                 # ju sam iskoristit ko placeholder varijablu da mozemo izracunat trenutnu
                                                 # u ovom slucaju nam svaki loop kad prode, pocetna postaje stara trenutna zapravo
    # print("Populacija nakon provedenog vremena: ", trenutna_populacija) isto ko gornji printevi komentar za debug
    if canvas:
        canvas.get_tk_widget().destroy()  # brisem stari graf kad se nes updatea
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(range(len(populations)), populations)
    plot.set_xlabel('Provedene godine pocevsi od 1')
    plot.set_ylabel('Populacija')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Kreira tkinter
root = tk.Tk()
root.title("Stopa rasta populacije")

# stvari za prvi slider
value_label_1 = tk.Label(root, text="Natalitet")
int_slider_1 = tk.Scale(root, from_=10, to=100, orient=tk.HORIZONTAL) #tu mogu mjenjat u ovom from to od kolko do kolko zelim, stavio sam neke realisticne cifre
int_slider_1.pack(pady=5)
value_label_1.pack()

# drugi slider
value_label_2 = tk.Label(root, text="Mortalitet")
int_slider_2 = tk.Scale(root, from_=5, to=15, orient=tk.HORIZONTAL)
int_slider_2.pack(pady=5)
value_label_2.pack()

# treci slider
value_label_3 = tk.Label(root, text="Pocetna populacija")
int_slider_3 = tk.Scale(root, from_= 1, to=50000, orient=tk.HORIZONTAL)
int_slider_3.pack(pady=5) #ovo je vizualno sam da napravi od ostalih slidera razmak malo, tak je za svaki slider ista komanda
value_label_3.pack()

# cetvrti slider
value_label_4 = tk.Label(root, text="Provedeno vrijeme")
int_slider_4 = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL)
int_slider_4.pack(pady=5) 
value_label_4.pack()
    
def simulacija_gumb():
    novi_prozor = tk.Toplevel(root)
    novi_prozor.geometry("400x300")
    natalitet = int_slider_1.get()  # Dobivanje vrijednosti nataliteta
    mortalitet = int_slider_2.get()  # Dobivanje vrijednosti mortaliteta
    pocetna_populacija = int_slider_3.get()  # Dobivanje pocetne populacije
    poc_populacija = pocetna_populacija #spremam si trenutnu vrijednost (pravu pocetnu) jer kasnije u kodu mjenjam pocetnu da formula radi, a treba mi prava pocetna za ispis
    vrijeme = int_slider_4.get() # Dobivanje vremena
    rast = (natalitet - mortalitet) / pocetna_populacija #ovo sad sve ponavljamo ko u updateanju, ali sada uzimamo samo trenutne vrijednosti za simulaciju
    for i in range(vrijeme):
        trenutna_populacija = pocetna_populacija + pocetna_populacija * rast
        pocetna_populacija = trenutna_populacija
    labela = tk.Label(novi_prozor, text="Vizualna reprezentacija broja ljudi nakon ispunjenja parametara:\nPocetna populacija: " + "{:.2f}".format(poc_populacija) + "\nPopulacija nakon " + str(vrijeme) + " godina: " + "{:.2f}".format(trenutna_populacija)) # u naslovu samo stavljam ovaj info o konkretnim brojevima
    labela.pack()
    app = Aplikacija(novi_prozor)
    app.nacrtaj_tockice(pocetna_populacija)

# gumb za simulaciju
gumb = tk.Button(root, text="Simulacija", command=simulacija_gumb)
gumb.pack(pady=10)
gumb.pack()



def update_values_continuous(): #Moramo napravit ovu funkciju koja nam se updatea svakih 100ms tak da mozemo spremit nove vrijednosti u varijable
    update_values()  
    root.after(100, update_values_continuous) #rekurvizna funkcija

update_values_continuous() #pozivam ovu funkciju
# runnam tkinter
root.mainloop()

