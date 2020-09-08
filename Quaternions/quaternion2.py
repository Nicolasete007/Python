from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def info(): #FINESTRA D'INFORMACIÓ

    ventinfo = Tk()
    ventinfo.geometry('680x600+520+50')
    ventinfo.resizable(width=False,height=False)
    ventinfo.title("Informació")
    ventinfo.config(bg = "dark slate gray")

    Label(ventinfo, text = "  I N F O R M A C I Ó  ", bg = "dark orange", fg = "dark slate gray", font = ("Helvetica", "18", "bold")).place(x = 70, y = 35)

    Label(ventinfo, text = """
    Aquesta és una aplicació creada per calcular i representar gràficament la rotació
    d'un punt  '' p = [X, Y, Z] ''  per un angle  '' Θ ''  sobre un eix  '' e = [X, Y, Z] '';
    mitjançant l'ús de quaternions*, un tipus de nombres hipercomplexos amb unes
    característiques determinades que ens permetrà fer les transmutacions.

    L'eix de rotació del punt es representarà al gràfic amb color blau, i tindrà el seu ori-
    gen a les coordenades [0, 0, 0]. El punt inicial anirà definit pel color verd i el punt
    final pel vermell.

    *Els quaternions són un tipus de nombres amb la forma q = w + xi + yj + zk, que
    tenen una manera especial de ser multiplicats, definida per la fórmula següent:

                                                i ²   =   j ²   =   k ²   =   i j k   =   - 1

    D'aquesta fórmula podem deduir un dels trets més característics dels quaternions:
    no tenen la propietat commutativa a la multiplicació.

    A més, tenim una fòrmula molt simple basada en la multiplicació de quaternions per
    a la rotació de punts en l'espai R³:

                                                            p '   =   q p q '

    On p és el punt a transmutar, representat com un quaternió pur  ( xi, yj, zk ) , q és
    l'eix amb mòdul | q | = 1, representat per un altre quaternió mitjançant la fórmula
    d'Euler per a quaternions, i q ' el quaternió invers de q.
    """, justify = "left", bg = "dark slate gray", fg = "white", font = ("Arial", "11")).place(x = 50, y = 70)

    bsortir = Button(ventinfo, text='SORTIR', command=ventinfo.destroy, width=11, bg="orange", fg="dark slate gray", relief = FLAT, activebackground = "dark orange", activeforeground = "white", font = ("Helvetica", "10", "bold")).place(x = 520, y = 520)

    ventinfo.mainloop()

def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1                                 #   Aquí es defineix la funció de la
    w2, x2, y2, z2 = q2                                 #   multiplicació de quaternions,
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2           #   seguint la norma de:
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2           #
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2           #   i^2 = j^2 = k^2 = ijk = -1
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def transform(eix, angle):
    aX, aY, aZ = eix
    w1 = np.cos(angle/2)
    x1 = aX * np.sin(angle/2)           #   Aquí transformem l'eix
    y1 = aY * np.sin(angle/2)           #   donat en el quaternió q.
    z1 = aZ * np.sin(angle/2)
    return w1, x1, y1, z1

def inv_quat(eix, angle, norma):
    aX, aY, aZ = eix
    x2 = -aX * np.sin(angle/2)/norma**2         #   Aquí definim l'invers
    y2 = -aY * np.sin(angle/2)/norma**2         #   del quaternió:
    z2 = -aZ * np.sin(angle/2)/norma**2         #
    w2 = np.cos(angle/2)/norma**2               #   q' = q^-1
    return w2, x2, y2, z2

def resultat():

    resultat_final = proces()

    resX.delete(0, END) #ESBORRA L'ENTRADA DE RESULTAT X
    resY.delete(0, END) #ESBORRA L'ENTRADA DE RESULTAT Y
    resZ.delete(0, END) #ESBORRA L'ENTRADA DE RESULTAT Z
    resX.insert(0, round(resultat_final[0], 12)) #INSERTA L'ENTRADA DE RESULTAT X
    resY.insert(0, round(resultat_final[1], 12)) #INSERTA L'ENTRADA DE RESULTAT Y
    resZ.insert(0, round(resultat_final[2], 12)) #INSERTA L'ENTRADA DE RESULTAT Z

