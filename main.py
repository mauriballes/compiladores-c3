#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from codigo_3.Codigo3 import Codigo3
from codigo_3.TSVAR import TSVar
from codigo_3.TSS import TSS
from codigo_3.Cuadrupla import Cuadrupla

from Interprete.Interprete import Interprete

from tkinter import *

def Mostrar(c3):
    print(c3.getTSVar())
    print(c3.getTSS())
    print(c3)

def GenerarExamen():
    tsvar = TSVar()
    tss = TSS()
    c3 = Codigo3(tsvar, tss)

    tsvar.addProc("$Main")
    tsvar.addVar("x", TSVar.TIPOINT)
    tsvar.addVar("y", TSVar.TIPOINT)
    tss.add("No es Mayor")
    tss.add("Si es Mayor")
    tsvar.setValorI(0, 0)
    tsvar.setValorF(0, 8)
    tsvar.setCantTmp(0, 0)

    c3.add(Cuadrupla.OPREAD, -1)
    c3.add(Cuadrupla.OPREAD, -2)
    c3.add(Cuadrupla.NOP, -1, -2, 1)
    c3.add(Cuadrupla.OPWRITES, 0)
    c3.add(Cuadrupla.OPGOTO, 2)
    c3.add(Cuadrupla.ETIQUETA, 1)
    c3.add(Cuadrupla.OPWRITES, -1)
    c3.add(Cuadrupla.ETIQUETA, 2)
    c3.add(Cuadrupla.OPRET)

    c3.Save("Examen.c3")

def GenerarFactorial():
    tsvar = TSVar()
    tss = TSS()
    c3 = Codigo3(tsvar, tss)

    # Agregando metodos
    tsvar.addProc("Lectura")
    tsvar.addProc("$Main")
    tsvar.addVar("N", TSVar.TIPOINT)
    tsvar.addVar("I", TSVar.TIPOINT)
    tsvar.addVar("F", TSVar.TIPOINT)
    tss.add("Introduzca N:")
    tss.add("Factorial : ")
    tsvar.setValorI(0, 0)
    tsvar.setValorF(0, 6)
    tsvar.setCantTmp(0, 2)
    tsvar.setValorI(1, 7)
    tsvar.setValorF(1, 19)
    tsvar.setCantTmp(1, 1)

    c3.add(Cuadrupla.ETIQUETA, 1)
    c3.add(Cuadrupla.OPWRITES, 0)
    c3.add(Cuadrupla.OPREAD, -2)
    c3.add(Cuadrupla.OPASIGNNUM, 1, 0)
    c3.add(Cuadrupla.OPMAI, 2, -2, 1)
    c3.add(Cuadrupla.OPIF0, 1, 1)
    c3.add(Cuadrupla.OPRET)
    c3.add(Cuadrupla.OPCALL, 0)
    c3.add(Cuadrupla.OPASIGNNUM, -3, 1)
    c3.add(Cuadrupla.OPASIGNNUM, -4, 1)
    c3.add(Cuadrupla.ETIQUETA, 2)
    c3.add(Cuadrupla.OPMEI, 1, -3, -2)
    c3.add(Cuadrupla.OPIF0, 1, 3)
    c3.add(Cuadrupla.OPPOR, -4, -4, -3)
    c3.add(Cuadrupla.OPINC, -3)
    c3.add(Cuadrupla.OPGOTO, 2)
    c3.add(Cuadrupla.ETIQUETA, 3)
    c3.add(Cuadrupla.OPWRITES, -1)
    c3.add(Cuadrupla.OPWRITE, -4)
    c3.add(Cuadrupla.OPRET)

    c3.Save("factorial2.c3");

