#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Pila:

    def __init__(self):
        self.P = []
        self.cima = -1

    def Push(self, Ele):
        self.cima += 1
        self.P.append(Ele)

    def Pop(self):
        self.cima -= 1
        return self.P.pop()

    def Get(self, Index = -1):
        return self.P[Index]

    def Set(self, Index, Valor):
        if -len(self.P) < Index and Index < len(self.P):
            self.P[Index] = Valor

    def Vacia(self):
        return (self.cima == -1)

    def __str__(self):
        S = str(self.P)