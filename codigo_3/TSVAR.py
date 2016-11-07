#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from codigo_3.Cuadrupla import Cuadrupla
#from codigo_3.Codigo3 import Codigo3
from codigo_3.TSS import TSS
from codigo_3.Utils import Utils
from codigo_3.Tupla import Tupla

from DataStream.DataInputStream import DataInputStream
from DataStream.DataOutputStream import DataOutputStream

# Esta class manipula la Tabla de Simbolos de los ID's.
class TSVar:

    # CONSTANTES QUE DEFINEN LOS TIPOS DE LAS VARIABLES
    TIPOINT     = -2
    TIPOBOOLEAN = -3

    # METODOS DE LA CLASS
    MAXIDS = 50

    # Construye una tabla vacia
    def __init__(self):
        self.V = [];
        for i in range(self.MAXIDS + 1):
            self.V.append(None)

        self.n = -1

    # Inicializa la TSVAR.  Es decir, TSVAR=(Vacía).
    def Init(self):
        self.n = -1

    # Devuelve la cantidad de elementos de la tabla.
    def lenght(self):
        return self.n + 1

    # Devuelve la posicion (indice de V[]) donde se encuentra el ID con NombreID.  Si no existe devuelve -1.
    def Existe(self, NombreID):
        NombreID = self.Validar(NombreID)
        for i in range(0, self.n + 1):
            if self.V[i].getNombreID() == NombreID:
                return i
        return -1

    # Inserta un nuevo Proc a la TSVAR con C3 vacio (ValorI=ValorF=-1). Devuelve la posición donde esta/fue alojado.
    def addProc(self, NombreID):
        return self.addTupla(NombreID, -1, -1, 0)

    # Inserta una nueva Var con su Tipo  a la TSVAR. Devuelve la posicion donde esta/fue alojada.
    def addVar(self, NombreID, Tipo):
        if self.TipoCorrecto(Tipo):
            return self.addTupla(NombreID, 0, Tipo, 0)
        # Devolver -1 para que el llamante sepa que la Variable no se inserto a la tabla.
        return -1

    # Devuelve true sii la tupla de la posicion Index es un Proc
    def isProc(self, Index):
        return (self.PosValida(Index) and self.V[Index].getValorF() >= -1)

    # Devuelve true sii la tupla de la posicion Index es una Var.
    def isVar(self, Index):
        return (self.PosValida(Index) and self.V[Index].getValorF() < -1)

    # ******** SETTER's & GETTER's de la tupla especificada en la pTS Index ********

    # Actualiza el ValorI de la Tupla Index
    def setValorI(self, Index, ValorI):
        if self.PosValida(Index):
            self.V[Index].setValorI(ValorI)

    # Actualiza el ValorF de la Tupla Index (sii es un Proc).
    def setValorF(self, Index, ValorF):
        if self.isProc(Index):
            self.V[Index].setValorF(ValorF)

    # Actualiza el ValorF de la Tupla Index (sii es una Var).
    def setTipo(self, Index, Tipo):
        if self.isVar(Index) and self.TipoCorrecto(Tipo):
            self.V[Index].setValorF(Tipo)

    # Actualiza el ValorF de la Tupla Index (sii es una Var).
    def setCantTmp(self, Index, CantTmp):
        if self.isProc(Index):
            self.V[Index].setCantTmp(CantTmp)

    # Devuelve la Tupla de la posición Index
    def getTupla(self, Index):
        if self.PosValida(Index):
            return self.V[Index]
        return None

    # Devuelve el nombre del ID alojado en la posicion Index
    def getNombreID(self, Index):
        if self.PosValida(Index):
            return self.V[Index].getNombreID()
        return ""

    # Devuelve el ValorI de la tupla Index
    def getValorI(self, Index):
        if self.PosValida(Index):
            return self.V[Index].getValorI()
        return 0

    # Devuelve el ValorF de la tupla Index
    def getValorF(self, Index):
        if self.PosValida(Index):
            return self.V[Index].getValorF()
        return 0

    # Devuelve el campo CantTmp de la tupla Index
    def getCantTmp(self, Index):
        if self.PosValida(Index):
            return self.V[Index].getCantTmp()
        return 0

    # ****** END Setter's & Getter's de la tupla especificada en la pTS Index ******

    def PosValida(self, Index):
        return (0 <= Index and Index <= self.n)

    # Guarda la TSVAR al Flujo F. Si hubo error al guardar, devuelve false.
    def Save(self, F):
        try:
                # Guardar la Cant. de Tuplas.
            F.write_int(self.lenght())

                # Guardar las Tuplas.
            b = True
            i = 0
            while b and i <= self.n:
                # Guardar Tupla
                b = self.V[i].Save(F)
                i = i + 1

            return b
        except Exception as e:
            return False

    # Lee la TSVAR del Flujo F.
    def Open(self, F):
        try:
                # Leer la Cant. de Tuplas.
            self.n = F.read_int() - 1

                # Leer Tuplas.
            b = True
            i = 0
            while b and i <= self.n:
                if self.V[i] is None:
                    self.V[i] = Tupla()
                # Lee la tupla
                b = self.V[i].Open(F)
                i = i + 1

            return b
        except Exception as e:
            return False

    # *****
    TITLE = ["NombreID", "ValorI", "ValorF", "CantTmp"]

    # Para mostrar la TSVAR usando Print
    def __str__(self):
        if self.lenght() == 0:
            return "(TSVAR Vacia)"

        LF = "\n"
        PADDLEFT = "    "

        FieldNombre = self.FieldLength(0)
        FieldValorI = self.FieldLength(1)
        FieldValorF = self.FieldLength(2)
        FieldCantTmp = self.FieldLength(3)
        Total = FieldNombre + FieldValorI + FieldValorF + FieldCantTmp

        BordeSup = PADDLEFT + " " + Utils.RunLength(self, "_", Total)
        Title    = PADDLEFT + "|" + Utils.FieldCenter(self, self.TITLE[0], FieldNombre) + Utils.FieldCenter(self, self.TITLE[1], FieldValorI) + Utils.FieldCenter(self, self.TITLE[2], FieldValorF) + Utils.FieldCenter(self, self.TITLE[3], FieldCantTmp) + "|"
        BordeInf = PADDLEFT + "+" + Utils.RunLength(self, "-", Total) + "+"

        Result = BordeSup + LF + Title + LF + BordeInf + LF

        for i in range(0, self.n + 1):
            Posicion = Utils.FieldRight(self, "" + str(i), len(PADDLEFT)) + "|"
            Nombre   = Utils.FieldLeft(self, " " + str(self.getElem(i, 0)), FieldNombre)
            ValorI   = Utils.FieldCenter(self, self.getElem(i, 1), FieldValorI)
            ValorF   = Utils.FieldCenter(self, self.getElem(i, 2), FieldValorF)
            CantTmp  = Utils.FieldCenter(self, self.getElem(i, 3), FieldCantTmp) + "|"
            Result = Result + Posicion + Nombre + ValorI + ValorF + CantTmp + LF

        return (Result + BordeInf + LF)

    def FieldLength(self, Col):
        May = len(self.TITLE[Col])
        for i in range(0, self.n + 1):
            Lon = len(self.getElem(i, Col))
            if Lon > May:
                May = Lon

        return (May + 2)

    def getElem(self, Fila, Col):
        if Col == 0:
            return self.V[Fila].getNombreID()
        elif Col == 1:
            return ("" + str(self.V[Fila].getValorI()))
        elif Col == 2:
            if self.isVar(Fila):
                if self.V[Fila].getValorF() == self.TIPOINT:
                    return "TIPOINT"
                else:
                    return "TIPOBOOLEAN"
            return ("" + str(self.V[Fila].getValorF()))

        if self.isVar(Fila):
            return "-"

        return ("" + str(self.V[Fila].getCantTmp()))

    # *****
    # Inserta una nueva tupla, validando NombreID.
    def addTupla(self, NombreID, ValorI, ValorF, CantTmp):
        NombreID = self.Validar(NombreID)

        # Si el NombreID es vacio...
        # ...devolver -1, indicando que la tupla no se inserto.
        if NombreID == "":
            return -1

        Pos = self.Existe(NombreID)
        # El ID ya existe en la TSVAR.
        if Pos != -1:
            self.V[Pos].Make(NombreID, ValorI, ValorF, CantTmp)
            return Pos

        # No hay mas espacio en V[].
        if self.n >= self.MAXIDS:
            return -1

        self.n = self.n + 1
        if self.V[self.n] is None:
            self.V[self.n] = Tupla(NombreID, ValorI, ValorF, CantTmp)
        else:
            self.V[self.n].Make(NombreID, ValorI, ValorF, CantTmp)

        # Devolver la posicion donde fue insertada la nueva tupla.
        return self.n

    # Devuelve true sii el int especificado, corresponde a TIPOBOOLEAN o TIPOINT.
    def TipoCorrecto(self, Tipo):
        return (self.TIPOBOOLEAN <= Tipo and Tipo <= self.TIPOINT)

    # Realiza un semi validacion del NombreID. (Si el usuario de esta class fuese el compilador, esta funcion es innecesaria).
    def Validar(self, NombreID):
        # Eliminar espacios iniciales y finales
        NombreID = NombreID.strip()
        if NombreID[0] == "$":
            NombreID = NombreID.upper()

        return (NombreID.replace(" ", "_"))
