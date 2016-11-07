#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Interprete.Pila import Pila
from codigo_3.Codigo3 import Codigo3
from codigo_3.TSS import TSS
from codigo_3.TSVAR import TSVar
from codigo_3.Cuadrupla import Cuadrupla

class Interprete:

    def __init__(self):
        self.c3 = Codigo3()
        self.pila = Pila()
        self.IP = -1

        # Metodo activo que hace referencia a la TSVar
        # Si no se ha abierto se coloca -1
        # Despues siempre tendra una valor positivo
        self.procActivo = -1

    def Open(self, Filename):
        if self.c3.Open(Filename):
            self.tss = self.c3.getTSS()
            self.tsvar = self.c3.getTSVar()

            self.procActivo = self.tsvar.Existe('$MAIN')
            self.IP = self.tsvar.getValorI(self.procActivo)

            self.pila.Push(-1)
            cantTMP = self.tsvar.getCantTmp(self.procActivo)
            for i in range(cantTMP):
                self.pila.Push(0)

    # ******************************

    # Devuelve el indice del procedimiento al cual pertenece la cuadrula
    def getProc(self, lnCuadrupla):
        n = self.tsvar.lenght()
        for i in range(n):
            if self.tsvar.isProc(i):
                ini = self.tsvar.getValorI(i)
                fin = self.tsvar.getValorF(i)
                if ini <= lnCuadrupla and lnCuadrupla <= fin:
                    return i
        return -1

    # Devuelve el indice de la cuadrupla que tiene la etiqueta
    def getDirEtiqueta(self, etiqueta):
        n = self.c3.lenght()
        for i in range(n):
            cuadrupla = self.c3.getCuadrupla(i)
            if cuadrupla.getOpCode() == Cuadrupla.ETIQUETA and cuadrupla.getDir(1) == etiqueta:
                return i
        return -1

    # Modifica el valor de un temporal en la pila del procActivo
    def setTemporalPila(self, Index, Valor):
        cantTMP = self.tsvar.getCantTmp(self.procActivo)
        if cantTMP == 0:
            return
        self.pila.Set(-cantTMP + Index - 1, Valor)

    # Obtiene el valor de un temporal en la pila del procActivo
    def getTemporalPila(self, Index):
        cantTMP = self.tsvar.getCantTmp(self.procActivo)
        if cantTMP == 0:
            return 0
        return self.pila.Get(-cantTMP + Index - 1)

    # Settea a una variable temporal o de la tabla de simbolo
    def setVariable(self, Index, Valor):
        if Index > 0:
            self.setTemporalPila(Index, Valor)
        elif Index < 0:
            self.tsvar.setValorI(-Index, Valor)

    # Obtiene el valor de una variable temporal o de la tabla de simbolo
    def getVariable(self, Index):
        if Index > 0:
            return self.getTemporalPila(Index)
        elif Index < 0:
            return self.tsvar.getValorI(-Index)
        return 0

    # ******************************

    def HayCodigoCargado(self):
        return (self.c3 is not None)

    def Run(self):
        if not(self.HayCodigoCargado()):
            print("Error, no existe codigo cargado")
            return

        if self.procActivo == -1:
            print("Error, no existe el metodo $MAIN")
            return

        while True:
            cuadrupla = self.c3.getCuadrupla(self.IP)
            self.InterpretarCuadrupla(cuadrupla)
            if self.IP == -1:
                print("\nInterpretacion Finalizada")
                return

    # Interpreta la cuadrupla y actualiza el IP
    def InterpretarCuadrupla(self, cuadrupla):
        opCode = cuadrupla.getOpCode()
        if opCode == Cuadrupla.NOP:
            # NOP
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPNL:
            # OPNL
            print("")
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPRET:
            # OPRET
            cantTMP = self.tsvar.getCantTmp(self.procActivo)
            for i in range(cantTMP):
                self.pila.Pop()
            self.IP = self.pila.Pop()
            self.procActivo = self.getProc(self.IP)
            pass
        elif opCode == Cuadrupla.OPCALL:
            # OPCALL
            retorno = self.IP + 1
            self.pila.Push(retorno)
            self.procActivo = -cuadrupla.getDir(1)
            cantTMP = self.tsvar.getCantTmp(self.procActivo)
            for i in range(cantTMP):
                self.pila.Push(0)
            self.IP = self.tsvar.getValorI(self.procActivo)
            pass
        elif opCode == Cuadrupla.OPGOTO:
            # OPGOTO
            etiqueta = cuadrupla.getDir(1)
            self.IP = self.getDirEtiqueta(etiqueta)
            pass
        elif opCode == Cuadrupla.OPINC:
            # OPINC
            variable = cuadrupla.getDir(1)
            valor = self.getVariable(variable)
            self.setVariable(variable, valor + 1)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPDEC:
            #OPDEC
            variable = cuadrupla.getDir(1)
            valor = self.getVariable(variable)
            self.setVariable(variable, valor - 1)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPWRITE:
            # OPWRITE
            variable = cuadrupla.getDir(1)
            valor = self.getVariable(variable)
            print(valor, end='')
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPREAD:
            # OPREAD
            variable = cuadrupla.getDir(1)
            valor = int(input())
            self.setVariable(variable, valor)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPWRITES:
            # OPWRITES
            pos = -cuadrupla.getDir(1)
            s = self.tss.getStr(pos)
            print(s, end="")
            self.IP += 1
            pass
        elif opCode == Cuadrupla.ETIQUETA:
            #ETIQUETA
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPNOT:
            #OPNOT
            destino = cuadrupla.getDir(1)
            fuente = cuadrupla.getDir(2)
            valor = self.getVariable(fuente)
            if valor == 0:
                valor = 1
            else:
                valor = 0
            self.setVariable(destino, valor)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPAND:
            # OPAND
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) == 0 or self.getVariable(fuente2) == 0:
                self.setVariable(destino, 0)
            else:
                self.setVariable(destino, 1)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPOR:
            # OPOR
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) != 0 or self.getVariable(fuente2) != 0:
                self.setVariable(destino, 1)
            else:
                self.setVariable(destino, 0)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPSUMA:
            # OPSUMA
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            suma = self.getVariable(fuente1) + self.getVariable(fuente2)
            self.setVariable(destino, suma)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPMENOS:
            # OPMENOS
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            suma = self.getVariable(fuente1) - self.getVariable(fuente2)
            self.setVariable(destino, suma)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPPOR:
            # OPPOR
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            suma = self.getVariable(fuente1) * self.getVariable(fuente2)
            self.setVariable(destino, suma)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPDIV:
            # OPDIV
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            suma = self.getVariable(fuente1) // self.getVariable(fuente2)
            self.setVariable(destino, suma)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPMOD:
            # OPMOD
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            suma = self.getVariable(fuente1) % self.getVariable(fuente2)
            self.setVariable(destino, suma)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPMEN:
            # OPMEN
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) < self.getVariable(fuente2):
                self.setVariable(destino, 1)
            else:
                self.setVariable(destino, 0)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPMAY:
            # OPMAY
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) > self.getVariable(fuente2):
                self.setVariable(destino, 1)
            else:
                self.setVariable(destino, 0)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPIGUAL:
            # OPIGUAL
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) == self.getVariable(fuente2):
                self.setVariable(destino, 1)
            else:
                self.setVariable(destino, 0)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPDIS:
            # OPDIS
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) != self.getVariable(fuente2):
                self.setVariable(destino, 1)
            else:
                self.setVariable(destino, 0)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPMEI:
            # OPMEI
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) <= self.getVariable(fuente2):
                self.setVariable(destino, 1)
            else:
                self.setVariable(destino, 0)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPMAI:
            # OPMAI
            destino = cuadrupla.getDir(1)
            fuente1 = cuadrupla.getDir(2)
            fuente2 = cuadrupla.getDir(3)
            if self.getVariable(fuente1) >= self.getVariable(fuente2):
                self.setVariable(destino, 1)
            else:
                self.setVariable(destino, 0)
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPIF0:
            # OPIF0
            fuente = cuadrupla.getDir(1)
            destino = cuadrupla.getDir(2)
            if self.getVariable(fuente) == 0:
                self.IP = self.getDirEtiqueta(destino)
            else:
                self.IP += 1
            pass
        elif opCode == Cuadrupla.OPIF1:
            # OPIF1
            fuente = cuadrupla.getDir(1)
            destino = cuadrupla.getDir(2)
            if self.getVariable(fuente) != 0:
                self.IP = self.getDirEtiqueta(destino)
            else:
                self.IP += 1
            pass
        elif opCode == Cuadrupla.OPASIGNID:
            # OPASIGNID
            destino = cuadrupla.getDir(1)
            fuente = cuadrupla.getDir(2)
            self.setVariable(destino, self.getVariable(fuente))
            self.IP += 1
            pass
        elif opCode == Cuadrupla.OPASIGNNUM:
            # OPASIGNNUM
            destino = cuadrupla.getDir(1)
            fuente = cuadrupla.getDir(2)
            self.setVariable(destino, fuente)
            self.IP += 1
            pass

        # Revisar en caso de no tener los RET en las funciones
        proc = self.getProc(self.IP)
        if proc == self.procActivo:
            return
        # Hacer un RET Virtual
        # OPRET
        cantTMP = self.tsvar.getCantTmp(self.procActivo)
        for i in range(cantTMP):
            self.pila.Pop()
        self.IP = self.pila.Pop()
        self.procActivo = self.getProc(self.IP)
        pass