def proces():

    #AGAFEM LES DADES DE LES ENTRADES
    #####################################
    pX = float(puntX.get())
    pY = float(puntY.get())
    pZ = float(puntZ.get())

    aX = float(eixX.get())
    aY = float(eixY.get())
    aZ = float(eixZ.get())
    #####################################


    #PREPAREM LES DADES PER REALITZAR ELS CÀLCULS
    #(PASSAR TOT A |m| = 1, TRANSFORMAR-HO EN QUATERNIONS, ETC.)
    ############################################################
    modul_eix = np.sqrt(aX**2 + aY**2 + aZ**2)
    modul_punt = np.sqrt(pX**2 + pY**2 + pZ**2)

    eix_unit = aX/modul_eix, aY/modul_eix, aZ/modul_eix
    punt = 0.0, pX, pY, pZ

    if combo.get() == "Graus":
        angle = float(angl.get())*np.pi/180
    elif combo.get() == "π Radians":
        angle = float(angl.get())*np.pi
    else:
        angle = float(angl.get())
    ############################################################


    #REALITZEM TOTS ELS CÀLCULS A PARTIR DE LES FUNCIONS ABANS CREADES
    ###########################################################################################################################
    q = transform(eix_unit, angle)
    a_mitjes = quat_mult(q, punt)                       # Això és r = q * p
    inv_eix = inv_quat(eix_unit, angle, modul_eix)      # Això és q'
    resultat = quat_mult(a_mitjes, inv_eix)             # Per últim calculem p' = r * q'

    modul_final = np.sqrt(resultat[1]**2 + resultat[2]**2 + resultat[3]**2)
    resultat_final = resultat[1]/modul_final*modul_punt, resultat[2]/modul_final*modul_punt, resultat[3]/modul_final*modul_punt

    return resultat_final
    ###########################################################################################################################

def grafic():

    matplotlib.rcParams.update({'font.size': 6})
    plt.clf() #Esborra el gràfic anterior

    #AGAFEM LES DADES DE LES ENTRADES
    #####################################
    resultat_final = proces()

    pX1 = float(puntX.get())
    pY1 = float(puntY.get())
    pZ1 = float(puntZ.get())

    aX1 = float(eixX.get())
    aY1 = float(eixY.get())
    aZ1 = float(eixZ.get())
    #####################################


    #PREPAREM LES DADES PER REALITZAR ELS CÀLCULS
    #(PASSAR TOT A |m| = 1, TRANSFORMAR-HO EN QUATERNIONS, ETC.)
    ############################################################
    modul_eix = np.sqrt(aX1**2 + aY1**2 + aZ1**2)
    modul_punt = np.sqrt(pX1**2 + pY1**2 + pZ1**2)

    pXinicial_grafic = [pX1]  #PUNT INICIAL
    pYinicial_grafic = [pY1]  #PUNT INICIAL
    pZinicial_grafic = [pZ1]  #PUNT INICIAL

    pXfinal_grafic = [resultat_final[0]]  #PUNT FINAL
    pYfinal_grafic = [resultat_final[1]]  #PUNT FINAL
    pZfinal_grafic = [resultat_final[2]]  #PUNT FINAL

    final_eixX = aX1/modul_eix*modul_punt  #EIX
    final_eixY = aY1/modul_eix*modul_punt  #EIX   (ARA TÉ EL MATEIX MÒDUL QUE ELS PUNTS)
    final_eixZ = aZ1/modul_eix*modul_punt  #EIX
    ############################################################


    #CREEM LA REPRESENTACIÓ GRÀFICA
    ##########################################################################################################################
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal', 'box')

    #PUNTS
    ax.scatter(pXinicial_grafic, pYinicial_grafic, pZinicial_grafic, label='Punt inicial', c='g', marker='o') #punt inicial
    ax.scatter(pXfinal_grafic, pYfinal_grafic, pZfinal_grafic, label='Punt rotat', c='r', marker='o')   #punt final

    #EIXOS (VECTORS)
    ax.quiver(0, 0, 0, final_eixX, final_eixY, final_eixZ, label='Eix', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, pXfinal_grafic, pYfinal_grafic, pZfinal_grafic, arrow_length_ratio=0.1, color=['red'])
    ax.quiver(0, 0, 0, pXinicial_grafic, pYinicial_grafic, pZinicial_grafic, arrow_length_ratio=0.1, color=['green'])

    #ETIQUETES DELS EIXOS
    ax.set_xlabel('Eix X')
    ax.set_ylabel('Eix Y')
    ax.set_zlabel('Eix Z')

    #DIMENSIONS DEL GRÀFIC
    minim = min(pX1, resultat_final[0], final_eixX, 0, pY1, resultat_final[1], final_eixY, pZ1, resultat_final[2], final_eixZ)
    maxim = max(pX1, resultat_final[0], final_eixX, 0, pY1, resultat_final[1], final_eixY, pZ1, resultat_final[2], final_eixZ)

    ax.set_xlim(minim, maxim)
    ax.set_ylim(minim, maxim)
    ax.set_zlim(minim, maxim)

    matplotlib.rcParams['legend.fontsize'] = 6
    ax.legend()

    fig.canvas.draw()
    ##########################################################################################################################

#AQUI CREEM LA FINESTRA PRINCIPAL
####################################################

#CONFIGURACIÓ PRINCIPAL
raiz = Tk()
raiz.geometry('1070x600+120+50')
raiz.resizable(width=False,height=False)
raiz.title("Rotació d'un punt qualsevol a l'espai")
raiz.config(bg = "dark slate gray")

