#!/usr/bin/env python3

import math
import sys
import readPOSCAR

def readElementsFromPOTCAR(filename):
  with open(filename, 'r') as rf:
    lines = rf.readlines()
  elems = []
  for line in lines:
    if 'VRHFIN' in line:
      elems.append(line.split('=')[1].split(':')[0].lstrip().rstrip())
  return elems

def readRWIGSMinRadiiFromPOTCAR(filename):
  with open(filename, 'r') as rf:
    lines = rf.readlines()
  radii = []
  for line in lines:
    if 'RWIGS' in line:
      radii.append(float(line.split('=')[2].split('wigner')[0].lstrip().rstrip()))
  return radii

def readRWIGSFromPOTCAR(filename):
  rwigs = {}

  elems = readElementsFromPOTCAR(filename)
  rwigsMinRadii = readRWIGSMinRadiiFromPOTCAR(filename)

  if len(elems) != len(rwigsMinRadii):
    sys.exit('Error: elems and rwigsMinRadii are not the same length!\n' \
             'Check that you POSCAR and POTCAR match.')

  for i in range(len(elems)):
    rwigs[elems[i]] = rwigsMinRadii[i]

  return rwigs

def sphereVolume(r):
  return 4.0 / 3.0 * math.pi * (r**3)

crystal = readPOSCAR.readPOSCAR("POSCAR")

volume = crystal.getVolume()

print('==============================================================')
print('Volume of the crystal:', volume)

rwigs = readRWIGSFromPOTCAR("POTCAR")

print('RWIGS read from POTCAR:')
for key in rwigs:
  print(' ', key, ':', rwigs[key])

atoms = crystal.getAtoms()

totalAtomVolume = 0.0
for atom in atoms:
  if not atom.symbol in rwigs:
    sys.exit('Error: missing RWIG for atom:' + atom.symbol)
  totalAtomVolume += sphereVolume(rwigs[atom.symbol])

print('Total atom volume is:', totalAtomVolume)

scaleFactor = (volume / totalAtomVolume)**(1./3)

print('RWIGS scaling factor:', scaleFactor)

print('Final RWIGS values:')
for key in rwigs:
  rwigs[key] *= scaleFactor
  print(' ', key, ':', rwigs[key])

print('==============================================================')
