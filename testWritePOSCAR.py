#!/usr/bin/env python3

from crystal import Crystal
from readPOSCAR import readPOSCAR

import sys

if len(sys.argv) != 2:
  sys.exit("Usage: <script> <poscarFile>")

c = readPOSCAR(sys.argv[1])

poscar = c.writePoscar()
print(poscar)
