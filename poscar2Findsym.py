#!/usr/bin/python

import sys
from crystal import *
from createFindsymInputString import *
from readPOSCAR import *
import subprocess

if len(sys.argv) == 1:
  print "Error: please enter the name of the POSCAR to be read after",
  print "the name of this executable.\nTolerance may be entered as an",
  print "argument after the name of the POSCAR\n"
  sys.exit()

tol = 0
if len(sys.argv) == 2:
  print "Tolerance was not specified. Setting the tolerance to 0.001"
  print "You may specify the tolerance after the name of the POSCAR"
  tol = 0.001

if len(sys.argv) > 2:
  tol = float(sys.argv[2])
  print "Tolerance is: ", tol

crys = readPOSCAR(sys.argv[1])

if crys.cartesian:
  print "Error: this program does not yet convert cartesian to fractional!"
  print "Coords need to be fractional for Findsym to work"
  sys.exit()

inputStr = createFindsymInputString(crys, tol)
#print "\n"
#print inputStr

# Open up findsym as a subprocess
process=subprocess.Popen(['/home/patrick/src/findsym/findsym'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
stdoutdata,stderrdata=process.communicate(input=inputStr)

with open("findsym.out", "w") as wf:
  wf.write(stdoutdata)

spgStr = ""
lines = stdoutdata.splitlines()
for line in lines:
  if "Space Group" in line:
    spgStr = line
    break

print stdoutdata

print "Output was printed to 'findsym.out'\n"
print "Tolerance is ", tol
print spgStr