def GenerarPiramide():
    tsvar = TSVar()
    tss = TSS()
    c3 = Codigo3(tsvar, tss)

    # Agregando metodos
    tsvar.addProc("$Main") # 0
    tsvar.addProc("Lectura") # 1
    tsvar.addProc("Linea") # 2
    tsvar.addProc("Espacio") # 3
    tsvar.addVar("N", TSVar.TIPOINT) # 4
    tsvar.addVar("I", TSVar.TIPOINT) # 5
    tsvar.addVar("J", TSVar.TIPOINT) # 6
    tsvar.addVar("K", TSVar.TIPOINT) # 7
    tss.add("Introduzca N: ")
    tss.add("* ")
    tss.add(" ")
    tsvar.setValorI(0, 17)
    tsvar.setValorF(0, 28)
    tsvar.setCantTmp(0, 1)
    tsvar.setValorI(1, 0)
    tsvar.setValorF(1, 6)
    tsvar.setCantTmp(1, 2)
    tsvar.setValorI(2, 7)
    tsvar.setValorF(2, 16)
    tsvar.setCantTmp(2, 1)
    tsvar.setValorI(3, 29)
    tsvar.setValorF(3, 37)
    tsvar.setCantTmp(3, 2)

    c3.add(Cuadrupla.OPASIGNNUM, 1, 0)
    c3.add(Cuadrupla.ETIQUETA, 1)
    c3.add(Cuadrupla.OPWRITES, 0)
    c3.add(Cuadrupla.OPREAD, -4)
    c3.add(Cuadrupla.OPMEI, 2, -4, 1)
    c3.add(Cuadrupla.OPIF1, 2, 1)
    c3.add(Cuadrupla.OPRET)

    c3.add(Cuadrupla.OPASIGNNUM, -6, 1)
    c3.add(Cuadrupla.ETIQUETA, 2)
    c3.add(Cuadrupla.OPMEI, 1, -6, -7)
    c3.add(Cuadrupla.OPIF0, 1, 3)
    c3.add(Cuadrupla.OPWRITES, -1)
    c3.add(Cuadrupla.OPINC, -6)
    c3.add(Cuadrupla.OPGOTO, 2)
    c3.add(Cuadrupla.ETIQUETA, 3)
    c3.add(Cuadrupla.OPNL)
    c3.add(Cuadrupla.OPRET)

    c3.add(Cuadrupla.OPCALL, -1)
    c3.add(Cuadrupla.OPASIGNNUM, -5, 1)
    c3.add(Cuadrupla.ETIQUETA, 4)
    c3.add(Cuadrupla.OPMEI, 1, -5, -4)
    c3.add(Cuadrupla.OPIF0, 1, 5)
    c3.add(Cuadrupla.OPASIGNID, -7, -5)
    c3.add(Cuadrupla.OPCALL, -3)
    c3.add(Cuadrupla.OPCALL, -2)
    c3.add(Cuadrupla.OPINC, -5)
    c3.add(Cuadrupla.OPGOTO, 4)
    c3.add(Cuadrupla.ETIQUETA, 5)
    c3.add(Cuadrupla.OPRET)

    c3.add(Cuadrupla.OPASIGNID, 1, -4)
    c3.add(Cuadrupla.ETIQUETA, 7)
    c3.add(Cuadrupla.OPMEN, 2, -5, 1)
    c3.add(Cuadrupla.OPIF0, 2, 6)
    c3.add(Cuadrupla.OPWRITES, -2)
    c3.add(Cuadrupla.OPDEC, 1)
    c3.add(Cuadrupla.OPGOTO, 7)
    c3.add(Cuadrupla.ETIQUETA, 6)
    c3.add(Cuadrupla.OPRET)

    c3.Save("triangulo3.c3");

def main(args):
    # c3 = Codigo3()
    # GenerarExamen()
    # c3.Open("Examen.c3")
    # Mostrar(c3)

    interprete = Interprete()
    interprete.Open("triangulo3.c3")
    interprete.Run()

    # root = Tk()
    # frame = Frame(root)
    # frame.pack()
    #
    # bottomframe = Frame(root)
    # bottomframe.pack(side=BOTTOM)
    #
    # redbutton = Button(frame, text="Red", fg="red")
    # redbutton.pack(side=LEFT)
    #
    # greenbutton = Button(frame, text="Brown", fg="brown")
    # greenbutton.pack(side=LEFT)
    #
    # bluebutton = Button(frame, text="Blue", fg="blue")
    # bluebutton.pack(side=LEFT)
    #
    # blackbutton = Button(bottomframe, text="Black", fg="black")
    # blackbutton.pack(side=BOTTOM)
    #
    # root.mainloop()


if __name__ == '__main__':
    main(sys.argv)