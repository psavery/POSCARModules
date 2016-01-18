#!/usr/bin/env python

import sys
import readPOSCAR

if len(sys.argv) != 2:
  print "Error: Please put one argument after the executable:" + \
        " the name of the POSCAR to be read"
  sys.exit()

crystal = readPOSCAR.readPOSCAR(sys.argv[1])

crystal.display()
