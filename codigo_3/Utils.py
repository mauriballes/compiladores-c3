#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Esta class, contiene procedimientos de uso común.

class Utils:

    # Devuelve S con Ancho caracteres (padding derecho con espacios).  (Padding singnifica "relleno").
    def FieldLeft(self, S, Ancho):
        return S + Utils.Espacios(self, Ancho - len(S))

    # Devuelve S con Ancho caracteres (padding izquierdo con espacios).
    def FieldRight(self, S, Ancho):
        return Utils.Espacios(self, Ancho - len(S)) + S

    def FieldCenter(self, S, Ancho):
        if len(S) > Ancho:
            return S[:Ancho - 1]

        Padding = (Ancho - len(S)) // 2

        S = Utils.Espacios(self, Padding) + S

        return S + Utils.Espacios(self, Ancho - len(S))

    def Espacios(self, n):
        BLANK = " "
        return Utils.RunLength(self, BLANK, n)

    def RunLength(self, c, n):
        S = ""
        for i in range(0, n):
            S += c
        return S