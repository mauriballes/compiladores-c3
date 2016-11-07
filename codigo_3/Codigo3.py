#!/usr/bin/python3
# -*- coding: utf-8 -*-

from codigo_3.Cuadrupla import Cuadrupla
from codigo_3.TSVAR import TSVar
from codigo_3.TSS import TSS
from codigo_3.Utils import Utils
from codigo_3.Tupla import Tupla

from DataStream.DataInputStream import DataInputStream
from DataStream.DataOutputStream import DataOutputStream

class Codigo3:

    MAXCUADRUPLAS = 500

    # En la Arq. de un Compilador, se observa la relación del C3 con la TS.
    def __init__(self, TsVar = None, Tss = None):
        self.Make(TsVar, Tss)

    def Make(self, TsVar, Tss):
        self.TsVar = TsVar  # Tabla de símbolos de Variables y Procs.
        self.Tss = Tss      # Tabla de símbolos de StringCtte's

        self.V = []
        for i in range(self.MAXCUADRUPLAS + 1):
            self.V.append(None)

        self.n = -1
        self.CantLbl = 0    # Contador de Etiquetas.

    # Getter de la TSVAR utilizada por el C3.
    def getTSVar(self):
        return self.TsVar

    # Getter de la TSS utilizada por el C3.
    def getTSS(self):
        return self.Tss

    # Setter de la TSVAR utilizada por el C3.
    def setTSVar(self, TsVar):
        self.TsVar = TsVar

    # Setter de la TSS utilizada por el C3.
    def setTSS(self, Tss):
        self.Tss = Tss

    # Devuelve la cantidad de Cuadruplas insertadas en el C3.
    def lenght(self):
        return self.n + 1

    # Inserta la Cuadrupla (TipoOp, Dir1, Dir2, Dir3) devolviendo la posición donde fue insertada.
    def add(self, TipoOp, Dir1 = 0, Dir2 = 0, Dir3 = 0):
        if self.n < self.MAXCUADRUPLAS:
            self.n += 1
            if self.V[self.n] is None:
                self.V[self.n] = Cuadrupla(TipoOp, Dir1, Dir2, Dir3)
            else:
                self.V[self.n].Make(TipoOp, Dir1, Dir2, Dir3)

            return self.n
        return -1 # La Cuadrupla no fue insertada.

    # Inserta la Cuadrupla C al Codigo3, devolviendo la posición donde fue insertada.
    def addCuadrupla(self, C):
        if self.n < self.MAXCUADRUPLAS and C is not None:
            self.n += 1
            self.V[self.n] = C
            return self.n
        return -1 # La cuadrupla no fue insertada.

    # Devuelve la Cuadrupla de la posición Index (0<= Index <=length()-1)
    def getCuadrupla(self, Index):
        if self.IndexCorrecto(Index):
            return self.V[Index]
        return None

    def IndexCorrecto(self, Index):
        return (0 <= Index and Index <= self.n)

    # Guarda el C3, con sus tablas TSVAR y TSS y su CantTemp al archivo Filename. Si hay error, devuelve false.
    def Save(self, Filename):
        Out = self.AbrirEscribir(Filename)

        Msj = "Codigo3.Save: Error al escribir en el archivo " + '"' + Filename + '"'
        try:
            Out.write_int(self.lenght()) # Guardar Cant. de Cuadruplas.

                # Guardar las Cuadruplas.
            b = True
            i = 0
            while (b and i <= self.n):
                b = self.V[i].Save(Out) # Guardar la Cuadrupla V[i].
                i += 1

            # Guardar TSVAR
            if self.TsVar is None:
                Out.write_int(0) # Indicarle al Open que no hay tuplas.
            else:
                b = (b and self.TsVar.Save(Out))

            # Guardar TSS
            if self.Tss is None:
                Out.write_int(0)
            else:
                b = (b and self.Tss.Save(Out))

            Out.close()

            # Hubo error al escribir algunos de los elementos.
            if (not b):
                print(Msj)
                return False
            return True
        except Exception as e:
            print(Msj)
        return False

    def Open(self, Filename):
        In = self.AbrirLeer(Filename)
        if In is None:
            return False
        Msj = "Codigo3.Open: El archivo " + '"' + Filename + '"' + " no tiene el formato de un .c3"
        try:
            self.n = In.read_int() - 1 # Leer Cant. de Cuadruplas.
                # Leer las Cuadruplas.
            b = True
            i = 0
            while (b and i <= self.n):
                if self.V[i] is None:
                    self.V[i] = Cuadrupla()

                b = self.V[i].Open(In) # Leer la Cuadrupla V[i].
                i += 1

            # Leer la TSVAR
            if self.TsVar is None:
                self.TsVar = TSVar()

            b = (b and self.TsVar.Open(In))

            # Leer la TSS
            if self.Tss is None:
                self.Tss = TSS()

            b = (b and self.Tss.Open(In))

            In.close()

            # Hubo error al leer algunos de los elementos.
            if (not b):
                print(Msj)
                return False
            return True
        except Exception as e:
            print(Msj)
        return False

    #***** MANEJO DE LOS TEMPORALES y ETIQUETAS (Usado por el compiler).

    # Devuelve el número de la prox. etiqueta.
    def getNextLabel(self):
        self.CantLbl += 1
        return self.CantLbl

    # Inicializa el contador de temporales.
    def InitTmp(self):
        self.CantTmp = 0

    # Devuelve el número del prox. temporal.
    def getNextTmp(self):
        self.CantTmp += 1
        return self.CantTmp

    # Getter de la cantidad de temporales utilizados.
    def getCantTmp(self):
        return self.CantTmp

    # Setter de la cantidad de temporales utilizados.
    def setCantTmp(self, CantTmp):
        self.CantTmp = CantTmp

    #***** END Manejo de Temporales y Etiquetas.

    # Para usar con Print.
    def __str__(self):
        if self.lenght() == 0:
            return "(Codigo3 Vacio)"

        LF = "\n"
        S = ""
        for i in range(0,self.n + 1):
            S = S + Utils.FieldRight(self, "" + str(i), 3) + " " + self.V[i].__str__(self) + LF

        if(self.Tss is None or self.TsVar is None):
            S += "-------" + LF
            if self.TsVar is None:
                S += "  *Los ID's se muestran sin nombre, porque la TSVAR no fue especificada (o sea vale null)." + LF

            if self.Tss is None:
                S += "  *Las StringCtte's se muestran sin contenido, porque la TSS no fue especificada (o sea vale null)." + LF

        return S

    # Abre, para escribir, el archivo FileName, retornado el flujo abierto.
    def AbrirEscribir(self, Filename):
        try:
            F = open(Filename, 'wb') # Crear archivo (sobreescribiendo si existiese).
            Out = DataOutputStream(F)
            return Out
        except IOError as e:
            print("Codigo3.Save: Error al guardar ")
            print(e)
        return None

    # Abre, para leer, el archivo FileName, retornado el flujo abierto.
    def AbrirLeer(self, Filename):
        try:
            F = open(Filename, 'rb')
            In = DataInputStream(F)
            return In
        except IOError as e:
            print("Codigo3.Open: Error al abrir ")
            print(e)
        return None