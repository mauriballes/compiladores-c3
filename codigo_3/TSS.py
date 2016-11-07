#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from codigo_3.Cuadrupla import Cuadrupla
#from codigo_3.TSVAR import TSVar
#from codigo_3.Codigo3 import Codigo3
from codigo_3.Utils import Utils
from codigo_3.Tupla import Tupla

from DataStream.DataInputStream import DataInputStream
from DataStream.DataOutputStream import DataOutputStream

# Esta class manipula la TS de las String cttes
class TSS:

    def __init__(self):
        self.L = []

    # Inicializa la TSS.  Es decir, TSS=(Vacía).
    def Init(self):
        self.L.clear()

    def length(self):
        return len(self.L)

    # Devuelve la posición (índice de L) donde se encuentra la StringCtte Str.  Si no existe devuelve -1.
    def Existe(self, Str):
        for i in range(0, len(self.L)):
            if self.L[i] == Str:
                return i
        return -1

    # Inserta una nueva StringCtte. Devuelve la posición donde está/fue alojado.  Si no se pudo insertar return -1.
    def add(self, Str):
        pos = self.Existe(Str)
        if pos != -1:
            return pos # La Str ya existe en la TSS.

        self.L.append(Str)
        # La Str fue insertada al final.
        return (len(self.L) - 1)

    def getStr(self, Index):
        if not (self.PosValida(Index)):
            print("TSS.getStr:Posición inválida.")
            return ""
        return self.L[Index]

    def PosValida(self, Index):
        return (0 <= Index and Index <= (len(self.L) - 1))

    # Guarda la TSS al Flujo F. Si hay error, return false.
    def Save(self, F):
        try:
            # Guardar la Cant. de StringCtte's.
            n = self.length()
            F.write_int(n)

            # Guardar los StringCtte's.
            for i in range(0,n):
                F.write_utf(bytes(self.L[i], encoding="UTF-8"))

            return True
        except Exception as e:
            pass

        return  False

    # Lee la TSS del Flujo F.
    def Open(self, F):
        Aux = []
        try:
            # Leer la Cant. de StringCtte's.
            n = F.read_int()

            # Leer los StringCtte's y depositarlas en la lista Aux.
            for i in range(0,n):
                Aux.append(F.read_utf().decode("utf-8"))

            # Copiar lista Aux a L y liberar Aux
            self.L.clear()
            self.L = None
            self.L = self.Clonar(Aux)
            Aux.clear()
            Aux = None

            return True
        except Exception as e:
            pass

        return False

    # *****
    TITLE = "TSS"

    def __str__(self):
        if self.length() == 0:
            return "(" + self.TITLE + " Vacia)"

        LF = "\n"
        PADDLEFT = "    "
        n = self.LongitudFila()

        BordeSup = PADDLEFT + " " + Utils.RunLength(self, "_", n)
        Titulo   = PADDLEFT + "|" + Utils.FieldCenter(self, self.TITLE, n) + "|"
        BordeInf = PADDLEFT + "+" + Utils.RunLength(self, '-', n) + "+"

        Result = BordeSup + LF + Titulo + LF + BordeInf + LF

        FieldPos = len(PADDLEFT)
        for i in range(0, len(self.L)):
            Posicion = Utils.FieldRight(self, "" + str(i), FieldPos)
            Fila     = "|" + Utils.FieldLeft(self, '"' + str(self.L[i]) + '"', n) + "|"
            Result += Posicion + Fila + LF

        return Result + BordeInf + LF

    # Corrutina de print().
    def LongitudFila(self):
        May = len(self.TITLE)
        for i in range(0, len(self.L)):
            LonStr = len(self.L[i])
            if LonStr > May:
                May = LonStr

        # +2 comillas
        return May + 2

    def Clonar(self, L):
        Aux = []
        for i in range(0, len(L)):
            Aux.append(L[i])
        return Aux