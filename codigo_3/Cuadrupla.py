#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from codigo_3.Codigo3 import Codigo3
from codigo_3.TSVAR import TSVar
from codigo_3.TSS import TSS
from codigo_3.Utils import Utils
from codigo_3.Tupla import Tupla

from DataStream.DataInputStream import DataInputStream
from DataStream.DataOutputStream import DataOutputStream

class Cuadrupla:

    # CONSTANTES PARA EL OpCode (usan el prefijo "OP" de "OPeration").  ¡¡NO MODIFIQUE SUS VALORES!!
    NOP        = 0  # No-Operation.
    OPNL       = 1  # Salto de linea.
    OPRET      = 2  # return.

    OPCALL     = 3  # e.g.CALL Proc
    OPGOTO     = 4  # e.g.GOTO Etiqueta

    OPINC      = 5  # e.g.INC Var
    OPDEC      = 6  # e.g.DEC Var

    OPWRITE    = 7  # e.g.WRITE(VAR)
    OPREAD     = 8  # e.g.READ(Var)
    OPWRITES   = 9  # e.g.WRITES(StringCtte)

    ETIQUETA   = 10 # e.g.E1

    OPNOT      = 11 # ! (not)
    OPAND      = 12 # && e.g.var = var and var
    OPOR       = 13 # ||

    OPSUMA     = 14 # +   e.g.var = var + var
    OPMENOS    = 15 # -
    OPPOR      = 16 # *
    OPDIV      = 17 # DIV(división entera)
    OPMOD      = 18 # MOD

    OPMEN      = 19 # < e.g.var = (var < var)
    OPMAY      = 20 # >
    OPIGUAL    = 21 # ==
    OPDIS      = 22 # != (distinto)
    OPMEI      = 23 # <=
    OPMAI      = 24 # >=

    OPIF0      = 25 # e.g.IF(Var=0) = > GOTO Etiqueta
    OPIF1      = 26 # e.g.IF(Var=1) = > GOTO Etiqueta

    OPASIGNID  = 27 # e.g.Var = Var
    OPASIGNNUM = 28 # e.g.Var = Número

    # METODOS DE LA CLASE
    def __init__(self, TipoOp = NOP, Dir1 = 0, Dir2 = 0, Dir3 = 0):
        self.Dir = [0, 0, 0]
        self.Make(TipoOp, Dir1, Dir2, Dir3)

    # Setter del Codigo de Operacion
    def setOpCode(self, TipoOp):
        self.OpCode = self.Validar(TipoOp)

    # Setter de la Dir de Memoria Index (1<=Index<=3)
    # e.g  C.setDir(1, 2), actualizara la 1era. Dir. de Mem con 2.
    def setDir(self, Index, dir):
        if 1 <= Index and Index <= 3:
            self.Dir[Index - 1] = dir

    # Getter del Codigo de Operacion
    def getOpCode(self):
        return self.OpCode

    # Getter de la Dir de Memoria Index (1<=Index<=3)
    def getDir(self, Index):
        if 1 <= Index and Index <= 3:
            return self.Dir[Index - 1]
        return 0

    def Make(self, OpCode, Dir1, Dir2, Dir3):
        self.OpCode = OpCode
        self.Dir[0] = Dir1
        self.Dir[1] = Dir2
        self.Dir[2] = Dir3

    def Save(self, F):
        try:
            F.write_int(self.OpCode)
            F.write_int(self.getDir(1))
            F.write_int(self.getDir(2))
            F.write_int(self.getDir(3))
            return True
        except Exception as e:
            pass
        return False

    def Open(self, F):
        try:
            self.OpCode = F.read_int()
            self.setDir(1, F.read_int())
            self.setDir(2, F.read_int())
            self.setDir(3, F.read_int())
            return True
        except Exception as e:
            pass
        return False

    DESCONOCIDO = "??"

    def __str__(self, c3):
        TsVar = c3.getTSVar()
        Tss = c3.getTSS()

        Simbolo = self.SimboloOP()
        Dir1 = self.getDir(1)
        Arg = ""

        if self.OPCALL <= self.OpCode and self.OpCode <= self.OPDEC:
            if self.OpCode == self.OPGOTO:
                Arg = self.Etiqueta(Dir1)
            else:
                if self.OpCode == self.OPCALL:
                    Arg = self.getNombreProc(TsVar, Dir1)
                else:
                    Arg = self.getNombreVar(TsVar, Dir1)

            return str(Simbolo) + " " + str(Arg)

        if self.OPWRITE <= self.OpCode and self.OpCode <= self.OPWRITES:
            if self.OpCode == self.OPWRITES:
                Arg = self.getStrCtte(Tss, Dir1)
            else:
                Arg = self.getNombreVar(TsVar, Dir1)

            return str(Simbolo) + "(" + str(Arg) + ")"

        if self.OPAND <= self.OpCode and self.OpCode <= self.OPMOD:
            return self.getNombreVar(TsVar, Dir1) + " = " + self.getNombreVar(TsVar, self.getDir(2)) + " " + Simbolo + " " + self.getNombreVar(TsVar, self.getDir(3))

        if self.OPMEN <= self.OpCode and self.OpCode <= self.OPMAI:
            return str(self.getNombreVar(TsVar, Dir1)) + " = (" + str(self.getNombreVar(TsVar, self.getDir(2))) + " " + Simbolo + " " + str(self.getNombreVar(TsVar, self.getDir(3))) + ")"

        Dir2 = self.getDir(2)

        if self.OpCode == self.ETIQUETA:
            return self.Etiqueta(Dir1) + ":"
        elif self.OpCode == self.OPNOT:
            return self.getNombreVar(TsVar, Dir1) + " = NOT " + self.getNombreVar(TsVar, Dir2)
        elif self.OpCode == self.OPIF0:
            return "IF (" + self.getNombreVar(TsVar, Dir1) + "=0) => GOTO " + self.Etiqueta(Dir2)
        elif self.OpCode == self.OPIF1:
            return "IF (" + self.getNombreVar(TsVar, Dir1) + "=1) => GOTO " + self.Etiqueta(Dir2)
        elif self.OpCode == self.OPASIGNID:
            return str(self.getNombreVar(TsVar, Dir1)) + " = " + str(self.getNombreVar(TsVar, Dir2))
        elif self.OpCode == self.OPASIGNNUM:
            return str(self.getNombreVar(TsVar, Dir1)) + " = " + str(Dir2)

        return Simbolo

    # *****
    # Valida el Tipo de Operacion
    def Validar(self, TipoOp):
        if self.NOP <= TipoOp and TipoOp <= self.OPASIGNNUM:
            return TipoOp
        return self.NOP

    # Devuelve el simbolo o string que caracteriza al Tipo de Operacion de la Cuadrupla.
    def SimboloOP(self):
        Simbolo = ["NOP", "NL", "RET", "CALL", "GOTO", "INC", "DEC", "WRITE", "READ", "WriteS", "E", "NOT", "AND", "OR", "+", "-", "*", "DIV", "MOD", "<", ">", "==", "!=", "<=", ">=", "IF", "IF"]

        if self.NOP <= self.OpCode and self.OpCode <= self.OPIF1:
            return Simbolo[self.OpCode]
        return self.DESCONOCIDO

    def Etiqueta(self, Dir):
        if Dir <= 0:
            return "E " + self.DESCONOCIDO
        return "E" + str(Dir)

    def getNombreVar(self, TsVar, Dir):
        if Dir > 0:
            return "t" + str(Dir)

        Dir = -Dir

        if TsVar is None:
            return "Var" + str(Dir)

        if TsVar.isVar(Dir):
            return TsVar.getNombreID(Dir)

        return self.DESCONOCIDO

    def getNombreProc(self, TsVar, Dir):
        if Dir <= 0:
            Dir = -Dir
            if TsVar is None:
                return "Proc" + str(Dir)

            if TsVar.isProc(Dir):
                return TsVar.getNombreID(Dir)

        return self.DESCONOCIDO

    def getStrCtte(self, Tss, Dir):
        if Dir <= 0:
            Dir = -Dir
            if Tss is None:
                return "Str" + str(Dir)

            if Tss.PosValida(Dir):
                return '"' + str(Tss.getStr(Dir)) + '"'

        return self.DESCONOCIDO