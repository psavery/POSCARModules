# Author -- Patrick S. Avery -- 2016

"""
'crystal' should be a Crystal object
"""

def createFindsymInputString(crystal, tolerance = float):
  inputStr = crystal.title # First line is title
  inputStr += str(tolerance) + "\n" # Second line is tolerance
  inputStr += "1\n" # This line indicates the form that the lattice params will be entered (i. e., vectors vs lengths & angles)
  for i in range(3): # These lines are the lattice vectors being entered
    for j in range(3):
      inputStr += str(crystal.latticeVecs[i][j]) + " "
    inputStr += "\n"
  inputStr += "2\n" # This is the form of the centering to be entered. We're just going to enter "primitive" or "P"
  inputStr += "P\n"
  inputStr += str(crystal.numAtoms()) + "\n" # This is the number of atoms
  positions = []
  for atom in crystal.atoms: # Add atom symbols and store the positions
    inputStr += atom.symbol + " "
    positions.append(atom.pos.getCoordsString(" "))
  inputStr += "\n"
  for pos in positions: # Add the positions
    inputStr += pos + "\n"
  inputStr += "done\n" # Done!
  return inputStr
