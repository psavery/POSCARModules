#!/usr/bin/env python

import sys

from crystal import *
from readPOSCAR import *

# Find the smallest representation of this vector
def getMinimumImage(v):
  while v.x >   0.5: v.x -= 1.0
  while v.x <= -0.5: v.x += 1.0
  while v.y >   0.5: v.y -= 1.0
  while v.y <= -0.5: v.y += 1.0
  while v.z >   0.5: v.z -= 1.0
  while v.z <= -0.5: v.z += 1.0

# This next function is used for sorting
def getKey(item): return float(item.split()[1])

if (len(sys.argv) != 2):
  print "Please enter the name of a POSCAR as an argument"
  sys.exit()

c = readPOSCAR(sys.argv[1])

atoms = c.atoms
if c.cartesian: c.convertAtomsToFractional()

strings = []

# Loop through every distance combination
for i in range(len(atoms) - 1):
  for j in range(i + 1,len(atoms)):
    # Get distance
    v = atoms[i].pos - atoms[j].pos
    getMinimumImage(v)

    # Convert to Cartesian
    a = Atom('', v)
    c.convertAtomToCartesian(a)
    strings.append(atoms[i].symbol + '(' + str(i) + ')-' + atoms[j].symbol + '(' + str(j) + '): ' + str(a.pos.getNorm()))

# This will sort them by distance
sortedStrings = sorted(strings, key=getKey)

# Print em out!
for string in sortedStrings:
  print string

