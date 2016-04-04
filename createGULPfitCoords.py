#!/usr/bin/env python

# Author -- Patrick Avery -- 2016

# Call this while you are in a directory with VASP output subdirectories
# It reads the OSZICAR, CONTAR, and a charges.txt file (you have to make this
# yourself) and creates an input file for GULP fitting

# charges.txt file is a "<symbol> <charge>" format as such:
# H 0.6
# O -1.2

import os
import sys
sys.path.insert(0, '/home/patrick/src/customPythonModules')
sys.path.insert(0, '/home/patrick/src/customPythonModules/POSCARModules')

import vaspUtil as vu
import readPOSCAR as rp

# First, store the charges in a dictionary
# This just opens up a file that has the charges as such:
# H 0.6
# O -1.2
# You should create this file if you don't have one
charges = {}
filename = "charges.txt"
with open(filename, "r") as f:
  lines = f.readlines()
  for line in lines:
    if line.strip() == '': continue
    symbol = line.split()[0]
    charge = line.split()[1]
    charges[symbol] = charge

for root, dirs, files in os.walk('.'):
  for d in dirs:
    energy = vu.getOszicarFreeEnergy(d + "/OSZICAR")
    coords = '#Begin: ' + d + '\n'

    # c is of type Crystal
    c = rp.readPOSCAR(d + "/CONTCAR")
    if c.cartesian: c.convertAtomsToFractional()

    coords += 'cell\n'
    coords += (str(c.getA()) + '  ')
    coords += (str(c.getB()) + '  ')
    coords += (str(c.getC()) + '  ')
    coords += (str(c.rad2Deg(c.getAlpha())) + '  ')
    coords += (str(c.rad2Deg(c.getBeta())) + '  ')
    coords += (str(c.rad2Deg(c.getGamma())) + '\n')

    numAtoms = c.numAtoms()
    coords += ('fractional  ' + str(numAtoms) + '\n')

    atoms = c.atoms

    for atom in atoms:
      coords += atom.symbol
      coords += '   core  '
      coords += (("%11.8f" % atom.pos.x) + '  ')
      coords += (("%11.8f" % atom.pos.y) + '  ')
      coords += (("%11.8f" % atom.pos.z) + '  ')
      coords += ("%11.8f" % float(charges[atom.symbol]))
      coords += '\n'

    energy = vu.getOszicarFreeEnergy(d + "/OSZICAR")

    coords += '\nobservable\n'
    coords += 'energy ev\n'
    # The 100.0 is a weighting factor. Not sure if it's actually needed...
    coords += (str(energy) + '  100.0\n')
    coords += 'end\n\n'
    print coords
