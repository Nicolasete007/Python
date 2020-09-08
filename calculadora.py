# -*- coding: utf-8 -*-
from tkinter import *
import math, cmath

LIST_NUM  = []
LAST_OP   = ["."]
LAST_OP2  = ["="]
MEM       = [0.0]

############################
#         NUMEROS          #
############################

def one():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 1)

def two():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 2)

def three():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 3)

def four():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 4)

def five():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 5)

def six():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 6)

def seven():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 7)

def eigth():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 8)

def nine():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 9)

def zero():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, 0)

def dot():
    if LAST_OP2[-1] == "=":
        ENTRY.delete(0, END)
        LAST_OP2.append("nothing")
    ENTRY.insert(END, ".")

def pi():
    ENTRY.delete(0, END)
    ENTRY.insert(END, math.pi)

def ac():
    ENTRY.delete(0, END)
    ENTRY.insert(END, 0)

    for i in LAST_OP[:]:
        LAST_OP.pop(len(LAST_OP) -1)

    for j in MEM[:]:
        MEM.pop(len(MEM) -1)

    for k in LIST_NUM[:]:
        LIST_NUM.pop(len(LIST_NUM) -1)

    LAST_OP2.append("=")
    LAST_OP.append(".")
    Label(CALCULATOR, text = "%s %s %s" %("M :  ", 0.0, " " * 1000000), bg = "dark slate gray", fg = "white").place(x = 40, y = 240)

############################
#          NUMEROS         #
############################

#--------------------------#

############################
#         BOOLEANOS        #
############################

#Suma
def add():
    LIST_NUM.append(ENTRY.get())    #---Mete el número en la lista---#
    LAST_OP.append("+")             #----Mete el "+" en la lista-----#
    ENTRY.delete(0, END)            #--------Borra el entry----------#

#Resta
def sub():
    LIST_NUM.append(ENTRY.get())
    LAST_OP.append("-")
    ENTRY.delete(0, END)

#Multiplicación
def prd():
    LIST_NUM.append(ENTRY.get())
    LAST_OP.append("*")
    ENTRY.delete(0, END)

#División
def div():
    LIST_NUM.append(ENTRY.get())
    LAST_OP.append("/")
    ENTRY.delete(0, END)

############################
#         BOOLEANOS        #
############################

#--------------------------#

############################
#     DEMAS  OPERADORES    #
############################

#Porcentaje
def pcnt():
    NUM = ENTRY.get()
    ENTRY.delete(0, END)
    ENTRY.insert(END, float(NUM) / 100)
    LAST_OP2.append("=")

#Elevado al cuadrado
def x2():
    NUM = ENTRY.get()
    ENTRY.delete(0, END)
    ENTRY.insert(END, float(NUM)**2)
    LAST_OP2.append("=")

#1 entre X
def x_1():
    NUM = ENTRY.get()
    ENTRY.delete(0, END)
    ENTRY.insert(END, 1 / float(NUM))
    LAST_OP2.append("=")

#Raíz Cuadrada
def sqrt():
    if float(ENTRY.get()) < 0:
        RESULT = cmath.sqrt(float(ENTRY.get()))
        ENTRY.delete(0, END)
        ENTRY.insert(END, RESULT)
    elif float(ENTRY.get()) >= 0:
        RESULT = math.sqrt(float(ENTRY.get()))
        ENTRY.delete(0, END)
        ENTRY.insert(END, RESULT)

#Negación
def Mm():
    Mm = float(ENTRY.get()) * -1
    ENTRY.delete(0, END)
    ENTRY.insert(END, Mm)

############################
#     DEMAS  OPERADORES    #
############################

#--------------------------#

############################
#          MEMORIA         #
############################

#Memoria
#Suma M
def mem_m():
    MEM.append(MEM[-1] + float(ENTRY.get()))
    Label(CALCULATOR, text = "%s %s %s" %("M :  ", MEM[-1], " " * 10), bg = "dark slate gray", fg = "white").place(x = 40, y = 240)

#Resta M
def mem_l():
    MEM.append(MEM[-1] - float(ENTRY.get()))
    Label(CALCULATOR, text = "%s %s %s" %("M :  ", MEM[-1], " " * 10), bg = "dark slate gray", fg = "white").place(x = 40, y = 240)

#Añade M
def ms():
    MEM.append(float(ENTRY.get()))
    Label(CALCULATOR, text = "%s %s %s" %("M :  ", MEM[-1], " " * 10), bg = "dark slate gray", fg = "white").place(x = 40, y = 240)

#Visualiza M
def mr():
    ENTRY.delete(0, END)
    ENTRY.insert(END, MEM[-1])

#Borra M
def mc():
    for j in MEM[:]:
        MEM.pop(len(MEM) -1)
    MEM.append(0.0)
    Label(CALCULATOR, text = "%s %s %s" %("M :  ", 0.0, " " * 1000000), bg = "dark slate gray", fg = "white").place(x = 40, y = 240)

def delete():
    dele = ENTRY.get()
    if dele != "0":
        ENTRY.delete(0, END)
        new_num = dele[:-1]
        ENTRY.insert(END, new_num)
        if ENTRY.get() == "":
            ENTRY.insert(END, "0")
            LAST_OP2.append("=")

############################
#          MEMORIA         #
############################

#--------------------------#

############################
#         RESULTADO        #
############################

