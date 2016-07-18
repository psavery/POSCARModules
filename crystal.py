# Author -- Patrick S. Avery -- 2016

import math
import copy

class Vector3d:
  def __init__(self, x = float, y = float, z = float):
    self.x = x
    self.y = y
    self.z = z

  def __add__(self, other):
    x = self.x + other.x
    y = self.y + other.y
    z = self.z + other.z
    return Vector3d(x,y,z)

  def __sub__(self, other):
    x = self.x - other.x
    y = self.y - other.y
    z = self.z - other.z
    return Vector3d(x,y,z)

  def norm(self):
    return (self.x**2.0 + self.y**2.0 + self.z**2.0)**0.5

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

  def getUnitVolume(self):
    alpha = self.getAlpha()
    beta = self.getBeta()
    gamma = self.getGamma()
    return (1.0 - math.cos(alpha)**2 - math.cos(beta)**2 - math.cos(gamma)**2 \
            + 2 * math.cos(alpha) * math.cos(beta) * math.cos(gamma)) ** (0.5)

  def getVolume(self):
    return self.getA() * self.getB() * self.getC() * self.getUnitVolume()

  def toFractional(self, v):
    a = self.getA()
    b = self.getB()
    c = self.getC()
    alpha = self.getAlpha()
    beta = self.getBeta()
    gamma = self.getGamma()
    vol = self.getUnitVolume()
    # We'll just do the matrix multiplication by hand...
    v.x = (1.0 / a) * v.x + (-math.cos(gamma) / (a * math.sin(gamma))) * v.y + \
                 ((math.cos(alpha) * math.cos(gamma) - math.cos(beta)) / (a * vol * math.sin(gamma))) * v.z

    v.y = (1.0 / (b * math.sin(gamma))) * v.y + \
                 ((math.cos(beta) * math.cos(gamma) - math.cos(alpha)) / (b * vol * math.sin(gamma))) * v.z

    v.z = (math.sin(gamma) / (c * vol)) * v.z

  def convertAtomToFractional(self, atom):
    self.toFractional(atom.pos)

  def convertAtomsToFractional(self):
    if not self.cartesian:
      print "convertAtomsToFractional() was called, but the coordinates are already fractional! Returning..."
      return
    for atom in self.atoms:
      self.convertAtomToFractional(atom)
    self.cartesian = False

  def toCartesian(self, v):
    a = self.getA()
    b = self.getB()
    c = self.getC()
    alpha = self.getAlpha()
    beta = self.getBeta()
    gamma = self.getGamma()
    vol = self.getUnitVolume()

    # This is ugly, but we're just gonna do the matrix multiplication by
    # hand.
    v.x = a * v.x + b * math.cos(gamma) * v.y + c * math.cos(beta) * v.z
    v.y = b * math.sin(gamma) * v.y + c * (math.cos(alpha) - math.cos(beta) * math.cos(gamma)) / math.sin(gamma) * v.z
    v.z = c * vol / math.sin(gamma) * v.z

  def convertAtomToCartesian(self, atom):
    self.toCartesian(atom.pos)

  def convertAtomsToCartesian(self):
    if self.cartesian:
      print "convertAtomsToCartesian() was called, but the coordinates are already cartesian! Returning..."
      return
    for atom in self.atoms:
      self.convertAtomToCartesian(atom)
    self.cartesian = True

  # This does not edit the parameter. It returns the result.
  @staticmethod
  def minimumImageFractional(v):
    ret = copy.deepcopy(v)
    ret.x = ret.x - round(ret.x)
    ret.y = ret.y - round(ret.y)
    ret.z = ret.z - round(ret.z)
    return ret

  # This does not edit the parameter. It returns the result.
  def minimumImage(self, v):
    ret = copy.deepcopy(v)
    self.toFractional(ret)
    ret = self.minimumImageFractional(ret)
    self.toCartesian(ret)
    return ret

  def distance(self, atom1, atom2):
    vec = atom1.pos - atom2.pos
    if not self.cartesian:
      self.toCartesian(vec)
    return abs(self.minimumImage(vec).norm())

  def distances(self):
    ret = []
    for i in range(len(self.atoms)):
      for j in range(i + 1, len(self.atoms)):
        ret.append((self.atoms[i].symbol, self.atoms[j].symbol,
                    self.distance(self.atoms[i], self.atoms[j])))
    ret.sort(key=lambda tup: tup[2])
    return ret

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

  def displayDistances(self):
    print "\nDistances between atoms:"
    distances = self.distances()
    for distance in distances:
      print distance[0], distance[1], distance[2]

  def display(self):
    print "\nTitle of the crystal is: ", self.title
    print "Scaling factor is: ", self.scalingFactor
    print "Cartesian is: " , self.cartesian
    self.displayLattice()
    print "Volume is: ", self.getVolume()
    self.displayAtoms()
    print "\n",

