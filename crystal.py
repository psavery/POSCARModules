# Author -- Patrick S. Avery -- 2016

import math

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

  # We can do 0 for A, 1 for B, or 2 for C
  def getLenOfLatticeVec(self, ind = int):
    return (self.latticeVecs[ind][0]**2 + self.latticeVecs[ind][1]**2 + self.latticeVecs[ind][2]**2)**(0.5)

  # Returns a dot product between two indices that indicate the lattice vectors (0, 1, or 2)
  def getDotProd(self, ind1 = int, ind2 = int):
    return self.scalingFactor**2 * self.latticeVecs[ind1][0] * self.latticeVecs[ind2][0] + \
           self.scalingFactor**2 * self.latticeVecs[ind1][1] * self.latticeVecs[ind2][1] + \
           self.scalingFactor**2 * self.latticeVecs[ind1][2] * self.latticeVecs[ind2][2]

  @staticmethod
  def deg2Rad(num = int):
    return num * math.pi / 180.0

  @staticmethod
  def rad2Deg(num = int):
    return num * 180.0 / math.pi

  # We need to correct these with the scaling factor
  def getA(self):
    return self.scalingFactor * self.getLenOfLatticeVec(0)
  def getB(self):
    return self.scalingFactor * self.getLenOfLatticeVec(1)
  def getC(self):
    return self.scalingFactor * self.getLenOfLatticeVec(2)

  # Returns in radians
  def getAlpha(self):
    return math.acos(self.getDotProd(1, 2) / (self.getB() * self.getC()))
  def getBeta(self):
    return math.acos(self.getDotProd(0, 2) / (self.getA() * self.getC()))
  def getGamma(self):
    return math.acos(self.getDotProd(0, 1) / (self.getA() * self.getB()))

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

  def displayLatticeInfo(self):
    print "The lattice info is the following:"
    print " A is", self.getA()
    print " B is", self.getB()
    print " C is", self.getC()
    print " Alpha is", self.rad2Deg(self.getAlpha())
    print " Beta is", self.rad2Deg(self.getBeta())
    print " Gamma is", self.rad2Deg(self.getGamma())

  def display(self):
    print "\nTitle of the crystal is: ", self.title
    print "Scaling factor is: ", self.scalingFactor
    print "Cartesian is: " , self.cartesian
    self.displayLattice()
    self.displayAtoms()
    print "\n",

