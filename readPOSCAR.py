# Author -- Patrick S. Avery -- 2016

# This is so we can loop through the lower case alphabet...
from string import ascii_lowercase
import crystal

"""
Reads a POSCAR and returns a Crystal object
"""

def readPOSCAR(fileName = str):
  with open(fileName, "r") as f:
    lines = f.readlines()
    title = lines[0]
    scalingFactor = float(lines[1])

    latticeVecs = [[float(lines[2].split()[0]), float(lines[2].split()[1]), float(lines[2].split()[2])], \
                   [float(lines[3].split()[0]), float(lines[3].split()[1]), float(lines[3].split()[2])], \
                   [float(lines[4].split()[0]), float(lines[4].split()[1]), float(lines[4].split()[2])],]

    # If the next line is not an int, assume they are atomic symbols
    symbols = []
    i = 5
    if not lines[5].split()[0].isdigit:
      symbols = lines[5].split()
      i += 1

    numOfEachType = lines[i].split()
    # if symbols never got defined, we will just define them as 'a', 'b', 'c', etc...
    if len(symbols) == 0:
      # Loop through alphabet letters
      for c in ascii_lowercase:
        symbols.append(c)
        if len(symbols) == len(numOfEachType): break

    i += 1

    # Convert them to integers
    numOfEachType = [int(j) for j in numOfEachType]

    cartesian = False
    if lines[i][0] == 'C' or lines[i][0] == 'c' or \
       lines[i][0] == 'K' or lines[i][0] == 'k':
      cartesian = True

    if isinstance(lines[i].split()[0], str):
      i += 1

    atoms = []
    symbolsInd = 0
    # Now iterate over the atom coordinates
    for numAtoms in numOfEachType:
      for j in range(numAtoms):
        vec = crystal.Vector3d(float(lines[i].split()[0]), float(lines[i].split()[1]), float(lines[i].split()[2]))
        atoms.append(crystal.Atom(symbols[symbolsInd], vec))
        i += 1
      symbolsInd += 1

    # Create the crystal object
    crys = crystal.Crystal(title, scalingFactor, latticeVecs, cartesian, atoms)

    return crys