#Resultado
def result():
    #Suma
    if LAST_OP[-1] == "+":
        RESULT = float(LIST_NUM[-1]) + float(ENTRY.get())
        ENTRY.delete(0, END)
        ENTRY.insert(END, RESULT)

    #Resta
    elif LAST_OP[-1] == "-":
        RESULT = float(LIST_NUM[-1]) - float(ENTRY.get())
        ENTRY.delete(0, END)
        ENTRY.insert(END, RESULT)

    #Multiplicación
    elif LAST_OP[-1] == "*":
        RESULT = float(LIST_NUM[-1]) * float(ENTRY.get())
        ENTRY.delete(0, END)
        ENTRY.insert(END, RESULT)

    #División
    elif LAST_OP[-1] == "/":
        RESULT = float(LIST_NUM[-1]) / float(ENTRY.get())
        ENTRY.delete(0, END)
        ENTRY.insert(END, RESULT)

    LAST_OP2.append("=")

############################
#         RESULTADO        #
############################

#--------------------------#

############################
#         VENTANA          #
############################

#Ventana
CALCULATOR = Tk()
CALCULATOR.title("Calculadora")
CALCULATOR.geometry("250x280+420+200")
CALCULATOR.config(bg = "dark slate gray")
CALCULATOR.resizable(FALSE, FALSE)

Label(CALCULATOR, text = "%s %s %s" %("M :  ", MEM[-1], " " * 10), bg = "dark slate gray", fg = "white").place(x = 40, y = 240)

#Entradas
STR = StringVar()
ENTRY = Entry(CALCULATOR, bg = "white", width = 28, justify = "right", relief = FLAT)
ENTRY.place(x = 39, y = 25)
ENTRY.insert(END, 0)

#BOTONES
#Números
BTN_ONE   = Button(text = "1", width = 3, command = one,   bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_TWO   = Button(text = "2", width = 3, command = two,   bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_THREE = Button(text = "3", width = 3, command = three, bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_FOUR  = Button(text = "4", width = 3, command = four,  bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_FIVE  = Button(text = "5", width = 3, command = five,  bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_SIX   = Button(text = "6", width = 3, command = six,   bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_SEVEN = Button(text = "7", width = 3, command = seven, bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_EIGHT = Button(text = "8", width = 3, command = eigth, bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_NINE  = Button(text = "9", width = 3, command = nine,  bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_ZERO  = Button(text = "0", width = 3, command = zero,  bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_DOT   = Button(text = ".", width = 3, command = dot,   bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")
BTN_PI    = Button(text = "π", width = 3, command =   pi,  bg = "dark orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")

#Operadores
BTN_ADD   = Button(text = "+", width = 3, command = add,   bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_SUB   = Button(text = "-", width = 3, command = sub,   bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_PRD   = Button(text = "×", width = 3, command = prd,   bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_DIV   = Button(text = "÷", width = 3, command = div,   bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")

BTN_SQRT  = Button(text = "√", width = 3, command = sqrt,  bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_PCNT  = Button(text = "%", width = 3, command = pcnt,  bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_X2    = Button(text = "x²",width = 3, command = x2,    bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_1X    = Button(text ="1/x",width = 3, command = x_1,   bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")

BTN_AC    = Button(text ="AC", width = 3, command =   ac,  bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_RSLT  = Button(text = "=", width = 3, height = 3, command = result, bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_Mm    = Button(text = "±", width = 3, command =   Mm,  bg = "orange", fg = "white", relief = FLAT, activebackground = "dark orange", activeforeground = "white")

#Memoria
BTN_MEM_M = Button(text ="M+", width = 3, command = mem_m , bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_MEM_L = Button(text ="M-", width = 3, command = mem_l , bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_MS    = Button(text ="MS", width = 3, command = ms    , bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_MR    = Button(text ="MR", width = 3, command = mr    , bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")
BTN_MC    = Button(text ="MC", width = 3, command = mc    , bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")

BTN_DEL   = Button(text ="DEL",width = 3, command = delete, bg = "dark orange", fg = "white", relief = FLAT, activebackground = "DarkOrange2", activeforeground = "white")


BTN_ONE.place(x = 40,  y = 180)
BTN_TWO.place(x = 75,  y = 180)
BTN_THREE.place(x = 110, y = 180)
BTN_FOUR.place(x = 40,  y = 150)
BTN_FIVE.place(x = 75,  y = 150)
BTN_SIX.place(x = 110, y = 150)
BTN_SEVEN.place(x = 40,  y = 120)
BTN_EIGHT.place(x = 75,  y = 120)
BTN_NINE.place(x = 110, y = 120)
BTN_ZERO.place(x = 75,  y = 210)
BTN_DOT.place(x = 110, y = 210)
BTN_PI.place(x = 180, y = 150)
BTN_ADD.place(x = 145, y = 210)
BTN_SUB.place(x = 145, y = 180)
BTN_PRD.place(x = 145, y = 150)
BTN_DIV.place(x = 145, y = 120)

BTN_SQRT.place(x = 180, y = 120)
BTN_PCNT.place(x = 145, y = 90)
BTN_X2.place(x = 110, y = 90)
BTN_1X.place(x = 75, y = 90)

BTN_AC.place(x = 180, y = 60)
BTN_RSLT.place(x = 180, y = 180)
BTN_Mm.place(x = 40, y = 210)
BTN_MEM_M.place(x = 110, y = 60)
BTN_MEM_L.place(x = 145, y = 60)
BTN_MS.place(x = 40, y = 60)
BTN_MR.place(x = 75, y = 60)
BTN_MC.place(x = 40, y = 90)
BTN_DEL.place(x = 180, y = 90)

#Loop
CALCULATOR.mainloop()

############################
#         VENTANA          #
############################
