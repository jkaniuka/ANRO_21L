#!/usr/bin/env python

# import bibliotek
import json
import math
import PyKDL
import mathutils
import numpy

# odczytanie pliku json 
def readDHfile():
    file = open('Tablica_MD-H.json', 'r')
    values = json.loads(file.read())
    return values


# zapis wartości do pliku
def wrtieYaml(xyz, rpy, mark, a, file, d):
    file.write(mark + ":\n")
    if(mark == "row1"):
        file.write("  j_xyz: "+str(xyz[0])+" "+str(xyz[1])+" "+str(xyz[2]+1)+"\n")
    else:
        file.write("  j_xyz: "+str(xyz[0])+" "+str(xyz[1])+" "+str(xyz[2])+"\n")
    file.write("  j_rpy: "+str(rpy[0])+' '+str(rpy[1])+' '+str(rpy[2])+'\n')
    file.write("  l_xyz: "+str(0)+' '+str(0)+' '+str(float(d)*(-0.5))+'\n')
    file.write("  l_rpy: "+str(0)+' '+str(0)+' '+str(0)+'\n')
    file.write("  l_len: "+str(d)+'\n')

# przeliczenie wartości do yaml
def DH_to_yaml():
    values = readDHfile()
    #otwiera plik do zapisu
    file = open('urdf/urdf_wartosci.yaml', 'w')
    for mark in values.keys():
        a, d, alpha, theta = values[mark]
        a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
        # przekształcenia macierzowe
        translation_z = mathutils.Matrix.Translation((0, 0, d))
        rotation_z = mathutils.Matrix.Rotation(theta, 4, 'Z')
        translation_x = mathutils.Matrix.Translation((a, 0, 0))
        rotation_x =mathutils.Matrix.Rotation(alpha,4,  'X')

        # przemnożenie macierzy
        m = translation_x @ rotation_x @ rotation_z @ translation_z 

        rpy = m.to_euler()
        xyz = m.to_translation()
        # zapis danych
        wrtieYaml(xyz, rpy, mark, a, file, d)

if __name__ == '__main__':
    DH_to_yaml()
