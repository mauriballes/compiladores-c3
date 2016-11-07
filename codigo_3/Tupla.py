#!/usr/bin/python3
# -*- coding: utf-8 -*-

from DataStream.DataInputStream import DataInputStream
from DataStream.DataOutputStream import DataOutputStream

# Esta class representa la tupla de la TSVAR.
class Tupla:

    def __init__(self, NombreID = "", ValorI = 0, ValorF = 0, CantTmp = 0):
        self.Make(NombreID, ValorI, ValorF, CantTmp)

    def setNombreID(self, NombreID):
        self.NombreID = NombreID

    def setValorF(self, ValorF):
        self.ValorF = ValorF

    def setValorI(self, ValorI):
        self.ValorI = ValorI

    def setCantTmp(self, CantTmp):
        self.CantTmp = CantTmp

    def getNombreID(self):
        return self.NombreID

    def getValorI(self):
        return self.ValorI

    def getValorF(self):
        return self.ValorF

    def getCantTmp(self):
        return self.CantTmp

    def Make(self, NombreID, ValorI, ValorF, CantTmp):
        self.NombreID = NombreID
        self.ValorI = ValorI
        self.ValorF = ValorF
        self.CantTmp = CantTmp

    # Guarda la tupla al flujo F. Si hay error, return false.
    def Save(self, F):
        try:
            F.write_utf(bytes(self.NombreID, encoding="UTF-8"))
            F.write_int(self.ValorI)
            F.write_int(self.ValorF)
            F.write_int(self.CantTmp)
            return True
        except Exception as e:
            pass
        return False

    # Lee del flujo F, una tupla.
    def Open(self, F):
        try:
            self.NombreID = F.read_utf().decode("utf-8")
            self.ValorI = F.read_int()
            self.ValorF = F.read_int()
            self.CantTmp = F.read_int()
            return True
        except Exception as e:
            pass
        return False