#ESPAI PER A LA REPRESENTACIÓ GRÀFICA
fig = plt.figure(dpi=150, figsize=(3, 3.32))
grafico = FigureCanvasTkAgg(fig, master=raiz)
grafico.get_tk_widget().place(x = 560, y = 50)
Label(raiz, text = "R E P R E S E N T A C I Ó  G R À F I C A", bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 556, y = 20)

#IMATGE
imatge = PhotoImage(file="Ejes.png")
Label(raiz, image=imatge).place(x = 50, y = 270)

#BOTONS
####################################################################################################################################################################################################################
bcalcular = Button(raiz, text="CALCULAR", command=resultat, width=25, bg="orange", fg="dark slate gray", relief = FLAT, activebackground = "dark orange", activeforeground = "white", font = ("Helvetica", "10", "bold")).place(x = 300, y = 480)
bgrafic   = Button(raiz, text="GRÀFIC", command=grafic, width=11, bg="orange", fg = "dark slate gray", relief = FLAT, activebackground = "dark orange", activeforeground = "white", font = ("Helvetica", "10", "bold")).place(x = 300, y = 520)
bsortir   = Button(raiz, text='SORTIR', command=raiz.destroy, width=11, bg="orange", fg="dark slate gray", relief = FLAT, activebackground = "dark orange", activeforeground = "white", font = ("Helvetica", "10", "bold")).place(x = 411, y = 520)
binfo     = Button(raiz, text='+ INFO', command=info, width=26, bg="orange", fg="dark slate gray", relief = FLAT, activebackground = "dark orange", activeforeground = "white", font = ("Helvetica", "10", "bold")).place(x = 50, y = 520)
####################################################################################################################################################################################################################

#COMBOBOX
########################################################
combo = ttk.Combobox(raiz, state='readonly', width = 10)
combo.place(x = 424, y = 219)
combo["values"] = ("Graus", "Radians", "π Radians")
combo.current(0)
########################################################

#ENTRADES
###############################################################################
puntX = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
puntY = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
puntZ = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
eixX  = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
eixY  = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
eixZ  = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
angl  = Entry(raiz, bg = "white", width = 8,  justify = "right", relief = FLAT)
resX  = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
resY  = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)
resZ  = Entry(raiz, bg = "white", width = 18, justify = "right", relief = FLAT)

puntX.place(x = 145, y = 130)
puntY.place(x = 145, y = 160)
puntZ.place(x = 145, y = 190)
eixX.place (x = 395, y = 130)
eixY.place (x = 395, y = 160)
eixZ.place (x = 395, y = 190)
angl.place (x = 360, y = 220)
resX.place (x = 370, y = 320)
resY.place (x = 370, y = 350)
resZ.place (x = 370, y = 380)

puntX.insert(0, "0")
puntY.insert(0, "0")
puntZ.insert(0, "0")
eixX.insert(0, "0")
eixY.insert(0, "0")
eixZ.insert(0, "0")
angl.insert(0, "0")
resX.insert(0, "0")
resY.insert(0, "0")
resZ.insert(0, "0")
###############################################################################

#LABELS
#################################################################################################
Label(raiz, text = "  R O T A C I Ó  D E  P U N T S  E N  R ³  ", bg = "dark orange", fg = "dark slate gray", font = ("Helvetica", "18", "bold")).place(x = 50, y = 50)
Label(raiz, text = "S E N T I T      D E L S      E I X O S :", bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 46, y = 245)

Label(raiz, text = "P U N T"      , bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 141, y = 105)
Label(raiz, text = "E I X"        , bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 391, y = 105)

Label(raiz, text = "Coordenada X:", bg = "dark slate gray", fg = "white").place(x = 50 , y = 130)
Label(raiz, text = "Coordenada Y:", bg = "dark slate gray", fg = "white").place(x = 50 , y = 160)
Label(raiz, text = "Coordenada Z:", bg = "dark slate gray", fg = "white").place(x = 50 , y = 190)
Label(raiz, text = "Coordenada X:", bg = "dark slate gray", fg = "white").place(x = 300, y = 130)
Label(raiz, text = "Coordenada Y:", bg = "dark slate gray", fg = "white").place(x = 300, y = 160)
Label(raiz, text = "Coordenada Z:", bg = "dark slate gray", fg = "white").place(x = 300, y = 190)
Label(raiz, text = "Angle Θ:"     , bg = "dark slate gray", fg = "white").place(x = 300 , y = 220)

Label(raiz, text = "Resultat:"    , bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 300, y = 348)
Label(raiz, text = "X"            , bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 492, y = 320)
Label(raiz, text = "Y"            , bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 492, y = 350)
Label(raiz, text = "Z"            , bg = "dark slate gray", fg = "white", font = ("Helvetica", "10", "bold")).place(x = 492, y = 380)
#################################################################################################

raiz.mainloop() #loop
