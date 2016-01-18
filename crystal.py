
class Vector3d:
  def __init__(self, x = float, y = float, z = float):
    self.x = x
    self.y = y
    self.z = z

  def getCoordsString(self, delim = ","):
    return str(self.x) + delim + str(self.y) + delim + str(self.z)

  def display(self):
    print "(" + self.getCoordsString() + ")"

class Atom:
  def __init__(self, symbol = str, pos = Vector3d):
    self.symbol = symbol
    self.pos = pos

  def display(self):
    print "  For " + self.symbol + ", coords are: ",
    self.pos.display()

class Crystal:
  """
  latticeVecs needs to be a list of list of doubles. Each list needs to be size 3.
  atoms is a list of Atom objects
  """
  def __init__(self, title = str, scalingFactor = float, \
               latticeVecs = [[]], cartesian = bool, atoms = []):
    self.title = title
    self.scalingFactor = scalingFactor
    self.latticeVecs = latticeVecs
    self.cartesian = cartesian
    self.atoms = atoms

  def numAtoms(self):
    return len(self.atoms)

  def displayAtoms(self):
    print "\nThe following are the atom positions in the crystal:"
    for atom in self.atoms:
      atom.display()

  def displayLattice(self):
    print "The lattice is the following:"
    for i in range(3):
      for j in range(3):
        print self.latticeVecs[i][j],
      print "\n",

  def display(self):
    print "\nTitle of the crystal is: ", self.title
    print "Scaling factor is: ", self.scalingFactor
    print "Cartesian is: " , self.cartesian
    self.displayLattice()
    self.displayAtoms()
    print "\n",

