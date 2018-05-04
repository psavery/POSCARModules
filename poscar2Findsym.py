#!/usr/bin/env python3

# Author -- Patrick S. Avery -- 2016

import sys
import os
import subprocess

# This needs to be added so we can find the correct modules...
sys.path.append('/projects/academic/ezurek/software/customPythonModules/POSCARModules/')

from crystal import *
from createFindsymInputString import *
from readPOSCAR import *
from spgNumToLatticeSymbol import *

def crystal2Findsym(crys, tolerance):
  crystal = crys
  if crystal.cartesian:
    print("Coords are in cartesian. Converting them to fractional...")
    crystal.convertAtomsToFractional()

  inputStr = createFindsymInputString(crystal, tolerance)
  #print "\n"
  #print inputStr

  # Open up findsym as a subprocess
  process=subprocess.Popen(['/projects/academic/ezurek/software/findsym/findsym'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
  stdoutdata,stderrdata=process.communicate(input=inputStr.encode())
  stdoutdata = stdoutdata.decode()

  lines = stdoutdata.splitlines()

  spgStr = ''
  spgNum = 0
  centering = ''
  numAtomsInCell = 0
  for i, line in enumerate(lines):
    if "Space Group" in line:
      spgStr = line
      spgNum = spgStr.split()[2].strip()
      centering = line.split()[4].strip()[0]

    if '_atom_site_occupancy' in line:
      numAtomsInCell = 0
      for j in range(i + 1, len(lines) - 1):
        numAtomsInCell += int(lines[j].split()[2])

  latticeSymbol = spgNumToLatticeSymbol(int(spgNum))

  # If the centering is 'R', we always end up with 3* the number of atoms
  # for some reason. So reduce it.
  if centering == 'R' and numAtomsInCell % 3 == 0:
    numAtomsInCell /= 3

  pearsonSymbol = latticeSymbol + centering + str(numAtomsInCell)

  return spgNum, spgStr, centering, stdoutdata


if __name__ == '__main__':
  if len(sys.argv) == 1:
    print("Error: please enter the name of the POSCAR to be read after", end=' ')
    print("the name of this executable.\nTolerance may be entered as an", end=' ')
    print("argument after the name of the POSCAR\n")
    sys.exit()

  tol = 0
  if len(sys.argv) == 2:
    print("Tolerance was not specified. Setting the tolerance to 0.001")
    print("You may specify the tolerance after the name of the POSCAR")
    tol = 0.001

  if len(sys.argv) > 2:
    tol = float(sys.argv[2])
    print("Tolerance is: ", tol)

  # Add the ISODATA variable to our path. This is required for findsym to work
  os.environ["ISODATA"]="/projects/academic/ezurek/software/findsym/"

  crys = readPOSCAR(sys.argv[1])

  spgNum, spgStr, pearsonSymbol, stdoutdata = crystal2Findsym(crys, tol)

  print("\n")
  print("******* FINDSYM OUTPUT *******\n")
  print(stdoutdata)
  print("******* END OF FINDSYM OUTPUT *******\n")

  print("Tolerance is", tol, "\n(you may change the tolerance by inputting it after the name of the POSCAR)\n")
  print("Pearson symbol:", pearsonSymbol, '\n')
  print(spgStr, '\n')
  os.system("rm findsym.log")
